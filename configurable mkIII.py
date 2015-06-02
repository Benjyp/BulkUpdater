__author__='benjy'

import gspread
import os
import csv
import urllib
import time
import shutil
import json
from oauth2client.client import SignedJwtAssertionCredentials

#Determines if the value is numeric or not
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Increments the trailing integers of a string
def increment(s):
    if is_number(s[len(s) - 1]):
        if s[len(s) - 1] == '9':
            s=increment(s[:len(s) - 1]) + '0'
        else:
            s=s[:len(s) - 1] + str(int(s[len(s) - 1]) + 1)
    else:
        s=s + '1'
    return s

#Returns a sorted array of keys in a dictionary
def keysort(dict):
    line=[]
    for (key, value) in sorted(dict.items()):
        line.append(value)
    return line

#Constructs a custom option string from constituent values
def cconcat(name, price, sort):
    final=name
    """
    if price != 0:
        final=final + ':fixed:' + str(price)
    """
    final=final + ':fixed:' + str(price)
    final=final + ':' + name.lower().replace(' ', '-') + ':' + str(sort)
    return final

eTime=time.time()
os.chdir("configurable mkIII")
file='upload.csv'
writer=csv.writer(open(file, 'w+'), quotechar="'")

#Should the script handle images?
images=False

#Retrieve data from Google docs
dlTime=time.time()
json_key = json.load(open('../gspread-token.json'))
scope = ['https://spreadsheets.google.com/feeds']
credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
g=gspread.authorize(credentials)
products=g.open("products").worksheet('configurable').get_all_values()
options=g.open("Hardware Pricing")
optionsProcs=options.worksheet('Procs, 11th Gen').get_all_values()[1:]
optionsSDrives=options.worksheet('HDDs, 2.5"').get_all_values()[1:]
optionsBDrives=options.worksheet('HDDs, 3.5"').get_all_values()[1:]
optionsRAM=options.worksheet("RAM, DDR3").get_all_values()[1:]
dlTime=time.time()-dlTime

#Dictionaries for final csv generation
outProducts=dict()
outExtras=dict()

#Array to prevent duplicate SKUs
SKUs=[]

#List of headers in input file
header=products[0]
for r in range(0,len(header)):
    if header[r] == "sku":
        skuRow=r
    elif header[r] == "Name":
        nameRow=r
    elif header[r] == "Attributes":
        attribute_setRow=r
    elif header[r] == "Featured":
        featuredRow=r
    elif header[r] == "Manufacturer":
        manufacturerRow=r
    elif header[r] == "Generation":
        generationRow=r
    elif header[r] == "Price":
        priceRow=r
    elif header[r] == "Max CPU Quantity":
        cpu_quantity_maxRow=r
    elif header[r] == "Proc":
        processorRow=r
    elif header[r] == "Max HDD Quantity":
        hdd_quantity_maxRow=r
    elif header[r] == "HDD Size":
        hdd_sizeRow=r
    elif header[r] == "HDD Tech":
        hdd_techRow=r
    elif header[r] == "Max RAM Quantity":
        ram_quantity_maxRow=r
    elif header[r] == "RAM Tech":
        ram_technologyRow=r
    elif header[r] == "Drive":
        driveRow=r
    elif header[r] == "Server Type":
        server_typeRow=r
    elif header[r] == "Extras":
        extrasRow=r
    elif header[r] == "Weight":
        weightRow=r
    elif header[r] == "Bezel":
        bezelRow=r
    elif header[r] == "Redundant Power":
        powerRow=r
    elif header[r] == "3 Year Warranty":
        warrantyRow=r
    elif header[r] == "Rails":
        railsRow=r

#Business time, looking at each line/product in the input file
for inRow in products[1:]:

    #Create a dictionary to store the attributes of each product
    attributes=dict(
        name=str(inRow[nameRow]),
        attribute_set=inRow[attribute_setRow],
        price=inRow[priceRow],
        accept_offer_price='',
        decline_offer_price='',
        sku='',
        server_type=inRow[server_typeRow],
        image='',
        featured=inRow[featuredRow],
        short_description="Need an Upgrade? Call Us!<br><strong>770-850-8400</strong>",
        manufacturer=inRow[manufacturerRow],
        generation=inRow[generationRow],
        cpu_quantity_max=inRow[cpu_quantity_maxRow],
        drive=inRow[driveRow],
        hdd_size=inRow[hdd_sizeRow],
        hdd_tech=inRow[hdd_techRow],
        hdd_quantity_max=inRow[hdd_quantity_maxRow],
        processor=inRow[processorRow],
        ram_quantity_max=inRow[ram_quantity_maxRow],
        ram_technology=inRow[ram_technologyRow],
        weight=inRow[weightRow],
        store='',
        type='simple',
        root_category='"Default Category"',
        categories='',
        product_websites='base',
        description='"<strong>For Additional Configurations and Operating Systems Call Us at 770-850-8400</strong>"',
        special_price='',
        special_from_date='',
        special_to_date='',
        cost='',
        meta_title='',
        meta_keyword='',
        meta_description='',
        small_image='',
        thumbnail='',
        media_gallery='',
        color='',
        news_from_date='',
        news_to_date='',
        gallery='',
        status='1',
        url_key='',
        url_path='',
        minimal_price='',
        visibility='4',
        custom_design='',
        custom_design_from='',
        custom_design_to='',
        custom_layout_update='',
        page_layout='',
        options_container='"Block after Info Column"',
        required_options='0',
        has_options='0',
        image_label='',
        small_image_label='',
        thumbnail_label='',
        created_at='"2015-01-13 16:24:33"',
        updated_at='"2015-01-13 16:45:04"',
        country_of_manufacture='',
        msrp_enabled='"Use config"',
        msrp_display_actual_price_type='"Use config"',
        msrp='',
        tax_class_id='2',
        gift_message_available='',
        condition='',
        part_type='',
        part_number='',
        server_compatibility='',
        qty='0.0000',
        min_qty='0.0000',
        use_config_min_qty='1',
        is_qty_decimal='0',
        backorders='0',
        use_config_backorders='1',
        min_sale_qty='1.0000',
        use_config_min_sale_qty='1',
        max_sale_qty='0.0000',
        use_config_max_sale_qty='1',
        is_in_stock='0',
        notify_stock_qty='1.0000',
        use_config_notify_stock_qty='1',
        manage_stock='0',
        use_config_manage_stock='1',
        stock_status_changed_auto='1',
        use_config_qty_increments='1',
        qty_increments='0.0000',
        use_config_enable_qty_inc='1',
        enable_qty_increments='0',
        is_decimal_divided='0',
        _links_related_sku='',
        _links_related_position='',
        _links_crosssell_sku='',
        _links_crosssell_position='',
        _links_upsell_sku='',
        _links_upsell_position='',
        _associated_sku='',
        _associated_default_qty='',
        _associated_position='',
        _tier_price_website='',
        _tier_price_customer_group='',
        _tier_price_qty='',
        _tier_price_price='',
        _group_price_website='',
        _group_price_customer_group='',
        _group_price_price='',
        _media_attribute_id='88',
        _media_image='',
        _media_lable='',
        _media_position='1',
        _media_is_disabled='0',
        _custom_option_store='',
        _custom_option_type='',
        _custom_option_title='',
        _custom_option_is_required='',
        _custom_option_price='',
        _custom_option_sku='',
        _custom_option_max_characters='',
        _custom_option_sort_order='',
        _custom_option_row_title='',
        _custom_option_row_price='',
        _custom_option_row_sku='',
        category_reset='0',
        _custom_option_row_sort='',
        Bezel='',
        Warranty='',
        Power='',
        Rails=''
    )

    #Infer product categories
    if attributes['attribute_set'] == "Laptop":
        attributes['categories']="Laptops"
    elif attributes['attribute_set'] == "Storage":
        attributes['categories']="Storage"
    elif attributes['attribute_set'] == "Workstation":
        attributes['categories']="Workstations"
    else:
        attributes['categories']="Servers"

    #Attributes generated from other attributes
    attributes['accept_offer_price']=attributes['price']
    attributes['decline_offer_price']=float(attributes['price']) - 1
    attributes['sku']=attributes['name'].replace(" ", "-").replace("---", "-").replace("--", "-").replace('"', "").lower() + "-1"
    attributes['image']='+' + attributes['sku'][:-2].replace("-configurable", "") + '.jpg'
    attributes['small_image']=attributes['image']
    attributes['thumbnail']=attributes['image']
    attributes['url_key']=attributes['sku']
    attributes['url_path']=attributes['sku']
    attributes['image_label']=attributes['name']
    attributes['small_image_label']=attributes['name']
    attributes['thumbnail_label']=attributes['name']
    attributes['_media_image']=attributes['image']
    attributes['_media_lable']=attributes['name']
    attributes['meta_title']=attributes['name'] + ' ' + attributes['categories']
    attributes['meta_description']='Buy your ' + attributes['meta_title'] + ' today or call us to configure one for your needs. Full warranty and thoroughly tested before shipping to you.'

    #Added some columns to the import sheet for custom options, this code handles that stuff
    if inRow[bezelRow] != '':
        attributes['Bezel']='None:fixed:0:none:0|Bezel:fixed:'+inRow[bezelRow]+':bezel:1'
    if inRow[warrantyRow] != '':
        attributes['Warranty']='1 Year Warranty:fixed:0:1-year-warranty:0|3 Year Warranty:fixed:'+str(inRow[warrantyRow])+':3-year-warranty:1'
    if inRow[powerRow] != '':
        attributes['Power']='Single Power:fixed:0:single-power:0|Redundant Power:fixed:'+str(inRow[powerRow])+':redundant-power:1'
    if inRow[railsRow] != '':
        attributes['Rails']='None:fixed:0:none:0|Rails:fixed:'+str(inRow[railsRow])+':rails:1'

    #Generate unique sku
    while attributes['sku'] in SKUs:
        attributes['sku']=increment(attributes['sku'])
    SKUs.append(attributes['sku'])

    #Try to retrieve missing images
    if images == True:
        if os.path.isfile('images/'+attributes['image']) == False:
                urllib.urlretrieve("http://www.buysellservers.com/media/catalog/product/"+attributes['image'][0]+"/"+attributes['image'][1]+"/"+attributes['image'], 'images/' + attributes['image'])
        if os.path.getsize('images/'+attributes['image']) < 1:
            os.remove('images/' + attributes['image'])

    #Begin constructing custom options
    if 'Processor' not in outExtras:
        outExtras['Processor']=dict()
    line=''
    for p in range(0, len(optionsProcs)):
        line=line + cconcat(optionsProcs[p][0],optionsProcs[p][1],p) + '|'
    outExtras['Processor'][attributes['name']]=line[:-1]

    if 'RAM' not in outExtras:
        outExtras['RAM']=dict()
    line=''
    for r in range(0, len(optionsRAM)):
        if optionsRAM > attributes['ram_quantity_max']:
            break
        line=line + cconcat(optionsRAM[r][0],optionsRAM[r][1],r) + '|'
    outExtras['RAM'][attributes['name']]=line[:-1]

    #Sort values for custom options
    outExtras['Processor']['sort']=10
    outExtras['RAM']['sort']=11
    hddSortMod=20
    extraSortMod=50
    sorts=dict(
        Bezel=30,
        Warranty=32,
        Rails=31,
        Power=33
    )

    #Add 2.5" hard drives
    if attributes['hdd_size'] == '2.5"':
        for n in range(0, int(attributes['hdd_quantity_max'])):
            if ('Hard Drive ' + str(n+1)) not in outExtras:
                outExtras['Hard Drive ' + str(n+1)]=dict()
                outExtras['Hard Drive ' + str(n+1)]['sort']=hddSortMod+n
            line=''
            for d in range(0, len(optionsSDrives)):
                line=line + cconcat(optionsSDrives[d][0],optionsSDrives[d][1],d) + '|'
            outExtras['Hard Drive ' + str(n+1)][attributes['name']]=line[:-1]

    #Add 3.5" hard drives
    if attributes['hdd_size'] == '3.5"':
        for n in range(0, int(attributes['hdd_quantity_max'])):
            if ('Hard Drive ' + str(n+1)) not in outExtras:
                outExtras['Hard Drive ' + str(n+1)]=dict()
                outExtras['Hard Drive ' + str(n+1)]['sort']=hddSortMod+n
            line=''
            for d in range(0, len(optionsBDrives)):
                line=line + cconcat(optionsBDrives[d][0],optionsBDrives[d][1],d) + '|'
            outExtras['Hard Drive ' + str(n+1)][attributes['name']]=line[:-1]

    #Parse unique custom options
    for extra in inRow[extrasRow].split(";"):
        if extra == "":
            continue
        elements=extra.split(",")
        column=elements[0]
        options=elements[2].split('|')
        line=''
        for o in range(0, len(options)):
            optionElements=options[o].split('$')
            line=line + cconcat(optionElements[0], optionElements[1], o) + '|'
        if column not in outExtras:
            outExtras[column]=dict()
            outExtras[column]['sort']=elements[1]
        outExtras[column][attributes['name']]=line[:-1]

    #Array of categories the product should be placed in
    Cs=[attributes['categories']]

    #Appending the categories array
    if attributes['attribute_set'] == "Workstation":
        if attributes['manufacturer'] == "Dell":
            Cs.append(Cs[len(Cs)-1]+"/Dell Workstations")
        elif attributes['manufacturer'] == "HP":
            Cs.append(Cs[len(Cs)-1]+"/HP Workstations")
    elif attributes['categories'] == "Storage":
        if attributes['manufacturer'] == "Dell":
            Cs.append(Cs[len(Cs)-1]+"/Dell Storage")
        elif attributes['manufacturer'] == "HP":
            Cs.append(Cs[len(Cs)-1]+"/HP Storage")
    elif attributes['categories'] == "Servers":
        if attributes['manufacturer'] == "Dell":
            Cs.append(Cs[len(Cs)-1]+"/Dell Servers")
            if attributes['server_type'] == "Tower":
                Cs.append(Cs[len(Cs)-1]+"/Dell Tower Servers")
            elif attributes['server_type'][:4] == "Rack":
                if "1U" in attributes['server_type']:
                    Cs.append(Cs[len(Cs)-1]+"/Dell 1U Racks")
                elif "2U" in attributes['server_type']:
                    Cs.append(Cs[len(Cs)-1]+"/Dell 2U Racks")
                else:
                    Cs.append(Cs[len(Cs)-1]+"/Dell 4U+ Racks")
        elif attributes['manufacturer'] == "HP":
            Cs.append(Cs[len(Cs)-1]+"/HP Servers")
            if attributes['server_type'] == "Tower":
                Cs.append(Cs[len(Cs)-1]+"/HP Tower Servers")
            elif attributes['server_type'][:4] == "Rack":
                if "1U" in attributes['server_type']:
                    Cs.append(Cs[len(Cs)-1]+"/HP 1U Racks")
                elif "2U" in attributes['server_type']:
                    Cs.append(Cs[len(Cs)-1]+"/HP 2U Racks")
                else:
                    Cs.append(Cs[len(Cs)-1]+"/HP 4U+ Racks")

    #Constructing the categories attribute string
    for c in Cs:
        if c != Cs[1]:
            attributes['categories']=attributes['categories'] + ';;' + c

    #Generate an array of the products attributes
    product=[keysort(attributes)]

    #Add product attributes array to the dictionary of products to be printed
    outProducts[attributes['name']]=product

#Begin final CSV generation
headers=sorted(attributes.keys())
for header in headers:
    for col in sorts:
        if header == col:
            header = str(header)+':drop_down:0:'+str(sorts[header])

#Construct headers for each custom option
for h in outExtras.keys():
    headers.append((h+':drop_down:0:' + str(outExtras[h]['sort'])))
writer.writerow(headers)

#Finally, dump the contents of the dictionaries into the csv
for (pkey, pvalue) in outProducts.items():
    for (ekey, evalue) in outExtras.items():
        written=False
        for (okey, ovalue) in evalue.items():
            if pkey != okey:
                continue
            outProducts[pkey][0].append(ovalue)
            written=True
        if written == False:
            outProducts[pkey][0].append('')
for (pkey, pvalue) in outProducts.items():
    for l in pvalue:
        writer.writerow(l)

#Display the number of products in the csv
print str(len(outProducts)) + " products"
print "download time: %.2f/%.2f seconds total" % (dlTime, time.time()-eTime)