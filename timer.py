# -*- coding: utf-8 -*-

import time
import datetime

class Timer(object):

  start_time     = 0
  stop_time      = 0
  duration       = 0


  def now(self):
    return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")


  def start(self):
    self.start_time = round(time.time())


  def stop(self):
    self.stop_time = round(time.time())
    self.duration  = self.stop_time - self.start_time

    return self.__format_time(self.duration)


  def __format_time(self, sec):
    return str(datetime.timedelta(seconds=sec))
