from bento import bars
import threading
import time

class UpdatableBar(bars.BasicBar):
    def __init__(self, *args, update_interval: float=1, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_thread = None
        self.update_interval = update_interval

        self.running = threading.Event()
        self.running.set()

        self.kill = threading.Event()
        self.kill.clear()

    def create(self):
        super().create(0.001)

    def do_update(self):
        raise NotImplementedError("Please subclass this and implement it!")

    def mainloop(self):
        while not self.kill.is_set():
            while not self.is_running():
                self.running.wait(timeout=1)
                if self.kill.is_set():
                    return
            self.do_update()
            time.sleep(self.update_interval)

    def is_running(self):
        return self.running.is_set()

    def start_update(self):
        self.running.set()
        if self.update_thread is None or not self.update_thread.is_alive():
            self.update_thread = threading.Thread(
                target=self.mainloop, args=())
            self.update_thread.start()

    def pause_update(self, delay=1):
        self.running.clear()

    def stop_update(self):
        self.kill.set()
        self.wait_for_exit()

    def wait_for_exit(self):
        self.update_thread.join()
