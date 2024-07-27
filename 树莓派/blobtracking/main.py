import cv2
import time
import numpy as np
from threading import Thread
from servo import Servo
from pid import PID

# 初始化伺服电机

pan = Servo(pin=17)
tilt = Servo(pin=18)
panAngle =  0
tiltAngle = 45
pan.set_angle(panAngle)
tilt.set_angle(tiltAngle)


# 定义视频流类
class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.stream.set(cv2.CAP_PROP_FPS, 30)
        self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.grabbed, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            self.grabbed, self.frame = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

# 启动视频流
vs = VideoStream(src=0).start()

# 设置 PID 控制器参数
pan_pid = PID(0.05, 0.01, 0.001)
tilt_pid = PID(0.05, 0.01, 0.001)
pan_pid.initialize()
tilt_pid.initialize()

def reset():
    panAngle = 0
    tiltAngle = 10
    pan.set_angle(panAngle)
    tilt.set_angle(tiltAngle) 
# 计算帧率
fps = 0
pos = (10, 20)
font = cv2.FONT_HERSHEY_SIMPLEX
height = 0.5
weight = 1
myColor = (0, 0, 255)

def nothing(x):
    pass
'''
cv2.namedWindow('PID Tuner')
cv2.createTrackbar('Pan Kp', 'PID Tuner', int(pan_pid.kP * 100), 100, nothing)
cv2.createTrackbar('Pan Ki', 'PID Tuner', int(pan_pid.kI * 100), 100, nothing)
cv2.createTrackbar('Pan Kd', 'PID Tuner', int(pan_pid.kD * 100), 100, nothing)
cv2.createTrackbar('Tilt Kp', 'PID Tuner', int(tilt_pid.kP * 100), 100, nothing)
cv2.createTrackbar('Tilt Ki', 'PID Tuner', int(tilt_pid.kI * 100), 100, nothing)
cv2.createTrackbar('Tilt Kd', 'PID Tuner', int(tilt_pid.kD * 100), 100, nothing)
'''
last_update = time.time()
update_interval = 0.1  # 控制更新频率

try:
    while True:
        tStart = time.time()
        frame = vs.read()
        if frame is None:
            print("Failed to grab frame")
            break

        frame = cv2.flip(frame, 1)
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #cv2.putText(frame, str(int(fps)) + ' FPS', pos, font, height, myColor, weight)

        lowerBound = np.array([168, 89, 72])
        upperBound = np.array([255, 150, 198])

        myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
        contours, _ = cv2.findContours(myMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) > 0:
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            contour = contours[0]
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

            # 计算误差
            print(x, y, w, h)
            errorX = (x + w / 2) - (480)
            errorY = (y + h / 2) - (320) 
            #errorY = (240 / 2) - (y + h / 2)  # 反转误差方向
            #errorX = x + w / 2
            #errorY = y + h / 2  # 反转误差方向
            print(errorX, errorY)

            if time.time() - last_update > update_interval:
                # 获取PID参数并更新
                #pan_pid.kP = cv2.getTrackbarPos('Pan Kp', 'PID Tuner') / 100
                #pan_pid.kI = cv2.getTrackbarPos('Pan Ki', 'PID Tuner') / 100
                #pan_pid.kD = cv2.getTrackbarPos('Pan Kd', 'PID Tuner') / 100
                #tilt_pid.kP = cv2.getTrackbarPos('Tilt Kp', 'PID Tuner') / 100
                #tilt_pid.kI = cv2.getTrackbarPos('Tilt Ki', 'PID Tuner') / 100
                #tilt_pid.kD = cv2.getTrackbarPos('Tilt Kd', 'PID Tuner') / 100
                pan_pid.kP = 5/ 100
                pan_pid.kI = 0/ 100
                pan_pid.kD = 0/ 100
                tilt_pid.kP = 5/ 100
                tilt_pid.kI = 0/ 100
                tilt_pid.kD = 0/ 100
                panAdjustment = pan_pid.update(errorX, sleep=0)
                tiltAdjustment = tilt_pid.update(errorY, sleep=0)

                panAngle += panAdjustment
                tiltAngle += tiltAdjustment

                # 限制角度范围
                panAngle = max(-50, min(panAngle, 50))
                tiltAngle = max(40, min(tiltAngle, 60))

                # 设置伺服电机角度
                pan.set_angle(panAngle)
                tilt.set_angle(tiltAngle)
                last_update = time.time()

        # 仅在图形环境中显示图像窗口
        try:
            cv2.imshow('Camera', frame)
            #cv2.imshow('Mask', myMask)
        except cv2.error as e:
            print(f"OpenCV error: {e}")

        if cv2.waitKey(1) == ord('q'):
            break

        tEnd = time.time()
        loopTime = tEnd - tStart
        fps = .9 * fps + .1 * (1 / loopTime)

finally:
    vs.stop()
    cv2.destroyAllWindows()



