'''
使用时仅调整摄像头阈值和焦距
'''
import sensor
import time

class laser:
    def __init__(self):
        sensor.reset()  # Reset and initialize the sensor.
        sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
        sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
        sensor.skip_frames(time=2000)  # Wait for settings take effect.
        sensor.set_contrast(-3)
        sensor.set_brightness(-1)
        sensor.set_auto_gain(False)
        sensor.set_auto_whitebal(False)
        sensor.set_auto_exposure(False, exposure_us=2000)
        self.clock = time.clock()  # Create a clock object to track the FPS.
        self.laser = [(38, 100, 22, 127, -128, 127)]

    def find_laser(self, threshold):
        img = sensor.snapshot()
        blobs = img.find_blobs(threshold)
        if blobs:
            b = blobs[0]
            cx = b.cx()
            cy = b.cy()
            img.draw_cross(cx, cy, color=(0, 255, 128))
            return cx, cy
        return None, None

    def run(self):
        self.clock.tick()  # Update the FPS clock.
        laser_x, laser_y = self.find_laser(self.laser)
        print(laser_x, laser_y)
            #print(self.clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
            # to the IDE. The FPS should increase once disconnected.

# 在主函数中使用
#if __name__ == "__main__":
    #openmv = laser()
    #while True:
        #openmv.run()
