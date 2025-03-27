from COB_Test import *

# # 基本数字逻辑
# for ip in range(0,1):
#     test3_1_ReadID(target_ip=ip)
#     test3_2_Read_PageBuffer(target_ip=ip)

# # trim合集
# # str_lst=[]
# for ip_idx in range(0,8):
#     # str=test4_1_Trim_IBIAS(binstr='100',target_ip=ip_idx)
#     # str=test4_2_Trim_IBLC(binstr='1010',target_ip=ip_idx)
# #     # 换GPIO CS模式
#     str=test4_3_Trim_IREF(binstr='110010',target_ip=ip_idx)
# #     # 换回常规CS模式
# #     str_lst.append(str)

# # print('\t'.join(str_lst))


# Forming & Cycle
# test_res_lst=[]
# for ip in range(0,8):
#     # test_res = test6_1_Forming(target_ip=ip)
#     # 下电再上电
#     # test_res = test6_2_Precycle(target_ip=ip)
#     test_res = test6_3_Cycle(target_ip=ip)
#     test_res_lst.append(test_res)

# print('Test results are as follows:')
# for idx,item in enumerate(test_res_lst):
#     print(f'status reg for subip{idx} is:', item)



# # write & read CFGR
# test_res_lst=[]
# for ip in range(0,8):
#     test_res = test7_1_Write_CFGR(target_ip=ip)
#     test_res_lst.append(test_res)

# print('Test results are as follows:')
# for idx,item in enumerate(test_res_lst):
#     print(f'status reg for subip{idx} is:', item)

# Read_res_list=[]
# for ip in range(0,8):
#     # test4_1_Trim_IBIAS_notrim(target_ip=ip)
#     # test4_2_Trim_IBLC_notrim(target_ip=ip)

#     Read_res=test_read_CFGR(ip)
#     Read_res_list.append(Read_res)

# for idx,item in enumerate(Read_res_list):
#     print(f'Read RRAM result for subip{idx} is:', Read_res_list[idx])

# # 更多 Cycle!
# for cycle_time in range(0,10):
#     for ip_idx in range (0,8):
#         test6_3_Cycle(target_ip=ip_idx)


# # Write Page
# for _ in range(10):
#     for ip_idx in range(0, 8):
#         test7_2_WritePage(target_ip=ip_idx, page_idx=0)
#         test7_2_WritePage(target_ip=ip_idx, page_idx=1)

# Read Page
# for ip_idx in range(0,8):
#     test7_2_ReadPage(target_ip=ip_idx,filename=f'./Pagedata/RRAMpage_SUBIP{ip_idx}.txt',ECC_on=False)
#     # test7_2_ReadPage(target_ip=ip_idx,filename=f'./Pagedata/RRAMpage_SUBIP{ip_idx}.txt',ECC_on=True)





# --------------------------------------------------------------- #





# test3_1_ReadID(ip)
# test_read_CFGR(ip)

# test3_1_ReadID()
# test3_2_Read_PageBuffer()
# test4_1_Trim_IBIAS()
# test4_2_Trim_IBLC()
# test4_3_Trim_IREF()
# GPIO_test()

# test_read_CFGR()


# test7_2_ReadBack(1)

# for ip_idx in range(2,3):
#     test7_2_ReadPage(target_ip=ip_idx,filename=f'./Pagedata/RRAMpage_SUBIP{ip_idx}.txt',ECC_on=True)

# test3_1_ReadID(target_ip=0)
# test7_2_ReadPage(target_ip=0,filename=f'./Pagedata/RRAMpage_SUBIP0_1.txt')
# test6_3_Cycle(target_ip=0)

# test7_1_Write_CFGR(0)
# test_read_CFGR(0)

# for ip in range(0,8):
#     test7_1_Write_CFGR(ip)

#
# test7_1_Write_CFGR(0)
#
# Read_res_list=[]
# for ip in range(0,8):
#     # test4_1_Trim_IBIAS_notrim(target_ip=ip)
#     # test4_2_Trim_IBLC_notrim(target_ip=ip)
#
#     # test3_1_ReadID(ip)
#     # Read_res=test_read_CFGR(ip)
#     Read_res_list.append(Read_res)
#
# for idx,item in enumerate(Read_res_list):
#     print(f'Read RRAM result for subip{idx} is:', Read_res_list[idx])
