__author__ = 'benjy'

from lxml import html
from lxml import etree
import csv
import sys
import shutil
import os
import urllib
import re
import time
from PIL import Image

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def increment(s):
    if is_number(s[len(s) - 1]):
        if s[len(s) - 1] == '9':
            s = increment(s[:len(s) - 1]) + '0'
        else:
            s = s[:len(s) - 1] + str(int(s[len(s) - 1]) + 1)
    else:
        s = s + '1'
    return s

def resize(image):
    max = (500, 500)
    im = Image.open(image)
    width, height = im.size

    if width > max[0] or height > max[1]:
        aspect_ratio = width / float(height)
        new_height = int(max[0] / aspect_ratio)

        if new_height < max[1]:
            final_width = max[0]
            final_height = new_height
        else:
            final_width = int(aspect_ratio * max[1])
            final_height = max[1]

        imaged = im.resize((final_width, final_height), Image.ANTIALIAS)
        imaged.save(image, quality=90)
        print image, 'resized'

os.chdir("download")
shutil.rmtree('images', ignore_errors=True)
os.makedirs('images')
with open('products.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'output.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")

    products = 0
    header = reader.next()
    for r in range(0,len(header)):

        if header[r] == "sku":
            skuRow = r
        elif header[r] == "name":
            nameRow = r
        elif header[r] == "_attribute_set":
            _attribute_setRow = r
        elif header[r] == "featured":
            featuredRow = r
        elif header[r] == "manufacturer":
            manufacturerRow = r
        elif header[r] == "generation":
            generationRow = r
        elif header[r] == "price":
            priceRow = r
        elif header[r] == "cpu_quantity":
            cpu_quantityRow = r
        elif header[r] == "cpu_speed":
            cpu_speedRow = r
        elif header[r] == "cpu_cores":
            cpu_coresRow = r
        elif header[r] == "processor":
            processorRow = r
        elif header[r] == "hdd1_quantity":
            hdd1_quantityRow = r
        elif header[r] == "hdd1_capacity":
            hdd1_capacityRow = r
        elif header[r] == "hdd_size":
            hdd_sizeRow = r
        elif header[r] == "hdd_tech":
            hdd_techRow = r
        elif header[r] == "raid":
            raidRow = r
        elif header[r] == "ram_quantity":
            ram_quantityRow = r
        elif header[r] == "ram_technology":
            ram_technologyRow = r
        elif header[r] == "drive":
            driveRow = r
        elif header[r] == "power_supply":
            power_supplyRow = r
        elif header[r] == "server_type":
            server_typeRow = r
        elif header[r] == "warranty":
            warrantyRow = r
        elif header[r] == "image":
            imageRow = r

    order = [nameRow, generationRow, _attribute_setRow, featuredRow, manufacturerRow, priceRow, cpu_quantityRow, cpu_speedRow, cpu_coresRow, processorRow, hdd1_quantityRow, hdd1_capacityRow, hdd_sizeRow, hdd_techRow, raidRow, ram_quantityRow, ram_technologyRow, driveRow, power_supplyRow, server_typeRow, warrantyRow]

    outRow = []
    for row in order:
        outRow.append(header[row])
    writer.writerow(outRow)
    reader.next()

    for inRow in reader:
        if inRow[0] != "":
            products = products + 1
            outRow = []
            for row in order:
                outRow.append(inRow[row])
            urllib.urlretrieve("http://www.buysellservers.com/media/catalog/product" + inRow[imageRow], 'images/' + inRow[imageRow][5:])
            writer.writerow(outRow)
    print products, "products"