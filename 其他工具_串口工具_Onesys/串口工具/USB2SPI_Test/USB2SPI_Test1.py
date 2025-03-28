"""
文件说明：USB2XXX ADC相关函数测试程序
更多帮助：www.usbxyz.com
"""
from ctypes import *
import platform
from time import sleep
from usb_device import *
from usb2spi import *

# 定义电压输出值
POWER_LEVEL_NONE    = 0 # 不输出
POWER_LEVEL_1V8     = 1 # 输出1.8V
POWER_LEVEL_2V5     = 2 # 输出2.5V
POWER_LEVEL_3V3     = 3 # 输出3.3V
POWER_LEVEL_5V0     = 4 # 输出5.0V


if __name__ == '__main__': 
    DevIndex = 0
    DevHandles = (c_uint * 20)()
    # Scan device
    ret = USB_ScanDevice(byref(DevHandles))
    if(ret == 0):
        print("No device connected!")
        exit()
    else:
        print("Have %d device connected!"%ret)
    # Open device
    ret = USB_OpenDevice(DevHandles[DevIndex])
    if(bool(ret)):
        print("Open device success!")
    else:
        print("Open device faild!")
        exit()
    # Get device infomation
    USB2XXXInfo = DEVICE_INFO()
    USB2XXXFunctionString = (c_char * 256)()
    ret = DEV_GetDeviceInfo(DevHandles[DevIndex],byref(USB2XXXInfo),byref(USB2XXXFunctionString))
    if(bool(ret)):
        print("USB2XXX device infomation:")
        print("--Firmware Name: %s"%bytes(USB2XXXInfo.FirmwareName).decode('ascii'))
        print("--Firmware Version: v%d.%d.%d"%((USB2XXXInfo.FirmwareVersion>>24)&0xFF,(USB2XXXInfo.FirmwareVersion>>16)&0xFF,USB2XXXInfo.FirmwareVersion&0xFFFF))
        print("--Hardware Version: v%d.%d.%d"%((USB2XXXInfo.HardwareVersion>>24)&0xFF,(USB2XXXInfo.HardwareVersion>>16)&0xFF,USB2XXXInfo.HardwareVersion&0xFFFF))
        print("--Build Date: %s"%bytes(USB2XXXInfo.BuildDate).decode('ascii'))
        print("--Serial Number: ",end='')
        for i in range(0, len(USB2XXXInfo.SerialNumber)):
            print("%08X"%USB2XXXInfo.SerialNumber[i],end='')
        print("")
        print("--Function String: %s"%bytes(USB2XXXFunctionString.value).decode('ascii'))
    else:
        print("Get device infomation faild!")
        exit()
    # Initialize spi
    SPIConfig = SPI_CONFIG()
    SPIConfig.Mode = SPI_MODE_SOFT_FDX      # 硬件半双工模式
    SPIConfig.Master = SPI_MASTER    # 主机模式
    SPIConfig.CPOL = 0
    SPIConfig.CPHA = 0
    SPIConfig.LSBFirst = SPI_MSB
    SPIConfig.SelPolarity = SPI_SEL_LOW
    SPIConfig.ClockSpeedHz = 100000

    ret = SPI_Init(DevHandles[DevIndex],SPI1_CS0,byref(SPIConfig))
    if(ret != SPI_SUCCESS):
        print("Initialize spi faild!")
        exit()
    else:
        print("Initialize spi success")

    
    state = DEV_SetPowerLevel(DevHandles[DevIndex], POWER_LEVEL_1V8)    # 调用 DEV_SetPowerLevel 函数
    if not state:
        print("Set powerlevel error!")
        exit()
    else:
        print("Set powerlevel success")


    # SPI write bits
    ret = SPI_WriteBits(DevHandles[DevIndex],SPI1_CS0,b"101101001001")
    if(ret != SPI_SUCCESS):
        print("SPI write bits faild!")
        exit()
    else:
        print("SPI write bits success!")

    # SPI write data
    WriteBuffer = (c_ubyte * 16)()
    for i in range(0,len(WriteBuffer)):
        WriteBuffer[i] = i
    ret = SPI_WriteBytes(DevHandles[DevIndex],SPI1_CS0,byref(WriteBuffer),len(WriteBuffer))
    if(ret != SPI_SUCCESS):
        print("SPI write data faild!")
        exit()
    else:
        print("SPI write data success!")


    
    # # SPI read data
    # ReadBuffer = (c_ubyte * 16)()
    # ret = SPI_ReadBytes(DevHandles[DevIndex],SPI1_CS0,byref(ReadBuffer),len(ReadBuffer))
    # if(ret != SPI_SUCCESS):
    #     print("SPI read data faild!")
    #     exit()
    # else:
    #     print("SPI read data:")
    #     for i in range(0,len(ReadBuffer)):
    #         print("%02X "%ReadBuffer[i],end='')
    #     print("")

    # # SPI write read data
    # ret = SPI_WriteReadBytes(DevHandles[DevIndex],SPI1_CS0,byref(WriteBuffer),len(WriteBuffer),byref(ReadBuffer),len(ReadBuffer),10)
    # if(ret != SPI_SUCCESS):
    #     print("SPI write&read data faild!")
    #     exit()
    # else:
    #     print("SPI write&read data:")
    #     for i in range(0,len(ReadBuffer)):
    #         print("%02X "%ReadBuffer[i],end='')
    #     print("")

    # Close device
    ret = USB_CloseDevice(DevHandles[DevIndex])
    if(bool(ret)):
        print("Close device success!")
    else:
        print("Close device faild!")
        exit()
