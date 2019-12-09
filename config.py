# Training
# TRAIN_WIDER_PATH = "../face-detection-project-prakash/WIDER_train/images/"
# TRAIN_WIDER_PATH = "../FaceDetection-DSFD/data/ImageNet/train/"
# TRAIN_WIDER_PATH = "../FaceDetection-DSFD/data/ImageNet/val/"
TRAIN_WIDER_PATH = "../FDDB/"
# TRAIN_WIDER_PATH = "./WIDER_train/"

# Validation
# VAL_WIDER_PATH = "../face-detection-project-prakash/WIDER_val/"
VAL_WIDER_PATH = None

# Testing
#TEST_WIDER_PATH = "./WIDER_test/"
TEST_WIDER_PATH = None

# Ground Truth
# GROUND_TRUTH_PATH = "../face-detection-project-prakash/wider_face_split/"
# GROUND_TRUTH_PATH = "../FaceDetection-DSFD/"
# GROUND_TRUTH_PATH = "../floating_head_generation/"
GROUND_TRUTH_PATH = "../FDDB/"

# GROUND_TRUTH_FILENAME = "wider_face_train_bbx_gt.txt"
# GROUND_TRUTH_FILENAME = "imagenet_bbox_randomized_train.txt"
# GROUND_TRUTH_FILENAME = "imagenet_bbox_randomized_val.txt"
# GROUND_TRUTH_FILENAME = "category_3_without_contour.txt"
GROUND_TRUTH_FILENAME = 'fddb_wider_annot.txt'

# Output
OUTPUT_PATH = "./output_cat1/"


# SHARD SIZE
# SHARD_SIZE = 13000 #for train
SHARD_SIZE = 4000 #for val

