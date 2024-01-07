import time
import mecmitool.errors


class timer:
    def __init__(self, timer_name= "timer_name") -> None:
        self.timer_name = timer_name
        self.time_start = time.time()
        self.start_status= 0
        self.accumulate_time = 0
    def reset(self):
        self.time_start = time.time()

    def get(self,check_start=False):
        if check_start and self.start_status == 0:
            return 0
        else:
            return time.time() - self.time_start
    def interval(self, auto_init=False):
        if self.start_status == 0:
            if auto_init==False:
                raise mecmitool.errors.TimerError(self.timer_name).no_init()
            else:
                self.start()
        time_now = time.time()
        time_interval =time_now - self.time_start
        self.time_start=time_now
        return time_interval
    def start(self):
        if self.start_status == 0:
            self.time_start = time.time()
            self.start_status = 1
    def accumulate(self,interval_time=None,init=True):
        if interval_time is  None:
            self.accumulate_time += self.interval(init)
        else:
            self.accumulate_time += interval_time
        return self.accumulate_time
