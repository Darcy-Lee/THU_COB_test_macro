from ctypes import *
import platform
import time
from usb_device import *
from usb2spi import *
from usb2gpio import *
from ctypes import c_ubyte, byref

# 定义电压输出值
POWER_LEVEL_NONE    = 0 # 不输出
POWER_LEVEL_1V8     = 1 # 输出1.8V
POWER_LEVEL_2V5     = 2 # 输出2.5V
POWER_LEVEL_3V3     = 3 # 输出3.3V
POWER_LEVEL_5V0     = 4 # 输出5.0V

def scan_and_open_device():
    DevHandles = (c_uint * 20)()
    ret = USB_ScanDevice(byref(DevHandles))
    if ret == 0:
        print("No device connected!")
        return None
    else:
        pass
        # print("Have %d device(s) connected!" % ret)
    ret = USB_OpenDevice(DevHandles[0])
    if bool(ret):
        # print("Open device success!")
        return DevHandles[0]
    else:
        print("Open device failed!")
        return None

def get_device_info(DevHandle):
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandle, byref(USB2XXXInfo), byref(USB2XXXFunctionString))
    if bool(ret):
        # print("USB2XXX device information:")
        # print("--Firmware Name: %s" % bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
        # print("--Firmware Version: v%d.%d.%d" % ((USB2XXXInfo.FirmwareVersion >> 24) & 0xFF, (USB2XXXInfo.FirmwareVersion >> 16) & 0xFF, USB2XXXInfo.FirmwareVersion & 0xFFFF))
        # print("--Hardware Version: v%d.%d.%d" % ((USB2XXXInfo.HardwareVersion >> 24) & 0xFF, (USB2XXXInfo.HardwareVersion >> 16) & 0xFF, USB2XXXInfo.HardwareVersion & 0xFFFF))
        # print("--Build Date: %s" % bytes(USB2XXXInfo.BuildDate).decode('ascii'))
        # print("--Serial Number: ", end='')
        for i in range(len(USB2XXXInfo.SerialNumber)):
            pass
            # print("%08X" % USB2XXXInfo.SerialNumber[i], end='')
        # print("")
        # print("--Function String: %s" % bytes(USB2XXXFunctionString.value).decode('ascii'))
    else:
        print("Get device information failed!")

def initialize_spi(DevHandle,ClockSpeedHz=1000*1000):
    SPIConfig = SPI_CONFIG()
    SPIConfig.Mode = SPI_MODE_SOFT_HDX
    SPIConfig.Master = SPI_MASTER
    SPIConfig.CPOL = 0
    SPIConfig.CPHA = 0
    SPIConfig.LSBFirst = SPI_MSB
    SPIConfig.SelPolarity = SPI_SEL_LOW
    SPIConfig.ClockSpeedHz = ClockSpeedHz

    ret = SPI_Init(DevHandle, SPI1_CS0, byref(SPIConfig))
    if ret != SPI_SUCCESS:
        print("Initialize SPI failed!")
        return False
    else:
        # print("Initialize SPI success")
        return True

def set_power_level(DevHandle, level):
    state = DEV_SetPowerLevel(DevHandle, level)
    if not state:
        print("Set power level error!")
        return False
    else:
        # print("Set power level success")
        return True

def gpio_test(DevHandle):
    GPIO_SetOutput(DevHandle, 0x00FF, 0)
    for i in range(10):
        GPIO_Write(DevHandle, 0x00FF, 0x00AA)
        GPIO_Write(DevHandle, 0x00FF, 0x0055)


def testen_up(DevHandle):
    GPIO_SetOutput(DevHandle, 0x0010, 0)
    ret = GPIO_Write(DevHandle, 0x0010, 0x0010)
    if ret != SPI_SUCCESS:
        print("testen_up failed!")
        return False
    else:
        print("testen_up success")
        return True


def testen_down(DevHandle):
    GPIO_SetOutput(DevHandle, 0x0010, 0)
    ret = GPIO_Write(DevHandle, 0x0010, 0x0000)
    if ret != SPI_SUCCESS:
        print("testen_down failed!")
        return False
    else:
        print("testen_down success")
        return True


def select_subip(DevHandle,target_ip):
    GPIO_SetOutput(DevHandle, 0x0007, 0)
    GPIO_Write(DevHandle, 0x0007, target_ip)


def spi_write_data(DevHandle):
    WriteBuffer = (c_ubyte * 2)()
    for i in range(len(WriteBuffer)):
        WriteBuffer[i] = 0x81
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    if ret != SPI_SUCCESS:
        print("SPI write data failed!")
        return False
    else:
        print("SPI write data success!")
        return True

def close_device(DevHandle):
    ret = USB_CloseDevice(DevHandle)
    if bool(ret):
        pass
        # print("Close device success!")
    else:
        print("Close device failed!")


def send_cmd(DevHandle,cmd):
    WriteBuffer = (c_ubyte * 1)(cmd)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    return ret

def send_cmd_GPIOCS(DevHandle,cmd):
    WriteBuffer = (c_ubyte * 1)(cmd)

    GPIO_SetOutput(DevHandle, 0x0010, 0)
    ret = GPIO_Write(DevHandle, 0x0010, 0x0000)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    ret = GPIO_Write(DevHandle, 0x0010, 0x0010)

    return ret

def send_testbits(DevHandle, testbits):
    cmd = 0x0F

    WriteBuffer = (c_ubyte * 9)(
        cmd  & 0xFF,
        (testbits >> 56) & 0xFF,
        (testbits >> 48) & 0xFF,
        (testbits >> 40) & 0xFF,
        (testbits >> 32) & 0xFF,
        (testbits >> 24) & 0xFF,
        (testbits >> 16) & 0xFF,
        (testbits >> 8) & 0xFF,
        testbits & 0xFF
    )

    # print("Set testbits: ", testbits)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    if (ret != SPI_SUCCESS):
        # print("Write Page faild!")
        exit()
    else :
        pass
        # print("Write Page success!")

def send_testbits_GPIOCS(DevHandle, testbits):
    cmd = 0x0F

    WriteBuffer = (c_ubyte * 9)(
        cmd  & 0xFF,
        (testbits >> 56) & 0xFF,
        (testbits >> 48) & 0xFF,
        (testbits >> 40) & 0xFF,
        (testbits >> 32) & 0xFF,
        (testbits >> 24) & 0xFF,
        (testbits >> 16) & 0xFF,
        (testbits >> 8) & 0xFF,
        testbits & 0xFF
    )

    # print('WriteBuffer:', WriteBuffer)
    GPIO_SetOutput(DevHandle, 0x0010, 0)

    ret = GPIO_Write(DevHandle, 0x0010, 0x0000)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    ret = GPIO_Write(DevHandle, 0x0010, 0x0010)

    if (ret != SPI_SUCCESS):
        print("Write Page faild!")
        exit()
    else :
        print("Write Page success!")

def stress_test(DevHandle):
    cmd = 0xEA
    stress_code = 0x00_02

    WriteBuffer = (c_ubyte * 17)(
        cmd & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        (stress_code >> 8) & 0xFF,
        stress_code & 0xFF
    )

    # print('WriteBuffer:', WriteBuffer)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    if (ret != SPI_SUCCESS):
        print("stress test faild!")
        exit()
    else:
        print("stress test success!")

    return

def stress_test_GPIOCS(DevHandle):
    cmd = 0xEA
    stress_code = 0x00_02

    WriteBuffer = (c_ubyte * 17)(
        cmd & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        0x00 & 0xFF,
        (stress_code >> 8) & 0xFF,
        stress_code & 0xFF
    )

    GPIO_SetOutput(DevHandle, 0x0010, 0)

    ret = GPIO_Write(DevHandle, 0x0010, 0x0000)
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    # if (ret != SPI_SUCCESS):
    #     print("stress test faild!")
    #     exit()
    # else:
    #     print("stress test success!")
    #
    # return
    string=input("输入测量值:")
    ret = GPIO_Write(DevHandle, 0x0010, 0x0010)
    return string

def enter_test_mode(DevHandle):
    data_values = [0x88, 0x28, 0x45]
    for data in data_values:
        ret = send_cmd(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Enter test mode failed!")
        return False
    else:
        # print("Enter test mode success!")
        return True

def enter_test_mode_GPIOCS(DevHandle):
    data_values = [0x88, 0x28, 0x45]
    for data in data_values:
        ret = send_cmd_GPIOCS(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Enter test mode failed!")
        return False
    else:
        # print("Enter test mode success!")
        return True

def exit_test_mode(DevHandle):
    data_values = [0x92]
    for data in data_values:
        ret = send_cmd(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Exit test_mode failed!")
        return False
    else:
        # print("Exit test_mode success!")
        return True

def exit_test_mode_GPIOCS(DevHandle):
    data_values = [0x92]
    for data in data_values:
        ret = send_cmd_GPIOCS(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Exit test_mode failed!")
        return False
    else:
        # print("Exit test_mode success!")
        return True

def read_status_reg(DevHandle, display=True):
    WriteBuffer = (c_ubyte * 1)(0x05)
    ReadBuffer = (c_ubyte * 1)()

    ret = SPI_WriteReadBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer), byref(ReadBuffer),
                             len(ReadBuffer), 0)
    if (ret != SPI_SUCCESS):
        print("SPI write&read data faild!")
        exit()
    else:
        # print("SPI write&read data:")
        for i in range(0, len(ReadBuffer)):

            if display:
                print('Status Reg:',format(ReadBuffer[i], '08b'), end='\n')
            return format(ReadBuffer[i], '08b')

def read_RRAM(DevHandle, ax, ay, addr_sr, read_byte_length):
    # 拼接4个字节的数据
    # 0x03 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    tmp = (0x03 << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)

    # 4个字节分割
    WriteBuffer = (c_ubyte * 4)(
        (tmp >> 24) & 0xFF,
        (tmp >> 16) & 0xFF,
        (tmp >> 8) & 0xFF,
        tmp & 0xFF
    )

    ReadBuffer = (c_ubyte * read_byte_length)()

    ret = SPI_WriteReadBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer), byref(ReadBuffer),
                             len(ReadBuffer), 0)
    if ret != SPI_SUCCESS:
        print("SPI write&read data failed!")
        exit()
    else:
        # print("Read RRAM:")
        read_data_list = []
        for i in range(0, len(ReadBuffer)):
            # print("%02X " % ReadBuffer[i], end='')
            read_data_list.append("%02X" % ReadBuffer[i])
            # if (i+1)%64==0 : print('\n')
        print('\n', end='')
    read_data_str = ' '.join(read_data_list)
    return read_data_str


def margin_Read_80(DevHandle, ax, ay, addr_sr, read_byte_length):
    # 用80指令读取数据，包括ECC bit都会输出出来。
    # 拼接4个字节的数据
    # 0x80 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    tmp = (0x80 << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)

    # 4个字节分割
    WriteBuffer = (c_ubyte * 4)(
        (tmp >> 24) & 0xFF,
        (tmp >> 16) & 0xFF,
        (tmp >> 8) & 0xFF,
        tmp & 0xFF
    )

    ReadBuffer = (c_ubyte * (read_byte_length + 1))()

    ret = SPI_WriteReadBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer), byref(ReadBuffer),
                             len(ReadBuffer), 0)
    if ret != SPI_SUCCESS:
        print("SPI write&read data failed!")
        exit()
    else:
        read_data_list = []
        for i in range(0, len(ReadBuffer)):
            read_data_list.append("%02X" % ReadBuffer[i])
        print('\n', end='')
    read_data_list = read_data_list[1:]
    read_data_str = ' '.join(read_data_list)
    return read_data_str


def margin_Read_81(DevHandle, ax, ay, addr_sr, read_byte_length):
    # 用81指令读取数据，包括ECC bit都会输出出来。
    # 拼接4个字节的数据
    # 0x80 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    tmp = (0x81 << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)

    # 4个字节分割
    WriteBuffer = (c_ubyte * 4)(
        (tmp >> 24) & 0xFF,
        (tmp >> 16) & 0xFF,
        (tmp >> 8) & 0xFF,
        tmp & 0xFF
    )

    ReadBuffer = (c_ubyte * (read_byte_length + 1))()

    ret = SPI_WriteReadBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer), byref(ReadBuffer),
                             len(ReadBuffer), 0)
    if ret != SPI_SUCCESS:
        print("SPI write&read data failed!")
        exit()
    else:
        read_data_list = []
        for i in range(0, len(ReadBuffer)):
            read_data_list.append("%02X" % ReadBuffer[i])
    read_data_list = read_data_list[1:]
    read_data_str = ' '.join(read_data_list)
    return read_data_str


def write_page(DevHandle, ax, ay, addr_sr, page_hex_string_Noprefix):
    #给出16进制无前缀的page string

    # page_hex_string_Noprefix='000137'
    page_int=int(page_hex_string_Noprefix,16)  #把string当做16进制字符串转为py的整数
    # page_bin_string=bin(page_int)#整数转为2进制字符串
    page_bin_length = len(page_hex_string_Noprefix) * 4  # 计算所需的二进制字符串长度page_hex是十六进制
    page_bin_string = '0b{:0{width}b}'.format(page_int, width=page_bin_length)  # 转为指定长度的二进制字符串

    #处理cmd_addr
    # 拼接4个字节的数据
    # 0x03 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    cmd_addr = (0x0A << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)
    cmd_addr_bin_string = '0b{:032b}'.format(cmd_addr)
    # cmd_addr_bin_string=bin(cmd_addr)#转为二进制字符串

    #合并
    dummy='0b0000'
    output_string = cmd_addr_bin_string[2:] + page_bin_string[2:] + dummy[2:]

    # SPI write bits
    output_byte_str=output_string.encode('utf-8')#encode函数会将二进制字符串转为字节字符串
    ret = SPI_WriteBits(DevHandle,SPI1_CS0,output_byte_str)

    if(ret != SPI_SUCCESS):
        # print("Write Page faild!")
        exit()
    else:
        pass
        # print("Write Page success!")


def write_page_nodummy(DevHandle, ax, ay, addr_sr, page_hex_string_Noprefix):
    #给出16进制无前缀的page string

    # page_hex_string_Noprefix='000137'
    page_int=int(page_hex_string_Noprefix,16)  #把string当做16进制字符串转为py的整数
    # page_bin_string=bin(page_int)#整数转为2进制字符串
    page_bin_length = len(page_hex_string_Noprefix) * 4  # 计算所需的二进制字符串长度page_hex是十六进制
    page_bin_string = '0b{:0{width}b}'.format(page_int, width=page_bin_length)  # 转为指定长度的二进制字符串

    #处理cmd_addr
    # 拼接4个字节的数据
    # 0x03 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    cmd_addr = (0x0A << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)
    cmd_addr_bin_string = '0b{:032b}'.format(cmd_addr)
    # cmd_addr_bin_string=bin(cmd_addr)#转为二进制字符串

    #合并
    dummy='0b0000'
    output_string = cmd_addr_bin_string[2:] + page_bin_string[2:] #+ dummy[2:]

    # SPI write bits
    output_byte_str=output_string.encode('utf-8')#encode函数会将二进制字符串转为字节字符串

    # start_time = time.time()

    ret = SPI_WriteBits(DevHandle,SPI1_CS0,output_byte_str)

    # write_time_cost=(time.time()-start_time)

    if(ret != SPI_SUCCESS):
        print("Write Page faild!")
        exit()
    else:
        # print('3',1000*(time.time()-start_time))
        return 0
        # print("Write Page success!")


def write_page_GPIOCS(DevHandle, ax, ay, addr_sr, page_hex_string_Noprefix):
    #给出16进制无前缀的page string

    # page_hex_string_Noprefix='000137'
    page_int=int(page_hex_string_Noprefix,16)  #把string当做16进制字符串转为py的整数
    # page_bin_string=bin(page_int)#整数转为2进制字符串
    page_bin_length = len(page_hex_string_Noprefix) * 4  # 计算所需的二进制字符串长度page_hex是十六进制
    page_bin_string = '0b{:0{width}b}'.format(page_int, width=page_bin_length)  # 转为指定长度的二进制字符串

    #处理cmd_addr
    # 拼接4个字节的数据
    # 0x03 (8位) | 4'b0000 (4位) | ax (11位) | ay (5位) | addr_sr (4位)
    cmd_addr = (0x0A << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)
    cmd_addr_bin_string = '0b{:032b}'.format(cmd_addr)
    # cmd_addr_bin_string=bin(cmd_addr)#转为二进制字符串

    #合并
    dummy='0b0000'
    output_string = cmd_addr_bin_string[2:] + page_bin_string[2:] + dummy[2:]

    # SPI write bits
    output_byte_str=output_string.encode('utf-8')#encode函数会将二进制字符串转为字节字符串
    GPIO_SetOutput(DevHandle, 0x0010, 0)

    ret = GPIO_Write(DevHandle, 0x0010, 0x0000)
    ret = SPI_WriteBits(DevHandle,SPI1_CS0,output_byte_str)
    ret = GPIO_Write(DevHandle, 0x0010, 0x0010)

    if(ret != SPI_SUCCESS):
        print("Write Page faild!")
        exit()
    else:
        print("Write Page success!")


def read_ID(DevHandle):
    WriteBuffer = (c_ubyte * 1)(0x9F)
    ReadBuffer = (c_ubyte * 3)()

    ret = SPI_WriteReadBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer), byref(ReadBuffer),
                             len(ReadBuffer), 0)
    if (ret != SPI_SUCCESS):
        print("SPI write&read data faild!")
        exit()
    else:
        print("SPI write&read data:")
        for i in range(0, len(ReadBuffer)):
            print("%02X " % ReadBuffer[i], end='')
        print('\n')

    # print(ReadBuffer)
    # if(ReadBuffer==[0x09,0x01,0x13]):
    #     print('Read ID success!')
    # else:
    #     print('Read ID failed!')

def write_enable(DevHandle):
    data_values = [0x06]
    for data in data_values:
        ret = send_cmd(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Write enable failed!")
        return False
    else:
        # print("Write enable success!")
        return True

def write_enable_GPIOCS(DevHandle):
    data_values = [0x06]
    for data in data_values:
        ret = send_cmd_GPIOCS(DevHandle,data)
    if ret != SPI_SUCCESS:
        print("Write enable failed!")
        return False
    else:
        print("Write enable success!")
        return True


def forming(DevHandle):
    data_values = [0xA9]
    for data in data_values:
        send_cmd(DevHandle, data)


def dword_forming(DevHandle, ax, ay, addr_sr):
    tmp = (0x82 << 24) | (0x0 << 20) | ((ax & 0x7FF) << 9) | ((ay & 0x1F) << 4) | (addr_sr & 0xF)

    # 5个字节分割
    WriteBuffer = (c_ubyte * 5)(
        (tmp >> 24) & 0xFF,
        (tmp >> 16) & 0xFF,
        (tmp >> 8) & 0xFF,
        tmp & 0xFF,
        0x00
    )

    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))


def stress(DevHandle, ax, ay, addr_sr, dinhv_add, dinhv, stress_code):
    tmp = (0xEA << 128) | (0x0 << 124) | ((ax & 0x7FF) << 113) | ((ay & 0x1F) << 108) | ((addr_sr & 0xF) << 104) | ((dinhv_add & 0xF) << 28) | ((dinhv & 0xFFF) << 16) | (stress_code & 0xFFFF)
    # 17个字节分割
    WriteBuffer = (c_ubyte * 17)(
        (tmp >> 128) & 0xFF,
        (tmp >> 120) & 0xFF,
        (tmp >> 112) & 0xFF,
        (tmp >> 104) & 0xFF,
        (tmp >> 96) & 0xFF,
        (tmp >> 88) & 0xFF,
        (tmp >> 80) & 0xFF,
        (tmp >> 72) & 0xFF,
        (tmp >> 64) & 0xFF,
        (tmp >> 56) & 0xFF,
        (tmp >> 48) & 0xFF,
        (tmp >> 40) & 0xFF,
        (tmp >> 32) & 0xFF,
        (tmp >> 24) & 0xFF,
        (tmp >> 16) & 0xFF,
        (tmp >> 8) & 0xFF,
        tmp & 0xFF 
    )
    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))

def precycle(DevHandle):
    data_values = [0xD9]
    for data in data_values:
        send_cmd(DevHandle, data)

def write_chkbd(DevHandle):
    data_values = [0xEF]
    for data in data_values:
        send_cmd(DevHandle, data)

#其实是同一个函数,差异在testbits中体现
def write_ichkbd(DevHandle):
    data_values = [0xEF]
    for data in data_values:
        send_cmd(DevHandle, data)

def verify_read(DevHandle):
    cmd = 0xFD
    info = 0x40
    WriteBuffer = (c_ubyte * 2)(
        cmd & 0xFF,
        info & 0xFF
    )

    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))


def clear_status_reg(DevHandle):

    cmd=0x1F
    info=0x01
    dummy=0x00
    WriteBuffer = (c_ubyte * 3)(
        cmd & 0xFF,
        info & 0xFF,
        dummy & 0xFF
    )

    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    if ret != SPI_SUCCESS:
        print("clear_status_reg failed")
        exit()
    else:
        print("clear_status_reg success")

def clear_repair(DevHandle):

    cmd=0x1F
    info=0x03
    dummy=0x00
    WriteBuffer = (c_ubyte * 3)(
        cmd & 0xFF,
        info & 0xFF,
        dummy & 0xFF
    )

    ret = SPI_WriteBytes(DevHandle, SPI1_CS0, byref(WriteBuffer), len(WriteBuffer))
    if ret != SPI_SUCCESS:
        print("clear_status_reg failed")
        exit()
    else:
        print("clear_status_reg success")

if __name__ == '__main__':
    DevHandle = scan_and_open_device()
    if DevHandle is None:
        exit()

    get_device_info(DevHandle)

    if not initialize_spi(DevHandle):
        exit()

    if not set_power_level(DevHandle, POWER_LEVEL_1V8):
        exit()

    gpio_test(DevHandle)

    # enter_test_mode(DevHandle)
    # read_status_reg(DevHandle)
    read_ID(DevHandle)
    # read_RRAM(DevHandle, 0x0, 0x0, 0x0, 4)
    # page_hex_string_Noprefix = '000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9FA0A1A2A3A4A5A6A7A8A9AAABACADAEAFB0B1B2B3B4B5B6B7B8B9BABBBCBDBEBFC0C1C2C3C4C5C6C7C8C9CACBCCCDCECFD0D1D2D3D4D5D6D7D8D9DADBDCDDDEDFE0E1E2E3E4E5E6E7E8E9EAEBECEDEEEFF0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F3031323334353637'
    # write_page(DevHandle,0,0,0,page_hex_string_Noprefix)

    testbits=0x00_00_04_00_00_00_00_00
    send_testbits(DevHandle,testbits)



    close_device(DevHandle)
