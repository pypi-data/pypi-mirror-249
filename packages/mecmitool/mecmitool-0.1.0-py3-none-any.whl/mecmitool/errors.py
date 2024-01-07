class OutRangeError(BaseException):
    def __init__(self, path, message):
        self.message = '\nOutRangeError: '+path+'\nError massage: '+ message
    
    def __str__(self):
        return self.message
    
class TimerError(BaseException):
    def __init__(self, timer_name):
        self.message = '\nTimerError: \n'+timer_name+': '
    def no_init(self):
        self.message = f"{self.message}time interval need initial point."
    def __str__(self):
        return self.message