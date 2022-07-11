from calendar import c
import math
from PIL import Image
from util import *
import json
from tkinter import StringVar, messagebox

class PrintOptions:
    def __init__(self, card_dict, source_directory, print_name, card_spacing, card_scaling, default_cardback):
        self.card_dict = card_dict
        self.source_directory = source_directory
        self.print_name = print_name
        self.card_spacing = card_spacing
        self.card_scaling = card_scaling
        self.default_cardback = default_cardback
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

def find_card_path(source_directory, card_name):
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            #if we find the slugified card directory with card name, return the path
            if(os.path.split(root)[1] == slugify(card_name)):
                return root
    return None

def print_cards(print_options: PrintOptions, processing_status_var: StringVar):
    
    card_dict = print_options.card_dict
    
    #create print directory if it doesn't exist
    if not os.path.exists(PRINT_DIRECTORY):
        os.mkdir(PRINT_DIRECTORY)

    #create specific print directory if it doesnt exist
    specific_print_directory = PRINT_DIRECTORY + "/" + print_options.print_name
    if not os.path.exists(specific_print_directory):
        os.mkdir(specific_print_directory)

    no_default_cardback = True
    if(print_options.default_cardback != None):
        no_default_cardback = False

    card_widths = []
    card_heights = [] 

    card_directories = []

    #measure average and max height and width of cards
    for card_name in card_dict:
        if card_name != "total":
            #recurse through source directory until we find slugified card directory name
            card_directory = find_card_path(print_options.source_directory, card_name)
            #if we found the card directory, add it to the list
            if(card_directory != None):
                card_directories.append(card_directory)
                #get all image files in the directory
                image_files = os.listdir(card_directory)
                #for each image file, load it and measure its width and height
                for image_file in image_files:
                    image_path = card_directory + "/" + image_file
                    image = Image.open(image_path)
                    width, height = image.size
                    card_widths.append(width)
                    card_heights.append(height)
            else:
                print("Could not find card directory for: " + card_name)

    #make sure we have no dimension errors
    dimension_error = False
    #make sure that every height is equal
    card_heights.sort()
    for i in range(1, len(card_heights)):
        if card_heights[i] != card_heights[i-1]:
            print("ERROR: Card heights are not equal!")
            dimension_error = True
            return
    #make sure that every width is equal
    card_widths.sort()
    for i in range(1, len(card_widths)):
        if card_widths[i] != card_widths[i-1]:
            print("ERROR: Card widths are not equal!")
            dimension_error = True
            return

    #print average height and width
    card_height = sum(card_heights) / len(card_heights)
    card_width = sum(card_widths) / len(card_widths)
    
    if(dimension_error):
        messagebox.showerror("Error", "Card dimensions are not all equal!")
        return
    
    #paper size is 8.5 x 11 inches
    page_width = int(card_width * 3.4)
    page_height = int(card_height * 3.14286)

    #set up variables for printing
    sheet_number = 0
    card_row = 0
    card_column = 0
    
    card_resize_height = int(card_height * print_options.card_scaling)
    card_resize_width = int(card_width * print_options.card_scaling)

    card_x_offset = (card_column * card_resize_width) + print_options.card_spacing
    card_y_offset = (card_row * card_resize_height) + print_options.card_spacing

    background_should_print = False

    #set up base images
    base_image = Image.new('RGB', (page_width, page_height), (255, 255, 255))
    background_image = Image.new('RGB', (page_width, page_height), (255, 255, 255))

    #get how many cards we can fit on a page using width and height
    cards_per_page = int(page_width / (card_resize_width + print_options.card_spacing)) * int(page_height / (card_resize_height + print_options.card_spacing)) - 1 

    processing_status_var.set("Building sheet {} of {}...".format(sheet_number, math.ceil(card_dict['total']/cards_per_page)))

    #arrange cards in base image
    for card_directory in card_directories:
        print("Processing card directory: " + card_directory)
        #get all image files in the directory
        image_files = os.listdir(card_directory)
        #if we have more than one image file, we need to print the second one on the background
        if(len(image_files) > 1):
            background_should_print = True
            #load and paste first image file into base image
            image_path = card_directory + "/" + image_files[0]
            image = Image.open(image_path)
            #only resize if resize value is not 1
            if(print_options.card_scaling != 1.0):
                image = image.resize((card_resize_width, card_resize_height), Image.ANTIALIAS)
            base_image.paste(image, (card_x_offset, card_y_offset))
            #load and paste second image file into background image
            image_path = card_directory + "/" + image_files[1]
            image = Image.open(image_path)
            if(print_options.card_scaling != 1.0):
                image = image.resize((card_resize_width, card_resize_height), Image.ANTIALIAS)
            background_image.paste(image, (card_x_offset, card_y_offset))
        else:
            #load and paste image file into base image
            image_path = card_directory + "/" + image_files[0]
            image = Image.open(image_path)
            if(print_options.card_scaling != 1.0):
                image = image.resize((card_resize_width, card_resize_height), Image.ANTIALIAS)
            base_image.paste(image, (card_x_offset, card_y_offset))
        #increment card column and row
        card_column += 1
        #update card x and y offsets
        card_x_offset = (card_column * card_resize_width)
        #add card spacing to x offset per column
        card_x_offset += print_options.card_spacing * (card_column + 1)

        if(card_column == 3):
            card_column = 0
            card_row += 1
            card_x_offset = (card_column * card_resize_width) + print_options.card_spacing
            card_y_offset = (card_row * card_resize_height)
            #add card spacing to y offset per row
            card_y_offset += print_options.card_spacing * (card_row + 1)
            #if we are on the last row, finish the page
            if(card_row == 3):
                card_column = 0
                card_row = 0
                card_x_offset = (card_column * card_resize_width) + print_options.card_spacing
                card_y_offset = (card_row * card_resize_height) + print_options.card_spacing
                #print base image
                base_image.save(specific_print_directory + "/page" + str(sheet_number) + ".png")
                #print background image if we need to
                if(background_should_print):
                    sheet_number += 1
                    background_image.save(specific_print_directory + "/page" + str(sheet_number) + ".png")
                #reset base image
                base_image = Image.new('RGB', (page_width, page_height), (255, 255, 255))
                #reset background image
                background_image = Image.new('RGB', (page_width, page_height), (255, 255, 255))
                #reset background flag
                background_should_print = False
                #increment sheet number
                sheet_number += 1
                processing_status_var.set("Building sheet {} of {}...".format(sheet_number, math.ceil(card_dict['total']/cards_per_page)))

    #print last page if we didn't finish on the last row and last column
    if(card_row <= 2 and card_column <= 2):
        sheet_number += 1
        processing_status_var.set("Building sheet {} of {}...".format(sheet_number, math.ceil(card_dict['total']/cards_per_page)))

        base_image.save(specific_print_directory + "/page" + str(sheet_number) + ".png")
        if(background_should_print):
            background_image.save(specific_print_directory + "/page" + str(sheet_number + 1) + ".png")
    
    processing_status_var.set("")
