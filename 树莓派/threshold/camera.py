import cv2
import numpy as np
cap = cv2.VideoCapture(0)#打开内置摄像机
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
flag = 1#播放视频
count = 0;#记录照相的次数
while cap.isOpened():#当摄像头打开时
    ret,frame=cap.read()#读取当前摄像头画面
    cv2.imshow('img',frame)#显示当前摄像头画面
    if cv2.waitKey(flag)==ord(' '):#按下空格键拍照
         c = str(count)#将countint转换成str型
         cv2.imwrite(c+'.jpg',frame)#保存图片
         count=count+1#计数加一
    if cv2.waitKey(flag)==ord('q'):#退出循环
        break;
cv2.destroyAllWindows()#关闭所有窗口
cap.release()#释放摄像头