import bento
from bento.bars import UpdatableBar
import psutil


class CPUBar(UpdatableBar):
    def __init__(self,
                 *args,
                 warning_threshold: int=10,
                 danger_threshold: int=30,
                 okay_color: (int, int, int)=(50, 200, 50),
                 warning_color: (int, int, int)=(200, 200, 0),
                 danger_color: (int, int, int)=(200, 50, 50),
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.okay_color = bento.canonicalize_color(okay_color)
        self.warning_color = bento.canonicalize_color(warning_color)
        self.danger_color = bento.canonicalize_color(danger_color)

        self.warning_threshold = warning_threshold
        self.danger_threshold = danger_threshold

    def do_update(self):
        pc = psutil.cpu_percent()
        self.set_text("CPU {}%".format(str(pc)))
        if pc >= self.danger_threshold:
            self.set_bg(*self.danger_color)
        elif pc >= self.warning_threshold:
            self.set_bg(*self.warning_color)
        else:
            self.set_bg(*self.okay_color)
