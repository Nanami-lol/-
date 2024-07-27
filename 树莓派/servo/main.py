import RPi.GPIO as GPIO
from time import sleep
 
servo_pin = 12                # 舵机信号线接树莓派GPIO17
 
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT, initial=False)
 
# 旋转角度转换到PWM占空比
def angleToDutyCycle(angle):
    return 2.5 + angle / 180.0 * 10
 
p = GPIO.PWM(servo_pin, 50)    # 初始频率为50HZ
p.start(angleToDutyCycle(90))  # 舵机初始化角度为90
sleep(0.05)
p.ChangeDutyCycle(0)           # 清空当前占空比，使舵机停止抖动

if __name__ == '__main__':
    print('当前为90度')
    while True:
        angle = int(input('旋转度数：'))
        if angle >= 0 and angle <= 180:
            p.ChangeDutyCycle(angleToDutyCycle(angle))
            sleep(0.1)
            p.ChangeDutyCycle(0) # 清空当前占空比，使舵机停止抖动
        else:
            print('旋转度数在0-180之间！')