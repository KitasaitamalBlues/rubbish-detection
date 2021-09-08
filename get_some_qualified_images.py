import os
import random
from PIL import Image
import shutil

#获取1000张图片中随机选出数量为sample_number*2的一部分图片的路径
def get_some_imagePath(dirPath, sample_number):
    fileName_list = os.listdir(dirPath)
    all_filePath_list = [os.path.join(dirPath, fileName) for fileName in fileName_list]
    all_imagePath_list = [filePath for filePath in all_filePath_list if '.jpg' in filePath]
    some_filePath_list = random.sample(all_filePath_list, k=sample_number*2)
    return some_filePath_list

#获取一部分像素足够，即长，宽都大于300的图片
def get_some_qualified_images(dirPath, sample_number, new_dirPath):
    some_imagePath_list = get_some_imagePath(dirPath, sample_number)
    if os.path.isdir(new_dirPath):
        shutil.rmtree(new_dirPath)
    os.mkdir(new_dirPath)
    i = 0
    for imagePath in some_imagePath_list:
        image = Image.open(imagePath)
        width, height = image.size
        if width > 300 and height > 300:
            i += 1
            new_imagePath = 'selected_images/%03d.jpg' %i
            shutil.copy(imagePath, new_imagePath)
        if i == sample_number:
            break

#获取数量为100的合格样本存放到selected_images文件夹中
get_some_qualified_images('n01440764', 100, 'selected_images')