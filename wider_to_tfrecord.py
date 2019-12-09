import tensorflow as tf
import numpy
import cv2
import os
import hashlib

import config
from utils import dataset_util

def parse_test_example(f, images_path):
    height = None # Image height
    width = None # Image width
    filename = None # Filename of the image. Empty if image is not from file
    encoded_image_data = None # Encoded image bytes
    image_format = b'jpeg' # b'jpeg' or b'png'

    filename = f.readline().rstrip()
    if not filename:
        raise IOError()

    filepath = os.path.join(images_path, filename)

    image_raw = cv2.imread(filepath)

    encoded_image_data = open(filepath, "rb").read()
    key = hashlib.sha256(encoded_image_data).hexdigest()

    height, width, channel = image_raw.shape

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(int(height)),
        'image/width': dataset_util.int64_feature(int(width)),
        'image/filename': dataset_util.bytes_feature(filename.encode('utf-8')),
        'image/source_id': dataset_util.bytes_feature(filename.encode('utf-8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        }))


    return tf_example


def parse_example(f, images_path):
    height = None # Image height
    width = None # Image width
    filename = None # Filename of the image. Empty if image is not from file
    encoded_image_data = None # Encoded image bytes
    image_format = b'jpeg' # b'jpeg' or b'png'

    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box (1 per box)
    classes_text = [] # List of string class name of bounding box (1 per box)
    classes = [] # List of integer class id of bounding box (1 per box)
    poses = []
    truncated = []
    difficult_obj = []

    filename = f.readline().rstrip()
#     print('filename is: ', filename)
    if not filename:
        raise IOError()

    filepath = os.path.join(images_path, filename)

    image_raw = cv2.imread(filepath)

    encoded_image_data = open(filepath, "rb").read()
    key = hashlib.sha256(encoded_image_data).hexdigest()

    height, width, channel = image_raw.shape

    face_num = int(f.readline().rstrip())
    if not face_num:
#         raise Exception()
#         print(filename, "has no faces")
        f.readline().rstrip().split()

    for i in range(face_num):
        annot = f.readline().rstrip().split()
        if not annot:
            raise Exception()

        # WIDER FACE DATASET CONTAINS SOME ANNOTATIONS WHAT EXCEEDS THE IMAGE BOUNDARY
        if(float(annot[2]) > 2.5):
            if(float(annot[3]) > 3.0):
                xmins.append( max(0.005, (float(annot[0]) / width) ) )
                ymins.append( max(0.005, (float(annot[1]) / height) ) )
                xmaxs.append( min(0.995, ((float(annot[0]) + float(annot[2])) / width) ) )
                ymaxs.append( min(0.995, ((float(annot[1]) + float(annot[3])) / height) ) )
                classes_text.append(b'face')
                classes.append(1)
                poses.append("front".encode('utf8'))
                truncated.append(int(0))


    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(int(height)),
        'image/width': dataset_util.int64_feature(int(width)),
        'image/filename': dataset_util.bytes_feature(filename.encode('utf-8')),
        'image/source_id': dataset_util.bytes_feature(filename.encode('utf-8')),
        'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
        'image/encoded': dataset_util.bytes_feature(encoded_image_data),
        'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
        'image/object/difficult': dataset_util.int64_list_feature(int(0)),
        'image/object/truncated': dataset_util.int64_list_feature(truncated),
        'image/object/view': dataset_util.bytes_list_feature(poses),
        }))


    return tf_example


def run(images_path, description_file, output_path, no_bbox=False, shard_size=1e10):
    f = open(description_file)
    

    
    
    
    i = 0
    count = 0
    
    writer = tf.python_io.TFRecordWriter(output_path+'-'+str(count))

    print("Processing {}".format(images_path))
    while True:
        
        try:
            if no_bbox:
                tf_example = parse_test_example(f, images_path)
            else:
                tf_example = parse_example(f, images_path)

            writer.write(tf_example.SerializeToString())
            i += 1
            if (i%shard_size == 0):
                count += 1
                writer.close()
                print('shard number ', count+1, 'done')
                writer = tf.python_io.TFRecordWriter(output_path+'-'+str(count))
            
        except IOError:
            break
        except Exception:
            raise

    writer.close()

    print("Correctly created record for {} images\n".format(i))


def main(unused_argv):
    # Training
    
    if not os.path.exists(config.OUTPUT_PATH):
        os.makedirs(config.OUTPUT_PATH)
    
    if config.TRAIN_WIDER_PATH is not None:
        images_path = config.TRAIN_WIDER_PATH
        description_file = os.path.join(config.GROUND_TRUTH_PATH, config.GROUND_TRUTH_FILENAME)
        output_path = os.path.join(config.OUTPUT_PATH, "train.tfrecord")
        shard_size = config.SHARD_SIZE
        run(images_path, description_file, output_path, shard_size=shard_size)

    # Validation
    if config.VAL_WIDER_PATH is not None:
        images_path = os.path.join(config.VAL_WIDER_PATH, "images")
        description_file = os.path.join(config.GROUND_TRUTH_PATH, "wider_face_val_bbx_gt.txt")
        output_path = os.path.join(config.OUTPUT_PATH, "val.tfrecord")
        shard_size = config.SHARD_SIZE
        run(images_path, description_file, output_path, shard_size=shard_size)

    # Testing. This set does not contain bounding boxes, so the tfrecord will contain images only
    if config.TEST_WIDER_PATH is not None:
        images_path = os.path.join(config.TEST_WIDER_PATH, "images")
        description_file = os.path.join(config.GROUND_TRUTH_PATH, "wider_face_test_filelist.txt")
        output_path = os.path.join(config.OUTPUT_PATH, "test.tfrecord")
        shard_size = config.SHARD_SIZE
        run(images_path, description_file, output_path, no_bbox=True, shard_size=shard_size)


if __name__ == '__main__':
    tf.app.run()
