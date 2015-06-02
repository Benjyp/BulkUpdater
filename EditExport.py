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

images = True

os.chdir("edit")
SKUs = []
with open('products.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'upload.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")

    header = reader.next()
    writer.writerow(header)
    imageHeaders = []
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
        elif header[r] == "meta_description":
            mDescriptionRow = r
        elif header[r] == "meta_title":
            mTitleRow = r
        elif header[r] == "meta_keyword":
            mKeywordRow = r
        elif "image" in header[r]:
            imageHeaders.append(r)

    line = 0
    for inRow in reader:
        line = line + 1
        outRow = inRow
        if inRow[0] != "":

            name = inRow[nameRow]

            meta_description = "Buy your %s today or call us to configure one for your needs. Full warranty and thoroughly tested before shipping to you." % name
            meta_title = name
            meta_keyword = meta_title.replace(" ", ", ")

            outRow[mDescriptionRow] = meta_description
            outRow[mTitleRow] = meta_title
            #outRow[mKeywordRow] = '"%s"' % meta_keyword
            for imageRow in imageHeaders:
                outRow[imageRow] = ""

        writer.writerow(outRow)