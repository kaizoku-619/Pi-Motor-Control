import RPi.GPIO as GPIO
import time
import sys
import tty
import termios
UP = 0
DOWN = 1
RIGHT = 2
LEFT = 3

def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    if ch == '0x03':
        raise KeyboardInterrupt
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return ord(c3) - 65  # 0=Up, 1=Down, 2=Right, 3=Left arrows

def init():
	GPIO.output(11,0)
	GPIO.output(12,0)
	GPIO.output(13,0)

def Forward():
	GPIO.output(11,0)
	GPIO.output(12,1)
	GPIO.output(13,0)

def Right():
	GPIO.output(11,1)
	GPIO.output(12,0)
	GPIO.output(13,0)

def Left():
	GPIO.output(11,0)
	GPIO.output(12,0)
	GPIO.output(13,1)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11,GPIO.OUT)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

init()
while True:
	keyp = readkey()
	if keyp == UP:
		Forward()
		print 'Forward'
	elif keyp == RIGHT:
		print 'Right'
		Right()
	elif keyp == LEFT:
		Left()
		print 'Left'
	elif keyp == 'x':
	    print 'exit'
	    GPIO.cleanup()
	    exit()