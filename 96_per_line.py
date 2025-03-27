def format_strings(input_filepath, output_filepath, max_strings_per_line=96):
    try:
        # 读取输入文件
        with open(input_filepath, 'r') as infile:
            # 读取所有内容并将其按空格或回车分隔为一个字符串列表
            content = infile.read().split()

        # 准备格式化后的行
        lines = []
        for i in range(0, len(content), max_strings_per_line):
            # 每次取 96 个字符串，拼接成一行，并用空格分隔
            line = ' '.join(content[i:i + max_strings_per_line])
            lines.append(line)

        # 将格式化后的内容写入输出文件
        with open(output_filepath, 'w') as outfile:
            outfile.write('\n'.join(lines))

        print(f"文件已生成并保存为 {output_filepath}")

    except Exception as e:
        print(f"发生错误: {e}")


# 示例用法
input_filepath = 'Pagedata\\Demura_8.txt'  # 输入文件路径
output_filepath = 'Pagedata\\Demura_8_96.txt'  # 输出文件路径
format_strings(input_filepath, output_filepath)
