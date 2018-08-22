import sys
import os
import fnmatch
import getopt
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.ElementTree as ET
from struct import unpack
import binascii
import struct


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
            print('test.py -i <input folder> -o <output folder>')
            sys.exit()
        elif opt in ("-i", "--i"):
            input_folder = arg
        elif opt in ("-o", "--o"):
            output_folder = arg

    is_dir = os.path.isdir(input_folder)

    if not is_dir:
        raise Exception(input_folder, "- It is not a folder")

    images = dict()

    for dir_name, sub_dir_list, file_list in os.walk(input_folder):
        for file_name in fnmatch.filter(file_list, "*.bmp"):
            path = os.path.join(dir_name, file_name)
            bmp = open(path, 'rb')
            bmp.seek(18)
            width = struct.unpack("I", bmp.read(4))[0]
            height = struct.unpack("I", bmp.read(4))[0]
            name = os.path.splitext(os.path.split(path)[1])[0]
            images[name] = {"width": width, "height": height}

    for dir_name, sub_dir_list, file_list in os.walk(input_folder):
        for file_name in fnmatch.filter(file_list, "*.xml"):
            path = os.path.join(dir_name, file_name)
            name = os.path.splitext(os.path.split(path)[1])[0]
            if images.get(name) is None:
                continue
            pascal_voc = process_file(path, images)
            pascal_voc_name = os.path.join(output_folder, file_name)
            print(pascal_voc_name)
            pascal_voc.write(open(pascal_voc_name, 'w+'), encoding='unicode')


def process_file(path, images):
    annotation = ET.Element("annotation")
    tree = ElementTree(annotation)
    filename = ET.SubElement(annotation, "filename")
    name = os.path.splitext(os.path.split(path)[1])[0]
    filename.text = name + ".bmp"
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = str(images[name].get("width"))
    height = ET.SubElement(size, "height")
    height.text = str(images[name].get("height"))
    depth = ET.SubElement(size, "depth")
    depth.text = str(0)
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = str(0)
    marmot_tree = ET.parse(path)
    marmot_root = marmot_tree.getroot()

    for table in marmot_root.findall("*/Composites/*[@Label='Table']"):
        obj = ET.SubElement(annotation, "object")
        obj_name = ET.SubElement(obj, "name")
        obj_name.text = "table"
        bndbox = ET.SubElement(obj, "bndbox")

        hexs = table.get("BBox").split(" ")
        bbox_array = [hex_to_double(x) for x in hexs]

        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(bbox_array[0])
        ymin = ET.SubElement(bndbox, "ymin")
        ymin.text = str(bbox_array[3])
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(bbox_array[2])
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(bbox_array[1])

    return tree

def hex_to_double(s):
    return unpack(">d", binascii.unhexlify(s))[0]


if __name__ == "__main__":
    main(sys.argv[1:])

