import serial 
import time
import serial.tools.list_ports
import threading
import struct
 
port_list = list(serial.tools.list_ports.comports())
print(port_list)
 
if len(port_list) == 0:
    print("无可用串口！")
else:
    for i in range(0, len(port_list)):
        print(port_list[i])
        
DATA = "" # 读取的数据
DATA_ALL = bytearray(40960)
DATA_LEN = 0
NOEND = True # 是否读取结束
CYCLING = False
DATA_IN_FLAG = 0
START_TIME = 0
EXITCMD = False
PERIOD = 0.05
INIT_TIME = 0
LOGFILE = "Pressure log.txt"
 
# 读数据的本体
def read_data(ser):
    global DATA, NOEND , DATA_IN_FLAG , START_TIME, DATA_ALL , DATA_LEN, INIT_TIME, LOGFILE, CYCLING
    START_TIME = time.time()
    
    # 循环接收数据（此为死循环，可用线程实现）
    while NOEND:
        if ser.in_waiting:
            START_TIME = time.time()
            DATA_IN_FLAG = 1
            length = ser.in_waiting
            
            DATA = ser.read(length)# 注意 ser.read了之后 in_waiting马上变成0了
            
            for i in  range(0, length):
                DATA_ALL[DATA_LEN+i] = DATA[i]
            
            DATA_LEN+=length
            
            if(DATA == "quit"):
                print("oppo seri has closen.\n>>", end="")
                    
        else:
            if DATA_IN_FLAG:
                #print("time.time() - START_TIME = %d \r\n"%(time.time()))
                if time.time() - START_TIME > 0.010:#串口超时10ms
                    DATA_PRINT = bytearray(DATA_LEN)
                    for i in  range(0, DATA_LEN):
                        DATA_PRINT[i] = DATA_ALL[i]
                    
                    DATA_PRINT = DATA_PRINT.hex()

                    # 自定义的MODBUS传感器数据格式
                    time_log = time.time() - INIT_TIME
                    # 大小端转换
                    hb, lb = DATA_PRINT[6:10], DATA_PRINT[10:14]
                    value = lb + hb
                    value = struct.unpack('!f', bytes.fromhex(value))[0]
                    if not CYCLING:
                        print("\n>> receive: ", DATA_PRINT, "\n value: ", value,"\n time: ", time_log, "\n>>", end="")
                    else:
                        log_message = str(time_log) + "," + str(value) + "\n"
                        with open(LOGFILE,"a") as f:
                            f.write(log_message)

                    START_TIME = time.time()
                    DATA_IN_FLAG = 0
                    DATA_LEN = 0

# 打开串口
def open_seri(portx, bps, timeout):
    ret = False
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
 
        # 判断是否成功打开
        if(ser.is_open):
            ret = True
            th = threading.Thread(target=read_data, args=(ser,)) # 创建一个子线程去等待读数据
            th.start()
    except Exception as e:
        print("error!", e)
 
    return ser, ret, th
 
 
 
# 关闭串口
def close_seri(ser):
    global NOEND, CYCLING
    NOEND = False
    CYCLING = False
    ser.close()
 
# 写数据
def write_to_seri(ser, text):
    text.replace("\n", "")
    res = ser.write(bytes.fromhex(text)) # 写
    return res
 
# 读数据
def read_from_seri():
    global DATA
    data = DATA
    DATA = "" #清空当次读取
    return data

# 周期发送
def cycle_send(ser, text, period = 5):
    global CYCLING
    while CYCLING:
        #print(text)
        write_to_seri(ser, text)
        time.sleep(period)
 
if __name__ == "__main__":
    # 打开一个串口
    port = input("输入串口名：")
    ser, ret, tr = open_seri(port, 19200, None) # 串口com3、bps为19200，等待时间为永久
    cf = False

    INIT_TIME = time.time()

    while True:
        # 单发模式
        text = input(">>")
        print(text)
        if text == "quit":
            close_seri(ser)
            tr.join()
            print("bye!")
            break
        if text == "cycle":
            # 进入循环发送模式
            cf = True
            break
        write_to_seri(ser, text)
    
    if cf == True:
        CYCLING = True
        # 自定义的传感器消息log表头
        with open(LOGFILE,"a") as f:
            f.write("Time(sec),Value(MPa)\n")
        text = input(">>")
        # 循环发送线程
        tc = threading.Thread(target=cycle_send, args=(ser, text, PERIOD))
        tc.start()
        while True:
            cmd = input(">>")
            if cmd == 'q' or cmd == 'Q':
                close_seri(ser)
                #等待线程结束
                tc.join()
                tr.join()
                print("bye!")
                break
        

