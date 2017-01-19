import json
import psutil
import colorsys

from functools import wraps

from time import sleep


class Bar(object):
    def __init__(self, name):
        self.name = name


def bento_cmd(arg):
    if callable(arg):

        @wraps(arg)
        def inner(name, *args, **kwargs):
            d = arg(*args, **kwargs)
            d['bar'] = name
            d['cmd'] = arg.__name__
            return send_to_fifo(d)

        return inner
    else:

        def _inner(func):
            @wraps(func)
            def inner(name, *args, **kwargs):
                d = func(*args, **kwargs)
                d['bar'] = name
                d['cmd'] = arg
                send_to_fifo(d)

            return inner

        return _inner


@bento_cmd('add_bar')
def create_bar(x, y, width, height:str):
    return {"x": x, "y": y, "width": width, "height": height}

@bento_cmd('show')
def show_bar():
    """Show the target bar."""
    return {}


@bento_cmd('hide')
def hide_bar():
    """Hide the target bar."""
    return {}


@bento_cmd
def set_text(text):
    return {"text": text}


@bento_cmd
def set_font(font_desc):
    return {"font_desc": font_desc}


@bento_cmd
def set_bg(red, green, blue):
    return {"red": red, "green": green, "blue": blue}


@bento_cmd
def set_bg_norm(red, green, blue):
    return {"red": red, "green": green, "blue": blue}


@bento_cmd('set_bg')
def set_bg_hex(red, green, blue):
    return {"red": red, "green": green, "blue": blue}

@bento_cmd('set_bg_norm')
def set_bg_from_hsv_float(h, s, v):
    return dict(zip(("red", "green", "blue"), colorsys.hsv_to_rgb(h, s, v)))


@bento_cmd('set_bg_norm')
def set_bg_from_hsv_uint(h, s, v):
    return dict(
        zip(("red", "green", "blue"), colorsys.hsv_to_rgb(*tuple(
            map(lambda x: x / 255.0, (h, s, v))))))


@bento_cmd
def set_opacity(opacity):
    return {"opacity": opacity}


@bento_cmd
def set_origin(x, y):
    return {"x": x, "y": y}


def set_bounds(name, x, y, width, height):
    set_origin(name, x, y)
    set_size(name, width, height)


@bento_cmd
def set_size(width, height):
    return {"width": width, "height": height}

@bento_cmd
def repaint():
    return {}

# Bar functions

def update_cpu_bar(bar_name=None):
    if bar_name is None:
        bar_name = 'cpu'

    pc = psutil.cpu_percent()
    set_text(bar_name,str(pc))
    if pc > 10:
        set_bg(bar_name,200,50,50)
    else:
        set_bg(bar_name,50,200,50)


# Utilities


def send_to_fifo(data, fifo_path=None):
    if fifo_path is None:
        fifo_path = "/tmp/snackbar_fifo"
    with open(fifo_path, "w") as fifo:
        fifo.write("{}\0".format(json.dumps(data)))


bs = ['batt', 'date', 'cpu']


def initExampleBars():
    create_bar('batt', 5, 5, 400, 22)
    create_bar('date', 410, 5, 405, 22)
    create_bar('cpu', 820, 5, 540, 22)

    for b in bs:
        set_font(b, 'Iosevka 11')
        set_text(b, b)


def colorShow():
    for i in range(256):
        set_bg_from_hsv_uint('batt', i, 255, 255)
        set_bg_from_hsv_uint('date', i + 64, 255, 255)
        set_bg_from_hsv_uint('cpu', i + 128, 255, 255)
        sleep(0.01)
