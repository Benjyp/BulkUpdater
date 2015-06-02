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

os.chdir("configurable upload")
SKUs = []

procs = [
    ["2 x Intel Xeon E5502 1.86GHz/4M/800MHz 2-Core", 0],
    ["2 x Intel Xeon E5503 2.0GHz/4M/800MHz 2-Core", 10],
    ["2 x Intel Xeon E5504 2.0GHz/4M/800MHz 4-Core", 40],
    ["2 x Intel Xeon E5506 2.13GHz/4M/800MHz 4-Core", 50],
    ["2 x Intel Xeon E5520 2.26GHz/8M/1066MHz 4-Core", 60],
    ["2 x Intel Xeon E5530 2.40GHz/8M/1066MHz 4-Core", 70],
    ["2 x Intel Xeon E5540 2.53GHz/8M/1333MHz 4-Core", 90],
    ["2 x Intel Xeon E5550 2.66GHz/8M/1333MHz 4-Core", 120],
    ["2 x Intel Xeon E5560 2.80GHz/8M/1333MHz 4-Core", 140],
    ["2 x Intel Xeon E5570 2.93GHz/8M/1333MHz 4-Core", 180],
    ["2 x Intel Xeon E5620 2.4GHz/12M/1066MHz 4-Core", 150],
    ["2 x Intel Xeon E5630 2.53GHz/12M/1066MHz 4-Core", 180],
    ["2 x Intel Xeon E5640 2.66GHz/12M/1066MHz 4-Core", 200],
    ["2 x Intel Xeon E5667 3.06GHz/12M/1333MHz 4-Core", 400],
    ["2 x Intel Xeon E5672 3.20GHz/12M/1333MHz 4-Core", 500],
    ["2 x Intel Xeon E5640 2.26GHz/12M/1333MHz 6-Core", 300],
    ["2 x Intel Xeon E5650 2.66GHz/12M/1333MHz 6-Core", 400],
    ["2 x Intel Xeon E5660 2.8GHz/12M/1333MHz 6-Core", 500],
    ["2 x Intel Xeon E5670 2.93GHz/12M/1333MHz 6-Core", 600],
    ["2 x Intel Xeon E5675 3.06GHz/12M/1333MHz 6-Core", 800]
]

Sdrives = [
    ["None", 0],
    ["146GB 10K SAS", 70],
    ["146GB 15K SAS", 99],
    ["300GB 10K SAS", 110],
    ["300GB 15K SAS", 250],
    ["600GB 10K SAS", 200],
    ["600GB 15K SAS", 475],
    ["900GB 10K SAS", 325],
    ["1.2TB 10K SAS", 450],
    ["250GB 7.2K SATA", 65],
    ["500GB 7.2K SATA", 110],
    ["1TB 7.2K SATA", 225]
]

Bdrives = [
    ["None", 0],
    ["146GB 10K SAS", 55],
    ["146GB 15K SAS", 75],
    ["300GB 10K SAS", 99],
    ["300GB 15K SAS", 130],
    ["450GB 15K SAS", 239],
    ["600GB 10K SAS", 255],
    ["600GB 15K SAS", 295],
    ["250GB 7.2K SATA", 55],
    ["500GB 7.2K SATA", 85],
    ["1TB 7.2K SATA", 110],
    ["2TB 7.2K SATA", 140]
]

RAM = [
    ["8GB", 0],
    ["16GB", 100],
    ["24GB", 195],
    ["32GB", 290],
    ["48GB", 485],
    ["64GB", 675],
    ["96GB", 1050],
    ["128GB", 1550],
    ["192GB", 2150]
]

outProcs = []
outDrives = []
outRAM = []
outExtras = []

with open('products - products.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'upload.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")
    writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))

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

    line = 0
    for inRow in reader:

        name = str(inRow[nameRow].replace("Dell ", "").replace("HP ", ""))
        if "R510" in name:
            name = "PowerEdge R510"

        price = inRow[priceRow]
        if price == "" or price == " " or price[:4].lower() == "call":
                price = 9999
        accept_price = price
        decline_price = float(price) - 1

        attributes = inRow[_attribute_setRow]
        server_type = inRow[server_typeRow]
        if server_type == "Rack - 4U":
            server_type = "Rack - 4U+"
        if name[-11:].lower() == 'workstation':
            attributes = "Workstation"
            name = name[:-12]
        elif name[:9].lower() == 'precision':
            attributes = "Workstation"
        elif name[:8].lower() == 'optiplex':
            attributes = "Workstation"
        elif name[-6:].lower() == 'laptop':
            attributes = 'Laptop'
            name = name[:-7]

        sku = name.replace(" ", "-").replace("---", "-").replace("--", "-").replace('"', "").lower() + "-1"
        for item in SKUs:
            if item == sku:
                sku = increment(sku)
        SKUs.append(sku)
        image = sku[:-2].replace("-configurable", "") + '.jpg'

        featured = inRow[featuredRow]
        attributes = inRow[_attribute_setRow]
        short_des = "Need an Upgrade? Call Us!<br><strong>770-850-8400</strong>"

        if attributes != "Default":
            manufacturer = inRow[manufacturerRow].replace(" ", "")
            generation = inRow[generationRow]
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

            hdd_capacity = inRow[hdd1_capacityRow].replace(" ", "").replace("147GB", "146GB")
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
            if ram_amount[-2:].lower() != "gb":
                ram_amount = ram_amount + "GB"
            ram_type = inRow[ram_technologyRow]

            """
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
            """
        else:
            manufacturer = ""
            generation = ""
            processor = ""
            cpu_quantity = ""
            cpu_speed = ""
            cpu_cores = ""
            ram_amount = ""
            ram_type = ""
            hdd_quantity = ""
            hdd_capacity = ""
            hdd_size = ""
            raid = ""
            warranty = ""
            power = ""
            hdd_tech = ""
            drive = ""

        if attributes == "Laptop":
            category = "Laptops"
        elif attributes == "Storage":
            category = "Storage"
        elif attributes == "Workstation":
            category = "Workstations"
        else:
            category = "Servers"

        if generation == "11":
            if "R610" in name or "R710" in name or "R510" in name:
                ram_amount = "8GB"
                ram_type = "DDR3"
                cpu_cores = "Dual"
                cpu_speed = "1.86GHz"
                cpu_quantity = "2"
                hdd_capacity = "Configurable"
                drive = "DVD"
                warranty = "1 Year"
                raid = "Perc 6/i"
            else:
                continue
        elif hdd_size == '2.5"':
            continue
        else:
            continue

        if attributes == "Laptop":
            continue

        if images == True:
            if os.path.isfile('images/'+image) == False:
                    urllib.urlretrieve("http://www.buysellservers.com/media/catalog/product/"+image[0]+"/"+image[1]+"/"+image, 'images/' + image)
            if os.path.getsize('images/'+image) < 1:
                os.remove('images/' + image)

        line = line + 1
        outRow = [sku,'',attributes,'simple',category,'"Default Category"','base',name,'"<strong>For Additional Configurations and Operating Systems Call Us at 770-850-8400</strong>"',short_des,price,'','','','','45.0000',manufacturer,'','','',image,image,image,'','','','','','1',sku,sku,'','4','','','','','','"Block after Info Column"','0','0',name,name,name,'"2015-01-13 16:24:33"','"2015-01-13 16:45:04"','','"Use config"','"Use config"','','2','','','','',accept_price,decline_price,'',featured,generation,server_type,processor,cpu_quantity,cpu_speed,cpu_cores,ram_amount,ram_type,hdd_quantity,hdd_capacity,hdd_size,raid,warranty,power,hdd_tech,drive,'0.0000','0.0000','1','0','0','1','1.0000','1','0.0000','1','0','1.0000','1','0','1','1','1','0.0000','1','0','0','','','','','','','','','','','','','','','','','88',image,name,'1','0','','','','','','','','','','','','']
        writer.writerow(outRow)

        template = ['', '', '', '', category, '"Default Category"', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

        if attributes == "Workstation":
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
                    if "1U" in server_type:
                        category = category+"/Dell 1U Racks"
                    elif "2U" in server_type:
                        category = category+"/Dell 2U Racks"
                    else:
                        category = category+"/Dell 4U+ Racks"
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
                    if "1U" in server_type:
                        category = category+"/HP 1U Racks"
                    elif "2U" in server_type:
                        category = category+"/HP 2U Racks"
                    else:
                        category = category+"/HP 4U+ Racks"
                    template[4] = '"'+category+'"'
                    writer.writerow(template)

        if hdd_size == '2.5"':
            for n in range(0, int(hdd_quantity)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Hard Drive ' + str(n+1), '0', '', '', '', n+2, '', '', '', '']
                if n > len(outDrives)-1:
                    outDrives.append([])
                outDrives[n].append(outRow)
                outDrives[n].append(template)
                for d in range(0, len(Sdrives)):
                    template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', Sdrives[d][0], Sdrives[d][1], Sdrives[d][0].lower().replace(' ', '-'), d]
                    outDrives[n].append(template)

        if hdd_size == '3.5"':
            for n in range(0, int(hdd_quantity)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Hard Drive ' + str(n+1), '0', '', '', '', n+2, '', '', '', '']
                if n > len(outDrives)-1:
                    outDrives.append([])
                outDrives[n].append(outRow)
                outDrives[n].append(template)
                for d in range(0, len(Bdrives)):
                    template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', Bdrives[d][0], Bdrives[d][1], Bdrives[d][0].lower().replace(' ', '-'), d]
                    outDrives[n].append(template)

        if generation == "11":
            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'RAM', '0', '', '', '', '1', '', '', '', '']
            outRAM.append(outRow)
            outRAM.append(template)
            for r in range(0, len(RAM)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', RAM[r][0] + " DDR3", RAM[r][1], RAM[r][0].lower(), r]
                outRAM.append(template)

            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Processor', '0', '', '', '', '0', '', '', '', '']
            outProcs.append(outRow)
            outProcs.append(template)
            for p in range(0, len(procs)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', procs[p][0], procs[p][1], procs[p][0][15:20], p]
                outProcs.append(template)

            outExtras.append(outRow)
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Bezel', '0', '', '', '', '20', '', '', '', ''])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'None', '0', 'none', 0])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Bezel', '45', 'bezel', 1])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Power Supply', '0', '', '', '', '21', '', '', '', ''])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Single Power', '0', 'single', 0])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Redundant Power', '75', 'redundant', 1])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Warranty', '0', '', '', '', '22', '', '', '', ''])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '1 Year Warranty', '0', '1yrwarranty', 0])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '3 Year Warranty', '99', '3yrwarranty', 1])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Rails', '0', '', '', '', '1233', '', '', '', ''])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'None', '0', 'none', 0])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Add Rails', '99', 'rails', 1])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'RAID', '0', '', '', '', '24', '', '', '', ''])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Perc 6/i', '0', 'perc', 0])
            outExtras.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'H700', '199', 'h700', 1])


    shutil.rmtree('extras', ignore_errors=True)
    os.makedirs('extras')
    os.chdir("extras")
    for d in range(0, len(outDrives)):
        file = 'upload-drives-' + str(d+1) + '.csv'
        writer = csv.writer(open(file, 'w+'), quotechar="'")
        writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
        for row in outDrives[d]:
            writer.writerow(row)

    file = 'upload-ram.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")
    writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
    for row in outRAM:
        writer.writerow(row)

    file = 'upload-procs.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")
    writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
    for row in outProcs:
        writer.writerow(row)

    file = 'upload-extras.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")
    writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity','cpu_speed','cpu_cores','ram_quantity','ram_technology','hdd1_quantity','hdd1_capacity','hdd_size','raid','warranty','power_supply','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
    for row in outExtras:
        writer.writerow(row)

    print str(line) + " products"