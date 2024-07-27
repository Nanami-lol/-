from pyb import UART, Timer, LED
import pyb
import sensor
from image import SEARCH_EX, SEARCH_DS
import sensor, image, time, struct
clock = time.clock()
threshold=(0, 73)
angle_err = 0
angle = 0
mode = 1
i = 0
flag = [0,0,0,0,0]
uart = UART(3, 115200)
rect_flag = 0
roi = [(0, 40, 5, 5),
	   (20, 40, 5, 5),
	   (37, 40, 5, 5),
	   (55, 40, 5, 5),
	   (75, 40, 5, 5)]
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQQVGA)
sensor.skip_frames(time=2000)
sensor.set_contrast(-3)
clock = time.clock()
rect_templates = ["/rect1.pgm", "/rect2.pgm", "/rect3.pgm"]
def straight( ):
	global goallineflag
	clock.tick()
	img = sensor.snapshot().binary([threshold])
	line = img.get_regression([(255,255)], robust=True)
	if line:
		img.draw_line(line.line(), color=127)
		angle = line.theta()
		if angle >= 90:
			angle_err =  angle - 90
		else:
			angle_err =  angle + 90
		print(angle_err)
		data = struct.pack('bbbb', 0xFF, angle_err, 0x01, 0xEE)
		uart.write(data)
def pulse():
	img = sensor.snapshot().binary([threshold])
	for t in rect_templates:
		   template = image.Image(t)
		   r = img.find_template(template, 0.50, step=4, search=SEARCH_EX)
		   if r:
				img.draw_rectangle(r)
				print(t)
				rect_flag = 1
				angle_err = 90
				start = pyb.millis()
				while True:
					if  pyb.elapsed_millis(start) >= 2000:
						break
					else:
						straight()
				start_time = pyb.millis()
				while True:
					if pyb.elapsed_millis(start_time) >=5000:
						break
					else :
						print('pulsing')
						data = struct.pack('bbbb', 0xFF, angle_err, 0x00, 0xEE)
						uart.write(data)
def turn():
	clock.tick()
	img = sensor.snapshot().binary([threshold])
	line = img.get_regression([(255,255)], robust=True)
	if not line:
		while True:
			img = sensor.snapshot().binary([threshold])
			line = img.get_regression([(255,255)], robust=True)
			if not line:
				angle_err = 250
				print('turning for lines')
				data = struct.pack('bbbb', 0xFF, angle_err, 0x00, 0xEE)
				uart.write(data)
			else:
				break
while True:
	straight()
	pulse()
	turn()