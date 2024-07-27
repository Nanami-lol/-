import serial
import time
#open serial
ser = serial.Serial("/dev/ttyAMA0", 115200)#set up serial
def main():
    while True:
        # 获得接收缓冲区字符
        count = ser.inWaiting()
        if count != 0:
            # 读取内容并回显
            recv = ser.read(count)  #树莓派串口接收数据
            ser.write(recv)         #树莓派串口发送数据
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
    
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        if ser != None:
            ser.close()