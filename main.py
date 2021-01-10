from guizero import App, Box, Text, PushButton, TextBox
import obd
from datetime import datetime
from signal import pause
from gpiozero import LED 
from gpiozero import Button
from picamera import PiCamera
from gps import *
from subprocess import check_call

###Set Defintions###

def checkphysicalbutton():
    button.when_pressed = capture
    power.when_held = shutdown
    getPositionData(gpsd)

#get gps info
def getPositionData(gps): #kind of copyed and pasted from gpsd
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        time = getattr(nx, 'time' , "Unknown")
        gps_lbl_resp_lon.value = str(round(longitude,2))
        gps_lbl_resp_lat.value = str(round(latitude,2))
        gps_lbl_resp_time.value = str(time)

#capture video    
def capture():
    if ready.is_lit: #are we alreading recording? if not record 
        #try:
        recording.on() #set recrding LED
        ready.off() #say we are not ready to record - we already are
        now = datetime.now() #get current date and time
        today = now.strftime("m-%md-%dy-%Yh-%Hm-%M-s%S")
        camera.start_preview(fullscreen=False, window = (650, 400, 150,100)) #show what we are recording
        camera.start_recording('/media/pi/VID/%s.h264' % today, 'h264') #record it
        today = now.strftime("m-%md-%dy-%Yh-%Hm-%M-s%S") #reset the day
    else: #second push to turn it off
        #try: #shut it down
        recording.off()
        led_write.on()
        camera.stop_recording()
        led_write.off()
        now = datetime.now()
        camera.stop_preview()
        ready.on() #Turn the ready light back on

#Nicely shut down the PI
def shutdown():
   check_call(['sudo', 'poweroff']) #Nicely turn off the pi

#Get the OBDII codes - could probably do this in one funtion with a while loop like the save. 
def code1():
    cmd = obd.commands.SPEED # select an OBD command (sensor)
    response = connection.query(cmd)
    res1.value = str(response.value.magnitude)

def code2(): 
    cmd = obd.commands.RPM # select an OBD command (sensor)
    response = connection.query(cmd)
    res2.value = str(response.value.magnitude)

def code3():
    cmd = obd.commands.ENGINE_LOAD # select an OBD command (sensor)
    response = connection.query(cmd)
    res3.value = str(round(response.value.magnitude,2))

def code4():
    cmd = obd.commands.COOLANT_TEMP # select an OBD command (sensor)
    response = connection.query(cmd)
    res4.value = str(response.value.magnitude)
def code5():
    cmd = obd.commands.INTAKE_PRESSURE # select an OBD command (sensor)
    response = connection.query(cmd)
    res5.value = str(response.value.magnitude)

def code6():
    cmd = obd.commands.INTAKE_TEMP # select an OBD command (sensor)
    response = connection.query(cmd)
    res6.value = str(response.value.magnitude)

def code7():
    cmd = obd.commands.MAF # select an OBD command (sensor)
    response = connection.query(cmd)
    res7.value = str(round(response.value.magnitude, 2))

def code8():
    cmd = obd.commands.FUEL_LEVEL # select an OBD command (sensor)
    response = connection.query(cmd)
    res8.value = str(round(response.value.magnitude, 2))

def code9():
    cmd = obd.commands.BAROMETRIC_PRESSURE # select an OBD command (sensor)
    response = connection.query(cmd)
    res9.value = str(response.value.magnitude)

def code10():
    cmd = obd.commands.AMBIANT_AIR_TEMP # select an OBD command (sensor)
    response = connection.query(cmd)
    res10.value = str(response.value.magnitude)

def gs_save():
    if gps_log:
        nx = gpsd.next()
        # For a list of all supported classes and fields refer to:
        # https://gpsd.gitlab.io/gpsd/gpsd_json.html
        led_write.on()
        if nx['class'] == 'TPV':
            latitude = getattr(nx,'lat', "Unknown")
            longitude = getattr(nx,'lon', "Unknown")
            time = getattr(nx, 'time' , "Unknown")
            #if gps_log:
            fileObject = open("GPSLOC.txt", "a")
            fileObject.write("Your position: lon = " + str(longitude) + ", lat = " + str(latitude) + ", Time is: " + str(time) + "\n")
            fileObject.close()
            gps_lbl_resp_lon.value = str(round(longitude,2))
            gps_lbl_resp_lat.value = str(round(latitude,2))
            gps_lbl_resp_time.value = str(time)
        led_write.off()
        
#Save the OBDII results to a txt file.
def OBDIIsave():
    print("Button was pressed")
    led_write.on()
    for i in range(len(obd_codes)):
        try:            
            cmd = obd_codes[i]
            response = connection.query(cmd)
            print(response.value)
            obd_fileObject = open("obdii-" + obd_today + ".txt", "a")
            obd_fileObject.write(str(response.value) + "\n")
            obd_fileObject.close()
            sleep(0.1)
        except:
            print(i)
    led_write.off()

def get_waypoint():
    nx = gpsd.next()
    # For a list of all supported classes and fields refer to:
    # https://gpsd.gitlab.io/gpsd/gpsd_json.html
    led_write.on()
    if nx['class'] == 'TPV':
        latitude = getattr(nx,'lat', "Unknown")
        longitude = getattr(nx,'lon', "Unknown")
        time = getattr(nx, 'time' , "Unknown")
        #if gps_log:
        fileObject = open(str(gps_waypoint.value) + ".txt", "a")
        fileObject.write("Your position: lon = " + str(longitude) + ", lat = " + str(latitude) + ", Time is: " + str(time) + "\n")
        fileObject.close()
        gps_lbl_resp_lon.value = str(round(longitude,2))
        gps_lbl_resp_lat.value = str(round(latitude,2))
        gps_lbl_resp_time.value = str(time)
    led_write.off()

def set_waypoint():
    if gps_log == False:
        gps_log = True
    if gps_log:
        gps_log = False

###Gloabal VARs

now = datetime.now() 
today = now.strftime("%m%d%Y%H%M%S")
camera = PiCamera()
gps_log = False

# SET IO
button = Button(2) #RED - J
recording = LED(4) #
ready = LED(14)
power = Button(15, hold_time=2)
led_write = LED(18)

#OBDII
obd_codes = [obd.commands.SPEED, obd.commands.RPM, obd.commands.ENGINE_LOAD, obd.commands.COOLANT_TEMP, obd.commands.INTAKE_PRESSURE, obd.commands.INTAKE_TEMP, obd.commands.MAF, obd.commands.FUEL_LEVEL, obd.commands.BAROMETRIC_PRESSURE, obd.commands.AMBIANT_AIR_TEMP]
connection = obd.OBD() # auto-connects to USB or RF port
obd_now = datetime.now()
obd_today = obd_now.strftime("%m%d%Y%H%M%S")

#SET LEDS
ready.on()
recording.off()

#GPS conn
gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)

#####GUI SECTION####
#GUI VARs
app = App(width=600, height=650, layout="grid")
box1 = Box(app, layout="grid", width=300, height=250, grid=[0,0], border=1)
box2 = Box(app, layout="grid", width=300, height=50, grid=[0,1], border=1)
box3 = Box(app, layout="grid", width=300, height=250, grid=[1,0], border=1)
box4 = Box(app, layout="grid", width=300, height=100, grid=[1,1], border=1)

#check outside stimuli
app.repeat(100, checkphysicalbutton)

###set box1###

#Set lables#
lbl1 = Text(box1, text="Speed = ", grid=[0,0], align="left")
lbl2 = Text(box1, text="RPM = ", grid=[0,1], align="left") 
lbl3 = Text(box1, text="Engine Load = ", grid=[0,2], align="left")
lbl4 = Text(box1, text="Coolant Temp = ", grid=[0,3], align="left")
lbl5 = Text(box1, text="Intake pressure = ", grid=[0,4], align="left")
lbl6 = Text(box1, text="Intake Temp = ", grid=[0,5], align="left")
lbl7 = Text(box1, text="MAF = ", grid=[0,6], align="left")
lbl8 = Text(box1, text="Fuel Level = ", grid=[0,7], align="left")
lbl9 = Text(box1, text="Baremetric Presure = ", grid=[0,8], align="left")
lbl10 = Text(box1, text="Ambiant Temp = ", grid=[0,9], align="left")
lbl11 = Text(box1, text="kph", grid=[2,0], align="right")
lbl12 = Text(box1, text="RPM", grid=[2,1], align="right") 
lbl13 = Text(box1, text="%", grid=[2,2], align="right")
lbl14 = Text(box1, text="degC", grid=[2,3], align="right")
lbl15 = Text(box1, text="kPa", grid=[2,4], align="right")
lbl16 = Text(box1, text="degC", grid=[2,5], align="right")
lbl17 = Text(box1, text="gps", grid=[2,6], align="right")
lbl18 = Text(box1, text="%", grid=[2,7], align="right")
lbl19 = Text(box1, text="kPa", grid=[2,8], align="right")
lbl20 = Text(box1, text="degC", grid=[2,9], align="left")

#Respnses readings from reader
res1 = Text(box1, text="resp", grid=[1,0], align="left")
res2 = Text(box1, text="resp", grid=[1,1], align="left")
res3 = Text(box1, text="resp", grid=[1,2], align="left")
res4 = Text(box1, text="resp", grid=[1,3], align="left")
res5 = Text(box1, text="resp", grid=[1,4], align="left")
res6 = Text(box1, text="resp", grid=[1,5], align="left")
res7 = Text(box1, text="resp", grid=[1,6], align="left")
res8 = Text(box1, text="resp", grid=[1,7], align="left")
res9 = Text(box1, text="resp", grid=[1,8], align="left")
res10 = Text(box1, text="resp", grid=[1,9], align="left")
res1.repeat(1000, code1)
res2.repeat(1000, code2)
res3.repeat(1000, code3)
res4.repeat(1000, code4)
res5.repeat(1000, code5)
res6.repeat(1000, code6)
res7.repeat(1000, code7)
res8.repeat(1000, code8)
res9.repeat(1000, code9)
res10.repeat(1000, code10)

###SET BOX2###
btn_save = PushButton(box2, text="SAVE", command=OBDIIsave, grid=[0,0])
btn_err = PushButton(box2, text="Error", grid=[1,0])

###SET BOX3###
gps_lbl_lon = Text(box3, text="longitude :", grid=[0,0])
gps_lbl_lat = Text(box3, text="latitude :", grid=[0,1])
gps_lbl_time = Text(box3, text="Time :", grid=[0,2])
gps_lbl_resp_lon = Text(box3, text="resp", grid=[1,0], align="left")
gps_lbl_resp_lat = Text(box3, text="resp", grid=[1,1])
gps_lbl_resp_time = Text(box3, text="resp", grid=[0,3,1,3])

###SET BOX4
gps_btn_save = PushButton(box4, text="WayPoint", grid=[0,0])
gps_btn_log = PushButton(box4, text="Start-log", command=get_waypoint, grid=[1,0])
gps_waypoint = TextBox(box4, text="whereamI?", grid=[0,1,1,1])

app.display()
