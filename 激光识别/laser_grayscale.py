'''
使用时调整灰度阈值和色块面积阈值
'''
import sensor, image, time

class laser:
    def __init__(self):
        sensor.reset()
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.VGA)
        sensor.skip_frames(time = 2000)
        self.threshold = [(200, 255)]
        self.clock = time.clock()

    def find_laser(self, img):
        blobs = img.find_blobs(self.threshold)
        if blobs:
            b = blobs[0]
            cx = b.cx()
            cy = b.cy()
            img.draw_cross(cx, cy, color=(0, 0, 0))
            return cx, cy
        return None, None

    def run(self):
        while(True):
            self.clock.tick()
            img = sensor.snapshot()
            laser_x, laser_y = self.find_laser(img)
            print(laser_x, laser_y)

# 使用方法：
#detector = laser()
#detector.run()
