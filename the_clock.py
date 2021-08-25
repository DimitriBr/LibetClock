from psychopy import visual, core, monitors, clock, event, logging
from math import radians, atan2, sin, cos, floor, ceil, acos, asin, degrees, sqrt
import random
import pandas as pd 
import numpy as np

class LClock():

    def __init__(self, screen_height, screen_weight, refresh_rate, duration_desired, ballcolor):
        self.screen_height = screen_height
        self.screen_weight = screen_weight
        self.radius = 0.32 * sqrt(screen_height * screen_weight)
        self.win = visual.Window(size = (screen_height, screen_weight),color = (1,1,1), units='pix')


        self.refresh_rate = refresh_rate
        self.duration = duration_desired
        self.one_step_dur = 1000 / refresh_rate
        self.amount_steps = ceil(self.duration / self.one_step_dur)


        self.ball = visual.Circle(self.win, radius = 0.024*self.radius, edges = 10, pos = (0,0), fillColor = ballcolor, lineColor = ballcolor, units = 'pix')

   
    def make_the_clockface(self, edges_of_the_clockface, color):

        circ = visual.Circle(win = self.win, radius = self.radius, edges = edges_of_the_clockface,  units = 'pix')
        circ.setLineColor(color)
        circ.draw()

        # Drawing the clock ouline
        r = self.radius
        for i in range (1, 61):
            x = r * cos (radians(90-6*i))
            y = r * sin(radians(90-6*i))
            if i % 5 == 0: #make special marks each 5 pseudoseconds
                v = (r-(1/14)*r) * cos(radians(90-6*i))
                w = (r-(1/14)*r) * sin(radians(90-6*i))
                c1 = (r + 0.085*r) * cos(radians(90 - 6*i))
                c2 = (r + 0.085*r) * sin(radians(90-6*i))
                cyph = visual.TextStim(win = self.win, pos = (c1,c2), text= str(i), color = color,  units = 'pix')
                cyph.draw()
            else: #make all the other line shorter (e.g. 5 and 10 are stressed, whereas 6, 7, 8, 9 are merely marked)
                v = (r-(3/140)*r) * cos(radians(90-6*i))
                w = (r-(3/140)*r) * sin(radians(90-6*i))
            zaseka = visual.Line(self.win, start = (x,y), end = (v,w),  units = 'pix') 
            zaseka.setLineColor(color)
            zaseka.draw()

        fixcir = visual.Circle(self.win, radius = 0.025*r, edges = edges_of_the_clockface, fillColor = color, lineColor = color, units = 'pix')
        fixcir.draw()
        self.win.flip()
        core.wait(0.05)
        clockface = visual.BufferImageStim(self.win, buffer = 'front')
        self.clockface = clockface 

    def draw_the_ball(self, ang):

        r = self.radius
        v = (r-0.13*r) * cos(radians(90-ang*(360/self.amount_steps)))
        w = (r-0.13*r) * sin(radians(90-ang*(360/self.amount_steps)))

        self.ball.pos = (v, w)  
        self.ball.draw()

    def text_window(self, text):
        event.clearEvents()
        while True:
            text_to_show = visual.TextStim(self.win, text = text, color = 'black', wrapWidth=1.5, antialias=True, units = 'norm', height = 0.06)
            text_to_show.draw()
            self.win.flip()
            press_to_start = event.getKeys()
            if len(press_to_start) > 0:
                break
            core.wait(0.25) 


    def rotation(self):

        #initializing trial
        event.clearEvents()
        timer = core.Clock()
        start_ang = int(random.uniform(1, ceil(self.amount_steps)))
        is_ang_fin_reached = False
        ang_fin = None

        ang = start_ang 
        i = 0
        while is_ang_fin_reached == False:

            #check if pressed
            press = event.getKeys(timeStamped=timer) 
            if len(press) > 0 and ang_fin is None:
                waiting_int = press[0][1] * 1000
                ang_press = ang
                clocktime_press = (ang_press / self.amount_steps) * 60

                #initialize ang_fin
                ang_fin = ang + int(random.uniform(ceil(500/self.one_step_dur), ceil (800/self.one_step_dur))) #determing the angle when the clock is to stop
                if ang_fin > self.amount_steps: #if angle is more than 154 and does not exist, correct it by the number of angles
                    ang_fin = ang_fin - self.amount_steps

            #Drawing
            self.clockface.draw()
            self.draw_the_ball(ang)
            self.win.flip()

            #Going to the next angle and checking whether the next cycle is on and whether the ang_fin is reached
            ang = ang + 1 
            if ang > self.amount_steps:
                ang = ang - self.amount_steps    
            if ang == ang_fin:
                is_ang_fin_reached = True

            i += 1


        press_info = {'Waiting': waiting_int, 'Angle_start' : start_ang, 'Angle_finish' : ang_fin, 'Clocktime_press:': clocktime_press, 'Extra_msecs' : round(timer.getTime() * 1000 - ( self.one_step_dur * i))}


        return press_info

    def judgement(self, warning_text):

        text_to_decide = visual.TextStim(win = self.win, text = warning_text, color = 'black', units = 'norm', wrapWidth=1.5, antialias=True)
        text_to_decide.draw()
        self.win.flip()
        event.clearEvents()
        core.wait(0.3)

        timer = core.Clock()
        self.clockface.draw()
        self.win.flip()
        event.clearEvents()
        mouse = event.Mouse(win = self.win)
        wasitclicked = mouse.getPressed()
        while wasitclicked[0] == False:
            x_pix, y_pix = mouse.getPos()
            wasitclicked = mouse.getPressed()
        recall_duration = timer.getTime()

        x = x_pix/self.radius
        y = y_pix/self.radius
        dist = sqrt(x**2 + y**2)
        angle = degrees(acos(x/dist))
        if y < 0:
            angle = 360-angle
        n = 90 - angle
        if n < 0:
            n = n + 360 

        clocktime_report = (1/6) * n #from 360-deg circle to 60 pseudosecond-scale

        judge_info = {'Waiting_recall': recall_duration, 'Clocktime_reported': clocktime_report}

        return (judge_info)




if __name__ == '__main__':


    the_clock = LClock(screen_height = 1024, screen_weight = 786, refresh_rate = 60, duration_desired = 2560)
    the_clock.make_the_clockface(edges_of_the_clockface = 100, color = 'black')

    is_ang_fin_reached = False
    to_rotate = True
    ang_fin = None
    event.clearEvents()
    waiting = core.StaticPeriod(screenHz = 60)
    while to_rotate == True:
        for ang in range (1, (ceil(the_clock.amount_steps) + 1)):        
            if ang == ang_fin:
                is_ang_fin_reached = True
            press = event.getKeys() 
            if len(press) > 0 and ang_fin is None:
                was_not_pressed = False
                ang_fin = ang + int(random.uniform(ceil(500/the_clock.one_step_dur), ceil (800/the_clock.one_step_dur)))
                if ang_fin > ceil(the_clock.amount_steps):
                    ang_fin = ang_fin - ceil(the_clock.amount_steps)
            if is_ang_fin_reached == False:
                waiting.start(the_clock.one_step_dur*0.001)
                the_clock.clockface.draw()
                the_clock.draw_the_ball(ang, 'red')
                the_clock.win.flip()
                waiting.complete()
            if is_ang_fin_reached == True:
                waiting.start(the_clock.one_step_dur*0.001)
                the_clock.clockface.draw()
                the_clock.win.flip()
                waiting.complete()
        if is_ang_fin_reached == True:
            to_rotate = False    