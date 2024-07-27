# 自动RGB565颜色跟踪示例
#
# 这个例子展示了使用OpenMV的单色自动RGB565色彩跟踪。
'''
import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
clock = time.clock()

# 捕捉图像中心的颜色阈值。
r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] #感兴趣区
for i in range(60):#这个60大概值，没有实际意义
    img = sensor.snapshot()
    img.draw_rectangle(r, color = (255, 255, 0), thickness = 1)#画出想确定阈值的感兴趣区

threshold = [50, 50, 0, 0, 0, 0] # Middle L, A, B values.
for i in range(60):
    img = sensor.snapshot().lens_corr(1.6)#镜头矫正
    hist = img.get_histogram(roi=r)
    lo = hist.get_percentile(0.01) # 获取1％范围的直方图的CDF（根据需要调整）！
    hi = hist.get_percentile(0.99) # 获取99％范围的直方图的CDF（根据需要调整）！
    # 平均百分位值。
    threshold[0] = (threshold[0] + int(lo.l_value()/2)) // 2#Lmin
    threshold[1] = (threshold[1] + int(hi.l_value()/2)) // 2#Lmax
    threshold[2] = (threshold[2] + int(lo.a_value()*1.2)) // 2#Amin
    threshold[3] = (threshold[3] + int(hi.a_value()*1.2)) // 2#Amax
    threshold[4] = (threshold[4] + int(lo.b_value()*1.2)) // 2#Bmin
    threshold[5] = (threshold[5] + int(hi.b_value()*1.2)) // 2#Bmax
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)


print("threshold",threshold)
#(30, 55, 29, 53, -9, 40)
while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    #print(clock.fps())
'''
import sensor, image, time


sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.


while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    # to the IDE. The FPS should increase once disconnected.
    hist = img.get_histogram()
    Thresholds = hist.get_threshold()
    print(Thresholds)
    v = Thresholds.value()
    img.binary([(0,v)])
