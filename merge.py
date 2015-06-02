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

os.chdir("merge")
ezProducts = []
with open('eztrade.csv', 'rb') as i:
    ezreader = csv.reader(i)
    ezheader = ezreader.next()
    for r in range(0,len(ezheader)):
        if ezheader[r] == "sku":
            EZskuCol = r
        elif ezheader[r] == "name":
            EZnameCol = r
        elif ezheader[r] == "_attribute_set":
            EZ_attribute_setCol = r
        elif ezheader[r] == "featured":
            EZfeaturedCol = r
        elif ezheader[r] == "manufacturer":
            EZmanufacturerCol = r
        elif ezheader[r] == "generation":
            EZgenerationCol = r
        elif ezheader[r] == "price":
            EZpriceCol = r
        elif ezheader[r] == "cpu_quantity":
            EZcpu_quantityCol = r
        elif ezheader[r] == "cpu_speed":
            EZcpu_speedCol = r
        elif ezheader[r] == "cpu_cores":
            EZcpu_coresCol = r
        elif ezheader[r] == "processor":
            EZprocessorCol = r
        elif ezheader[r] == "hdd1_quantity":
            EZhdd1_quantityCol = r
        elif ezheader[r] == "hdd1_capacity":
            EZhdd1_capacityCol = r
        elif ezheader[r] == "hdd_size":
            EZhdd_sizeCol = r
        elif ezheader[r] == "hdd_tech":
            EZhdd_techCol = r
        elif ezheader[r] == "raid":
            EZraidCol = r
        elif ezheader[r] == "ram_quantity":
            EZram_quantityCol = r
        elif ezheader[r] == "ram_technology":
            EZram_technologyCol = r
        elif ezheader[r] == "drive":
            EZdriveCol = r
        elif ezheader[r] == "power_supply":
            EZpower_supplyCol = r
        elif ezheader[r] == "server_type":
            EZserver_typeCol = r
        elif ezheader[r] == "warranty":
            EZwarrantyCol = r
        elif ezheader[r] == "meta_description":
            EZmDescriptionCol = r
        elif ezheader[r] == "meta_title":
            EZmTitleCol = r
        elif ezheader[r] == "meta_keyword":
           EZmKeywordCol = r
        elif ezheader[r] == "_category":
           EZcategoryCol = r
        elif ezheader[r] == "description":
           EZdescriptionCol = r

    EZname = ""
    EZattribute = ""
    EZtype = ""
    EZdescription = ""
    NewItem = True
    for EZinRow in ezreader:
        if EZinRow[0] != "":
            if NewItem == False:
                ezProducts.append([EZname, EZdescription, EZtype])
            EZname = EZinRow[EZnameCol]
            EZattribute = EZinRow[EZ_attribute_setCol]
            EZtype = ""
            EZdescription = EZinRow[EZdescriptionCol]
            if EZinRow[EZserver_typeCol][0:4] == "Rack":
                EZtype = "Rack"
            elif EZinRow[EZcategoryCol] == "Laptops":
                EZtype = "Laptop"
            elif EZinRow[EZcategoryCol] == "Storage":
                EZtype = "Rack"
        else:
            NewItem = False
            if EZattribute == "Server" and EZtype == "":
                if "rack" in EZinRow[EZcategoryCol].lower():
                    EZtype = "Rack"
                elif "tower" in EZinRow[EZcategoryCol].lower():
                    EZtype = "Tower"
                elif "workstation" in EZinRow[EZcategoryCol].lower():
                    EZtype = "Workstation"
                else:
                    print "Error:", EZname


print "----------------------------------------------"
with open('products.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'upload.csv'
    writer = csv.writer(open(file, 'w+'), quotechar='"')

    header = reader.next()
    writer.writerow(header)
    imageHeaders = []
    for r in range(0,len(header)):
        if header[r] == "sku":
            skuCol = r
        elif header[r] == "name":
            nameCol = r
        elif header[r] == "_attribute_set":
            _attribute_setCol = r
        elif header[r] == "featured":
            featuredCol = r
        elif header[r] == "manufacturer":
            manufacturerCol = r
        elif header[r] == "generation":
            generationCol = r
        elif header[r] == "price":
            priceCol = r
        elif header[r] == "cpu_quantity":
            cpu_quantityCol = r
        elif header[r] == "cpu_speed":
            cpu_speedCol = r
        elif header[r] == "cpu_cores":
            cpu_coresCol = r
        elif header[r] == "processor":
            processorCol = r
        elif header[r] == "hdd1_quantity":
            hdd1_quantityCol = r
        elif header[r] == "hdd1_capacity":
            hdd1_capacityCol = r
        elif header[r] == "hdd_size":
            hdd_sizeCol = r
        elif header[r] == "hdd_tech":
            hdd_techCol = r
        elif header[r] == "raid":
            raidCol = r
        elif header[r] == "ram_quantity":
            ram_quantityCol = r
        elif header[r] == "ram_technology":
            ram_technologyCol = r
        elif header[r] == "drive":
            driveCol = r
        elif header[r] == "power_supply":
            power_supplyCol = r
        elif header[r] == "server_type":
            server_typeCol = r
        elif header[r] == "warranty":
            warrantyCol = r
        elif header[r] == "meta_description":
            mDescriptionCol = r
        elif header[r] == "meta_title":
            mTitleCol = r
        elif header[r] == "meta_keyword":
            mKeywordCol = r
        elif "image" in header[r]:
            imageHeaders.append(r)
        elif header[r] == "description":
           descriptionCol = r
        elif ezheader[r] == "_category":
           categoryCol = r

    for inRow in reader:
        outRow = inRow
        if inRow[0] != "":
            name = inRow[nameCol]
            meta_title = "Refurbished " + name + " " + inRow[categoryCol]
            outRow[mTitleCol] = meta_title
            for p in ezProducts:
                if name in p[0]:
                    if p[2] == inRow[server_typeCol][0:len(p[2])]:
                        #print inRow[skuCol]
                        outRow[descriptionCol] = p[1].replace("\n", "").replace("\r", "")
                        spec1 = outRow[descriptionCol].split("<strong>Starting Specs:")[0]+"</div>"
                        if spec1:
                            outRow[descriptionCol] = spec1
                        spec2 = outRow[descriptionCol].split("<ul>")[0]+"</div>"
                        if spec2:
                            outRow[descriptionCol] = spec2
                        #print outRow[descriptionCol]
                        break



        writer.writerow(outRow)