#import tkinter as tk
from tkinter import *
import xml.etree.ElementTree
import copy
import re
import json



def fill_bib_list(thislist):
	print("filling list ...")
	thislist.sort(key=str.lower)
	for item in thislist:
		bibtex_listbox.insert(END, item)

	# alternating background colour
	for index in range(bibtex_listbox.size()):
		if index%2 == 0:
	 		bibtex_listbox.itemconfig(index, bg="thistle2")


def clear_bib_selection():
	titleText.delete("1.0", END)
	contentText.delete("1.0", END)
	snippets_listbox.delete(0, END)
	idText.delete("1.0", END)

def get_bib_data_by_title(title):
	global bibentries
	for sn in bibentries:
		if sn["title"] == title:
			return sn
	print("Error: bibtex entry with that title not found")


def get_bib_data_by_id(thisID):
	global bibentries
	for sn in bibentries:
		if sn["id"] == thisID:
			return sn
	print("Error: bibtex entry with that ID not found")



def save_to_json():
	global reftags
	global doctags
	global fragments
	global tagging
	global taglist


	print("saving to json ...")

	fragrelationsfile = open("fragmentrelations.json","w")
	fragreljson = json.dump(fragrelations, fragrelationsfile, indent=4)
	fragrelationsfile.close()

	taglistfile = open("tags.json","w")
	taglistjson = json.dump(taglist, taglistfile, indent=4)
	taglistfile.close()
	
	#save all reftags
	reffrags = []
	for fr in fragments:
		print(fr["id"])
		if fr["id"] in reftags:
			print("found one")
			itstags = tagging[str(fr["id"])]
			print(itstags)
			wholefrag = create_fragment(fr["id"], fr["title"], fr["content"], itstags)
			reffrags.append(copy.deepcopy(wholefrag))

	print(reffrags)
	print(len(reffrags))
	reffragfile = open("snippets.json", "w")
	reffragjson = json.dump(reffrags, reffragfile, indent=4)
	reffragfile.close()

	docfrags = []
	for fr in fragments:
		if fr["id"] in doctags:
			docfrags.append(copy.deepcopy(fr))

	print(docfrags)
	print(len(docfrags))
	docfragfile = open("bibtex.json","w")
	docfragjson = json.dump(docfrags, docfragfile, indent=4)
	docfragfile.close()

	print("... done.")


def load_from_json():
	global bibentries
		
	bibfile = open("bibtex.json","r")
	bibentries = json.load(bibfile)
	bibfile.close()

	print("loaded bib list ...")


def fill_snippets_listbox(thisDocID):
	relfile = open("fragmentrelations.json", "r")
	reljson = json.load(relfile)
	relfile.close()

	relatedSnippets = []
	for rj in reljson:
		rels = reljson[rj]
		if thisDocID in rels:
			print("found a reference")
			snippetDict = get_snippet_by_id(rj)
			relatedSnippets.append(snippetDict)
	print("result:")
	print(relatedSnippets)
	
	relatedSnippets.sort(key=str.lower)
	for item in relatedSnippets:
		snippets_listbox.insert(END, item)

	# alternating background colour
	for index in range(snippets_listbox.size()):
		if index%2 == 0:
			snippets_listbox.itemconfig(index, bg="thistle2")

def get_snippet_by_id(thisID):
	snippetfile = open("snippets.json", "r")
	snippets = json.load(snippetfile)
	snippetfile.close()

	for sn in snippets:
		if str(sn["id"]) == thisID:
			print("retrieved snippet")
			return sn["title"]
	return



def display_selection(event):
	index = bibtex_listbox.curselection()[0]
	print(index)
	seltext = bibtex_listbox.get(index)
	clear_bib_selection()
	
	titleText.insert("1.0", seltext)
	
	frdict = get_bib_data_by_title(seltext)
	
	contentText.insert("1.0", frdict["content"])
	
	fill_snippets_listbox(frdict["id"])

	idText.insert("1.0", frdict["id"])

def get_highest_id_in_json(jsonfile):
	thisfile = open(jsonfile, "r")
	data = json.load(thisfile)
	thisfile.close()

	highestID = 0
	for d in data:
		if int(d["id"]) > highestID:
			highestID = int(d["id"])
	return highestID

	
def generate_bib_id():
	global bibentries
	
	highestDocID  = get_highest_id_in_json("bibtex.json")
	highestSnippetID = get_highest_id_in_json("snippets.json")
	
	newid = max(highestDocID, highestSnippetID)+1
	return newid

def popup_snippet(event):
	index = snippets_listbox.curselection()[0]
	seltext = snippets_listbox.get(index)

	popup = Toplevel()
	popup.title("Snippet: "+seltext)
	
	snippet = get_snippet_by_title(seltext)

	#refLabel = Label(popup, text=seltext) 
	#refLabel.pack(padx=10, pady=10)
	refText = Label(popup, text=snippet["content"], wraplength=400, justify=LEFT)
	refText.pack(padx=10, pady=10)
	refTags = Label(popup, text=snippet["tags"], justify=RIGHT, relief=SUNKEN)
	refTags.pack(padx=10, pady=10, ipadx=10, ipady=10)

def get_snippet_by_title(seltext):

	snipfile = open("snippets.json","r")
	snippets = json.load(snipfile)
	snipfile.close()

	for sp in snippets:
		if sp["title"] == seltext:
			return sp
		






############################ main #########################
 

root = Tk()
root.title("Bibtex Reference Database")

# CONSTANTS

MAX_TITLE_LENGTH = 30
MAX_CONTENT_LENGTH = 60
MAX_CONTENT_LINES = 15
LISTBOX_HEIGHT = 50
LISTBOX_ROWSPAN = 10
GAME_START_COL = 2
SNIPS_LISTBOX_HEIGHT = 5

# LEFTMOST HALF: bibtex refs listbox

bibtexLabel = Label(root, text="Bibtex Entries")
bibtexLabel.grid(row=0, column=0, padx=10, pady=10)

bibtex_listbox = Listbox(root, width=MAX_TITLE_LENGTH, height=LISTBOX_HEIGHT)
bibtex_listbox.grid(row=1, column=0, padx=10, pady=10, rowspan=LISTBOX_ROWSPAN)

yscroll = Scrollbar(command=bibtex_listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=1, sticky=NS, rowspan=LISTBOX_ROWSPAN)
bibtex_listbox.configure(yscrollcommand=yscroll.set)

bibtex_listbox.bind("<ButtonRelease-1>", display_selection)
bibtex_listbox.bind("<Return>", display_selection)




# RIGHT HALF: content display
selectionLabel = Label(root, text="Selected Bibtex Entry")
selectionLabel.grid(row=0, column=GAME_START_COL, ipadx=10,ipady=10)


titleLabel = Label(root, text="title:")
titleLabel.grid(row=1, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
titleText = Text(root, width=MAX_TITLE_LENGTH, height=1)
titleText.grid(row=2, column=GAME_START_COL, padx=10, ipadx=10, ipady=10, sticky=NW)

contentLabel = Label(root, text="content:")
contentLabel.grid(row=3, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
contentText = Text(root, width=MAX_CONTENT_LENGTH, height=MAX_CONTENT_LINES)
contentText.grid(row=4, column=GAME_START_COL, ipadx=10, padx=10, ipady=10, sticky=NW)

snippetsLabel = Label(root, text="ref snippets:")
snippetsLabel.grid(row=5, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
snippets_listbox = Listbox(root, width=MAX_CONTENT_LENGTH, height=SNIPS_LISTBOX_HEIGHT)
snippets_listbox.grid(row=6, column=GAME_START_COL, padx=10, pady=10)

yscroll_snips = Scrollbar(command=snippets_listbox.yview, orient=VERTICAL)
yscroll_snips.grid(row=6, column=GAME_START_COL+1, sticky=NS, padx=10, pady=10)
snippets_listbox.configure(yscrollcommand=yscroll_snips.set)
snippets_listbox.bind("<ButtonRelease-1>", popup_snippet)
snippets_listbox.bind("<Return>", popup_snippet)

idLabel = Label(root, text="id:")
idLabel.grid(row=7, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
idText = Text(root, width=4, height=1)
idText.grid(row=8, column=GAME_START_COL, padx=10, ipadx=10, ipady=10, sticky=NW)




# load data
global bibentries
bibentries = {}

load_from_json()
print("no. of entries: "+str(len(bibentries)))

root.title("Bibtex Entry Database: "+str(generate_bib_id()-1)+" entries")

global bibtexTitles
bibtexTitles = []

for g in bibentries:
	bibtexTitles.append(copy.deepcopy(g["title"]))


# fill snippet list
fill_bib_list(bibtexTitles)


root.mainloop()



