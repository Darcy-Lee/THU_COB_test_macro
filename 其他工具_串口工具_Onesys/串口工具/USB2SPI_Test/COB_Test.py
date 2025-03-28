from COB_Lib import *
from trimtable import TrimTable
import time

def test_init(ClockSpeedHz=500000):
    DevHandle = scan_and_open_device()
    if DevHandle is None: exit()
    get_device_info(DevHandle)
    if not initialize_spi(DevHandle,ClockSpeedHz): exit()
    if not set_power_level(DevHandle, POWER_LEVEL_1V8): exit()

    return DevHandle
def test3_1_ReadID(target_ip=0):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    read_status_reg(DevHandle)
    read_ID(DevHandle)
    read_RRAM(DevHandle, 0x0, 0x0, 0x0, 4)

    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)

def test3_2_Read_PageBuffer(target_ip=0):
    DevHandle = test_init(10)

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    write_enable(DevHandle)
    page_hex_string_Noprefix = '000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F303132333435363738393A3B3C3D3E3F404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E7F808182838485868788898A8B8C8D8E8F909192939495969798999A9B9C9D9E9FA0A1A2A3A4A5A6A7A8A9AAABACADAEAFB0B1B2B3B4B5B6B7B8B9BABBBCBDBEBFC0C1C2C3C4C5C6C7C8C9CACBCCCDCECFD0D1D2D3D4D5D6D7D8D9DADBDCDDDEDFE0E1E2E3E4E5E6E7E8E9EAEBECEDEEEFF0F1F2F3F4F5F6F7F8F9FAFBFCFDFEFF000102030405060708090A0B0C0D0E0F101112131415161718191A1B1C1D1E1F202122232425262728292A2B2C2D2E2F3031323334353637'
    write_page(DevHandle,0x0, 0x0, 0x0, page_hex_string_Noprefix)

    send_testbits(DevHandle,0x00_00_04_00_00_00_00_00)
    read_RRAM(DevHandle,0x0, 0x0, 0x0, 312)

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)

def test4_1_Trim_IBIAS(binstr='100',target_ip=0):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    # send_testbits(DevHandle,0x00_35_00_00_02_00_00_00)
    # IBIAS_1= input("请输入IBIAS第一次测量值:")

    send_testbits(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable_IBIAS=TrimTable('AA8804FDFDA2A84A6F7FC0F7551C9C208410', 'hex')
    Trimtable_IBIAS.set_IBIAS(binstr)
    print(Trimtable_IBIAS.data_hex)
    write_page(DevHandle,0x0, 0x0, 0x0, Trimtable_IBIAS.data_hex)


    send_testbits(DevHandle,0x00_35_00_00_02_00_00_00)
    IBIAS_2= input("请输入IBIAS第二次测量值:")

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)

    print('测量值为',IBIAS_2)
    return IBIAS_2

def test4_1_Trim_IBIAS_notrim(target_ip=0):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle,0x00_35_00_00_02_00_00_00)
    input("请输入IBIAS第一次测量值:")

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)


def test4_2_Trim_IBLC(binstr='1010',target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    # send_testbits(DevHandle,0x10_05_00_00_0E_00_00_10)
    # IBLC_1= input("请输入Iblc第一次测量值:")

    send_testbits(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable_IBLC=TrimTable('AA8804FDFDA2A84A6F7FC0F7551C9C208410', 'hex')
    Trimtable_IBLC.set_IBIAS('100')
    Trimtable_IBLC.set_IBLC(binstr)
    print(Trimtable_IBLC.data_hex)
    write_page(DevHandle,0x0, 0x0, 0x0, Trimtable_IBLC.data_hex)

    send_testbits(DevHandle,0x10_05_00_00_0E_00_00_10)
    IBLC_2= input("请输入Iblc第二次测量值:")

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)
    # print('前后测量值分别为', IBLC_1, IBLC_2)
    return IBLC_2

def test4_2_Trim_IBLC_notrim(binstr='1010',target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle,0x10_05_00_00_0E_00_00_10)
    input("请输入Iblc第一次测量值:")

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)

def test4_3_Trim_IREF(binstr='100010',target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode_GPIOCS(DevHandle)

    # send_testbits_GPIOCS(DevHandle,0x40_06_00_2A_00_00_00_00)
    #
    # stress_test_GPIOCS(DevHandle)

    #
    send_testbits_GPIOCS(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable_GPIOCS(DevHandle)
    Trimtable_IREF=TrimTable('AA8804FDFDA2A84A6F7FC0F7551C9C208410', 'hex')
    Trimtable_IREF.set_IBIAS('100')
    Trimtable_IREF.set_IBLC('1010')
    Trimtable_IREF.set_RDREF(binstr)
    # print(Trimtable_IREF.data_hex)
    write_page_GPIOCS(DevHandle,0x0, 0x0, 0x0, Trimtable_IREF.data_hex)
    #
    send_testbits_GPIOCS(DevHandle,0x40_06_00_2A_00_00_00_00)
    # print('准备开始测量')
    test_res = stress_test_GPIOCS(DevHandle)
    #
    send_testbits_GPIOCS(DevHandle, 0x00_00_00_00_00_00_00_00)
    exit_test_mode_GPIOCS(DevHandle)
    # testen_down(DevHandle)

    close_device(DevHandle)
    return test_res

def test4_3_Trim_IREF_notrim(binstr='100010',target_ip=0):
    input('注意将HVPAD电压降到0.4V')
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode_GPIOCS(DevHandle)

    send_testbits_GPIOCS(DevHandle,0x40_06_00_2A_00_00_00_00)

    # print('准备开始测量')
    stress_test_GPIOCS(DevHandle)

    #
    send_testbits_GPIOCS(DevHandle, 0x00_00_00_00_00_00_00_00)
    exit_test_mode_GPIOCS(DevHandle)
    # testen_down(DevHandle)

    close_device(DevHandle)

def GPIO_test():
    DevHandle = test_init()

    testen_up(DevHandle)
    for i in range(0,8):
        select_subip(DevHandle,i)

    import time
    time.sleep(0.00001)

    testen_down(DevHandle)

def test6_1_Forming(target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)

    Trimtable=TrimTable('AA8804FDFDA2A84A6F7FC0F7551C9C208410', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle,0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_40_00_11_00)
    write_enable(DevHandle)
    forming(DevHandle)

    for i in range(0,40):
        print(f'forming time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('Forming success')
            break

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)
    return status_reg_str

def test6_2_Precycle(target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)
    clear_status_reg(DevHandle)#6-1 ESUS可能挂掉


    send_testbits(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)

    Trimtable=TrimTable('AA8804FDFDA2A84A6F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle,0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_00_00_00_00)
    write_enable(DevHandle)
    precycle(DevHandle)

    for i in range(0,60):
        print(f'precycle time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('precycle success')
            break

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)
    return status_reg_str

def test6_3_Cycle(target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle, 0x00_00_10_00_01_80_00_00)
    write_enable(DevHandle)
    rdn_data_str= '0000000000'
    write_page(DevHandle,0x0, 0x0, 0x0, rdn_data_str)


    clear_status_reg(DevHandle)

    # write ichkbd
    send_testbits(DevHandle, 0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable = TrimTable('AA8804FDFDA2A84A6F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle, 0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_01_00_00_00)
    write_enable(DevHandle)
    write_ichkbd(DevHandle)

    for i in range(0,60):
        print(f'write ichkbd time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('write ichkbd success')
            break

    # verify read
    send_testbits(DevHandle, 0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable = TrimTable('AA8804FDFDA2AA426F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle, 0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_01_00_00_00)
    write_enable(DevHandle)
    verify_read(DevHandle)

    for i in range(0,60):
        print(f'verify read time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('verify read success')
            break

    # write chkbd
    send_testbits(DevHandle, 0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable = TrimTable('AA8804FDFDA2A84A6F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle, 0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_00_80_00_00)
    write_enable(DevHandle)
    write_chkbd(DevHandle)

    for i in range(0,60):
        print(f'write chkbd time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('write chkbd success')
            break

    # verify read
    send_testbits(DevHandle, 0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)
    Trimtable = TrimTable('AA8804FDFDA2AA426F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    write_page(DevHandle, 0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_00_80_00_00)
    write_enable(DevHandle)
    verify_read(DevHandle)

    for i in range(0,60):
        print(f'verify read time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('verify read success')
            break

    status_reg_str_repair = read_status_reg(DevHandle)
    psus_str = status_reg_str_repair[4]
    esus_str = status_reg_str_repair[5]
    print(f'PSUS:{psus_str}  ESUS:{esus_str}')

    clear_repair(DevHandle)
    time.sleep(1)
    status_reg_str = read_status_reg(DevHandle)
    wip_str = status_reg_str[7]
    print(f'clear repair WIP:{wip_str}')

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)

    return status_reg_str_repair


def test_read_CFGR(target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle,0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)

    Trimtable=TrimTable('AA8804FDFDA2A84A6F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    print(Trimtable.data_hex)
    write_page(DevHandle,0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_00_00_08_00)

    read_data_str=read_RRAM(DevHandle,0x00D,0x0,0x0,312)

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)

    return read_data_str


def test7_1_Write_CFGR(target_ip=0):
    DevHandle = test_init()

    testen_up(DevHandle)
    select_subip(DevHandle, target_ip)
    enter_test_mode(DevHandle)

    send_testbits(DevHandle, 0x00_00_08_00_01_80_00_00)
    write_enable(DevHandle)

    Trimtable = TrimTable('AA8804FDFDA2A84A6F7F409A560F0F204210', 'hex')
    Trimtable.set_IBIAS('100')
    Trimtable.set_IBLC('1011')
    Trimtable.set_RDREF('101001')
    Trimtable.set_FORMVFY('100001')
    Trimtable.set_LRVFY('100001')
    Trimtable.set_HRVFY('110010')
    print(Trimtable.data_hex)
    write_page(DevHandle, 0x0, 0x0, 0x0, Trimtable.data_hex)

    send_testbits(DevHandle, 0x00_00_00_00_00_00_08_00)
    write_enable(DevHandle)
    page_data = 'AA000000AA000000AA000000880000008800000088000000040000000400000004000000FD000000FD000000FD000000FD000000FD000000FD0000006100000061000000610000009800000098000000980000004A0000004A0000004A0000006F0000006F0000006F000000BF000000BF000000BF0000004000000040000000400000009A0000009A0000009A0000005600000056000000560000000F0000000F0000000F0000008F0000008F0000008F000000200000002000000020000000420000004200000042000000100000001000000010000000'
    write_page_nodummy(DevHandle, 0x00D, 0x0, 0x0, page_data)

    for i in range(0,10):
        print(f'write CFGR time:{i} s')
        time.sleep(1)
        status_reg_str_CFGR = read_status_reg(DevHandle)
        wip_str = status_reg_str_CFGR[7]
        if wip_str == '0':
            print('write CFGR success')
            break

    send_testbits(DevHandle, 0x00_00_00_00_00_00_08_00)
    write_enable(DevHandle)
    rdn_data = '0'*384
    write_page_nodummy(DevHandle, 0x00C, 0x0, 0x0, rdn_data)

    for i in range(0,10):
        print(f'write wlrdn time:{i} s')
        time.sleep(1)
        status_reg_str=read_status_reg(DevHandle)
        wip_str=status_reg_str[7]
        if wip_str == '0':
            print('write wlrdn success')
            break

    send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    exit_test_mode(DevHandle)
    testen_down(DevHandle)
    close_device(DevHandle)

    return status_reg_str_CFGR

def test7_2_ReadBack(target_ip = 0):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    read_RRAM(DevHandle, 0x0, 0x0, 0x0, 312)

    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)

def test7_2_ReadSingleWL(target_ip = 0):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    read_RRAM(DevHandle, 0x0, 0x0, 0x0, 312)

    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)

def test7_2_ReadPage(filename="./Pagedata/RRAMpage.txt",target_ip = 0,ECC_on=True):
    DevHandle = test_init()

    # testen_up(DevHandle)
    select_subip(DevHandle,target_ip)
    enter_test_mode(DevHandle)

    if ECC_on:
        send_testbits(DevHandle,0x00_00_00_00_00_00_00_00)
    else:
        send_testbits(DevHandle,0x00_00_00_00_00_04_00_00)


    read_data_str_array=[]
    for ax in range(0,1178+1):
        read_data_str=read_RRAM(DevHandle, ax, 0x0, 0x0, 312)
        read_data_str_array.append(read_data_str)

    with open(filename, 'w') as file:
        for read_data_str in read_data_str_array:
            file.write(read_data_str + '\n')

    exit_test_mode(DevHandle)
    # testen_down(DevHandle)
    close_device(DevHandle)


if __name__ == '__main__':
    # for binstr in ['0000', '0001', '0010', '0011', '0100', '0101', '0110', '0111', '1000', '1001', '1010', '1011', '1100', '1101', '1110', '1111']:
    #     print('test for ', binstr)
    #     test4_2_Trim_IBLC(binstr)
    # test4_3_Trim_IREF()
    # for binstr in ['000000', '000001', '000010', '000011', '000100', '000101', '000110', '000111', '001000', '001001', '001010', '001011', '001100', '001101', '001110', '001111', '010000', '010001', '010010', '010011', '010100', '010101', '010110', '010111', '011000', '011001', '011010', '011011', '011100', '011101', '011110', '011111', '100000', '100001', '100010', '100011', '100100', '100101', '100110', '100111', '101000', '101001', '101010', '101011', '101100', '101101', '101110', '101111', '110000', '110001', '110010', '110011', '110100', '110101', '110110', '110111', '111000', '111001', '111010', '111011', '111100', '111101', '111110', '111111'] :
    #     print('test for ', binstr)
    #     test4_3_Trim_IREF(binstr)

    # test6_1_Forming()

    # test3_1_ReadID()
    # test3_2_Read_PageBuffer()
    # test4_1_Trim_IBIAS()
    # test4_2_Trim_IBLC()
    # test4_3_Trim_IREF()
    # test6_2_Precycle()
    # test6_3_Cycle()
    # test_read_CFGR()

    # test7_1_Write_CFGR()

    # test4_1_Trim_IBIAS_notrim()
    # test4_2_Trim_IBLC_notrim()
    test4_3_Trim_IREF_notrim()
    # test7_2_ReadBack()