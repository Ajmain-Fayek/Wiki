from django.shortcuts import render
import markdown
from . import util
import random


# Defining fuction to convert mark-down content into HTML content.
def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)


# Defining fuction about index.html
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Defining function about enrty.html
def entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html",{
            "massage": "The page you are looking for does not exist."
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })
    

# Defining function to execute search.
def search(request):
    if request.method == "POST":
        titleSearch = request.POST['q']
        ifContentExist = convert_md_to_html(titleSearch)
        if ifContentExist is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": titleSearch,
                "content": ifContentExist
            })
        else:
            allEntries = util.list_entries()
            recomendation = []
            for entry in allEntries:
                if titleSearch.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recomendation": recomendation
            })
        

# Defining function for Creating new page.
def createNewPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/createNewPage.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html",{
                "massage": "The page you would like to add is already exist."
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content": html_content
        })


# Defining function for edit page.
def editPage(request):
    if request.method == 'POST':
        title = request.POST['titleEntry']
        content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html",{
            "title": title,
            "content": content
        })
    
# Defining function for Saving Edits.
def saveEdit(request): 
        if request.method == 'POST':
            title = request.POST['editedTitle']
            content = request.POST['editedContent']
            util.save_entry(title, content)
            html_edited_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html",{
                "title": title,
                "content": html_edited_content
            })



# Defining Random Choice function
def randomPage(request):
    everyEntries = util.list_entries()
    randomEntry = random.choice(everyEntries)
    htmlContent = convert_md_to_html(randomEntry)
    return render(request, "encyclopedia/entry.html",{
        "title": randomEntry,
        "content": htmlContent
    })