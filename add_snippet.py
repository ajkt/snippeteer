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

def add_new_tags_to_system(taglist):
	
	tagfile = open("tags.json","r")
	taglist_sofar = json.load(tagfile)
	tagfile.close()

	newtags = check_for_new_tags(taglist_sofar, taglist)
	if newtags == None:
		return
	
	print("found new tags ... adding to tag collection")

	#create merged taglist
	for nt in newtags:
		taglist_sofar["tags"].append(nt)
	
	print(taglist_sofar)

	tagfile = open("tags.json","w")
	bla = json.dump(taglist_sofar, tagfile, indent=4)
	tagfile.close()

def check_for_new_tags(previouslist, potentiallynewtags):
	newtags = []
	for nt in potentiallynewtags:
		if nt in previouslist["tags"]:
			print(nt)
			print("already in tags collection")
			continue
		else:
			print("detected new tag:"+str(nt))
			newtags.append(nt)
	if len(newtags) > 0:
		return newtags
	else: return None

def add_fragment_relations(thisID, fragrelations):
	fragrelfile = open("fragmentrelations.json","r")
	allrelations = json.load(fragrelfile)
	fragrelfile.close()
	
	print(allrelations)

	newfraglist = []
	for fr in fragrelations.split(";"):
		fr = fr.lstrip(" ").rstrip("\n").rstrip(" ")
		newfraglist.append(fr)
	print(newfraglist)
	
	allrelations[thisID] = newfraglist
	fragrelfile = open("fragmentrelations.json", "w")
	bla = json.dump(allrelations, fragrelfile, indent=4)
	fragrelfile.close()
	


def prepareTags(tagstring):
	#create list from semi-colon separated string, remove starting white spaces, rstrip \n and \ts
	print("tagstring")
	print(tagstring)
	taglist = [] 
	for tl in tagstring.split(";"): 
		tl = tl.lstrip(" ").rstrip("\n").rstrip("\t").rstrip(" ")
		print("TL:")
		print(tl)
		taglist.append(tl)

	print(taglist)
	return taglist


def add_to_json():
	global snippets
	
	snippetfile = open("snippets.json","r")
	snippets = json.load(snippetfile)
	snippetfile.close()

	highestDocID = get_highest_id_in_json("bibtex.json")
	highestSnippetID = get_highest_id_in_json("snippets.json")

	newid = max(highestDocID, highestSnippetID)+1

	newdict = {}
	newdict["id"] = str(newid)
	newdict["title"] = titleText.get("1.0", END).rstrip("\n").rstrip("\t")
	newdict["content"] = contentText.get("1.0", END)
	tags = prepareTags(tagsText.get("1.0", END))
	newdict["tags"] = tags
	add_new_tags_to_system(tags)
	
	fragrelations = bibrefsText.get("1.0", END)
	add_fragment_relations(str(newid), fragrelations)

	snippets.append(newdict)
	
	snippetfile = open("snippets.json", "w")
	bla = json.dump(snippets, snippetfile, indent=4)
	snippetfile.close()

	titleText.delete("1.0",END)
	contentText.delete("1.0",END)
	tagsText.delete("1.0", END)
	bibrefsText.delete("1.0", END)

	print("added reference snippet entry ...")




############################ main #########################
 

root = Tk()
root.title("Reference Snippet Entry")

# CONSTANTS

MAX_TITLE_LENGTH = 30
MAX_CONTENT_LENGTH = 60
MAX_CONTENT_LINES = 15
LISTBOX_HEIGHT = 30
LISTBOX_ROWSPAN = 8
GAME_START_COL = 2





# RIGHT HALF: content display
selectionLabel = Label(root, text="Snippet Info")
selectionLabel.grid(row=0, column=GAME_START_COL, ipadx=10,ipady=10)

titleLabel = Label(root, text="snippet title:")
titleLabel.grid(row=1, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
titleText = Text(root, width=MAX_TITLE_LENGTH, height=1)
titleText.grid(row=2, column=GAME_START_COL, padx=10, ipadx=10, ipady=10, sticky=NW)

contentLabel = Label(root, text="snippet content:")
contentLabel.grid(row=3, column=GAME_START_COL, ipadx=10, ipady=10, sticky=W)
contentText = Text(root, width=MAX_CONTENT_LENGTH, height=MAX_CONTENT_LINES)
contentText.grid(row=4, column=GAME_START_COL, ipadx=10, padx=10, ipady=10, sticky=NW)

tagsLabel = Label(root, text="snippet tags (separated by semi-colons):")
tagsLabel.grid(row=5, column=GAME_START_COL, padx=10, pady=10, sticky=W)
tagsText = Text(root, width=MAX_CONTENT_LENGTH, height=3)
tagsText.grid(row=6, column=GAME_START_COL, padx=10, pady=10, sticky=NW)

bibrefsLabel = Label(root, text="referencing bibtex entries (separated by semi-colons):")
bibrefsLabel.grid(row=7, column=GAME_START_COL, padx=10, pady=10, sticky=W)
bibrefsText = Text(root, width=MAX_TITLE_LENGTH, height=1)
bibrefsText.grid(row=8, column=GAME_START_COL, padx=10, pady=10, sticky=NW)

addButton = Button(root, text="Add snippet", command=add_to_json)
addButton.grid(row=9, column=GAME_START_COL, padx=10, pady=10, sticky=E)







root.mainloop()



