# Copyright (c) 2019-2021 Thomas Kramer.
# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .types import *
from .tokenized import *

class LibertyParserError(ParserError):
    pass

class ParseIntError(LibertyParserError):
    pass

class ParseFloatError(LibertyParserError):
    pass

class ExceptionWithLineNum(LibertyParserError):

    def __init__(self, e, line_num, char_num):
        self.e = e
        self.line_num = line_num
        self.char_num = char_num

    def __str__(self):
        return f"Error on line {self.line_num}, position {self.char_num}: {self.e}"

def parse_liberty(data: str) -> Group:
    """
    Parse a string containing data of a liberty file.
    The liberty string must contain exactly one top library. If more than one top
    should be supported then `parse_multi_liberty()` should be used instead.

    :param data: Raw liberty string.
    :return: `Group` object of library.
    """
    top_groups = parse_multi_liberty(data)

    if len(top_groups) == 1:
        return top_groups[0]
    else:
        raise LibertyParserError("Liberty does not contain exactly one top group. Use `parse_multi_liberty()` instead.")


def parse_multi_liberty(data: str) -> List[Group]:
    """
    Parse a string containing data of a liberty file.
    The liberty file may contain many top-level libraries.
    :param data: Raw liberty string.
    :return: List of `Group` objects.
    """
    library = read_liberty_chars(iter(data))
    return library

def read_liberty_chars(chars: Iterable) -> List[Group]:
    """
    Parse liberty libraries from an iterator over characters.
    """
    assert isinstance(chars, Iterable)

    class CountLines:
        def __init__(self, iter):
            self.iter = iter
            self.line_num = 0
            self.char_num = 0 # Position on the line.

        def __iter__(self):
            return self
        
        def __next__(self):
            c = next(self.iter)
            self.char_num += 1
            if c == "\n":
                self.line_num += 1
                self.char_num = 0
            return c

    counted = CountLines(chars)
    
    try:
        result = __read_liberty_impl(counted)
    except Exception as e:
        raise ExceptionWithLineNum(e, counted.line_num, counted.char_num)
    
    return result

    

def __read_liberty_impl(chars) -> List[Group]:
    assert isinstance(chars, Iterable)
    tk = tokenize(chars, LibertyLexer())
    tk.advance()

    groups = []
    
    while True:
        item = __read_group_item(tk)
        if not isinstance(item, Group):
            raise LibertyParserError("library must start with a group but found:", type(item))
        groups.append(item)

        if tk.current_token_ref() is None:
            # End of file.
            break

    return groups

def __read_group_item(tk: Tokenized):
    assert isinstance(tk, Tokenized)

    name = tk.take_str()

    if tk.test_str("("):
        # Group or complex attribute.
        args = []
        while not tk.test_str(")"):
            args.append(__read_value(tk))
            if not tk.peeking_test_str(")"):
                tk.expect_str(",")

        if tk.test_str("{"):
            # It's a group.

            group = Group(name, args)

            while not tk.test_str("}"):
                # Recursively read group items.
                item = __read_group_item(tk)
                if isinstance(item, Group):
                    group.groups.append(item)
                elif isinstance(item, Attribute):
                    group.attributes.append(item)
                elif isinstance(item, Define):
                    group.defines.append(item)
                else:
                    assert False, "unexpected type"

            return group
        else:
            # It's a complex attribute or define statement.
            tk.test_str(";") # Consume optional trailing semicolon.
            if name == "define" and len(args) == 3:
                # Define statement

                # Values must be names or quoted names.

                strings = []
                for a in args:
                    if isinstance(a, EscapedString):
                        s = a.value
                    else:
                        s = str(a)
                    strings.append(s)

                attribute_name, group_name, attr_type = strings
                
                return Define(attribute_name, group_name, attr_type)
            else:
                # It's a complex attribute
                return Attribute(name, args)
    elif name.endswith(":") or tk.test_str(":"):
        # Simple attribute.
        value = __read_value(tk)
        
        if name.endswith(":"):
            # Fix for supporting absence of whitespace between attribute name and colon.
            name = name[:-1]

        is_expression = value in ["(", "-", "!"] or tk.current_token_str() in ["*", "+", "-"]
        if is_expression:
            # Read expression. Something like `VDD * 0.5 + 0.1`.
            expr = [str(value)]

            while not tk.test_str(";"):
                expr.append(tk.take_str())
            
            return Attribute(name, ArithExpression(" ".join(expr)))
        else:
            tk.test_str(";") # Read optional semicolon
            return Attribute(name, value)
    else:
        raise UnexpectedToken("'(' | ':'", tk.current_token_str())

def __read_value(tk: Tokenized):
    assert isinstance(tk, Tokenized)

    s = tk.current_token_str()
    if not s:
        raise UnexpectedEndOfFile()
    
    first_char = s[0]
    last_char = s[-1]

    if (first_char.isnumeric() or first_char == "-") and last_char.isnumeric():
        # Read a number
        is_int = all(c.isnumeric() for c in s[1:])
        s = tk.take_str()
        if is_int:
            return __read_int(s)
        else:
            try:
                return __read_float(s)
            except ParseFloatError:
                return s
    if __is_number_with_unit(s):
        return __read_number_with_unit(tk.take_str())
    elif first_char == '"':
        # Quoted string.
        # Strip away the quotes.
        without_quotes = s[1:-1]
        tk.advance()
        return EscapedString(without_quotes)
    else:
        name = tk.take_str()

        if tk.test_str("["):
            buspins = tk.take_str()
            tk.expect_str("]")
            splitted = buspins.split(":")
            print(splitted)

            if len(splitted) == 1:
                return NameBitSelection(name, int(splitted[0]))
            if len(splitted) == 2:
                return NameBitSelection(name, int(splitted[0]), int(splitted[1]))
            else:
                raise LibertyParserError("Invalid bus pins: {}".format(splitted))

        else:
            return name

def __read_int(s: str):
    try:
        return int(s)
    except ValueError as e:
        raise ParseIntError(e)
    
def __read_float(s: str):
    try:
        return float(s)
    except ValueError as e:
        raise ParseFloatError(e)

def __read_number_with_unit(s: str):
    try:
        unit_len = 0
        for c in s[::-1]:
            if c.isalpha():
                unit_len += 1
            else:
                break

        num = s[:-unit_len]
        unit = s[-unit_len:]

        num = float(num)

        return WithUnit(num, unit)
    except ValueError as e:
        return s

def __is_number_with_unit(s: str):
    if len(s) < 1:
        return False
    first = s[0]
    if first.isnumeric() or first == "-":
        return s[-1].isalpha()
    else:
        False

def test_read_liberty():
    
    data = r"""
    /*
    Author: somebody
    */
library (myLib) {
  time_unit : 1ns;
  simpleattr_int : 1;
  simpleattr_neg_int : -1;
  simpleattr_float : -1.12e-3;
    simple_attribute1 : value1;
    simple_attribute2 : value2;
    simple_attribute2 : value3;
    complex_attribute1 (value1, "value 2");

    // Single line comment // does not end here / also not here

    /* comment with ** * characters */

    cell (invx1) {
        simple_attribute1 : value;
    }
}
"""

    result = read_liberty_chars(iter(data))
    print(result)
    assert isinstance(result[0], Group)

def test_parse_liberty_simple():
    data = r"""
library(test) { 
  time_unit : 1ns;
  string : "asdf";
  mygroup(a, b) {}
  empty() {}
  somegroup(a, b, c) {
    nested_group(d, e) {
        simpleattr_float : 1.2;
    }
  }
  simpleattr_int : 1;
  complexattr(a, b);
  define(myNewAttr, validinthisgroup, float);
  pin(A[25]) {}
  pin(B[32:0]) {}
  pin(C[0:0]) {}
}
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)

    # Check attribute values.
    assert library.get_attribute('simpleattr_int') == 1
    assert library.get_attribute('complexattr') == ['a', 'b']

    # Format, parse, format and check that the result stays the same.
    str1 = str(library)
    library2 = parse_liberty(str1)
    str2 = str(library2)
    assert (str1 == str2)
    
def test_parse_liberty_no_space_before_colon():
    data = r"""
library(test) { 
  attr_name: value;
  }
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)

    # Check attribute values.
    assert library.get_attribute('attr_name') == "value"


def test_parse_liberty_with_unit():
    data = r"""
library(test) { 
  time_unit : 1ns ;
}
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)

    # Check values with unit.
    assert isinstance(library.get_attribute('time_unit'), WithUnit)
    assert library.get_attribute('time_unit').value == 1
    assert library.get_attribute('time_unit').unit == 'ns'

    # Format, parse, format and check that the result stays the same.
    str1 = str(library)
    library2 = parse_liberty(str1)
    str2 = str(library2)
    assert (str1 == str2)


def test_parse_liberty_with_multline():
    data = r"""
table(table_name2){ 
    str : "asd\
    f";
    index_1("1, 2, 3, 4, 5, 6, 7, 8"); 
    value("0001, 0002, 0003, 0004, \
    0005, 0006, 0007, 0008");
}
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)

    str1 = str(library)
    library2 = parse_liberty(str1)
    str2 = str(library2)
    assert (str1 == str2)


def test_parse_liberty_statetable_multiline():
    # From https://codeberg.org/tok/liberty-parser/issues/6
    data = r"""
statetable ("CK E SE","IQ") {
	     table : "L L L : - : L ,\
	              L L H : - : H ,\
	              L H L : - : H ,\
	              L H H : - : H ,\
	              H - - : - : N " ;
	}
"""

    library = parse_liberty(data)
    assert isinstance(library, Group)

    str1 = str(library)
    library2 = parse_liberty(str1)
    str2 = str(library2)
    assert (str1 == str2)


def test_parse_liberty_with_define():
    data = r"""
group(test){ 
    define (a, b, c);
    define (x, y, z);
}
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)
    assert isinstance(library.defines[0], Define)
    assert isinstance(library.defines[1], Define)

    str1 = str(library)
    library2 = parse_liberty(str1)
    str2 = str(library2)
    assert (str1 == str2)


def test_parse_liberty_multi_complex_attributes():
    data = r"""
group(test){ 
    define_group(g1, x);
    define_group(g2, z);
    voltage_map(VDD, 1.0);
    voltage_map(VSS, 0.0);
}
"""
    library = parse_liberty(data)
    assert isinstance(library, Group)

    # Check if `voltage_map` is parsed as expected.
    assert library.get_attributes('voltage_map')[0] == ['VDD', 1.0]
    assert library.get_attributes('voltage_map')[1] == ['VSS', 0.0]

    str1 = str(library)
    library2 = parse_liberty(str1)
    assert len(library.attributes) == 4
    str2 = str(library2)
    assert (str1 == str2)


def test_parse_liberty_freepdk():
    import os.path
    lib_file = os.path.join(os.path.dirname(__file__), '../../test_data/gscl45nm.lib')

    data = open(lib_file).read()

    library = parse_liberty(data)
    assert isinstance(library, Group)

    library_str = str(library)
    open('/tmp/lib.lib', 'w').write(library_str)
    library2 = parse_liberty(library_str)
    assert isinstance(library2, Group)
    library_str2 = str(library2)
    assert (library_str == library_str2)

    cells = library.get_groups('cell')

    invx1 = library.get_group('cell', 'XOR2X1')
    assert invx1 is not None

    pin_y = invx1.get_group('pin', 'Y')
    timings_y = pin_y.get_groups('timing')
    timing_y_a = [g for g in timings_y if g['related_pin'] == 'A'][0]
    assert timing_y_a['related_pin'] == 'A'

    array = timing_y_a.get_group('cell_rise').get_array('values')
    assert array.shape == (6, 6)


def test_wire_load_model():
    """
    Test that multiple attributes with the same name don't overwrite eachother.
    See: https://codeberg.org/tok/liberty-parser/issues/7
    """

    data = r"""
    wire_load("1K_hvratio_1_4") {
        capacitance : 1.774000e-01;
        resistance : 3.571429e-03;
        slope : 5.000000;
        fanout_length( 1, 1.3207 );
        fanout_length( 2, 2.9813 );
        fanout_length( 3, 5.1135 );
        fanout_length( 4, 7.6639 );
        fanout_length( 5, 10.0334 );
        fanout_length( 6, 12.2296 );
        fanout_length( 8, 19.3185 );
    }
"""
    wire_load = parse_liberty(data)
    fanout_lengths = wire_load.get_attributes("fanout_length")
    assert isinstance(fanout_lengths, list)
    assert len(fanout_lengths) == 7
    expected_fanoutlength = [
        [1, 1.3207],
        [2, 2.9813],
        [3, 5.1135],
        [4, 7.6639],
        [5, 10.0334],
        [6, 12.2296],
        [8, 19.3185],
    ]
    assert fanout_lengths == expected_fanoutlength


def test_argument_with_dot():
    """
    Parse names with dots like `a.b`.
    """
    # Issue #10
    data = r"""
operating_conditions(ff28_1.05V_0.00V_0.00V_0.00V_125C_7y50kR){
}    
"""
    group = parse_liberty(data)

    assert group.args == ["ff28_1.05V_0.00V_0.00V_0.00V_125C_7y50kR"]


def test_complex_attribute_without_semicolon():
    """
    Parse complex attributes without trailing `;`.
    """
    # Issue #10
    data = r"""
library(){
    cplxAttr1(1)
    cplxAttr2(1, 2)
    cplxAttr3(3);
    cplxAttr4(4)
}
"""
    group = parse_liberty(data)

    assert len(group.attributes) == 4


def test_simple_attribute_without_semicolon():
    """
    Parse simple attributes without trailing `;`.
    """
    # Issue #10
    data = r"""
library(){
    simpleAttr1 : 1ps
    simpleAttr2 : 2;
    simpleAttr3 : 3
}
"""
    group = parse_liberty(data)

    assert len(group.attributes) == 3


def test_multi_top_level_libraries():
    """
    Parse files with more than one top-level library.
    """
    # Issue #10
    data = r"""
library(lib1){
}
library(lib2){
}
"""
    tops = parse_multi_liberty(data)
    assert isinstance(tops, list)
    assert len(tops) == 2


def test_define():
    # Issue #10
    data = r"""
    library(){
        define ("a", "b", "c");
        define (d, "e", f);
        define (g, h, i)
    }
    """
    group = parse_liberty(data)
    assert isinstance(group, Group)
    assert len(group.defines) == 3

    assert group.defines[0].attribute_name == "a"
    assert group.defines[0].group_name == "b"
    assert group.defines[0].attribute_type == "c"
    assert group.defines[1].attribute_name == "d"
    assert group.defines[1].group_name == "e"
    assert group.defines[1].attribute_type == "f"
    assert group.defines[2].attribute_name == "g"
    assert group.defines[2].group_name == "h"
    assert group.defines[2].attribute_type == "i"


def test_arithmetic_expressions():
    # Issue 10

    data = r"""
    input_voltage(cmos) {
        vil : 0.5 * VDD ;
        vih : 0.7 * VDD ;
        vimin : -0.5 ;
        vimax : VDD * 1.1 + 0.5 ;
    }
"""
    group = parse_liberty(data)
    assert isinstance(group, Group)
    assert len(group.attributes) == 4

    for attr in group.attributes:
        expr_str = attr.value
        if not isinstance(attr.value, float):
            assert isinstance(expr_str, ArithExpression)

            expr = expr_str.to_sympy_expression()
            print(expr)

    assert group.attributes[3].value.to_sympy_expression() == sympy.parse_expr("VDD * 1.1 + 0.5")

def test_single_letter_units():
    # Issue 11

    data = r"""
    test() {
        int_value : 1V ; 
        float_value : 2.5e-1A ;
    }
"""

    group = parse_liberty(data)
    assert isinstance(group, Group)
    assert len(group.attributes) == 2
    assert group.attributes[0].value == WithUnit(1, "V")
    assert group.attributes[1].value == WithUnit(0.25, "A")

def test_units_starting_with_E():
    # Issue 11

    data = r"""
    test() {
        int_value : 1eV ; 
        float_value : 2.5e-1EV ;
    }
"""

    group = parse_liberty(data)
    assert isinstance(group, Group)
    assert len(group.attributes) == 2
    assert group.attributes[0].value == WithUnit(1, "eV")
    assert group.attributes[1].value == WithUnit(0.25, "EV")

def test_group_without_argument():

    data = r"""
    my_group() {
        some_attribute : "123";
    }
    """
    
    group = parse_liberty(data)
    assert isinstance(group, Group)

    print(group.args)

    assert len(group.args) == 0

def test_group_arguments_with_colon():
    # Issue 15

    data = r"""
    group (name_with:colon) {
        my_attribute : true;

        simple_attribute : 1;

        simple_attribute_2 : 2;
    }    
"""
    group = parse_liberty(data)
    assert isinstance(group, Group)

    assert group.args[0] == "name_with:colon"

def test_multiline_with_backslash():
    
    data = r"""
    group() {
        array ( \
            "0, 0, 0", \
            "0, 0, 0" \
        );
    }
    """

    group = parse_liberty(data)
    assert isinstance(group, Group)

def test_invalid_bus_pins():

    data = r"""
        library () {

        cell (x) {
            pin(A[1:2:3]) {}
        }
    }
    """

    error = None
    try:
        group = parse_liberty(data)
    except Exception as e:
        error = e

    assert error is not None
