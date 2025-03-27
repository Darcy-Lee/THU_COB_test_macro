def bin_to_hex_file(input_filepath, output_filepath, group_size=312):
    try:
        # 以二进制模式打开并读取文件内容
        with open(input_filepath, 'rb') as f:
            data = f.read()

        # 打开输出文件准备写入
        with open(output_filepath, 'w') as out_file:
            # 每次处理group_size个字节
            for i in range(0, len(data), group_size):
                # 获取当前分组的字节数据
                chunk = data[i:i + group_size]
                # 将当前字节数据转换为十六进制字符串并以空格分隔
                hex_chunk = ' '.join(f'{byte:02X}' for byte in chunk)
                # 写入当前行，并换行
                out_file.write(hex_chunk + '\n')

        print(f"已将文件转换为十六进制格式，并保存为 {output_filepath}")

    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # for i in range(8):
    #     bin_to_hex_file(f'BinData\\blk_{i}.Demura_8.bin',f'Pagedata\\blk_{i}.Demura_8.txt')
    bin_to_hex_file(f'BinData\\Demura_8.bin',
                    f'Pagedata\\Demura_8.txt')
