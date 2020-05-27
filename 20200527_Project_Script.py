import math
import smbus
import smtplib
import time

#---------------

#Change at setup

userName="Sammy Joe" #change to the name of the wearer
careEmail="abc@outlook.co.uk" #change to the caregiver's email

#---------------

GRAVITY=9.80665

class mpu6050:
        
    address=None
    bus=None
    
    SCALE_MODIFIER_2G=16384.0
    SCALE_MODIFIER_4G=8192.0
    SCALE_MODIFIER_8G=4096.0
    SCALE_MODIFIER_16G=2048.0
    
    RANGE_2G=0x00
    RANGE_4G=0x08
    RANGE_8G=0x10
    RANGE_16G=0x18
    
    PWR_MGMT_1=0x6B
    PWR_MGMT_2=0x6C
    
    XOUT=0x3B
    YOUT=0x3D
    ZOUT=0x3F
    
    ACCEL_CONFIG=0x1C
    
    def __init__(self,address,bus=1):
        self.address=address
        self.bus=smbus.SMBus(bus)
        self.bus.write_byte_data(self.address,self.PWR_MGMT_1,0x00)
        
    def read_i2c_word(self,register):        
        value=((self.bus.read_byte_data(self.address,register))<<8)+self.bus.read_byte_data(self.address,register+1)
        if (value>=0x8000):
            return -((65535-value)+1)
        else:
            return value
    
    def set_accel_range(self,accel_range):
        self.bus.write_byte_data(self.address,self.ACCEL_CONFIG,0x00)
        self.bus.write_byte_data(self.address,self.ACCEL_CONFIG,accel_range)
        
    def read_accel_range(self, raw=False):
        raw_data=self.bus.read_byte_data(self.address,self.ACCEL_CONFIG)
        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data==self.ACCEL_RANGE_2G:
                return 2
            elif raw_data==self.ACCEL_RANGE_4G:
                return 4
            elif raw_data==self.ACCEL_RANGE_8G:
                return 8
            elif raw_data==self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1
                
    def get_accel_data(self,g=False):
        
        x=self.read_i2c_word(self.XOUT)
        y=self.read_i2c_word(self.YOUT)
        z=self.read_i2c_word(self.ZOUT)
        
        scale_modifier=None
        aRange=self.read_accel_range(True)
        
        if aRange==self.RANGE_2G:
            scale_modifier=self.SCALE_MODIFIER_2G
        elif aRange==self.RANGE_4G:
            scale_modifier=self.SCALE_MODIFIER_4G
        elif aRange==self.RANGE_8G:
            scale_modifier=self.SCALE_MODIFIER_8G
        elif aRange==self.RANGE_16G:
            scale_modifier=self.SCALE_MODIFIER_16G
        else:
            scale_modifier=self.ACCEL_SCALE_MODIFIER_2G
            
        x=x/scale_modifier
        y=y/scale_modifier
        z=z/scale_modifier
        
        if g is True:
            return {'x':x,'y':y,'z':z}
        elif g is False:
            x=x*GRAVITY
            y=y*GRAVITY
            z=z*GRAVITY
            return {'x':x,'y':y,'z':z}

def send_alert_email():

    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('','') #Paste credentials here

    subject="EMERGENCY: FALL DETECTED"
    body="On {0} at {1} a fall was detected, please ensure {2} is safe".format(time.strftime("%d/%m/%Y",time.gmtime()),time.strftime("%H:%M:%S",time.gmtime()),userName)

    server.sendmail("E4S.IoT.DR@gmail.com",careEmail,"Subject: {0}\n\n{1}".format(subject,body))

while True:

    aScaled=mpu6050(0x68).get_accel_data()
    
    aX=aScaled['x']
    aY=aScaled['y']
    aZ=aScaled['z']
    
    smvXYZ=math.sqrt((aX**2)+(aY**2)+(aZ**2))
    
    if smvXYZ>=5*GRAVITY:
        send_alert_email()
    else:
        if smvXYZ>=1.4*GRAVITY:
            trunk=math.degrees(math.acos((aZ)/(smvXYZ)))
            if trunk>=60:
                send_alert_email()
