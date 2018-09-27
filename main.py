import sys
import os
import fnmatch
import getopt
from xml.etree.ElementTree import ElementTree
import xml.etree.ElementTree as ET
from struct import unpack
import binascii
import shutil
from PIL import Image
from rect import Rect


def main(argv):
    input_folder = ''
    output_folder = 'out'
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

    annotations_path = os.path.join(output_folder, "annotations")
    xmls_path = os.path.join(annotations_path, "xmls")
    images_path = os.path.join(output_folder, "images")

    if os.path.exists(annotations_path):
        shutil.rmtree(annotations_path)
    if os.path.exists(images_path):
        shutil.rmtree(images_path)
    if os.path.exists(xmls_path):
        shutil.rmtree(xmls_path)

    os.makedirs(images_path)
    os.makedirs(annotations_path)
    os.makedirs(xmls_path)

    images = dict()

    for dir_name, sub_dir_list, file_list in os.walk(input_folder):
        for file_name in fnmatch.filter(file_list, "*.bmp"):
            path = os.path.join(dir_name, file_name)
            name = os.path.splitext(os.path.split(path)[1])[0]
            save_path = os.path.join(images_path, name + ".jpeg")
            with Image.open(path) as img:
                width, height = img.size
                img.save(save_path)
                images[name] = {"width": width, "height": height}

    trainval_file = open(os.path.join(annotations_path, "trainval.txt"), 'w')

    for dir_name, sub_dir_list, file_list in os.walk(input_folder):
        for file_name in fnmatch.filter(file_list, "*.xml"):
            path = os.path.join(dir_name, file_name)
            name = os.path.splitext(os.path.split(path)[1])[0]
            if images.get(name) is None:
                continue

            pascal_voc = process_file(path, images_path, images)
            if pascal_voc is None:
                continue

            pascal_voc_name = os.path.join(xmls_path, file_name)
            print(pascal_voc_name)
            pascal_voc.write(open(pascal_voc_name, 'w'), encoding='unicode')
            trainval_file.write(name + "\n")


def process_file(path, images):
    annotation = ET.Element("annotation")
    tree = ElementTree(annotation)
    filename = ET.SubElement(annotation, "filename")
    name = os.path.splitext(os.path.split(path)[1])[0]
    filename.text = name + ".jpeg"
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    width.text = str(images[name].get("width"))
    height = ET.SubElement(size, "height")
    height.text = str(images[name].get("height"))
    depth = ET.SubElement(size, "depth")
    depth.text = str(3)
    segmented = ET.SubElement(annotation, "segmented")
    segmented.text = str(0)
    marmot_tree = ET.parse(path)
    marmot_root = marmot_tree.getroot()

    tables = marmot_root.findall("*/Composites/*[@Label='TableBody']")
    
    if not tables:
        return None

    for table in tables:
        obj = ET.SubElement(annotation, "object")
        obj_name = ET.SubElement(obj, "name")
        obj_name.text = "table"
        bndbox = ET.SubElement(obj, "bndbox")
        hexs = table.get("BBox").split(" ")
        bbox_array = [hex_to_double(x) for x in hexs]
        re = Rect(bbox_array[0], bbox_array[3], bbox_array[2], bbox_array[1])
        xmin = ET.SubElement(bndbox, "xmin")
        xmin.text = str(re.x0())
        ymin = ET.SubElement(bndbox, "ymin")
        fymin = images[name].get("height") - re.y1()
        ymin.text = str(fymin)
        xmax = ET.SubElement(bndbox, "xmax")
        xmax.text = str(re.x1())
        fymax = images[name].get("height") - re.y0()
        ymax = ET.SubElement(bndbox, "ymax")
        ymax.text = str(fymax)

    return tree


def hex_to_double(s):
    return unpack(">d", binascii.unhexlify(s))[0]


if __name__ == "__main__":
    main(sys.argv[1:])
