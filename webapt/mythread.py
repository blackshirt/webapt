import time
import threading

class my_thread(threading.Thread):
    def __init__(self, file):
        self.file = file
        threading.Thread.__init__(self)

    def run(self):
        self.file.write('<html><body>')
        # test streamed html output
        self.file.flush()
        time.sleep(1)  # simulate long-running process
        self.file.write('</body></html>')
        self.file.close()