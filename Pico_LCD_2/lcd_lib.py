from machine import Pin,SPI,PWM
import framebuf
import time
import os

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9


class LCD_2inch(framebuf.FrameBuffer): # For 320x240 display
    def __init__(self):
        self.width = 320
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        self.black =   0x0000
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x01)
        self.write_data(0x3f)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
        
  
pwm = PWM(Pin(BL))
pwm.freq(1000)
pwm.duty_u16(32768)#max 65535

LCD = LCD_2inch()
#color BRG
LCD.fill(LCD.white)


LCD.show()



key0 = Pin(15,Pin.IN,Pin.PULL_UP)
key1 = Pin(3,Pin.IN,Pin.PULL_UP)
key2 = Pin(17 ,Pin.IN,Pin.PULL_UP)
key3 = Pin(2 ,Pin.IN,Pin.PULL_UP)


running = True

while running:
    
    t = 0
    
    if key0.value() == 0:
        LCD.fill_rect(15,15,30,30,LCD.red)
        t=t+1
    else: 
        LCD.fill_rect(15,15,30,30,LCD.white)
        LCD.rect(15,15,30,30,LCD.red)
        
        
    if(key1.value() == 0):
        LCD.fill_rect(15,195,30,30,LCD.red)
        t=t+2
    else :
        LCD.fill_rect(15,195,30,30,LCD.white)
        LCD.rect(15,195,30,30,LCD.red)
        
    if(key2.value() == 0):
        LCD.fill_rect(275,15,30,30,LCD.red)
        t=t+4
    else :
        LCD.fill_rect(275,15,30,30,LCD.white)
        LCD.rect(275,15,30,30,LCD.red)
        
    if(key3.value() == 0):
        LCD.fill_rect(275,195,30,30,LCD.red)
        t=t+8
    else :
        LCD.fill_rect(275,195,30,30,LCD.white)
        LCD.rect(275,195,30,30,LCD.red)
        
    if(t !=0):
        LCD.fill_rect(114,120,120,8,LCD.white)
        LCD.text("key "+str(t)+" pressed",114,120,LCD.red)
    else:
        LCD.fill_rect(114,120,120,8,LCD.white)
        
    LCD.show()
time.sleep(1)
LCD.fill(0xFFFF)

