###For correct display of Graphics it is suggested to use Psychopy software (or any other software with corresponding version of Python)

from psychopy import visual, core, monitors, clock, event, logging, parallel
import pyglet
from math import radians, atan2, sin, cos, floor, ceil, acos, asin, degrees, sqrt
import random
import pandas as pd 

### GENERAL SETTINGS
datafile = open("W_test.txt", "w") #creation of a log-file for PRESCREENING of data! All the Data is accumulated in .csv file (see the script bottom)
logging.console.setLevel(logging.CRITICAL) #for conveniece of use non-compatible Python versions. Note that without this setting, a lot of extra logs are present in console (meaningless ones)
#portEEG = parallel.ParallelPort(address=16124) 
screen_width = 1024 #pix IF YOU DON'T WANT TO USE FULL SCREEN WINDOW
screen_height = 768 #pix
r  = 0.34 * screen_height #set coefficient according to your own experiment place
refresh = 60 #refresh rate of the monotor
step = 1000/refresh #Duration of a step of rotation, ms
duration = 2560 #The overall duration
duration_upd = 2566.7 #Correction of duration according to the speed of particular PC (must be constant - check the .csv file)
amount = duration / step #Amount of red ball steps
script_code = 1 #W-script; = 9 for M-script. Script Code is used for diferentiation of exp modes in the EEG recording
win = visual.Window(size = (screen_width, screen_height),color = (1,1,1), monitor = '', units='pix')
trial_number = 2

### CREATION OF THE CLOCK FACE USING PSYCHOPY GRAPHICAL FUNCTIONS
circ = visual.Circle(win, radius=r, edges = 100,  units = 'pix')
circ.setLineColor("black")
circ.draw()
for i in range (1, 61):
    x = r * cos (radians(90-6*i))
    y = r * sin(radians(90-6*i))
    if i % 5 == 0:
        v = (r-(1/14)*r) * cos(radians(90-6*i))
        w = (r-(1/14)*r) * sin(radians(90-6*i))
        c1 = (r + 0.085*r) * cos(radians(90 - 6*i))
        c2 = (r + 0.085*r) * sin(radians(90-6*i))
        cyph = visual.TextStim(win, pos = (c1,c2), text= str(i), color = 'black',  units = 'pix' )
        cyph.draw()
    else:
        v = (r-(3/140)*r) * cos(radians(90-6*i))
        w = (r-(3/140)*r) * sin(radians(90-6*i))
    zaseka = visual.Line(win, start = (x,y), end = (v,w),  units = 'pix')
    zaseka.setLineColor('black')
    zaseka.draw()
fixcir = visual.Circle(win, radius = 0.025*r, edges = 1000, color = 'black', units = 'pix')
fixcir.draw()
win.flip()
core.wait(0.05)
clockey = visual.BufferImageStim(win, buffer = 'front')

### DETERMINE A FUNCTION FOR RED BALL TO ROTATE
def draw_the_ball(ang):
    v = (r-0.13*r) * cos(radians(90-ang*(360/amount)))
    w = (r-0.13*r) * sin(radians(90-ang*(360/amount)))
    ball = visual.Circle(win, radius = 0.024*r, edges = 100, pos = (v,w), fillColor = 'red', lineColor = 'red', units = 'pix')
    ball.draw()

def text_window(text_pr):
    event.clearEvents()
    while True:
        text_to_show = visual.TextStim(win, text = text_pr, color = 'black', wrapWidth=1.5, antialias=True, units = 'norm', height = 0.06)
        text_to_show.draw()
        win.flip()
        press_to_start = event.getKeys()
        if len(press_to_start) > 0:
            break
        core.wait(0.25) 
##############################################################################################
### TUTORIAL START - CAN BE SKIPPED

text_pr = 'WELCOME TEXT'
text_window(text_pr)

text_pr = 'PRESENTING CLOCK TEXT'
text_window(text_pr)

#presenting clock
event.clearEvents()
while True:
    clockey.draw()
    win.flip()
    press_to_start = event.getKeys()
    if len(press_to_start) > 0:
        break
    core.wait(0.25) 


text_pr = 'PRESENTING RED BALL TEXT'
text_window(text_pr)

rot_end = False
to_rotate = True
ang_fin = None
event.clearEvents()
waiting = core.StaticPeriod(screenHz = 60)
while to_rotate == True:
    for ang in range (1, (ceil(amount) + 1)):        
        if ang == ang_fin:
            rot_end = True
        press = event.getKeys() 
        if len(press) > 0 and ang_fin is None:
            was_not_pressed = False
            ang_fin = ang + int(random.uniform(ceil(500/step), ceil (800/step)))
            if ang_fin > ceil(amount):
                ang_fin = ang_fin - ceil(amount)
        if rot_end == False:
            waiting.start(step*0.001)
            clockey.draw()
            draw_the_ball(ang)
            win.flip()
            waiting.complete()
        if rot_end == True:
            waiting.start(step*0.001)
            clockey.draw()
            win.flip()
            waiting.complete()
    if rot_end == True:
        to_rotate = False    


text_pr = 'INSTRUCTIONS TEXT'
text_window(text_pr)

text_pr = 'ARE YOU READY-LIKE TEXT'
text_window(text_pr)
####################################TUTORIAL END###################################################

### CREATION OF EMPTY LISTS TO FURTHER ACCUMULATE DATA TO THE .CSV FILE
time_of_recall = [i for i in range(trial_number)]
absolute_time_of_recall_s = [i for i in range(trial_number)]
time_of_press_ms = [i for i in range(trial_number)]
absolute_time_of_press_s = [i for i in range(trial_number)]
real_duration_ms = [i for i in range(trial_number)]
position_reported_in_pseudo_s = [i for i in range(trial_number)]
report_to_real_ms = [i for i in range(trial_number)]
difference_btw_reported_and_real_time_ms = [i for i in range(trial_number)]
early_press = [i for i in range(trial_number)]

#CLOCK ROTATION ONSET
for trial in range(trial_number):
    #portEEG.setData(script_code) #trial start, pin with respect to script_code
    waiting = core.StaticPeriod(screenHz = 60)
    abs_timer = core.Clock()
    timer_press = core.Clock()
    rot_end = False
    to_rotate = True
    ang_fin = None
    i = 0
    early_press[trial] = 0
    shift = 0
    real_duration_ms[trial] = duration_upd
    start_ang = int(random.uniform(1, ceil(amount)))
    while to_rotate == True:
        timer_press.reset()
        for ang in range (start_ang, (ceil(amount) + 1)):        
            if ang == ang_fin:
                rot_end = True
            press = event.getKeys(timeStamped=timer_press) 
            if len(press) > 0 and ang_fin is None:
                #portEEG.setData(2) #press is made
                was_not_pressed = False
                time_of_press_ms[trial] = press[0][1] * 1000
                absolute_time_of_press_s[trial] = abs_timer.getTime()
                ang_fin = ang + int(random.uniform(ceil(500/step), ceil (800/step)))
                if ang_fin > ceil(amount):
                    ang_fin = ang_fin - ceil(amount)
                    shift = 1
            if rot_end == False:
                waiting.start(step*0.001)
                clockey.draw()
                draw_the_ball(ang)
                win.flip()
                waiting.complete()
            elif rot_end == True:
                to_rotate = False
                break
        if to_rotate == True and i != 0:
            real_duration_ms[trial] = timer_press.getTime() * 1000 
        i = i + 1
        #if to_rotate == True:
            #portEEG.setData(4+i%2) #12 o'clock 
        start_ang = 1
    if i == 1 or (i == 2 and shift == 1):
        early_press[trial] = 1

    ### JUDGEMENT PHASE
    text_to_decide = visual.TextStim(win, text = 'W/M', color = 'black', units = 'norm', wrapWidth=1.5, antialias=True)
    text_to_decide.draw()
    win.flip()
    event.clearEvents()
    core.wait(0.3)

    #portEEG.setData(8) #judgement clock onset
    timer_for_recall = core.Clock()
    clockey.draw()
    win.flip()
    event.clearEvents()
    mouse = event.Mouse(win = win)
    wasitclicked = mouse.getPressed()
    while wasitclicked[0] == False:
        x_pix, y_pix = mouse.getPos()
        wasitclicked = mouse.getPressed()
    #portEEG.setData(7)
    time_of_recall[trial] = timer_for_recall.getTime()
    absolute_time_of_recall_s[trial] = abs_timer.getTime()

    x = x_pix/r
    y = y_pix/r
    dist = sqrt(x**2 + y**2)
    angle = degrees(acos(x/dist))
    if y < 0:
        angle = 360-angle
    n = 90 - angle
    if n < 0:
        n = n + 360 
    position_reported_in_pseudo_s[trial] = (1/6) * n
    report_to_real_ms[trial] = (position_reported_in_pseudo_s[trial]/60) * real_duration_ms[trial] 
    difference_btw_reported_and_real_time_ms[trial] = report_to_real_ms[trial] - time_of_press_ms[trial]


    if (trial + 1) < trial_number:
        text_pr = 'NEXT TRIAL START AFTER PRESS'
        text_window(text_pr)
        
    else:
        after_text = visual.TextStim(win, text = 'FIN', color = 'black', units = 'norm', wrapWidth=1.5, antialias=True)
        after_text.draw()
        win.flip()
        core.wait(8.5)  

###########################################################################
###SOME MANIPULATION FOR MAKING PRESCREENING MORE CONVINIENT (AVERAGING DATA)
#simple filtering bad trials (for prescreening use only - all the data are included into Data_Frame without any kind of filtering!)
real_duration_ms_filtered = []
time_of_press_ms_filtered = []
position_reported_in_pseudo_s_filtered = []
report_to_real_ms_filtered = []
difference_btw_reported_and_real_time_ms_filtered = []
trials_saved = 0
for i in range (trial_number):
    if abs(difference_btw_reported_and_real_time_ms[i]) < 1000:
        real_duration_ms_filtered.append(real_duration_ms[i])
        time_of_press_ms_filtered.append(time_of_press_ms[i])
        position_reported_in_pseudo_s_filtered.append(position_reported_in_pseudo_s[i])
        report_to_real_ms_filtered.append(report_to_real_ms[i])
        difference_btw_reported_and_real_time_ms_filtered.append(difference_btw_reported_and_real_time_ms[i])
        trials_saved = trials_saved + 1
trials_dropped = trial_number - trials_saved

#a function for averaging a list
def average_of_list(list):
    average = sum(list)/len(list)
    return average

################################################################################################################

### AFTER ALL
win.close()

Data_Frame = pd.DataFrame({'Early press (before first reaching 12)': early_press,
'Time of a press (with respect to 12 o"clock), ms': time_of_press_ms,
'Time of press (absolute), s': absolute_time_of_press_s,
'Updated duration of a cycle, ms': real_duration_ms,
'Reported position (W), pseudosecons':  position_reported_in_pseudo_s,
'Reported position converted to time W (with respect to 12 o"oclock), ms': report_to_real_ms,
'Difference between W and real time of a press, ms': difference_btw_reported_and_real_time_ms,
'Time of recall (from onset of recall window), ms': time_of_recall,
'Time of recall (absolute), s': absolute_time_of_recall_s})

Data_Frame.to_csv('Name.csv')