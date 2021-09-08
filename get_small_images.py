import os
from PIL import Image
import shutil
def get_smaller_images(dirPath, new_dirPath):
    fileName_list = os.listdir(dirPath)
    filePath_list = [os.path.join(dirPath, fileName) for fileName in fileName_list]
    imagePath_list = [filePath for filePath in filePath_list if '.jpg' in filePath]
    if os.path.isdir(new_dirPath):
        shutil.rmtree(new_dirPath)
    os.mkdir(new_dirPath)
    for imagePath in imagePath_list:
        image = Image.open(imagePath)
        width, height = image.size
        imageName = imagePath.split('\\')[-1]
        save_path = os.path.join(new_dirPath, imageName)
        if width >= 600 and height >= 600:
            minification = min(width, height) // 300 #此变量表示缩小倍数
            new_width = width // minification
            new_height = height // minification
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            print('图片%s原来的宽%d,高%d, 图片缩小后宽%d,高%d' %(
                imageName, width, height, new_width, new_height))
            resized_image.save(save_path)
        else:
            image.save(save_path)

get_smaller_images('selected_images', 'smaller_images')