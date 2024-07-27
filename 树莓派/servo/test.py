
#!/usr/bin/python
# coding:utf-8
# servo_PWM_GPIO.py
# 树莓派GPIO控制外部舵机来回摆动，角度范围为0~180°，周期为4秒。
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges. "
          " You can achieve this by using 'sudo' to run your script")
import time


def servo_map(before_value, before_range_min, before_range_max, after_range_min, after_range_max):
    """
    功能:将某个范围的值映射为另一个范围的值
    参数：原范围某值，原范围最小值，原范围最大值，变换后范围最小值，变换后范围最大值
    返回：变换后范围对应某值
    """
    percent = (before_value - before_range_min) / (before_range_max - before_range_min)
    after_value = after_range_min + percent * (after_range_max - after_range_min)
    return after_value


GPIO.setmode(GPIO.BOARD)  # 初始化GPIO引脚编码方式
servo_SIG = 12
servo_VCC = 4
servo_GND = 6
servo_freq = 50
servo_time = 0.01
servo_width_min = 2.5
servo_width_max = 12.5
# servo_degree_div =servo_width_max - servo_width_min)/180
GPIO.setup(servo_SIG, GPIO.OUT)
# 如果你需要忽视引脚复用警告，请调用GPIO.setwarnings(False)
GPIO.setwarnings(False)
servo = GPIO.PWM(servo_SIG, servo_freq)  # 信号引脚=servo_SIG 频率=servo_freq in HZ
servo.start(10)
'''
servo.ChangeDutyCycle((servo_width_min+servo_width_max)/2)  # 回归舵机中位
print('预设置完成，两秒后开始摆动')
time.sleep(2)
try:  # try和except为固定搭配，用于捕捉执行过程中，用户是否按下ctrl+C终止程序
    while 1:
        for dc in range(1, 181, 1):
            dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max)
            servo.ChangeDutyCycle(dc_trans)
            # print(dc_trans)
            time.sleep(servo_time)
        time.sleep(0.2)
        for dc in range(180, -1, -1):
            dc_trans = servo_map(dc, 0, 180, servo_width_min, servo_width_max)
            servo.ChangeDutyCycle(dc_trans)
            # print(dc_trans)
            time.sleep(servo_time)
        time.sleep(0.2)
except KeyboardInterrupt:
    pass
servo.stop()  # 停止pwm
GPIO.cleanup()  # 清理GPIO引脚
'''