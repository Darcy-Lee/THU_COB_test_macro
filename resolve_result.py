def filter_data_lines(input_filepath, output_filepath):
    try:
        # 打开输入文件进行读取
        with open(input_filepath, 'r') as infile:
            lines = infile.readlines()

        # 处理并保留需要的行
        filtered_lines = []
        for line in lines:
            # 检查每行是否以 "Data: " 开头
            if line.startswith("Data: "):
                # 如果不是以 "Data: " 开头，则保留该行，去掉 "Data: " 前缀
                filtered_lines.append(line.lstrip())

        # 将处理后的内容写入新的输出文件
        with open(output_filepath, 'w') as outfile:
            outfile.writelines(filtered_lines)

        print(f"文件处理完成，已保存为 {output_filepath}")

    except Exception as e:
        print(f"发生错误: {e}")


# 示例用法
input_filepath = 'Pagedata\\result6.txt'  # 输入文件路径
output_filepath = 'Pagedata\\result6_resolved.txt'  # 输出文件路径
filter_data_lines(input_filepath, output_filepath)
