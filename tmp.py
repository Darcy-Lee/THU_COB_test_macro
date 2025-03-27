import time

# 记录程序开始运行的时间点
start_time = time.perf_counter()

# 暂停0.5秒
time.sleep(0.001)

# 记录程序暂停后的时间点
end_time = time.perf_counter()

# 输出程序实际暂停的时间
print("程序实际暂停的时间：", end_time - start_time)
