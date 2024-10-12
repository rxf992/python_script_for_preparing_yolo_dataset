import os  
import sys  
  
def modify_txt_files(directory, target_value, new_value):  
    # 检查目录是否存在  
    if not os.path.isdir(directory):  
        print(f"指定的目录 {directory} 不存在。")  
        return  
  
    # 遍历目录及其所有子目录下的所有文件  
    for root, dirs, files in os.walk(directory):  
        for filename in files:  
            if filename.endswith(".txt"):  
                filepath = os.path.join(root, filename)  
                with open(filepath, 'r') as file:  
                    lines = file.readlines()  
  
                # 替换每行第一个字段的数值  
                modified_lines = []  
                for line in lines:  
                    fields = line.split()  # 假设字段是由空格分隔的  
                    if fields:  # 检查是否有字段  
                        # 替换第一个字段的值  
                        fields[0] = new_value if fields[0] == target_value else fields[0]  
                        modified_line = ' '.join(fields) + '\n'  
                        modified_lines.append(modified_line)  
                    else:  
                        # 如果行为空（或只有空白字符），则保持不变  
                        modified_lines.append(line)  
  
                # 将修改后的内容写回文件  
                with open(filepath, 'w') as file:  
                    file.writelines(modified_lines)  
  
                print(f"文件 {filepath} 已修改。")  
  
if __name__ == "__main__":  
    # 检查命令行参数  
    if len(sys.argv) < 4:  
        print("用法: python script.py <目录> <需要被修改的数值> <修改后的数值>")  
        sys.exit(1)  
  
    directory = sys.argv[1]  
    target_value = sys.argv[2]  
    new_value = sys.argv[3]  
  
    # 这里我们假设目标值和新的值都是字符串，如果它们是数值，您可以在这里添加转换逻辑  
    # 例如：target_value = int(sys.argv[2]) 和 new_value = int(sys.argv[3])  
    # 但请注意，如果这样做，您需要确保文件中的字段也是以相同的类型（数值）存储的  
  
    modify_txt_files(directory, target_value, new_value)