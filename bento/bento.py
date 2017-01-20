import json
import colorsys
import yaml

from functools import wraps


def bento_cmd(arg):
    """
    Everyday we stray further from Haskell's light
    """
    if callable(arg):

        @wraps(arg)
        def inner(self, *args, **kwargs):
            d = arg(self, *args, **kwargs)
            d['bar'] = self.bar_name
            d['cmd'] = arg.__name__
            return send_to_fifo(d)

        return inner
    else:

        def _inner(func):
            @wraps(func)
            def inner(self, *args, **kwargs):
                d = func(self, *args, **kwargs)
                d['bar'] = self.bar_name
                d['cmd'] = arg
                send_to_fifo(d)

            return inner

        return _inner

# Utilities


def send_to_fifo(data, fifo_path=None):
    if fifo_path is None:
        fifo_path = "/tmp/snackbar_fifo"
    with open(fifo_path, "w") as fifo:
        fifo.write("{}\0".format(json.dumps(data)))


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    if lv == 1:
        v = int(value, 16) * 17
        return (v, v, v)
    if lv == 3:
        return tuple(int(value[i:i + 1], 16) * 17 for i in range(0, 3))
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def canonicalize_color(value):
    if type(value) is str:
        value = hex_to_rgb(value)
    return value


def bar_from_dict(*args, **kwargs):
    bar_class = kwargs['type']

    import bento.bars
    bar_classes = {
        'cpu': bento.bars.system.CPUBar,
        'shell': bento.bars.ShellCommandBar,
        'mpd': bento.bars.MPDBar
    }

    if type(bar_class) is str:
        bar_class = bar_classes[bar_class]

    kwargs.pop('type')

    return bar_class(*args, **kwargs)


def mainloop(bars, create=True):
    try:
        for bar in bars:
            if create:
                bar.create()
            bar.start_update()
        for bar in bars:
            bar.wait_for_exit()
    except KeyboardInterrupt:
        print("Caught C-c.")
        for bar in bars:
            bar.stop_update()
        print("All bars stopped.")


def load_config_file(fname):
    with open(fname) as f:
        panels = yaml.load(f)
    bars = []
    for (panel_name, panel_data) in panels.items():
        opts = panel_data['options']

        x = opts['x']
        if 'padding' in opts:
            padding = opts['padding']
        else:
            padding = 5

        for bar_opts in panel_data['bars']:
            bar_name = bar_opts['name']
            bar_opts.pop('name')
            bar_opts.update(opts)
            bar_opts.pop('x')
            if 'padding' in bar_opts:
                bar_opts.pop('padding')
            if 'bar_name' in bar_opts:
                bar_opts.pop('bar_name')
            extra_opts = {
                'x': x,
                'bar_name': "{}/{}".format(panel_name, bar_name)
            }
            extra_opts.update(bar_opts)
            print(extra_opts)

            bar = bar_from_dict(**extra_opts)
            bars.append(bar)
            x = x + padding + extra_opts['width']
    return bars


def run_from_config():
    import argparse

    parser = argparse.ArgumentParser(description='Load a Bento configuration.')
    parser.add_argument(
        '-n',
        '--nocreate',
        dest='create',
        action='store_const',
        default=True,
        const=False,
        help='Don\'t create the bars before starting the update loop.')

    parser.add_argument(
        '-f',
        '--config',
        default='bento_config.yaml',
        help='Load a configuration file.')

    args = parser.parse_args()
    bars = load_config_file(args.config)
    mainloop(bars, create=args.create)
