from django.shortcuts import render, redirect
from markdown2 import Markdown
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse 
from django.contrib import messages
from random import randint

from . import util

wiki_entries = "entries/"

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    if entry not in util.list_entries():
        raise Http404()

    content = util.get_entry(entry)
    return render(request, "encyclopedia/wiki.html", {
        "title": entry,
        "content": Markdown().convert(content)
    })

def search(request):
    query = request.GET['q']
    if util.get_entry(query):
        return HttpResponseRedirect(reverse("wiki", args=(query,)))
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": [entry for entry in util.list_entries() if query.lower() in entry.lower()],
            "title": f'"{query}"' ,
            "heading": f'Results for "{query}"'
        })

def new_entry(request):
    return render(request, "encyclopedia/new.html", {
        'edit': False,
        'edit_page_title': '',
        'edit_page_contents': ''
    })

def save_entry(request, title=None):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse("index"))
    else:
        assert (request.method == 'POST')
        entry_content = request.POST['entry-content']
        if not title:
            title = request.POST['title']
            if title.lower() in [entry.lower() for entry in util.list_entries()]:
                return render(request, "encyclopedia/index.html", {
                    "heading": f'"{title}" already exist',
                })
                
        
        filename = wiki_entries + title + ".md"
        with open(filename, "w") as f:
            f.write(entry_content)
        return HttpResponseRedirect(reverse("wiki", args=(title,)))

def edit_entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        return HttpResponseRedirect(reverse("index"))

    return render(request, "encyclopedia/new.html", {
        'edit': True,
        'edit_entry_title': title,
        'edit_entry_content': entry_content
    })

def random_entry(request):
    entries = util.list_entries()
    entry = entries[randint(0, len(entries) - 1)]
    return redirect("wiki", entry)