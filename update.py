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
    if os.path.isfile(image) == True:
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

images = True

os.chdir("upload")
SKUs = []

i = open('products.csv', 'rb')
reader1 = csv.reader(i)
c = open('catalog.csv', 'rb')
reader2 = csv.reader(c)

file = 'upload.csv'
writer = csv.writer(open(file, 'w+'), quotechar="'")
writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled'))

headerRows = [reader1.next(), reader2.next()]
headers = [
"sku",
"name",
"_attribute_set",
"featured",
"manufacturer",
"price",
"cpu_quantity",
"cpu_speed",
"cpu_cores",
"processor",
"hdd1_quantity",
"hdd1_capacity",
"hdd_size",
"hdd_tech",
"raid",
"ram_quantity",
"ram_technology",
"drive",
"power_supply",
"server_type",
"warranty"
]

for h in range(0,len(headerRows)):
    for r in range(0,len(headerRows[h])):
        for header in headers:
            if headerRows[h][r] == header:
                print r

"""
line = 0
for inRow in reader1:
    line = line + 1
    name = inRow[nameRow].replace("Dell ", "").replace("HP ", "")
    sku = name.replace(" ", "-").replace("---", "-").replace("--", "-").replace('"', "").lower() + "-1"
    for item in SKUs:
        if item == sku:
            sku = increment(sku)
    SKUs.append(sku)
    image = sku[:-2] + '.jpg'

    if images == True:
        if os.path.isfile('images/'+image) == False:
            if os.path.isfile('images-old/'+image):
                shutil.copy('images-old/'+image,'images/'+image)
            else:
                urllib.urlretrieve("http://www.buysellservers.com/media/catalog/product/"+image[0]+"/"+image[1]+"/"+image, 'images/' + image)
                if os.path.getsize('images/'+image) < 1:
                    os.remove('images/' + image)
                    urllib.urlretrieve("http://www.eztradelive.com/media/catalog/product/"+image[0]+"/"+image[1]+"/"+image, 'images/' + image)
    if os.path.getsize('images/'+image) < 1:
        os.remove('images/' + image)
        print image
    resize('images/'+image)

    price = inRow[priceRow]
    if price == "" or price == " " or price[:4].lower() == "call":
            price = 9999
    accept_price = price
    decline_price = float(price) - 1

    server_type = inRow[server_typeRow]
    if name[-11:].lower() == 'workstation':
        server_type = "Workstation"

    featured = inRow[featuredRow]
    attributes = inRow[_attribute_setRow]
    short_des = "Need an Upgrade? Call Us!<br><strong>770-850-8400</strong>"

    if attributes != "Default":
        manufacturer = inRow[manufacturerRow].replace(" ", "")
        warranty = inRow[warrantyRow]
        if warranty == "":
            warranty = "None"

        cpu_cores = inRow[cpu_coresRow].replace(" ", "")
        cpu_quantity = inRow[cpu_quantityRow].replace(" ", "")
        cpu_speed = inRow[cpu_speedRow].replace(" ", "")
        if cpu_speed != "" and cpu_speed != " " and cpu_speed != "None" and cpu_speed[-3:].lower() != "ghz":
            cpu_speed = cpu_speed + "GHz"

        drive = inRow[driveRow]
        if drive.lower() != "dvd":
            drive = "Optical"

        hdd_capacity = inRow[hdd1_capacityRow].replace(" ", "")
        hdd_size = inRow[hdd_sizeRow].replace(" ", "")
        if hdd_size[-1:] != '"':
            hdd_size = hdd_size + '"'
        hdd_tech = inRow[hdd_techRow].replace(" ", "")
        hdd_quantity = inRow[hdd1_quantityRow].replace(" ", "")

        power = inRow[power_supplyRow].replace(" ", "")
        if power == "":
            power = "Single"
        processor = inRow[processorRow].replace(" ", "")
        raid = inRow[raidRow].replace("None", "No").replace("No", "None").replace(" ", "")

        ram_amount = inRow[ram_quantityRow].replace(" ", "").replace("Gb ", "GB").replace("gb ", "GB")
        ram_type = inRow[ram_technologyRow]


        print "name:", name
        print "price:", price
        print "attributes:", attributes
        print "manufacturer:", manufacturer
        print "server_type:", server_type
        print "warranty:", warranty
        print "cpu_cores:", cpu_cores
        print "cpu_quantity:", cpu_quantity
        print "cpu_speed:", cpu_speed
        print "drive:", drive
        print "hdd_capacity:", hdd_capacity
        print "hdd_size:", hdd_size
        print "hdd_tech:", hdd_tech
        print "hdd_quantity:", hdd_quantity
        print "power:", power
        print "processor:", processor
        print "raid:", raid
        print "ram_amount:", ram_amount
        print "ram_type:", ram_type
        print ""


    if name[:8] == "Latitude":
        category = "Laptops"
    elif attributes == "Storage":
        category = "Storage"
    elif server_type == "Workstation":
        category = "Workstations"
    else:
        category = "Servers"
    outRow = (sku,'',attributes,'simple',category,'"Default Category"','base',name,'"<strong>For Additional Configurations and Operating Systems Call Us at 770-850-8400</strong>"',short_des,price,'','','','','45.0000',manufacturer,'','','',image,image,image,'','','','','','1',sku,sku,'','4','','','','','','"Block after Info Column"','0','0',name,name,name,'"2015-01-13 16:24:33"','"2015-01-13 16:45:04"','','"Use config"','"Use config"','','2','','','','',accept_price,decline_price,'',featured,server_type,processor,cpu_quantity,cpu_speed,cpu_cores,ram_amount,ram_type,hdd_quantity,hdd_capacity,hdd_size,raid,warranty,power,hdd_tech,drive,'0.0000','0.0000','1','0','0','1','1.0000','1','0.0000','1','0','1.0000','1','0','1','1','1','0.0000','1','0','0','','','','','','','','','','','','','','','','','88',image,name,'1','0')
    writer.writerow(outRow)

    template = ['', '', '', '', category, '"Default Category"', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    if server_type == "Workstation":
        if manufacturer == "Dell":
            category = category+"/Dell Workstations"
            template[4] = '"'+category+'"'
            writer.writerow(template)
        elif manufacturer == "HP":
            category = category+"/HP Workstations"
            template[4] = '"'+category+'"'
            writer.writerow(template)
    elif category == "Storage":
        if manufacturer == "Dell":
            category = category+"/Dell Storage"
            template[4] = '"'+category+'"'
            writer.writerow(template)
        elif manufacturer == "HP":
            category = category+"/HP Storage"
            template[4] = '"'+category+'"'
            writer.writerow(template)
    elif category == "Servers":
        if manufacturer == "Dell":
            category = category+"/Dell Servers"
            template[4] = '"'+category+'"'
            writer.writerow(template)
            if server_type == "Tower":
                category = category+"/Dell Tower Servers"
                template[4] = '"'+category+'"'
                writer.writerow(template)
            elif server_type[:4] == "Rack":
                category = category+"/Dell Rack Servers"
                template[4] = '"'+category+'"'
                writer.writerow(template)
        elif manufacturer == "HP":
            category = category+"/HP Servers"
            template[4] = '"'+category+'"'
            writer.writerow(template)
            if server_type == "Tower":
                category = category+"/HP Tower Servers"
                template[4] = '"'+category+'"'
                writer.writerow(template)
            elif server_type[:4] == "Rack":
                category = category+"/HP Rack Servers"
                template[4] = '"'+category+'"'
                writer.writerow(template)

print str(line) + " products"
        """