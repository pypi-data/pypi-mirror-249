# SPDX-FileCopyrightText: 2022 Thomas Kramer
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .parser import parse_liberty
from .types import *


def test_select_timing_group():
    data = r"""
pin(Y){ 
    timing() {
        test_label: 1;
        related_pin: "A";
        when: "B";
        cell_rise() {
            test_label: 11;
        }
    }
    timing() {
        test_label: 2;
        related_pin: "A";
        when: "!B";
        cell_rise() {
            test_label: 21;
        }
    }
    timing() {
        test_label: 3;
        related_pin: "B";
        when: "A";
        cell_rise() {
            test_label: 31;
        }
    }
}
"""
    pin_group = parse_liberty(data)
    assert isinstance(pin_group, Group)

    timing_group = select_timing_group(pin_group, related_pin="A")
    assert timing_group['test_label'] == 1

    timing_group = select_timing_group(pin_group, related_pin="A", when='B')
    assert timing_group['test_label'] == 1

    timing_group = select_timing_group(pin_group, related_pin="A", when='!B')
    assert timing_group['test_label'] == 2

    timing_group = select_timing_group(pin_group, related_pin="B")
    assert timing_group['test_label'] == 3

    assert select_timing_table(pin_group, related_pin="A", when='!B', table_name='cell_rise')['test_label'] == 21

def test_replace_array():
    """
    'set_array' should replace existing arrays instead of appending a new one.
    
    See: https://codeberg.org/tok/liberty-parser/issues/16
    """

    data = r"""
    group() {
        myArray ( \
    "0, 0, 0", \
    "0, 0, 0" \
    );
    }
    """

    group = parse_liberty(data)
    assert isinstance(group, Group)

    assert len(group.attributes) == 1

    group.set_array("myArray", np.array([1, 2, 3]))

    assert len(group.attributes) == 1
    assert (group.get_array("myArray") == [1, 2, 3]).all()


def test_select_timing_group():
    """
    Select timing groups by their `timing_type` attribute.

    Test fix proposed in https://codeberg.org/tok/liberty-parser/issues/16.
    """

    data = r"""
        pin(Y) {
            timing() {
                related_pin : "CLK";
                timing_type : hold_falling;
            }
            timing() {
                related_pin : "CLK";
                timing_type : setup_falling;
            }
        }    
    """

    pin = parse_liberty(data)
    assert isinstance(pin, Group)


    timing_hold_falling = select_timing_group(pin, related_pin = "CLK", timing_type = "hold_falling")
    assert isinstance(timing_hold_falling, Group)
    assert timing_hold_falling.get_attribute("timing_type") == "hold_falling"

    timing_setup_falling = select_timing_group(pin, related_pin = "CLK", timing_type = "setup_falling")
    assert isinstance(timing_setup_falling, Group)
    assert timing_setup_falling.get_attribute("timing_type") == "setup_falling"
    



def test_library_colon_in_group_argument():
    """
    See https://codeberg.org/tok/liberty-parser/issues/15
    """

    data = r"""
        library(mylib) {
            input_ccb (FOO:a) {}
        }
    """

    lib = parse_liberty(data)
    assert isinstance(lib, Group)


def test_library_name_begins_with_digit():
    """
    See https://codeberg.org/tok/liberty-parser/issues/17
    """

    data = r"""
        library(0V95XXX) {
        
        }
    """

    lib = parse_liberty(data)
    assert isinstance(lib, Group)
    
def test_library_name_with_minus():
    """
    See issue 18.
    """

    data = r"""
        library(some_lib_-10C) {
        
        }
    """

    lib = parse_liberty(data)
    assert isinstance(lib, Group)
