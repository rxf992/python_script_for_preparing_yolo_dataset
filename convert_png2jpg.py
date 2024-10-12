import os  
import shutil  
from PIL import Image  
  
def convert_png_to_jpg(directory):  
    for root, dirs, files in os.walk(directory):  
        for file in files:  
            if file.lower().endswith('.png'):  
                # 构造完整的文件路径  
                png_path = os.path.join(root, file)  
                jpg_path = os.path.splitext(png_path)[0] + '.jpg'  
                  
                # 打开PNG图片并转换为JPG格式  
                try:  
                    with Image.open(png_path) as img:  
                        img.convert('RGB').save(jpg_path, "JPEG")  
                    # 删除原来的PNG图片  
                    os.remove(png_path)  
                    print(f"Converted {png_path} to {jpg_path} and deleted the PNG file.")  
                except Exception as e:  
                    print(f"Failed to convert {png_path} to JPG: {e}")  
  
# 指定要处理的目录（使用双反斜杠或原始字符串避免转义字符）  
# directory_to_process = r"C:\path\to\your\directory"  # 或者使用 "C:\\path\\to\\your\\directory"  
directory_to_process = r"D:\BaiduNetdiskDownload\airbirds\images8"  # 或者使用 "C:\\path\\to\\your\\directory"  
# 调用函数进行转换  
convert_png_to_jpg(directory_to_process)