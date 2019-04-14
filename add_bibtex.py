#import tkinter as tk
from tkinter import *
import xml.etree.ElementTree
import copy
import re
import json


def get_highest_id_in_json(filename):
	thisfile = open(filename, "r")
	data = json.load(thisfile)
	thisfile.close()

	highestID = 0
	for sn in data: 
		if int(sn["id"]) > highestID:
			highestID = int(sn["id"])
	return highestID

def add_to_json():
	global docs


	
	docfile = open("bibtex.json","r")
	docs = json.load(docfile)
	docfile.close()

	highestDocID = get_highest_id_in_json("bibtex.json")
	highestSnippetID = get_highest_id_in_json("snippets.json")

	newid = max(highestDocID, highestSnippetID)+1

	newdict = {}
	newdict["id"] = str(newid)
	newdict["title"] = titleText.get("1.0", END).rstrip("\n").rstrip("\t")
	newdict["content"] = contentText.get("1.0", END)
	docs.append(newdict)

	docfile = open("bibtex.json", "w")
	bla = json.dump(docs, docfile, indent=4)
	docfile.close()

	titleText.delete("1.0",END)
	contentText.delete("1.0",END)

	print("added bibtex doc entry ... id: "+str(newid))




############################ main #########################
 

root = Tk()
root.title("Document Bibtex Entry")

# CONSTANTS

MAX_TITLE_LENGTH = 30
MAX_CONTENT_LENGTH = 60
MAX_CONTENT_LINES = 15
LISTBOX_HEIGHT = 30
LISTBOX_ROWSPAN = 8
GAME_START_COL = 2





# RIGHT HALF: content display
selectionLabel = Label(root, text="Bibtex Info")
selectionLabel.grid(row=0, column=GAME_START_COL, ipadx=10,ipady=10)

titleLabel = Label(root, text="title (authors & year):")
titleLabel.grid(row=1, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
titleText = Text(root, width=MAX_TITLE_LENGTH, height=1)
titleText.grid(row=2, column=GAME_START_COL, padx=10, ipadx=10, ipady=10, sticky=NW)

contentLabel = Label(root, text="content (bibtex entry):")
contentLabel.grid(row=3, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
contentText = Text(root, width=MAX_CONTENT_LENGTH, height=MAX_CONTENT_LINES)
contentText.grid(row=4, column=GAME_START_COL, ipadx=10, padx=10, ipady=10, sticky=NW)

addButton = Button(root, text="Add bibtex", command=add_to_json)
addButton.grid(row=5, column=GAME_START_COL, padx=10, pady=10, sticky=E)







root.mainloop()



