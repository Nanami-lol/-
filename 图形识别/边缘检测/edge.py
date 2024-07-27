import sensor, image, time

class edgedetect:
    def __init__(self):
        self.kernel_size = 1
        self.kernel = [-1, -1, -1, -1, +8, -1, -1, -1, -1]
        self.thresholds = [(100, 255)] # grayscale thresholds设置阈值

        sensor.reset() # 初始化 sensor.
        sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
        sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
        sensor.skip_frames(10) # 让新的设置生效
        self.clock = time.clock() # 跟踪FPS帧率
        if (sensor.get_id() == sensor.OV7725):
            sensor.__write_reg(0xAC, 0xDF)
            sensor.__write_reg(0x8F, 0xFF)

    def run(self):
        self.clock.tick() # 追踪两个snapshots()之间经过的毫秒数.
        img = sensor.snapshot() # 拍一张照片，返回图像
        img.laplacian(1, sharpen=True)
        img.morph(self.kernel_size, self.kernel)
        img.binary(self.thresholds)
        img.erode(2, threshold = 2)
        #print(self.clock.fps()) # 注意: 当连接电脑后，OpenMV会变成一半的速度。当不连接电脑，帧率会增加。

# 在主函数中使用
#if __name__ == "__main__":
#    openmv = edgedetect()
#    while True:
#        openmv.run()
