import os
import sys
from collections import defaultdict  
  
def read_classes(directory):  
    # 构造classes.txt文件的路径，首先搜索当前目录  
    classes_file = os.path.join(directory, 'classes.txt')  
    # print("!!!" +  classes_file)
    # 如果当前目录没有classes.txt，则搜索上一级目录  
    if not os.path.isfile(classes_file):  
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))  
        classes_file = os.path.join(parent_directory, 'classes.txt')  
        # print("!!!" + parent_directory)

        # 如果上一级目录也没有classes.txt，则报错  
        if not os.path.isfile(classes_file):  
            raise FileNotFoundError(f"Error: 'classes.txt' not found in {directory} or its parent directory.")  
      
    # 读取classes.txt文件  
    with open(classes_file, 'r') as f:  
        classes = [line.strip() for line in f.readlines()]  
      
    # 检查是否有重复的类别名称  
    if len(classes) != len(set(classes)):  
        raise ValueError("Error: 'classes.txt' contains duplicate class names.")  
      
     
    # class_to_idx = {cls: idx for idx, cls in enumerate(classes)}  # 创建从类别名称到索引的映射 
    idx_to_class = {idx: cls for idx, cls in enumerate(classes)}  # 创建从索引到类别名称的映射 
    return idx_to_class
  
def count_yolo_labels(directory):        
    # 读取类别映射  
    idx_to_class = read_classes(directory)  
    # 如果标签文件中使用的是类别名称，我们需要这个映射来计数  
    print("~~~~~~~~~~~~~~~~~~")
    print(idx_to_class)
    print("~~~~~~~~~~~~~~~~~~")
    # 初始化一个字典，用于存储每个类别的目标框数量  
    category_count = defaultdict(int)  
      
    # 遍历指定目录及其子目录  
    for root, _, files in os.walk(directory):  
        for file in files:  
            if file.endswith('.txt') and file!='classes.txt':  
                file_path = os.path.join(root, file)  
                print("open file:"+file_path)
                # 读取标签文件  
                with open(file_path, 'r') as f:  
                    for line in f:  
                        # YOLO格式的第一列是索引  
                        parts = line.strip().split()  
                        if parts:  
                            # print("parts=",parts)
                            category_id = int(parts[0])  
                            # 使用类别名称来查找索引，并计数  
                            if category_id in idx_to_class:  
                                category_count[category_id] += 1  
                            else:  
                                print(f"Warning: Unknown category '{category_id}' in {file_path}")  
      
    # 打印结果  
    print(f"Total number of unique categories: {len(category_count)}")  
    for idx, count in category_count.items():  
        # 如果使用的是类别名称计数，则直接打印类别名称  
        # 如果使用的是索引计数，则可能需要从索引映射回类别名称  
        print(f"Category '{idx_to_class[idx]}': {count} bounding boxes")

if __name__ == "__main__":  
    # 检查命令行参数  
    if len(sys.argv) < 2:  
        print("用法: python script.py <目录> ")  
        sys.exit(1)  
  
    directory = sys.argv[1]
  

    # directory = r"D:\BaiduNetdiskDownload\airbirds"
    count_yolo_labels(directory)