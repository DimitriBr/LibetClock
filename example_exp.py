from psychopy import visual, core, monitors, clock, event, logging
from math import radians, atan2, sin, cos, floor, ceil, acos, asin, degrees, sqrt
import random
import pandas as pd 
from win32api import GetSystemMetrics
import matplotlib.pyplot as plt
from the_clock import LClock

hgt = GetSystemMetrics(0)
wdt = GetSystemMetrics(1) 
the_clock = LClock(screen_height = hgt, screen_weight = wdt, refresh_rate = 60, duration_desired = 2560, ballcolor = 'red')
the_clock.make_the_clockface(edges_of_the_clockface = 100, color = 'black') 



### EXAMPLE TRIAL BLOCK

the_clock.text_window('Buena sera, segnori e segnore')
ntrials = 3
for trial in range(ntrials):
    wait_before_rotation = random.uniform(0.5,5)

    the_clock.clockface.draw()
    the_clock.win.flip()
    core.wait(wait_before_rotation)

    press_info = the_clock.rotation()
    judge_info = the_clock.judgement('W')
    trial_info = {**press_info, **judge_info}

    the_clock.text_window('Grazie mille! Press SPACE to continue\n\n' + str(ntrials - trial - 1) + ' trials left')

    print(trial_info)

the_clock.text_window

