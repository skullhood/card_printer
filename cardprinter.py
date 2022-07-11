from tkinter import *
from tkinter import messagebox
from turtle import width
import os
from mtg import download_cards_not_downloaded
from util import *
from print import print_cards, PrintOptions
import asyncio
from async_tkinter_loop import async_handler, async_mainloop

WINDOW_TITLE  = "SH Card Printer"
WINDOW_WIDTH  = 640
WINDOW_HEIGHT = 480 
WINDOW_X_POS  = 600
WINDOW_Y_POS  = 200

LOCAL_SOURCE = "Local"
SCRYFALL_OPTION = "MTG: Scryfall"

SOURCE_OPTIONS = [LOCAL_SOURCE, SCRYFALL_OPTION]


#create cards folder if it doesn't exist
create_cards_folder()

window = Tk()

#set icon
window.iconbitmap(SCRIPT_DIRECTORY + "/icon.ico")

#source variable for card source
source_var = StringVar()
#set default source
source_var.set(SOURCE_OPTIONS[0])

current_grid_row = 0
def next_grid_row():
    global current_grid_row
    current_grid_row += 1
    return current_grid_row

frame  = Frame(window)
frame.pack()

#top padding frame
top_padding = Frame(frame, height=50)
top_padding.grid(row=current_grid_row, column=0, columnspan=4)

#print name
label = Label(frame, text="Print Name: ")
label.grid(row=next_grid_row(), column=0)

#print name entry
print_name_var  = StringVar()
print_name_entry = Entry(frame, width=30, textvariable=print_name_var)
print_name_entry.grid(row=current_grid_row, column=1, columnspan=3)

#source selection label
label = Label(frame , text = "Source: " )
label.grid(row=next_grid_row(), column=0)

#source selection dropdown
drop = OptionMenu(frame, source_var , *SOURCE_OPTIONS)\
#set width to fit largest text in source options
drop.config(width=len(max(SOURCE_OPTIONS, key=len)))
drop.grid(row=current_grid_row, column=1)

#center padding
center_padding = Frame(frame, height=25)
center_padding.grid(row=next_grid_row(), column=0, columnspan=4)

#spacing label
label = Label(frame, text="Spacing: ")
label.grid(row=next_grid_row(), column=0)

#spacing entry
spacing_value_str = StringVar()
spacing_value_str.set("5")
spacing_entry = Entry(frame, textvariable=spacing_value_str, width=4)
spacing_entry.grid(row=current_grid_row, column=1, sticky=W)

#scaling label
label = Label(frame, text="Scaling: ")
label.grid(row=current_grid_row, column=2)

#scaling entry
scaling_value_str = StringVar()
scaling_value_str.set("1.0")
scaling_entry = Entry(frame, textvariable=scaling_value_str, width=4)
scaling_entry.grid(row=current_grid_row, column=3, sticky=W)

#card list
label = Label(frame , text = "Card List " )
label.grid(row=next_grid_row(), column=1)

card_list_text = StringVar()
cardnum = IntVar()
card_list_entry = Text(frame, width=40, height=10)
card_list_entry.grid(row=next_grid_row(), column=0, columnspan=4)

def set_cardnum():
    text = card_list_entry.get("1.0", "end")
    card_list_text.set(text)
    card_dict = build_card_dictionary(text)
    cardnum.set(card_dict.get("total"))

#change cardnum when user enters text
card_list_entry.bind("<KeyRelease>", lambda event: set_cardnum())

#cardnumber counter
cardnumtext = Label(frame , text = "Number of Cards: ")
cardnumtext.grid(row=next_grid_row(), column=0)

cardnumcount = Label(frame , textvariable=cardnum)
cardnumcount.grid(row=current_grid_row, column=1)

processing_status_var = StringVar()
processing_status_var.set("Waiting...")

#print cards action for button
def print_cards_action():
    global source_var
    global card_list_text
    global scaling_value_str

    print_name = print_name_var.get()

    if(print_name.strip() != ""):
        source = source_var.get()
        card_dict = build_card_dictionary(card_list_text.get())
        window.config(cursor="wait")
        source_directory = ""
        
        if(source == LOCAL_SOURCE):
            source_directory = LOCAL_DIRECTORY
        if(source == SCRYFALL_OPTION):          
            download_cards_not_downloaded(card_dict, processing_status_var)  
            source_directory = MTG_DIRECTORY
        
        scaling_value = 1.0
        try:
            scaling_value = float(scaling_value_str.get())
        except ValueError:
            print("Invalid scaling value")

        spacing_value = 10
        try:
            spacing_value = int(spacing_value_str.get())
        except ValueError:
            print("Invalid spacing value")

        print_options = PrintOptions(card_dict, source_directory, print_name, spacing_value, scaling_value, None)

        print_cards(print_options, processing_status_var)

        window.config(cursor="")
    else:
        #alert user to enter a print name with tk dialog
        messagebox.showerror("Error", "Missing print name!")

#print cards button
print_button = Button(frame, text="Print Cards", command=print_cards_action)
print_button.grid(row=next_grid_row(), column=3, columnspan=4)

#center padding
bottom_padding = Frame(frame, height=25)
bottom_padding.grid(row=next_grid_row(), column=0, columnspan=4)

#processing status label
label = Label(frame, textvariable=processing_status_var)
label.grid(row=next_grid_row(), column=0, columnspan=4)

#Start window at the center of the screen
window.title(WINDOW_TITLE)
window.geometry('{}x{}+{}+{}'.format(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X_POS, WINDOW_Y_POS))
window.mainloop()
