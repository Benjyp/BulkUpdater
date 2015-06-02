__author__ = 'benjy'

import gspread
import os
import csv
import urllib
import shutil

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

os.chdir("configurable mkII")

g = gspread.login('tradeez@gmail.com', 'hits4all')
products = g.open("products").worksheet('configurable').get_all_values()
options = g.open("Hardware Pricing")

optionsProcs = options.worksheet('Procs, 11th Gen').get_all_values()[1:]
optionsSDrives = options.worksheet('HDDs, 2.5"').get_all_values()[1:]
optionsBDrives = options.worksheet('HDDs, 3.5"').get_all_values()[1:]
optionsRAM = options.worksheet("RAM, DDR3").get_all_values()[1:]

outProcs = []
outDrives = []
outRAM = []
outExtras = []

images = False
SKUs = []
numProducts = 0

file = 'upload.csv'
writer = csv.writer(open(file, 'w+'), quotechar="'")
writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity_max','ram_quantity_max','ram_technology','hdd_quantity_max','hdd_size','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', '_custom_option_type', '_custom_option_title', '_custom_option_is_required', '_custom_option_price', '_custom_option_sku', '_custom_option_max_characters', '_custom_option_sort_order', '_custom_option_row_title', '_custom_option_row_price', '_custom_option_row_sku', '_custom_option_row_sort'))

header = products[0]
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
    elif header[r] == "cpu_quantity_max":
        cpu_quantity_maxRow = r
    elif header[r] == "processor":
        processorRow = r
    elif header[r] == "hdd_quantity_max":
        hdd_quantity_maxRow = r
    elif header[r] == "hdd_size":
        hdd_sizeRow = r
    elif header[r] == "hdd_tech":
        hdd_techRow = r
    elif header[r] == "ram_quantity_max":
        ram_quantity_maxRow = r
    elif header[r] == "ram_technology":
        ram_technologyRow = r
    elif header[r] == "drive":
        driveRow = r
    elif header[r] == "server_type":
        server_typeRow = r
    elif header[r] == "extras":
        extrasRow = r
    elif header[r] == "weight":
            weightRow = r

for inRow in products[1:]:
    name = str(inRow[nameRow])
    _attribute_set = inRow[_attribute_setRow]
    if _attribute_set != "Configurable":
        continue
    price = inRow[priceRow]
    accept_offer_price = price
    decline_offer_price = float(price) - 1
    sku = name.replace(" ", "-").replace("---", "-").replace("--", "-").replace('"', "").lower() + "-1"
    for item in SKUs:
        if item == sku:
            sku = increment(sku)
    SKUs.append(sku)
    server_type = inRow[server_typeRow]
    image = sku[:-2].replace("-configurable", "") + '.jpg'
    featured = inRow[featuredRow]
    short_description = "Need an Upgrade? Call Us!<br><strong>770-850-8400</strong>"
    manufacturer = inRow[manufacturerRow]
    generation = inRow[generationRow]
    cpu_quantity_max = inRow[cpu_quantity_maxRow]
    drive = inRow[driveRow]
    hdd_size = inRow[hdd_sizeRow]
    hdd_tech = inRow[hdd_techRow]
    hdd_quantity_max = inRow[hdd_quantity_maxRow]
    processor = inRow[processorRow]
    ram_quantity_max = inRow[ram_quantity_maxRow]
    ram_technology = inRow[ram_technologyRow]
    extras = inRow[extrasRow]
    weight = inRow[weightRow]

    _store = ''
    _type = 'simple'
    _root_category = '"Default Category"'
    _product_websites = 'base'
    description = '"<strong>For Additional Configurations and Operating Systems Call Us at 770-850-8400</strong>"'
    special_price = ''
    special_from_date = ''
    special_to_date = ''
    cost = ''
    meta_title = ''
    meta_keyword = ''
    meta_description = ''
    image = image
    small_image = image
    thumbnail = image
    media_gallery = ''
    color = ''
    news_from_date = ''
    news_to_date = ''
    gallery = ''
    status = '1'
    url_key = sku
    url_path = sku
    minimal_price = ''
    visibility = '4'
    custom_design = ''
    custom_design_from = ''
    custom_design_to = ''
    custom_layout_update = ''
    page_layout = ''
    options_container = '"Block after Info Column"'
    required_options = '0'
    has_options = '0'
    image_label = name
    small_image_label = name
    thumbnail_label = name
    created_at = '"2015-01-13 16:24:33"'
    updated_at = '"2015-01-13 16:45:04"'
    country_of_manufacture = ''
    msrp_enabled = '"Use config"'
    msrp_display_actual_price_type = '"Use config"'
    msrp = ''
    tax_class_id = '2'
    gift_message_available = ''
    condition = ''
    part_type = ''
    part_number = ''
    server_compatibility = ''
    qty = '0.0000'
    min_qty = '0.0000'
    use_config_min_qty = '1'
    is_qty_decimal = '0'
    backorders = '0'
    use_config_backorders = '1'
    min_sale_qty = '1.0000'
    use_config_min_sale_qty = '1'
    max_sale_qty = '0.0000'
    use_config_max_sale_qty = '1'
    is_in_stock = '0'
    notify_stock_qty = '1.0000'
    use_config_notify_stock_qty = '1'
    manage_stock = '0'
    use_config_manage_stock = '1'
    stock_status_changed_auto = '1'
    use_config_qty_increments = '1'
    qty_increments = '0.0000'
    use_config_enable_qty_inc = '1'
    enable_qty_increments = '0'
    is_decimal_divided = '0'
    _links_related_sku = ''
    _links_related_position = ''
    _links_crosssell_sku = ''
    _links_crosssell_position = ''
    _links_upsell_sku = ''
    _links_upsell_position = ''
    _associated_sku = ''
    _associated_default_qty = ''
    _associated_position = ''
    _tier_price_website = ''
    _tier_price_customer_group = ''
    _tier_price_qty = ''
    _tier_price_price = ''
    _group_price_website = ''
    _group_price_customer_group = ''
    _group_price_price = ''
    _media_attribute_id = '88'
    _media_image = image
    _media_lable = name
    _media_position = '1'
    _media_is_disabled = '0'
    _custom_option_store = ''
    _custom_option_type = ''
    _custom_option_title = ''
    _custom_option_is_required = ''
    _custom_option_price = ''
    _custom_option_sku = ''
    _custom_option_max_characters = ''
    _custom_option_sort_order = ''
    _custom_option_row_title = ''
    _custom_option_row_price = ''
    _custom_option_row_sku = ''
    _custom_option_row_sort = ''

    #name = str(inRow[nameRow])
    #attributes = inRow[_attribute_setRow]
    #price = inRow[priceRow]
    #accept_price = price
    #decline_price = float(price) - 1
    #server_type = inRow[server_typeRow]
    #sku = name.replace(" ", "-").lower() + "-1"
    #image = sku[:-2].replace("-configurable", "") + '.jpg'
    #featured = inRow[featuredRow]
    #short_des = "Need an Upgrade? Call Us!<br><strong>770-850-8400</strong>"
    #manufacturer = inRow[manufacturerRow]
    #generation = inRow[generationRow]
    #drive = inRow[driveRow]
    #hdd_size = inRow[hdd_sizeRow]
    #hdd_tech = inRow[hdd_techRow]
    #processor = inRow[processorRow]
    #ram_type = inRow[ram_technologyRow]

    if _attribute_set == "Laptop":
        _category = "Laptops"
    elif _attribute_set == "Storage":
        _category = "Storage"
    elif _attribute_set == "Workstation":
        _category = "Workstations"
    else:
        _category = "Servers"

    if images == True:
        if os.path.isfile('images/'+image) == False:
                urllib.urlretrieve("http://www.buysellservers.com/media/catalog/product/"+image[0]+"/"+image[1]+"/"+image, 'images/' + image)
        if os.path.getsize('images/'+image) < 1:
            os.remove('images/' + image)

    numProducts = numProducts + 1
    outRow = [sku, _store, _attribute_set, _type, _category, _root_category, _product_websites, name, description, short_description, price, special_price, special_from_date, special_to_date, cost, weight, manufacturer, meta_title, meta_keyword, meta_description, image, small_image, thumbnail, media_gallery, color, news_from_date, news_to_date, gallery, status, url_key, url_path, minimal_price, visibility, custom_design, custom_design_from, custom_design_to, custom_layout_update, page_layout, options_container, required_options, has_options, image_label, small_image_label, thumbnail_label, created_at, updated_at, country_of_manufacture, msrp_enabled, msrp_display_actual_price_type, msrp, tax_class_id, gift_message_available, condition, part_type, part_number, accept_offer_price, decline_offer_price, server_compatibility, featured, generation, server_type, processor, cpu_quantity_max, ram_quantity_max, ram_technology, hdd_quantity_max, hdd_size, hdd_tech, drive, qty, min_qty, use_config_min_qty, is_qty_decimal, backorders, use_config_backorders, min_sale_qty, use_config_min_sale_qty, max_sale_qty, use_config_max_sale_qty, is_in_stock, notify_stock_qty, use_config_notify_stock_qty, manage_stock, use_config_manage_stock, stock_status_changed_auto, use_config_qty_increments, qty_increments, use_config_enable_qty_inc, enable_qty_increments, is_decimal_divided, _links_related_sku, _links_related_position, _links_crosssell_sku, _links_crosssell_position, _links_upsell_sku, _links_upsell_position, _associated_sku, _associated_default_qty, _associated_position, _tier_price_website, _tier_price_customer_group, _tier_price_qty, _tier_price_price, _group_price_website, _group_price_customer_group, _group_price_price, _media_attribute_id, _media_image, _media_lable, _media_position, _media_is_disabled, _custom_option_store, _custom_option_type, _custom_option_title, _custom_option_is_required, _custom_option_price, _custom_option_sku, _custom_option_max_characters, _custom_option_sort_order, _custom_option_row_title, _custom_option_row_price, _custom_option_row_sku, _custom_option_row_sort]
    writer.writerow(outRow)

    template = ['', '', '', '', _category, '"Default Category"', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

    if _attribute_set == "Workstation":
        if manufacturer == "Dell":
            _category = _category+"/Dell Workstations"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
        elif manufacturer == "HP":
            _category = _category+"/HP Workstations"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
    elif _category == "Storage":
        if manufacturer == "Dell":
            _category = _category+"/Dell Storage"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
        elif manufacturer == "HP":
            _category = _category+"/HP Storage"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
    elif _category == "Servers":
        if manufacturer == "Dell":
            _category = _category+"/Dell Servers"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
            if server_type == "Tower":
                _category = _category+"/Dell Tower Servers"
                template[4] = '"'+_category+'"'
                writer.writerow(template)
            elif server_type[:4] == "Rack":
                if "1U" in server_type:
                    _category = _category+"/Dell 1U Racks"
                elif "2U" in server_type:
                    _category = _category+"/Dell 2U Racks"
                else:
                    _category = _category+"/Dell 4U+ Racks"
                template[4] = '"'+_category+'"'
                writer.writerow(template)
        elif manufacturer == "HP":
            _category = _category+"/HP Servers"
            template[4] = '"'+_category+'"'
            writer.writerow(template)
            if server_type == "Tower":
                _category = _category+"/HP Tower Servers"
                template[4] = '"'+_category+'"'
                writer.writerow(template)
            elif server_type[:4] == "Rack":
                if "1U" in server_type:
                    _category = _category+"/HP 1U Racks"
                elif "2U" in server_type:
                    _category = _category+"/HP 2U Racks"
                else:
                    _category = _category+"/HP 4U+ Racks"
                template[4] = '"'+_category+'"'
                writer.writerow(template)

    if hdd_size == '2.5"':
        for n in range(0, int(hdd_quantity_max)):
            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Hard Drive ' + str(n+1), '0', '', '', '', n+10, '', '', '', '']
            if n > len(outDrives)-1:
                outDrives.append([])
            outDrives[n].append(outRow)
            outDrives[n].append(template)
            for d in range(0, len(optionsSDrives)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', optionsSDrives[d][0], optionsSDrives[d][1], optionsSDrives[d][0].lower().replace(' ', '-'), d]
                outDrives[n].append(template)

    if hdd_size == '3.5"':
        for n in range(0, int(hdd_quantity_max)):
            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Hard Drive ' + str(n+1), '0', '', '', '', n+10, '', '', '', '']
            if n > len(outDrives)-1:
                outDrives.append([])
            outDrives[n].append(outRow)
            outDrives[n].append(template)
            for d in range(0, len(optionsBDrives)):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', optionsBDrives[d][0], optionsBDrives[d][1], optionsBDrives[d][0].lower().replace(' ', '-'), d]
                outDrives[n].append(template)

    if generation == "11":
        outRAM.append(outRow)
        template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'RAM', '0', '', '', '', '1', '', '', '', '']
        outRAM.append(template)
        for r in range(0, len(optionsRAM)):
            if int(optionsRAM[r][0].replace("GB", "")) <= int(ram_quantity_max.replace("GB", "")):
                template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', optionsRAM[r][0] + " DDR3", optionsRAM[r][1], optionsRAM[r][0].lower(), r]
                outRAM.append(template)

        outProcs.append(outRow)
        template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', 'Processor', '0', '', '', '', '0', '', '', '', '']
        outProcs.append(template)
        for p in range(0, len(optionsProcs)):
            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', optionsProcs[p][0], optionsProcs[p][1], optionsProcs[p][0][15:20], p]
            outProcs.append(template)

    outExtras.append(outRow)
    for extra in extras.split(";"):
        if extra == "":
            continue
        elements = extra.split(",")
        template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'default', 'drop_down', elements[0], '0', '', '', '', elements[1], '', '', '', '']
        outExtras.append(template)
        lines = elements[2].split("|")
        for line in range(0, len(lines)):
            attribs = lines[line].split("$")
            template = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', attribs[0], attribs[1], attribs[0].lower().replace(" ", "-"), line]
            outExtras.append(template)

shutil.rmtree('extras', ignore_errors=True)
os.makedirs('extras')
os.chdir("extras")
for d in range(0, len(outDrives)):
    file = 'upload-drives-' + str(d+1) + '.csv'
    writer = csv.writer(open(file, 'w+'), quotechar="'")
    writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity_max','ram_quantity_max','ram_technology','hdd_quantity_max','hdd_size','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
    for row in outDrives[d]:
        writer.writerow(row)

file = 'upload-ram.csv'
writer = csv.writer(open(file, 'w+'), quotechar="'")
writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity_max','ram_quantity_max','ram_technology','hdd_quantity_max','hdd_size','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
for row in outRAM:
    writer.writerow(row)

file = 'upload-procs.csv'
writer = csv.writer(open(file, 'w+'), quotechar="'")
writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity_max','ram_quantity_max','ram_technology','hdd_quantity_max','hdd_size','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
for row in outProcs:
    writer.writerow(row)

file = 'upload-extras.csv'
writer = csv.writer(open(file, 'w+'), quotechar="'")
writer.writerow(('sku','_store','_attribute_set','_type','_category','_root_category','_product_websites','name','description','short_description','price','special_price','special_from_date','special_to_date','cost','weight','manufacturer','meta_title','meta_keyword','meta_description','image','small_image','thumbnail','media_gallery','color','news_from_date','news_to_date','gallery','status','url_key','url_path','minimal_price','visibility','custom_design','custom_design_from','custom_design_to','custom_layout_update','page_layout','options_container','required_options','has_options','image_label','small_image_label','thumbnail_label','created_at','updated_at','country_of_manufacture','msrp_enabled','msrp_display_actual_price_type','msrp','tax_class_id','gift_message_available','condition','part_type','part_number','accept_offer_price','decline_offer_price','server_compatibility','featured','generation','server_type','processor','cpu_quantity_max','ram_quantity_max','ram_technology','hdd_quantity_max','hdd_size','hdd_tech','drive','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders','use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty','is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock','stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc','enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku','_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku','_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty','_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id','_media_image','_media_lable','_media_position','_media_is_disabled', '_custom_option_store', ' _custom_option_type', ' _custom_option_title', ' _custom_option_is_required', ' _custom_option_price', ' _custom_option_sku', ' _custom_option_max_characters', ' _custom_option_sort_order', ' _custom_option_row_title', ' _custom_option_row_price', ' _custom_option_row_sku', ' _custom_option_row_sort'))
for row in outExtras:
    writer.writerow(row)

print str(numProducts) + " products"