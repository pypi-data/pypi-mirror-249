# Part of the RoboticsWare project - https://roboticsware.uz
# Copyright (C) 2022 RoboticsWare (neopia.uz@gmail.com)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import os
from . import keyboard


if os.name == "nt":  # sys.platform == "win32":
    import msvcrt

    class Keyboard(object):
        BACKSPACE = 8
        TAB = 9
        ENTER = 13
        ESC = 27
        F1 = 59
        F2 = 60
        F3 = 61
        F4 = 62
        F5 = 63
        F6 = 64
        F7 = 65
        F8 = 66
        F9 = 67
        F10 = 68
        F11 = 133
        F12 = 134

        HOME = 71
        UP = 72
        PAGE_UP = 73
        LEFT = 75
        RIGHT = 77
        END = 79
        DOWN = 80
        PAGE_DOWN = 81
        INSERT = 82
        DELETE = 83
        
        _special_keys = (BACKSPACE, TAB, ENTER, ESC)
        _function_numpads = (F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, HOME, UP, PAGE_UP, LEFT, RIGHT, END, DOWN, PAGE_DOWN, INSERT, DELETE)

        @staticmethod
        def read():
            if msvcrt.kbhit():
                key = msvcrt.getch()
                code = ord(key)
                if code == 224: # special key (F11, F12, HOME, UP, PAGE_UP, LEFT, RIGHT, END, DOWN, PAGE_DOWN, INSERT, DELETE)
                    return ord(msvcrt.getch())
                elif code == 0: # function key (F1 - F10) or num pad
                    code = ord(msvcrt.getch())
                    if code in Keyboard._function_numpads:
                        return code
                elif code in Keyboard._special_keys:
                    return code
                else:
                    return key.decode("utf-8")
else:
    import sys
    import termios
    from contextlib import contextmanager
    class Keyboard(object):
        BACKSPACE = 'delete'
        TAB = 'tab'
        ENTER = 'enter'
        F1 = 'f1'
        F2 = 'f2'
        F3 = 'f3'
        F4 = 'f4'
        F5 = 'f5'
        F6 = 'f6'
        F7 = 'f7'
        F8 = 'f8'
        F9 = 'f9'
        F10 = 'f10'
        F11 = 'f11'
        F12 = 'f12'

        HOME = 'home'
        UP = 'up'
        PAGE_UP = 'page up'
        LEFT = 'left'
        RIGHT = 'right'
        END = 'end'
        DOWN = 'down'
        PAGE_DOWN = 'page down'
        SPACE = 'space'
        DELETE = 'forward delete'
        
        _special_keys = (BACKSPACE, TAB, ENTER)

        @staticmethod
        @contextmanager
        def _mode(file):
            old_attrs = termios.tcgetattr(file.fileno())
            new_attrs = old_attrs[:]
            new_attrs[3] = new_attrs[3] & ~(termios.ECHO | termios.ICANON)
            try:
                termios.tcsetattr(file.fileno(), termios.TCSADRAIN, new_attrs)
                yield
            finally:
                termios.tcsetattr(file.fileno(), termios.TCSADRAIN, old_attrs)

        @staticmethod
        def read():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                return event.name
            # with Keyboard._mode(sys.stdin):
            #     key = sys.stdin.read(1)
            #     code = ord(key)
            #     if code == 27: # special key
            #         code = ord(sys.stdin.read(1))
            #         if code == 79:
            #             return ord(sys.stdin.read(1))
            #         elif code == 91:
            #             code = ord(sys.stdin.read(1))
            #             if code >= 65:
            #                 return code
            #             else:
            #                 code2 = ord(sys.stdin.read(1))
            #                 if code2 == 126:
            #                     return code + 100
            #                 else:
            #                     sys.stdin.read(1) # 126
            #                     return code2
            #         else:
            #             return code
            #     elif code in Keyboard._special_keys:
            #         return code
            #     else:
            #         return key