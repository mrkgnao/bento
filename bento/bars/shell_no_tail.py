import bento
from bento.bars import UpdatableBar
import subprocess


class ShellCommandBar(UpdatableBar):
    def __init__(self, *args, command, **kwargs):
        super().__init__(*args, **kwargs)
        self.command = command

    def do_update(self):
        self.set_text(
            subprocess.Popen(
                self.command, shell=True, stdout=subprocess.PIPE).stdout.read(
                ).decode())
