#import tkinter as tk
from tkinter import *
import xml.etree.ElementTree
import copy
import re
import json
import os

def search_list():
	keyword = searchEntry.get("1.0", END).rstrip()
	print("searching for "+str(keyword)+" ...")
	
	global snippetTitles
	matchcount = 0
	matchingList = []
	for ct in snippetTitles:
		#keyword in ct?
		if re.search(".*"+keyword+".*", ct):
			matchcount += 1
			matchingList.append(copy.deepcopy(ct))
	#refill listbox
	print("search results: "+str(matchcount))
	print(matchingList)
	remove_all_snippets()
	fill_snippet_list(matchingList)

def search_list_by_tag(event):
	
	index = tags_listbox.curselection()[0]
	#print(index)
	keytag = tags_listbox.get(index)
	clear_snippet_selection()
	print("searching for tag "+str(keytag)+" ...")
	
	global snippets
	matchcount = 0
	matchinglist = []
	for sp in snippets:
		sptags = sp["tags"]
		if keytag in sptags:
			matchcount += 1
			matchinglist.append(copy.deepcopy(sp["title"]))
	print("tag filter results: "+str(matchcount))
	print(matchinglist)
	remove_all_snippets()
	fill_snippet_list(matchinglist)


def remove_all_snippets():
	snippets_listbox.delete(0, END)


def clear_snippet_list():
	remove_all_snippets()
	searchEntry.delete("1.0", END)
	reset_snippet_list("")
	#global snippetTitles
	#fill_snippet_list(snippetTitles)


def fill_snippet_list(thislist):
	print("filling list ...")
	for item in thislist:
		snippets_listbox.insert(END, item)

	# alternating background colour
	for index in range(snippets_listbox.size()):
		if index%2 == 0:
	 		snippets_listbox.itemconfig(index, bg="thistle2")

def fill_tag_list(thislist):
	print("filling taglist ...")
	thislist.sort(key=str.lower)
	for item in thislist:
		tags_listbox.insert(END, item)

	# alternating background colour
	for index in range(tags_listbox.size()):
		if index%2 == 0:
			tags_listbox.itemconfig(index, bg="thistle2")


def clear_snippet_selection():
	titleText.delete("1.0", END)
	contentText.delete("1.0", END)
	tagText.delete("1.0", END)
	referenceListbox.delete(0, END)
	print("... cleared snippet selection")


def get_snippet_data_by_title(title):
	global snippets
	for sn in snippets:
		if sn["title"] == title:
			return sn
	print("Error: snippet with that title not found")

def get_fragment_data_by_title(title):
	# fragments is list of dicts
	for fr in fragments:
		if fr["title"] == title:
			return fr
	print("fragment not found (searched by title)")

def get_snippet_data_by_id(thisID):
	global snippets
	for sn in snippets:
		if sn["id"] == thisID:
			return sn
	print("Error: snippet with that ID not found")

def get_fragment_data_by_id(thisID):
	for fr in fragments:
		if fr["id"] == thisID:
			return fr
	print("fragment not found (searched by id)")

def get_doc_by_id(thisID):
	global docs
	for dc in docs:
		if dc["id"] == thisID:
			return dc
	print("Error: doc / bibtex with that ID not found")
	return None

def get_references_by_tag_id(frid):
	# in FRAGMENT_RELATION_ID: FROM_ID (2nd column, [1]) and TO_ID (3rd column, [2])
	global fragrelations
	global docs
	print(fragrelations)
	print(frid)
	relatedDocIDs = fragrelations[str(frid)]
	print("Related IDs:")
	print(relatedDocIDs)
	allRelatedDocs = []
	for docID in relatedDocIDs:
		docresult = get_doc_by_id(docID)
		print("searching for related id "+str(docresult)+" in...")
		if docresult == None:
			print("not found.")
			continue
		else:
			#print("found match in docs/bibtex")
			allRelatedDocs.append(copy.deepcopy(docresult))

	if len(allRelatedDocs) > 0:
		return allRelatedDocs
	else:
		print("over")
		return None

def removeNullItems():
	print(len(fragments))
	for fm in fragments:
		if fm["title"] == None:
			fragments.remove(fm)
	print(len(fragments))

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
			#print("found one")
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
	global fragments
	global fragrelations
	global taglist
	global tagging
	
	global docs
	global snippets
	
	docsfile = open("bibtex.json","r")
	docs = json.load(docsfile)
	docsfile.close()

	snippetsfile = open("snippets.json","r")
	snippets = json.load(snippetsfile)
	snippetsfile.close()


	#fragsfile = open("fragments.json","r")
	#fragments = json.load(fragsfile)
	#fragsfile.close()
	
	fragrelationsfile = open("fragmentrelations.json","r")
	fragrelations = json.load(fragrelationsfile)
	fragrelationsfile.close()
	
	taglistfile = open("tags.json","r")
	taglistjson = json.load(taglistfile)
	print(taglistjson)
	taglist = taglistjson
	print(taglist)
	print(len(taglist))
	taglistfile.close()

	#taggingfile = open("tagging.json","r")
	#taggingjson = json.load(taggingfile)
	#print(taggingjson)
	#tagging = taggingjson
	#print(tagging)
	#print(len(tagging))
	#taggingfile.close()

	print("loaded fragments and fragment relations and tags and tagging ...")


def get_tags_for_id(thisID):
	thisSnippet = get_snippet_data_by_id(thisID)
	templist = thisSnippet["tags"]

	tagstring = ""
	for tl in templist:
		tagstring += tl
		tagstring += "; "
	print(tagstring)
	return tagstring

def display_selection(event):
	index = snippets_listbox.curselection()[0]
	print(index)
	seltext = snippets_listbox.get(index)
	clear_snippet_selection()
	
	titleText.insert("1.0", seltext)
	
	frdict = get_snippet_data_by_title(seltext)
	
	contentText.insert("1.0", frdict["content"])
	
	tagstr = get_tags_for_id(frdict["id"])
	tagText.insert("1.0", tagstr)

	allrefs = get_references_by_tag_id(frdict["id"])
	if allrefs == None:
		referenceListbox.insert(END, "")
	else:
		for ar in allrefs:
			referenceListbox.insert(END, ar["id"]+" : "+ar["title"])
	print("... loaded snippet selection")

def popup(event):
	index = referenceListbox.curselection()[0]
	print(index)
	seltext = referenceListbox.get(index)
	
	popup = Toplevel()
	popup.title("Bibtex: "+seltext)
	
	bibText = Text(popup, width=80, height=18, padx=20, pady=20)
	bibtex = get_doc_by_id(seltext.split(" : ")[0])
	bibText.insert("1.0", bibtex["content"])
	bibText.pack()
	


# create fragment dict construct
def create_fragment(fid, title, content, tags):
	fragdict = {}
	fragdict["id"] = fid
	fragdict["title"] = title
	fragdict["content"] = content
	fragdict["tags"] = tags
	return fragdict

def generate_fragment_id():
	global snippets
	global docs
	highestsofar = 0
	for sp in snippets:
		if int(sp["id"]) > highestsofar:
			highestsofar = int(sp["id"])
	for d in docs:
		if int(d["id"]) > highestsofar:
			highestsofar = int(d["id"])
	#highestsofar = fragments[-1]["id"]
	print(highestsofar)
	return int(highestsofar) + 1
		

# get list of all fragments from piggydb xml file:
def get_fragments():
	e = xml.etree.ElementTree.parse("piggydb.xml").getroot()
	print(e)
	for tab in e.iter("table"):
		print(tab)
		print(tab.attrib)	
		tabname = tab.get("name")
		print(tabname)
		if tabname == "FRAGMENT":
			print("loading fragments ...")
			fragmentlist = []
			for row in tab.iter("row"):
				#value 1: FRAGMENT_ID
				print(row[0].text)
				#value 2: TITLE
				print(row[1].text)
				#value 3: CONTENT
				print(row[2].text)
				#value 
				frag = create_fragment(row[0].text, row[1].text, row[2].text)
				fragmentlist.append(frag)
	return fragmentlist



def add_snippet_popup():
	#create add snippet popup
	
	addSnippetPopup = Toplevel(root)
	addSnippetPopup.title("Add a snippet:")
	
	newSnippetTitleLabel = Label(addSnippetPopup, text="title:")
	newSnippetTitleLabel.grid(row=0, column=0, padx=10, pady=10, sticky=W)
	newSnippetText = Text(addSnippetPopup, width=65, height=1, padx=10, pady=10)
	newSnippetText.grid(row=1, column=0, padx=10, pady=10)

	newSnippetContentLabel = Label(addSnippetPopup, text="content:")
	newSnippetContentLabel.grid(row=2, column=0, padx=10, pady=10, sticky=W)
	newSnippetContent = Text(addSnippetPopup, width=65, height=14, padx=10, pady=10)
	newSnippetContent.grid(row=3, column=0, padx=10, pady=10)
	
	newSnippetTagsLabel = Label(addSnippetPopup, text="tags:")
	newSnippetTagsLabel.grid(row=4, column=0, padx=10, pady=10, sticky=W)
	newSnippetTags = Text(addSnippetPopup, width=65, height=1, padx=10, pady=10)
	newSnippetTags.grid(row=5, column=0, padx=10, pady=10)

	newSnippetButton = Button(addSnippetPopup, text="Add", command= lambda: add_snippet_text(newSnippetText.get("1.0",END), newSnippetContent.get("1.0",END),newSnippetTags.get("1.0",END)))
	newSnippetButton.grid(row=6, column=0, padx=10, pady=10, sticky=E)


def add_snippet_text(newSnippetTitle, newSnippetContent, newSnippetTags):
	#global fragments
	global tagging
	#global reflist
	#global reftags
	#global fragrelations

	global snippets
	global snippetTitles



	newID = generate_fragment_id()	
	newSnippetTitle = newSnippetTitle.rstrip("\n")
	print(newSnippetTitle)
	newfrag = create_fragment(newID, newSnippetTitle, newSnippetContent, newSnippetTags)
	print(newfrag)
	snippets.append(newfrag) 

	print("snippets length now: "+str(len(snippets)))#append(newfrag)


	#add id to tagging with ref tag
	tmp = []
	tmp.append("ref")
	tagging[str(newID)] = tmp

	#reload reflist
	reftags.append(str(newID))
	reflist.append(newSnippetTitle)

	#add to fragrelations as empty
	print(fragrelations)
	print(type(fragrelations))
	print(len(fragrelations))
	fragrelations[str(newID)] = []

	#clear and reload snippets:
	clear_snippet_list()

	feedbackPopup = Toplevel()
	feedbackPopup.title("Feedback")
	feedbackText = Label(feedbackPopup, text="Added to snippets.")
	feedbackText.grid(row=0, column=0, padx=10, pady=10)

	print("done")

	
def reset_snippet_list(event):
	curselection = tags_listbox.curselection()
	if curselection:
		tagindex = tags_listbox.curselection()[0]
		tags_listbox.selection_clear(tagindex)
	global snippetTitles
	fill_snippet_list(snippetTitles)


def add_ref_to_snippet():
	print("UNIMPLEMENTEDEXCEPTION")

# NO LONGER NEEDED WITHOUT PIGGYDB XML
def create_tags_from_xml():
	global taglist
	global tagging
	taggingLookup = {}
	e = xml.etree.ElementTree.parse("piggydb.xml").getroot()
	for tab in e.iter("table"):
		tabname = tab.get("name")
		if tabname == "TAG":
			for row in tab.iter("row"):
				#remember name and id:
				thisID = row[0].text
				thisTagname = row[1].text
				taggingLookup[row[0].text] = row[1].text
				taglist.append(row[1].text)
			print("... retrieved all " + str(len(taglist)) + " tag names:")
			print(taglist)
			#print(len(taggingLookup))
		if tabname == "TAGGING":
			#target id -> tag ids translated into tag names
			for row in tab.iter("row"):
				targetID = row[2].text
				tagID = row[1].text
				translated = taggingLookup[tagID]
				if targetID not in tagging.keys():
					newentry = []
					newentry.append(translated)
					tagging[str(targetID)] = newentry
				else:
					#get relations so far for this key
					sofar = tagging[str(targetID)]
					sofar.append(translated)
			print("... retrieved tagging info for "+ str(len(tagging)) + " fragment entries.")

# get all fragment ids belonging to fragments tagged as "ref" (tag id = 24)
def get_reftags():
	#tagging: all id keys where tags include "ref"
	global tagging
	global reftags
	print("... getting reftags: ids tagged as ref")
	#print(tagging.keys())
	for idkey in tagging.keys():
		if "ref" in tagging[idkey]:
			reftags.append(idkey)


# get all fragment ids belonging to fragments tagged as "paper" (tag id = 20)
def get_doctags():
	global doctags
	global tagging
	
	print(" ... getting doctags: ids tagged as paper")
	for idkey in tagging.keys():
		if "paper" in tagging[idkey]:
			doctags.append(idkey)

# get all fragment relations as a dict (fragid to list of other fragids)
def get_fragment_relations():
	e = xml.etree.ElementTree.parse("piggydb.xml").getroot()
	print("loading fragment relations ...")
	for tab in e.iter("table"):
		if tab.get("name") == "FRAGMENT_RELATION":
			relations = {}
			for row in tab.iter("row"):
				if row[1].text not in relations.keys():
					newref = []
					newref.append(row[2].text)
					relations[row[1].text] = newref
				else:
					#get relations so far for this key
					sofar = relations[row[1].text]
					sofar.append(row[2].text)
	return relations

def donothing():
	print("NOT IMPLEMENTED")

def call_add_snippet():
	os.system("python3 add_snippet.py")

def call_add_bibtex():
	os.system("python3 add_bibtex.py")

def call_add_game():
	os.system("python3 add_game.py")

def call_open_bibliography():
	os.system("python3 bibliography_database.py")

def call_open_game_database():
	os.system("python3 games_database.py")



############################ main #########################
 

root = Tk()
root.title("Reference Snippets")

# CONSTANTS
REFSNIPPET_MAX_TITLE_LENGTH = 70
REF_MAX_TITLE_LENGTH = 30
MENU_ROW = 9
LABEL_MAX_LENGTH = 20
LISTBOX_HEIGHT = 30
TAGS_START_COLUMN = 0
SNIPPETS_START_COLUMN = 2
SELECTION_START_COLUMN = 7
TAGLISTBOX_ROWSPAN = 8


# LEFTMOST HALF: tags listbox

tagsLabel = Label(root, text="Tags")
tagsLabel.grid(row=0, column=TAGS_START_COLUMN)

tags_listbox = Listbox(root, width=LABEL_MAX_LENGTH, height=LISTBOX_HEIGHT)
tags_listbox.grid(row=1, column=TAGS_START_COLUMN, padx=10, pady=10, rowspan=TAGLISTBOX_ROWSPAN)

yscrolltag = Scrollbar(command=tags_listbox.yview, orient=VERTICAL)
yscrolltag.grid(row=1, column=SNIPPETS_START_COLUMN-1, sticky=NS, rowspan=TAGLISTBOX_ROWSPAN)
tags_listbox.configure(yscrollcommand=yscrolltag.set)

tags_listbox.bind("<ButtonRelease-1>", search_list_by_tag)
tags_listbox.bind("<Return>", reset_snippet_list)









# LEFT HALF: snippet display

refsLabel = Label(root, text="Snippets")
refsLabel.grid(row=0, column=SNIPPETS_START_COLUMN)

snippets_listbox = Listbox(root, width=REFSNIPPET_MAX_TITLE_LENGTH, height=30)
snippets_listbox.grid(row=1, column=SNIPPETS_START_COLUMN, padx=10, pady=10, rowspan=TAGLISTBOX_ROWSPAN, columnspan=4, sticky=W)

yscroll = Scrollbar(command=snippets_listbox.yview, orient=VERTICAL)
yscroll.grid(row=1, column=SELECTION_START_COLUMN-1, sticky=NS, rowspan=TAGLISTBOX_ROWSPAN)
snippets_listbox.configure(yscrollcommand=yscroll.set)

snippets_listbox.bind("<ButtonRelease-1>", display_selection) #on left mouse click
snippets_listbox.bind("<Return>", display_selection) #on enter

addSnippetButton = Button(root, text="+", command=add_snippet_popup)
addSnippetButton.grid(row=MENU_ROW, column=SNIPPETS_START_COLUMN, padx=10, pady=10, sticky=NW)

searchFrame = Frame(height=1, bd=0)
searchFrame.grid(row=MENU_ROW, column=SNIPPETS_START_COLUMN, columnspan=4, pady=10, sticky=S, rowspan=2)

searchEntry = Text(searchFrame, width=30, height=1)
searchEntry.grid(row=MENU_ROW+1, column=SNIPPETS_START_COLUMN, pady=10, padx=20, sticky=SW)
searchButton = Button(searchFrame, text="Search by title ...", command=search_list)
searchButton.grid(row=MENU_ROW+1, column=SNIPPETS_START_COLUMN+1, pady=10, sticky=SW)


clearButton = Button(searchFrame, text="Clear search", command=clear_snippet_list)
clearButton.grid(row=MENU_ROW+1, column=SNIPPETS_START_COLUMN+2, pady=10, sticky=SW)




# RIGHT HALF: content display
selectionLabel = Label(root, text="Snippet Selection")
selectionLabel.grid(row=0, column=SELECTION_START_COLUMN, ipadx=10,ipady=10)

titleLabel = Label(root, text="title:")
titleLabel.grid(row=1, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, sticky=W)
titleText = Text(root, width=REFSNIPPET_MAX_TITLE_LENGTH, height=1)
titleText.grid(row=2, column=SELECTION_START_COLUMN, padx=10, ipadx=10, ipady=10, sticky=NW)

contentLabel = Label(root, text="content:")
contentLabel.grid(row=3, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, sticky=W)
contentText = Text(root, width=REFSNIPPET_MAX_TITLE_LENGTH, height=15)
contentText.grid(row=4, column=SELECTION_START_COLUMN, ipadx=10, padx=10, ipady=10, sticky=NW)

tagLabel = Label(root, text="tags:")
tagLabel.grid(row=5, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, sticky=W)
tagText = Text(root, width=REFSNIPPET_MAX_TITLE_LENGTH, height=1)
tagText.grid(row=6, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, padx=10, sticky=NW)

referencesLabel = Label(root, text="refs:")
referencesLabel.grid(row=7, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, sticky=W)
referenceListbox = Listbox(root, width=REF_MAX_TITLE_LENGTH, height=4)
referenceListbox.grid(row=8, column=SELECTION_START_COLUMN, ipadx=10, ipady=10, padx=10, sticky=NW)
referenceAddButton = Button(root, text="+", command=search_list)
referenceAddButton.grid(row=9, column=SELECTION_START_COLUMN, padx=10, pady=10, sticky=NW)

# clickable references -> popup
referenceListbox.bind("<ButtonRelease-1>", popup) # on left mouse click

selectionMenuFrame = Frame(height=1, bd=0)
selectionMenuFrame.grid(row=MENU_ROW, column=SELECTION_START_COLUMN, columnspan=2, pady=10, padx=10, sticky=E)

clearSelectionButton = Button(selectionMenuFrame, text="Clear selection", command=clear_snippet_selection)
clearSelectionButton.grid(row=MENU_ROW, column=SELECTION_START_COLUMN, padx=10, pady=10, sticky=E)
saveButton = Button(selectionMenuFrame, text="Save snippet", command=search_list)
saveButton.grid(row=MENU_ROW, column=SELECTION_START_COLUMN+1, pady=10, padx=10, sticky=E)

saveEverythingButton = Button(selectionMenuFrame, text="Save all to database", command=save_to_json)
saveEverythingButton.grid(row=MENU_ROW+1, column=SELECTION_START_COLUMN+1, ipadx=10, ipady=10, padx=10, pady=10, sticky=SE)

menubar = Menu(root)
navmenu = Menu(menubar, tearoff=0)
navmenu.add_command(label="New Ref Snippet", command=call_add_snippet)
navmenu.add_command(label="New Bibtex Entry", command=call_add_bibtex)
navmenu.add_command(label="Open Bibtex Database", command=call_open_bibliography)
navmenu.add_command(label="Open Game Database", command=call_open_game_database)

menubar.add_cascade(label="Menu", menu=navmenu)
root.config(menu=menubar)



# load data
global fragments
fragments = {}

global fragrelations
fragrelations = {}

global taglist
taglist = []

global tagging
tagging = {}


global docs
docs = {}
global snippets
snippets = {}

load_from_json()
print("no. of fragments: "+str(len(fragments)))
print("no. of fragment relations: "+str(len(fragrelations)))
print("no. of tags: "+str(len(taglist)))
print("no. of taggings: "+str(len(tagging)))
print("no. of docs: "+str(len(docs)))
print("no. of snippets: "+str(len(snippets)))

print("NEXT ID: "+str(generate_fragment_id()))
root.title("Reference Snippets: "+str(generate_fragment_id()-1)+" snippets")




#create_tags_from_xml()
# modify save_to_json to add tags to tagsfile
# modify load_from_json to retrieve tags from tagsfile



#implement get tags function
global reftags
reftags = []
get_reftags()

print("found reftags:")
print(len(reftags))

global doctags
doctags = []
get_doctags()
print("found doctags:")
print(len(doctags))

# distinguish between refs and docs, remove None titles

global doclist
doclist = []
global reflist
reflist = []

global snippetTitles
snippetTitles = []

for sn in snippets:
	snippetTitles.append(copy.deepcopy(sn["title"]))


print("final: refs & docs")
print(len(reflist))
print(len(doclist))
	
	

# fill snippet list
fill_snippet_list(snippetTitles)

# fill tag list
fill_tag_list(taglist["tags"])



root.mainloop()



