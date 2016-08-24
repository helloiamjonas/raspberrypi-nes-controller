#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic usage example of the nesctrl module
"""
import nesctrl
nesctrl.setup(22, 17, 4)

try:
    while 1:
        if nesctrl.read_controller_state()["A"]:
            print("'A' button pressed.")
        else:
            print("'A' button not pressed.")

except KeyboardInterrupt:
    nesctrl.cleanup()
