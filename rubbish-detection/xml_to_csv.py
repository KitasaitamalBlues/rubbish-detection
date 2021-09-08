import os
import pandas as pd
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split

def xmlPath_list_to_df(xmlPath_list):
    xmlContent_list = []
    for xmlPath in xmlPath_list:
        tree = ET.parse(xmlPath)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xmlContent_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xmlContent_df = pd.DataFrame(xmlContent_list, columns=column_name)   
    return xmlContent_df

def dirPath_to_csv(dirPath):
    fileName_list = os.listdir(dirPath)
    all_xmlPath_list = [os.path.join(dirPath, fileName) for fileName in fileName_list if '.xml' in fileName]
    train_xmlPath_list, test_xmlPath_list = train_test_split(all_xmlPath_list, test_size=0.1, random_state=1)
    train_df = xmlPath_list_to_df(train_xmlPath_list)
    train_df.to_csv('ssd/train.csv')
    #目标路径
    print('成功产生文件train.csv,训练集共有%d张图片' %len(train_xmlPath_list))
    test_df = xmlPath_list_to_df(test_xmlPath_list)
    test_df.to_csv('ssd/test.csv')
    #目标路径
    print('成功产生文件test.csv,测试集共有%d张图片' %len(test_xmlPath_list))
    
dirPath_to_csv('ssd/smaller_images')
#路径