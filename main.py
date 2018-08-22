import sys
import os
import fnmatch
import getopt
import xml.etree.ElementTree as ET
from struct import unpack
import binascii


def main(argv):
    input_folder = ''
    output_folder = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["input_folder=", "output_folder="])
    except getopt.GetoptError:
        print('test.py -i <input folder> -o <output folder>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--i"):
            input_folder = arg
        elif opt in ("-o", "--o"):
            output_folder = arg

    is_dir = os.path.isdir(input_folder)

    if not is_dir:
        raise Exception(input_folder, "- It is a folder")

    for dir_name, sub_dir_list, file_list in os.walk(input_folder):
        for file_name in fnmatch.filter(file_list, "*.xml"):
            path = os.path.join(dir_name, file_name)
            process_file(path)

    print('Input file is "', input_folder)
    print('Output file is "', output_folder)


def process_file(path):
    marmot_tree = ET.parse(path)
    marmot_root = marmot_tree.getroot()
    annotation = ET.Element('annotation')
    filename = ET.SubElement(annotation, 'filename')
    base = os.path.splitext(os.path.split(path)[1])[0] + ""
    filename.text = base + ".bmp"
    ET.dump(annotation)
    for table in marmot_root.findall("*/Composites/*[@Label='Table']"):
        hexs = table.get("BBox").split(" ")
        bbox = [hex_to_double(x) for x in hexs]
        print(bbox)


def hex_to_double(s):
    return unpack(">d", binascii.unhexlify(s))[0]


if __name__ == "__main__":
    main(sys.argv[1:])

