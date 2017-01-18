import json
import psutil
import colorsys

from time import sleep


def bento_cmd(arg):
    if callable(arg):

        def inner(name, *args, **kwargs):
            d = arg(*args, **kwargs)
            d['bar'] = name
            d['cmd'] = arg.__name__
            return send_to_fifo(d)

        return inner
    else:

        def _inner(func):
            def inner(name, *args, **kwargs):
                d = func(*args, **kwargs)
                d['bar'] = name
                d['cmd'] = arg
                send_to_fifo(d)

            return inner

        return _inner


@bento_cmd('add_bar')
def create_bar(x, y, width, height):
    return {"x": x, "y": y, "width": width, "height": height}


@bento_cmd('show')
def show_bar():
    return {}


@bento_cmd('show')
def show_bar():
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


@bento_cmd
def set_size(width, height):
    return {"width": width, "height": height}

# Utilities


def send_to_fifo(data, fifo_path=None):
    if fifo_path is None:
        fifo_path = "/tmp/snackbar_fifo"
    with open(fifo_path, "w") as fifo:
        fifo.write("{}\0".format(json.dumps(data)))


bs = ['batt', 'date', 'temp']


def initExampleBars():
    create_bar('batt', 5, 5, 400, 22)
    create_bar('date', 410, 5, 405, 22)
    create_bar('temp', 820, 5, 540, 22)

    for b in bs:
        set_font(b, 'Iosevka 11')
        set_text(b, "test text here")


def colorShow():
    for i in range(256):
        set_bg_from_hsv_uint('batt', i, 255, 255)
        set_bg_from_hsv_uint('date', i + 64, 255, 255)
        set_bg_from_hsv_uint('temp', i + 128, 255, 255)
        sleep(0.01)
