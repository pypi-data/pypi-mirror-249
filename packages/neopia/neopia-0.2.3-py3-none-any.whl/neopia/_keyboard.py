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
    
    @staticmethod
    def read():
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            return event.name
        