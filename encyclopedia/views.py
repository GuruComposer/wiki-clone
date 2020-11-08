from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from markdown2 import Markdown
from django.urls import reverse
import random

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if not entry == None:
        markdowner = Markdown()
        transformed = markdowner.convert(entry)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "entry": transformed
        })
    else:
        return render(request, "encyclopedia/no_entry_exists.html", {
            "title": title     
        })

def search(request):
    if request.method == "GET":
        query = request.GET.get('q')
        query = query.lower()
        matches = []
        for item in util.list_entries():
            lowerItem = item.lower()
            if query == lowerItem or query in lowerItem and item not in matches:
                matches.append(item)

        return render(request, "encyclopedia/search.html", {
            "query": query,
            "matches": matches
        })

def create(request):
    if request.method =="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"].capitalize()
            content = form.cleaned_data["content"]
            if(util.get_entry(title) is None or form.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("title", kwargs={"title": title}))
            else:
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "exisiting": True,
                    "title": title
                })
        else:
            return render(request, "encyclopedia/create.html", {
            "form": form,
            "existing": False
            })
    else:
        return render(request,"encyclopedia/create.html", {
            "form": NewEntryForm(),
            "existing": False
        })   


def edit(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/no_entry_exists.html", {
            "title": title
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entry
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "title": form.fields["title"].initial
        })

def randomPage(request):
    randomPage = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", kwargs={'title': randomPage}))