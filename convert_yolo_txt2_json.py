import os  
import json  
from PIL import Image  
import argparse  
  
# 类别到标签的映射，你需要根据你的数据集提供这个映射  
LABEL_MAPPING = {  
    5: "CivilAviation",  
    11: "Bird",  
    # 添加其他类别和标签的映射  
}  
  
def parse_arguments():  
    parser = argparse.ArgumentParser(description="Convert TXT labels to JSON format with images in the same directory")  
    parser.add_argument("--txt_dir", type=str, required=True, help="Directory containing TXT label files")  
    parser.add_argument("--image_dir", type=str, required=True, help="Directory containing corresponding image files")  
    parser.add_argument("--mapping_file", type=str, required=True, help="classes.txt file containing class mapping")  
    return parser.parse_args()  

def load_class_mapping(mapping_file):  
    with open(mapping_file, 'r') as f:  
        classes = f.read().splitlines()  
    class_mapping = {str(idx): class_name for idx, class_name in enumerate(classes)}  
    return class_mapping

def get_image_size(image_path):  
    with Image.open(image_path) as img:  
        width, height = img.size  
    return width, height  
  
def txt_to_json(txt_file_path, image_dir): 
    # 获取图像文件名（不带扩展名）  
    image_file_name = os.path.splitext(os.path.basename(txt_file_path))[0] + '.jpg'  
    # 构建图像文件路径  
    image_path = os.path.join(image_dir, image_file_name)  
    # 检查图像文件是否存在  
    if not os.path.exists(image_path):  
        raise FileNotFoundError(f"Image file not found: {image_path}")  
    # 获取图像尺寸  
    image_width, image_height = get_image_size(image_path)   
    # print(image_width, image_height)

    with open(txt_file_path, 'r') as txt_file:  
        lines = txt_file.readlines()  

    shapes = []  
    for line in lines:  
        parts = line.strip().split()  
        label_id = int(parts[0])  
        x_center, y_center, w, h = map(float, parts[1:])  

        # 将相对坐标转换为绝对坐标  
        x_min = int((x_center-w/2) * image_width)  
        y_min = int((y_center-h/2) * image_height)  
        x_max = int((x_center + w/2) * image_width)  
        y_max = int((y_center + h/2) * image_height)  
          
        # 构建形状信息  
        shape = {  
            "label": LABEL_MAPPING.get(label_id, "Unknown"),  
            "points": [  
                [x_min, y_min],  
                [x_max, y_min],  
                [x_max, y_max],  
                [x_min, y_max]  
            ],  
            "group_id": None,  
            "description": "",  
            "difficult": False,  
            "shape_type": "rectangle",  
            "flags": {},  
            "attributes": {}  
        }  
        shapes.append(shape)  
      
    # 构建JSON对象  
    json_data = {  
        "version": "2.3.6",  
        "flags": {},  
        "shapes": shapes,  
        "imagePath": image_file_name,  
        "imageData": None,  
        "imageHeight": image_height,  
        "imageWidth": image_width,  
        "text": ""  
    }  
      
    # 推导JSON文件路径  
    json_file_path = os.path.splitext(image_path)[0] + '.json'  
      
    # 保存JSON文件  
    with open(json_file_path, 'w') as json_file:  
        json.dump(json_data, json_file, indent=4)  
    # print("json_file writed to:",json_file_path)
  
def convert_all_txt_to_json(txt_dir, image_dir, mapping_file): 
    # 加载类别映射
    LABEL_MAPPING = load_class_mapping(mapping_file) 
    print("Label mapping:", LABEL_MAPPING)

    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]  
    for txt_file in txt_files:  
        txt_file_path = os.path.join(txt_dir, txt_file)  
        try:  
            txt_to_json(txt_file_path, image_dir)  
        except FileNotFoundError as e:  
            print(e, "skipped.")  # 打印错误信息，如果图像文件未找到  
  
if __name__ == "__main__":  
    args = parse_arguments()  
    convert_all_txt_to_json(args.txt_dir, args.image_dir,args.mapping_file)