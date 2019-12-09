import zipfile
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("path_to_zip_file")
parser.add_argument("directory_to_extract_to")
args = parser.parse_args()



zip_ref = zipfile.ZipFile(args.path_to_zip_file, 'r')
zip_ref.extractall(args.directory_to_extract_to)
zip_ref.close()
