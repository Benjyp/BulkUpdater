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

images = True

os.chdir("categorizer")
SKUs = []
with open('catalog.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'upload.csv'
    writer = csv.writer(open(file, 'w+'), quotechar='"')

    header = reader.next()
    writer.writerow(header)
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

    line = 0
    products = 0
    for inRow in reader:
        line = line + 1
        if inRow[0] != "":
            if "rack" in inRow[server_typeRow].lower():
                products = products + 1
                writer.writerow(inRow)

                if inRow[manufacturerRow] == "Dell":
                    writer.writerow(['', '', '', '', "Servers/Dell Servers", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
                    if inRow[server_typeRow] == "Rack - 1U":
                        outRow = ['', '', '', '', "Servers/Dell Servers/Dell 1U Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    elif inRow[server_typeRow] == "Rack - 2U":
                        outRow = ['', '', '', '', "Servers/Dell Servers/Dell 2U Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    elif inRow[server_typeRow] == "Rack - 4U+":
                        outRow = ['', '', '', '', "Servers/Dell Servers/Dell 4U+ Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    else:
                        print inRow[nameRow]
                    writer.writerow(outRow)
                elif inRow[manufacturerRow] == "HP":
                    writer.writerow(['', '', '', '', "Servers/HP Servers", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
                    if inRow[server_typeRow] == "Rack - 1U":
                        outRow = ['', '', '', '', "Servers/HP Servers/HP 1U Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    elif inRow[server_typeRow] == "Rack - 2U":
                        outRow = ['', '', '', '', "Servers/HP Servers/HP 2U Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    elif inRow[server_typeRow] == "Rack - 4U+":
                        outRow = ['', '', '', '', "Servers/HP Servers/HP 4U+ Racks", 'Default Category', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
                    else:
                        print inRow[nameRow]
                    writer.writerow(outRow)
                else:
                    print inRow[nameRow]

    print str(products) + " products"