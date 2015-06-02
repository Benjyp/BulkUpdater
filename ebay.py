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
        max = (600, 600)
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

os.chdir("ebay")
SKUs = []
descFile = open('desc.html', 'r+')
desc = descFile.read().replace("\n", "").replace("\r", "")

with open('products - products.csv', 'rb') as i:
    reader = csv.reader(i)

    file = 'upload.csv'
    writer = csv.writer(open(file, 'w+'))
    writer.writerow(('Site', 'Format', 'Currency', 'Title', 'Condition', 'ConditionDescription', 'SubtitleText', 'Custom Label', 'Description', 'Category 1', 'Category 2', 'Store Category', 'Store Category 2', 'PicURL', 'Quantity', 'LotSize', 'Duration', 'Starting Price', 'Reserve Price', 'BIN Price', 'Private Auction', 'Counter', 'Buyer pays shipping', 'Payment Instructions', 'Specifying Shipping Costs', 'Insurance Option', 'Insurance Amount', 'Sales Tax Amount', 'Sales Tax State', 'Apply tax to total', 'Accept PayPal', 'PayPal Email Address', 'Accept MO Cashiers', 'Accept Personal Check', 'Accept Visa/Mastercard', 'Accept AmEx', 'Accept Discover', 'IntegratedMerchantCreditCard', 'Accept Payment Other', 'Accept Payment Other Online', 'Accept COD', 'COD PrePay Delivery', 'Postal Transfer', 'Payment See Description', 'Accept Money Xfer', 'CCAccepted', 'CashOnPickupAccepted', 'MoneyXferAccepted', 'MoneyXferAcceptedinCheckout', 'Ship-To Option', 'Escrow', 'BuyerPaysFixed', 'Location - City/State', 'Location - Country', 'Title Bar Image', 'Gallery1.Gallery', 'Gallery Featured', 'FeaturedFirstDuration', 'Gallery URL', 'PicInDesc', 'PhotoOneRadio', 'PhotoOneURL', 'Gallery2.GalleryPlus', 'Bold', 'MotorsGermanySearchable', 'Border', 'LE.Highlight', 'Featured Plus', 'Home Page Featured', 'Subtitle in search results', 'Gift Icon', 'DepositType', 'DepositAmount', 'ShippingRate', 'ShippingCarrier', 'ShippingType', 'ShippingPackage', 'ShippingIrregular', 'ShippingWeightUnit', 'WeightMajor', 'WeightMinor', 'MeasurementUnit', 'CODCost', 'PackageDimension', 'ShipFromZipCode', 'PackagingHandlingCosts', 'Year', 'MakeCode', 'ModelCode', 'EngineCode', 'ThemeId', 'LayoutId', 'AutoPay', 'Apply Multi-item Shipping Discount', 'Attributes', 'Package Length', 'Package Width', 'Package Depth', 'ShippingServiceOptions', 'VATPercent', 'ProductID', 'ProductReferenceID', 'UseStockPhotoURLAsGallery', 'IncludeStockPhotoURL', 'IncludeProductInfo', 'UniqueIdentifier', 'GiftIcon.GiftWrap', 'GiftIcon.GiftExpressShipping', 'GiftIcon.GiftShipToRecipient', 'InternationalShippingServiceOptions', 'Ship-To Locations', 'Exclude Ship-To Locations', 'Exclude Ship-To Type Locations', 'Rate Tables Domestic', 'Rate Tables International', 'Zip', 'BuyerRequirementDetails/LinkedPayPalAccount', 'PM.PaisaPayAccepted', 'PaisaPayEscrowEMI', 'LE.ProPackBundle', 'BestOfferEnabled', 'LiveAuctionDetails/LotNumber', 'LiveAuctionDetails/SellerSalesNumber', 'LiveAuctionDetails/LowEstimate', 'LiveAuctionDetails/HighEstimate', 'LiveAuctionDetails/eBayBatchNumber', 'LiveAuctionDetails/eBayItemInBatch', 'LiveAuctionDetails/ScheduleID', 'LiveAuctionDetails/UserCatalogID', 'Item.ExportedImages', 'PhotoDisplayType', 'TaxTable', 'LoanCheck', 'CashInPerson', 'HoursToDeposit', 'DaysToFullPayment', 'UserHostedOptimizePictureWellBitmap', 'BuyerResponsibleForShipping', 'GetItFast', 'DispatchTimeMax', 'CharityID', 'CharityName', 'DonationPercentage', 'AutoDecline', 'ListingDetails/MinimumBestOfferPrice', 'ListingDetails/MinimumBestOfferMessage', 'LE.ValuePackBundle', 'LE.ProPackPlusBundle', 'LE.BasicUpgradePackBundle', 'LocalOnlyChk', 'ListingDetails/LocalListingDistance', 'ContactPrimaryPhone', 'ContactSecondaryPhone', 'LocationInfo', 'ExtendedSellerContactDetails/ClassifiedAdContactByEmailEnabled', 'ppl_PhoneEnabled', 'BuyerRequirementDetails/ShipToRegistrationCountry', 'BuyerRequirementDetails/ZeroFeedbackScore', 'BuyerRequirementDetails/MinimumFeedbackScore', 'BuyerRequirementDetails/MaximumUnpaidItemStrikesInfo', 'BuyerRequirementDetails/MaximumUnpaidItemStrikesInfo/Count', 'BuyerRequirementDetails/MaximumUnpaidItemStrikesInfo/Period', 'BuyerRequirementDetails/MaximumItemRequirements/MaximumItemCount', 'BuyerRequirementDetails/MaximumItemRequirements/MinimumFeedbackScore', 'BuyerRequirementDetails/VerifiedUserRequirements/VerifiedUser', 'BuyerRequirementDetails/VerifiedUserRequirements/MinimumFeedbackScore', 'DisableBuyerRequirements', 'BuyerRequirementDetails/MaximumBuyerPolicyViolations/Count', 'BuyerRequirementDetails/MaximumBuyerPolicyViolations/Period', 'Domestic Insurance Option', 'Domestic Insurance Amount', 'GlobalShippingService', 'InternationalShippingType', 'InternationalPackagingHandlingCosts', 'Domestic Profile Discount', 'International Profile Discount', 'Apply Profile Domestic', 'Apply Profile International', 'SellerTags', 'AutoAccept', 'ListingDetails/BestOfferAutoAcceptPrice', 'eBayNotes', 'Paymate', 'ProPay', 'Moneybookers', 'StandardPayment', 'UPC', 'ITEM_SHIPPING_POLICYID', 'ITEM_PAYMENT_POLICYID', 'ITEM_RETURN_POLICYID', 'ITEM_SHIPPING_POLICYNAME', 'ITEM_PAYMENT_POLICYNAME', 'ITEM_RETURN_POLICYNAME', 'PromoteCBT', 'ReturnsAccepted', 'ReturnsWithin', 'Refund', 'ShippingCostPaidBy', 'ReturnsRestockingFee', 'WarrantyOffered', 'WarrantyType', 'WarrantyDuration', 'ReturnsDetail', 'WofGMarketplace', 'WofGCategoryID', 'WofGDescription', 'WofGProducerInfo', 'WofGRegionOfOrigin', 'WofProduceerPictureURL', 'WofGQuestionSet', 'WofGTrustProvider', 'Fitments', 'Variations', 'PictureURL'))

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
        line = line + 1
        name = inRow[nameRow].replace("Dell ", "").replace("HP ", "")

        price = inRow[priceRow]

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

        sku = name.replace(" ", "-").replace("---", "-").replace("--", "-").replace('"', "").replace('*', '_').lower() + "-1"
        for item in SKUs:
            if item == sku:
                sku = increment(sku)
        SKUs.append(sku)

        imageName = sku[:-2] + '.jpg'
        imageURL = "http://www.buysellservers.com/media/catalog/product/"+imageName[0]+"/"+imageName[1]+"/"+imageName

        attributes = inRow[_attribute_setRow]

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

        category1 = ""
        title = ""

        if attributes == "Server":
            category1 = "11211"
            title = " ".join((manufacturer, name, cpu_quantity, "x", cpu_speed, "Proc", ram_amount, "RAM", hdd_quantity, "x", hdd_capacity, "HDDs"))
        if attributes == "Storage":
            category1 = "11211"
            title = " ".join((manufacturer, name, hdd_quantity, "x", hdd_capacity, "HDDs"))
        elif attributes == "Workstation":
            category1 = "11211"
            title = " ".join((manufacturer, name, cpu_quantity, "x", cpu_speed, "Proc", ram_amount, "RAM", hdd_quantity, "x", hdd_capacity, "HDDs"))
        elif attributes == "Laptop":
            category1 = "177"
            title = " ".join((manufacturer, name, cpu_speed, "Proc", ram_amount, "RAM", hdd_capacity, "HDD"))

        if category1 == "":
            print name

        quantity = 10
        description = desc.replace("^name", name).replace("^cpu_quantity", cpu_quantity).replace("^cpu_speed", cpu_speed).replace("^ram_quantity", ram_amount).replace("^hdd_quantity", hdd_quantity).replace("^hdd_capacity", hdd_capacity).replace("^raid", raid).replace("^power", power).replace("^server_type", server_type).replace("^warranty", warranty).replace("^drive", drive).replace("^hdd_size", hdd_size).replace("^title", title).replace("^image_url", imageURL)
        storeCategory = ""
        bestOffer = 1
        shippingOptions = 'PABT%0d%0aAGgAaQBwAHAAaQBuAGcAUwBlAHIAdgBpAGMAZQBPAHAAdABpAG8AbgBzAD4APABTAGgAaQBwAHAA%0d%0aaQBuAGcAUwBlAHIAdgBpAGMAZQBPAHAAdABpAG8AbgA+ADwAUwBoAGkAcABwAGkAbgBnAFMAZQBy%0d%0aAHYAaQBjAGUAPgAxADwALwBTAGgAaQBwAHAAaQBuAGcAUwBlAHIAdgBpAGMAZQA+ADwAUwBoAGkA%0d%0acABwAGkAbgBnAFMAZQByAHYAaQBjAGUAUAByAGkAbwByAGkAdAB5AD4AMQA8AC8AUwBoAGkAcABw%0d%0aAGkAbgBnAFMAZQByAHYAaQBjAGUAUAByAGkAbwByAGkAdAB5AD4APABGAHIAZQBlAFMAaABpAHAA%0d%0acABpAG4AZwA+ADEAPAAvAEYAcgBlAGUAUwBoAGkAcABwAGkAbgBnAD4APABTAGgAaQBwAHAAaQBu%0d%0aAGcAUwBlAHIAdgBpAGMAZQBDAG8AcwB0AD4AMAAuADAAMAA8AC8AUwBoAGkAcABwAGkAbgBnAFMA%0d%0aZQByAHYAaQBjAGUAQwBvAHMAdAA+ADwAUwBoAGkAcABwAGkAbgBnAFMAZQByAHYAaQBjAGUAQQBk%0d%0aAGQAaQB0AGkAbwBuAGEAbABDAG8AcwB0AD4APAAvAFMAaABpAHAAcABpAG4AZwBTAGUAcgB2AGkA%0d%0aYwBlAEEAZABkAGkAdABpAG8AbgBhAGwAQwBvAHMAdAA+ADwAUwBoAGkAcABwAGkAbgBnAFMAZQBy%0d%0aAHYAaQBjAGUAQQBkAGQAUwB1AHIAYwBoAGEAcgBnAGUAPgA8AC8AUwBoAGkAcABwAGkAbgBnAFMA%0d%0aZQByAHYAaQBjAGUAQQBkAGQAUwB1AHIAYwBoAGEAcgBnAGUAPgA8AFMAaABpAHAAcABpAG4AZwBT%0d%0aAGUAcgB2AGkAYwBlAFMAdQByAGMAaABhAHIAZwBlAFYAYQBsAD4APAAvAFMAaABpAHAAcABpAG4A%0d%0aZwBTAGUAcgB2AGkAYwBlAFMAdQByAGMAaABhAHIAZwBlAFYAYQBsAD4APAAvAFMAaABpAHAAcABp%0d%0aAG4AZwBTAGUAcgB2AGkAYwBlAE8AcAB0AGkAbwBuAD4APAAvAFMAaABpAHAAcABpAG4AZwBTAGUA%0d%0acgB2AGkAYwBlAE8AcAB0AGkAbwBuAHMAPgAAAA=='


        if "Special Edition" in name:
            print description


        outRow = ('0', '9', '1', title, '1000', '', '~', '~', description, category1, '', storeCategory, '0', imageURL, quantity, '~', '30', price, '~', '~', '0', '~', '0', '"Warranty as defined (see product description), Please email us with any questions, or call our Toll Free Number - 1-888-413-8900."', '1', '~', '~', '0', '~', '~', '1', 'tradeez@gmail.com', '~', '~', '1', '~', '1', '~', '~', '~', '~', '~', '~', '0', '~', '~', '~', '~', '~', '~', '0', '~', '~', 'US', '1', '0', '0', '~', '~', '~', '~', '~', '0', '0', '~', '0', '0', '0', '0', '0', '0', '~', '~', '~', '~', '0', '0', '~', '~', '~', '~', 'English', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '0', '0', '', '~', '~', '~', shippingOptions, '~', '', '~', '~', '~', '~', '~', '0', '0', '0', 'AAA=', 'AAA=', '', '~', '~', '~', '30062', '0', '~', '~', '~', bestOffer, '~', '~', '~', '~', '~', '~', '~', '~', '', '0', '0', '~', '~', '~', '~', '~', '0', '0', '1', '~', '~', '~', '~', '~', '~', '0', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '~', '', '~', '', '1', '~', '~', '~', '~', '0', '1', '~', '0||', '0||', '0', '0', '', '~', '~', '', '~', '~', '~', '~', '~', '~', '~', '~', '', '', '', '', '0', 'Days_14', 'MoneyBack', '0', 'NoRestockingFee', '~', '~', '~', 'RMA number needed for returns. 20%25 restocking fee applies on all returns for refund.', '~', '~', '', '~', '~', '~', '~', '~', '', '', imageURL)
        writer.writerow(outRow)

    print str(line) + " products"