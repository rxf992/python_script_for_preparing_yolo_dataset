# import os  
# import cv2  
# import glob  
# from PIL import Image, ImageDraw  
# import argparse  
# import numpy as np  
  
# # 假设我们有一个预定义的类别列表和颜色映射  
# class_to_color = {  
#     0: 'red',     # 类别0使用红色  
#     1: 'blue',    # 类别1使用蓝色  
#     2: 'green',   # 类别2使用绿色  
#     5:'green',
#     11:'red',
#     12:'yellow'
#     # ... 可以根据需要添加更多类别和颜色  
# }  
  
# def get_color(class_id):  
#     # 根据类别ID获取颜色，如果类别ID不在映射中，则返回一个默认颜色  
#     return class_to_color.get(class_id, 'yellow')  # 默认使用黄色  
  
# def draw_bounding_boxes(image_path, label_path):  
#     # 读取图像  
#     image = Image.open(image_path).convert('RGB')  
#     draw = ImageDraw.Draw(image)  
      
#     # 读取YOLO标签  
#     with open(label_path, 'r') as f:  
#         labels = f.readlines()  
      
#     for label in labels:  
#         parts = label.strip().split()  
#         if len(parts) < 5:  
#             continue  
#         class_id, x_center, y_center, width, height = map(float, parts[:5])  
          
#         # YOLO格式转换到图像坐标  
#         img_width, img_height = image.size  
#         x_center = int(x_center * img_width)  
#         y_center = int(y_center * img_height)  
#         width = int(width * img_width)  
#         height = int(height * img_height)  
          
#         # 计算矩形框左上角和右下角坐标  
#         x1 = int(x_center - width / 2)  
#         y1 = int(y_center - height / 2)  
#         x2 = int(x_center + width / 2)  
#         y2 = int(y_center + height / 2)  
          
#         # 获取类别颜色  
#         color = get_color(int(class_id))  
          
#         # 绘制矩形框  
#         draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)  
      
#     return image  
  
# def create_video_from_images(image_folder, label_folder, output_video_path, fps=1):  
#     # 获取排序后的图片文件列表和标签文件列表  
#     image_files = sorted(glob.glob(os.path.join(image_folder, '*.jpg')))  # 假设图片为jpg格式  
#     label_files = sorted(glob.glob(os.path.join(label_folder, '*.txt')))  # 假设标签为txt格式  
    
#     if len(image_files) != len(label_files):  
#         raise ValueError("图片文件和标签文件数量不一致")  
      
#     # 视频编写器初始化  
#     fourcc = cv2.VideoWriter_fourcc(*'H264')  # 或用 'mp4v'、'XVID' 等  
      
#     # 读取第一张图片以获取尺寸信息  
#     first_image = Image.open(image_files[0]).convert('RGB')  
#     img_width, img_height = first_image.size  
      
#     video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (img_width, img_height))  
      
#     for image_file, label_file in zip(image_files, label_files):  
#         # 绘制检测框  
#         image_with_boxes = draw_bounding_boxes(image_file, label_file)  
#         print(image_file)
#         # 转为cv2格式  
#         img_rgb = np.array(image_with_boxes)  
#         img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)  
          
#         # 写入视频帧  
#         video_writer.write(img_bgr)  
      
#     video_writer.release()  
#     print(f"视频已保存到 {output_video_path}")  
  
# if __name__ == "__main__":  
#     parser = argparse.ArgumentParser(description="根据图片和YOLO标签生成目标检测视频")  
#     parser.add_argument("image_dir", type=str, help="图片文件所在目录")  
#     parser.add_argument("label_dir", type=str, help="YOLO目标检测标签文件所在目录")  
#     parser.add_argument("output_video", type=str, default="output_detection.mp4", help="输出视频文件路径")  
      
#     args = parser.parse_args()  
      
#     create_video_from_images(args.image_dir, args.label_dir, args.output_video)

import os  
import cv2  
import glob  
from PIL import Image, ImageDraw  
import argparse  
import numpy as np  
  
# 假设我们有一个预定义的类别列表和颜色映射  
class_to_color = {  
    0: 'red',     # 类别0使用红色  
    1: 'blue',    # 类别1使用蓝色  
    2: 'green',   # 类别2使用绿色  
    5: 'green',  
    11: 'red',  
    12: 'yellow'  
    # ... 可以根据需要添加更多类别和颜色  
}  
  
def get_color(class_id):  
    # 根据类别ID获取颜色，如果类别ID不在映射中，则返回一个默认颜色  
    return class_to_color.get(class_id, 'yellow')  # 默认使用黄色  
  
def draw_bounding_boxes(image_path, label_path):  
    # 读取图像  
    image = Image.open(image_path).convert('RGB')  
    draw = ImageDraw.Draw(image)  
  
    # 读取YOLO标签  
    with open(label_path, 'r') as f:  
        labels = f.readlines()  
  
    for label in labels:  
        parts = label.strip().split()  
        if len(parts) < 5:  
            continue  
        class_id, x_center, y_center, width, height = map(float, parts[:5])  
  
        # YOLO格式转换到图像坐标  
        img_width, img_height = image.size  
        x_center = int(x_center * img_width)  
        y_center = int(y_center * img_height)  
        width = int(width * img_width)  
        height = int(height * img_height)  
  
        # 计算矩形框左上角和右下角坐标  
        x1 = int(x_center - width / 2)  
        y1 = int(y_center - height / 2)  
        x2 = int(x_center + width / 2)  
        y2 = int(y_center + height / 2)  
  
        # 获取类别颜色  
        color = get_color(int(class_id))  
  
        # 绘制矩形框  
        draw.rectangle([(x1, y1), (x2, y2)], outline=color, width=2)  
  
    return image  
  
def create_video_from_images(image_folder, label_folder, output_video_path, fps=1):  
    # 获取排序后的图片文件列表  
    image_files = sorted(glob.glob(os.path.join(image_folder, '*.jpg')))  # 假设图片为jpg格式  
  
    if not image_files:  
        raise ValueError("未找到图片文件")  
  
    # 视频编写器初始化  
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # 或用 'mp4v'、'XVID' 等  
  
    # 读取第一张图片以获取尺寸信息  
    first_image = Image.open(image_files[0]).convert('RGB')  
    img_width, img_height = first_image.size  
  
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (img_width, img_height))  
  
    for image_file in image_files:  
        # 根据图片文件名生成标签文件名  
        base_name = os.path.basename(image_file)  
        label_name = os.path.splitext(base_name)[0] + '.txt'  
        label_file = os.path.join(label_folder, label_name)  
  
        if not os.path.exists(label_file):  
            raise ValueError(f"未找到标签文件: {label_file}")  
  
        # 绘制检测框  
        image_with_boxes = draw_bounding_boxes(image_file, label_file)  
        print(image_file)  
  
        # 转为cv2格式  
        img_rgb = np.array(image_with_boxes)  
        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)  
  
        # 写入视频帧  
        video_writer.write(img_bgr)  
  
    video_writer.release()  
    print(f"视频已保存到 {output_video_path}")  
  
if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description="根据图片和YOLO标签生成目标检测视频")  
    parser.add_argument("image_dir", type=str, help="图片文件所在目录")  
    parser.add_argument("label_dir", type=str, help="YOLO目标检测标签文件所在目录")  
    parser.add_argument("output_video", type=str, default="output_detection.mp4", help="输出视频文件路径")  
  
    args = parser.parse_args()  
  
    create_video_from_images(args.image_dir, args.label_dir, args.output_video)