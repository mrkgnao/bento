import bento
import colorsys
import time
from bento import bento_cmd


class BasicBar(object):
    def __init__(self,
                 bar_name: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 font_desc: str="Iosevka 11", # None pattern?
                 background_color: (int,int,int)=(0,0,0),
                 opacity: int=80):
        self.bar_name = bar_name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_desc = font_desc
        self.background_color = bento.canonicalize_color(background_color)
        self.opacity = opacity

    @bento_cmd('add_bar')
    def _create(self):
        return {"x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height}

    def create(self, delay=0.01):
        self._create()
        self.set_font(self.font_desc)
        self.set_bg(*self.background_color)
        self.set_opacity(self.opacity)
        self.show_bar()
        self.force_repaint()

    @bento_cmd
    def force_repaint(self):
        """Force a bar update."""
        return {}

    @bento_cmd('show')
    def show_bar(self):
        """Show the target bar."""
        return {}

    @bento_cmd('hide')
    def hide_bar(self):
        """Hide the target bar."""
        return {}

    @bento_cmd
    def set_text(self, text: str):
        return {"text": "<small>{}</small>".format(text)}

    @bento_cmd
    def set_font(self, font_desc: str):
        return {"font_desc": font_desc}

    @bento_cmd
    def set_bg(self, red, green, blue):
        self.background_color = (red, green, blue)
        return {"red": red, "green": green, "blue": blue}

    @bento_cmd
    def set_bg_norm(self, red, green, blue):
        return {"red": red, "green": green, "blue": blue}

    @bento_cmd('set_bg')
    def set_bg_hex(self, hex_code):
        set_bg(bento.hex_to_rgb(hex_code))

    @bento_cmd('set_bg_norm')
    def set_bg_from_hsv_float(self, h, s, v):
        return dict(
            zip(("red", "green", "blue"), colorsys.hsv_to_rgb(h, s, v)))

    @bento_cmd('set_bg_norm')
    def set_bg_from_hsv_uint(self, h, s, v):
        return dict(
            zip(("red", "green", "blue"), colorsys.hsv_to_rgb(*tuple(
                map(lambda x: x / 255.0, (h, s, v))))))

    @bento_cmd
    def set_opacity(self, opacity: int):
        return {"opacity": opacity}

    @bento_cmd('set_size')
    def _set_size(self, width: int, height: int):
        return {"width": width, "height": height}

    def set_size(self, width, height):
        self._set_size(width, height)
        self.force_repaint()

    @bento_cmd
    def set_origin(self, x: int, y: int):
        return {"x": x, "y": y}

    def set_bounds(self, name: int, x: int, y: int, width: int, height: int):
        set_origin(name, x, y)
        set_size(name, width, height)

    def colorShow(self, delay=0.01):
        for i in range(256):
            self.set_bg_from_hsv_uint(i, 255, 255)
            time.sleep(delay)
