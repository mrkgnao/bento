import bento
from bento.bars import UpdatableBar
import mpd
import subprocess


class MPDBar(UpdatableBar):
    def __init__(self,
                 *args,
                 progress_bar_width=60,
                 total_width=150,
                 ip="127.0.0.1",
                 port=6600,
                 elapsed_char='.',
                 empty_char=' ',
                 playing_str='▶',
                 paused_str='⏸',
                 stopped_str='◼',
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.ip = ip
        self.port = port
        self.get_mpd_client()

        self.total_width = total_width

        self.elapsed_char = elapsed_char
        self.empty_char = empty_char

        self.paused_str = paused_str
        self.playing_str = playing_str
        self.stopped_str = stopped_str

    def do_update(self):
        def get_output(cmd):
            return subprocess.Popen(
                cmd, shell=True, stdout=subprocess.PIPE).stdout.read().decode()

        status = None
        try:
            toint = lambda s: int(float(s))

            song = self.mpd_client.currentsong()
            status = self.mpd_client.status()
            state = status['state']

            # elapsed = toint(status['elapsed'])
            # total = toint(subprocess.Popen(""))

            if state == 'stop':
                self.set_text("Stopped.")
            else:
                segments = []
                song_info = get_output(
                    "mpc -f '<b>%albumartist%</b> - %title% <i>(%album%)</i>' | head -n 1")
                percent = toint(
                    get_output(
                        "mpc status | head -2 | tail -1 | sed 's/.*(\\(.*\\)%)/\\1/'"))
                progress = get_output(
                    "mpc status | head -2 | tail -1 | tr -s ' ' | cut -d' ' -f3")
                elapsed = percent
                total = 100

                if state == 'pause':
                    segments.append(self.paused_str)
                else:
                    segments.append(self.playing_str)

                segments.append(song_info)

                s = " {} ".format(" ".join(segments).replace('\n', ''))
                progress = " ({})".format(progress).replace('\n', '')

                progress_bar_width = self.total_width - len(s) - len(progress)

                elapsed_section = self.elapsed_char * int(
                    progress_bar_width * (elapsed / total))
                empty_section = self.empty_char * (
                    progress_bar_width - len(elapsed_section))

                progress_bar = elapsed_section + empty_section

                self.set_text("{}{}{}".format(s, progress_bar, progress))

        except Exception as e:
            print(status)
            self.set_text("error, trying to refresh " + str(e))
            self.get_mpd_client()

    def get_mpd_client(self):
        mpd_client = mpd.MPDClient()
        mpd_client.connect(self.ip, str(self.port))
        self.mpd_client = mpd_client
