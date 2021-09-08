import os
import pandas as pd
import tensorflow as tf
from object_detection.utils import dataset_util
import shutil

def csv2tfrecord(csv_path, imageDir_path, tfrecord_path):
    objectInfo_df = pd.read_csv(csv_path)
    tfrecord_writer = tf.python_io.TFRecordWriter(tfrecord_path)
    for filename, group in objectInfo_df.groupby('filename'):
        height = group.iloc[0]['height']
        width = group.iloc[0]['width']
        filename_bytes = filename.encode('utf-8')
        image_path = os.path.join(imageDir_path, filename)
        with open(image_path, 'rb') as file:
            encoded_jpg = file.read()
        image_format = b'jpg'
        xmin_list = list(group['xmin'] / width)
        xmax_list = list(group['xmax'] / width)
        ymin_list = list(group['ymin'] / height)
        ymax_list = list(group['ymax'] / height)
        classText_list = [classText.encode('utf-8') for classText in group['class']]
        classLabel_list = [classText_to_classLabel(classText) for classText in group['class']]
        tf_example = tf.train.Example(
            features = tf.train.Features(
                feature = {
                    'image/height': dataset_util.int64_feature(height),
                    'image/width': dataset_util.int64_feature(width),
                    'image/filename': dataset_util.bytes_feature(filename_bytes),
                    'image/source_id': dataset_util.bytes_feature(filename_bytes),
                    'image/encoded': dataset_util.bytes_feature(encoded_jpg),
                    'image/format': dataset_util.bytes_feature(image_format),
                    'image/object/bbox/xmin': dataset_util.float_list_feature(xmin_list),
                    'image/object/bbox/xmax': dataset_util.float_list_feature(xmax_list),
                    'image/object/bbox/ymin': dataset_util.float_list_feature(ymin_list),
                    'image/object/bbox/ymax': dataset_util.float_list_feature(ymax_list),
                    'image/object/class/text': dataset_util.bytes_list_feature(classText_list),
                    'image/object/class/label': dataset_util.int64_list_feature(classLabel_list),
                }))
        tfrecord_writer.write(tf_example.SerializeToString())
    tfrecord_writer.close()
    print('成功产生tfrecord文件，保存在路径:%s' %tfrecord_path)

#如果训练自己的模型，目标检测的类别不同，需要修改此处
def classText_to_classLabel(row_label):
    if row_label == 'rubbish':
        return 1
    else:
        return None

dir_name = 'ssd/training'
if os.path.isdir(dir_name):
    shutil.rmtree(dir_name)
os.mkdir(dir_name)
csv2tfrecord('ssd/train.csv', 'ssd/smaller_images', 'ssd/training/train.tfrecord')
csv2tfrecord('ssd/test.csv', 'ssd/smaller_images', 'ssd/training/test.tfrecord')