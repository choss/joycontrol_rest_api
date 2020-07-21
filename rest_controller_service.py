from enum import Enum

class ControllerStick(str, Enum):
    l_stick = "l_stick"
    r_stick = "r_stick"

class ControllerAxis(str, Enum):
    x_axis = "x_axis"
    y_axis = "y_axis"

class ControllerButton(str, Enum):
    y = 'y'
    x = 'x'
    b = 'b'
    a = 'a'
    r = 'r'
    zr = 'zr'
    minus = 'minus'
    plus = 'plus'
    r_stick = 'r_stick'
    l_stick = 'l_stick'
    home = 'home'
    capture = 'capture'
    down = 'down'
    up = 'up'
    right = 'right'
    left = 'left'
    l = 'l'
    zl = 'zl'
    sr = 'sr'
    sl = 'sl'
