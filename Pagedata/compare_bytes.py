import os
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from matplotlib.colors import ListedColormap

# Global file lists
file1_list = [f"./bin/blk_{i}.Demura_8.txt" for i in range(8)]
file2_dir = "./Page_ECC_ID10_Bin_After230mA30mins/"
file2_list = [os.path.join(file2_dir, f"RRAMpage_SUBIP{i}.txt") for i in range(8)]

class ByteError:
    def __init__(self, line, column, subip):
        self.line = line
        self.column = column
        self.subip = subip

class ErrorMatrix:
    def __init__(self):
        self.errors = []

    def add_error(self, line, column, subip):
        self.errors.append(ByteError(line, column, subip))

    def generate_matrix(self):
        if not self.errors:
            return np.zeros((1, 1), dtype=int)
        
        max_line = max(error.line for error in self.errors)
        max_column = max(error.column for error in self.errors)
        matrix = np.zeros((max_line + 1, (max_column + 1) * 8), dtype=int)
        
        for error in self.errors:
            matrix[error.line, error.subip * (max_column + 1) + error.column] = 1
        
        # Flip the matrix vertically
        matrix = np.flipud(matrix)
        return matrix

def read_and_compare_files(file1_path, file2_path, subip):
    error_matrix = ErrorMatrix()
    
    with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
        
        min_lines = min(len(lines1), len(lines2))
        
        for line_num in range(min_lines):
            bytes1 = lines1[line_num].split()
            bytes2 = lines2[line_num].split()
            
            min_cols = min(len(bytes1), len(bytes2))
            
            for col_num in range(min_cols):
                if bytes1[col_num] != bytes2[col_num]:
                    error_matrix.add_error(line_num, col_num, subip)
    
    return error_matrix

def plot_combined_error_matrix(matrix):
    plt.figure(figsize=(20, 20), facecolor='white')
    ax = plt.gca()
    
    # 使用黑白颜色映射（0=白，1=黑）
    cmap = ListedColormap(['white', 'black'])
    img = ax.imshow(matrix, cmap=cmap, interpolation='none', vmin=0, vmax=1)
    
    # 设置背景和边框
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('black')  # 保留边框增强可读性
    
    # 隐藏坐标轴刻度
    ax.set_xticks([])
    ax.set_yticks([])
    
    # 计算每个SUBIP的错误数量
    cols_per_subip = matrix.shape[1] // 8
    error_counts = []
    for subip in range(8):
        start_col = subip * cols_per_subip
        end_col = (subip + 1) * cols_per_subip
        subip_matrix = matrix[:, start_col:end_col]
        error_counts.append(np.sum(subip_matrix))
    
    # 绘制SUBIP分隔线（蓝色细线）
    if matrix.shape[1] > 1:
        for subip in range(1, 8):
            ax.axvline(x=subip * cols_per_subip - 0.5, 
                      color='dodgerblue', linestyle='-', linewidth=1.2)
    
    # 添加SUBIP标签和错误计数
    for subip in range(8):
        x_center = (subip + 0.5) * cols_per_subip
        
        # SUBIP标签（底部）
        ax.text(x_center, -0.03, f'SUBIP{subip}',  # 使用负的轴坐标系坐标
               ha='center', va='top',
               transform=ax.get_xaxis_transform(),  # 混合坐标系
               fontsize=14, color='navy')
        
        # 错误计数（顶部，标题下方）
        ax.text(x_center, 1.03, f'Errors: {error_counts[subip]}',
               ha='center', va='bottom',
               transform=ax.get_xaxis_transform(),
               fontsize=12, color='darkred',
               bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
    
    # 调整标题位置和样式
    ax.set_title('Combined Byte Difference Heatmap (8 SUBIPs)', 
                fontsize=18, pad=40,  # 调整pad值来为错误计数留出空间
                color='darkred', weight='bold')
    
    # 保证保存时包含所有元素
    os.makedirs('./figs', exist_ok=True)
    save_path = "./figs/compare.png"
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Saved combined comparison plot to {save_path}")

def main():
    parser = ArgumentParser(description="Compare two sets of files byte by byte and generate a combined difference heatmap")
    parser.add_argument("--file1_dir", default="./bin/", help="Directory for first set of files")
    parser.add_argument("--file2_dir", default="./Page_ECC_ID17_after_bake_30mins/", help="Directory for second set of files")
    args = parser.parse_args()
    
    # Update file paths based on command line arguments
    global file1_list, file2_list
    file1_list = [os.path.join(args.file1_dir, f"blk_{i}.Demura_8.txt") for i in range(8)]
    file2_list = [os.path.join(args.file2_dir, f"RRAMpage_SUBIP{i}.txt") for i in range(8)]
    
    # Create a combined error matrix
    combined_error_matrix = ErrorMatrix()
    any_differences = False
    
    for subip in range(8):
        file1 = file1_list[subip]
        file2 = file2_list[subip]
        
        if not os.path.exists(file1):
            print(f"Warning: File {file1} not found, skipping")
            continue
        if not os.path.exists(file2):
            print(f"Warning: File {file2} not found, skipping")
            continue
            
        print(f"Comparing {file1} and {file2}...")
        error_matrix = read_and_compare_files(file1, file2, subip)
        
        # Add all errors to the combined matrix
        for error in error_matrix.errors:
            combined_error_matrix.add_error(error.line, error.column, error.subip)
            any_differences = True
    
    if any_differences:
        matrix = combined_error_matrix.generate_matrix()
        plot_combined_error_matrix(matrix)
    else:
        print("No differences found in any of the file comparisons")

if __name__ == '__main__':
    main()