from django import forms
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import util
import markdown2
import random

class NewSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class NewEditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data["search"]
            site = util.get_entry(f"{input}")
            if site == None:
                return render(request, "encyclopedia/search_results.html", {
                    "entries": util.list_entries(),
                    "query": input,
                    "form": NewSearchForm()
                })
            else:
                return HttpResponseRedirect(reverse("site", kwargs={'entry': input}))
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries(),
                "form": form
            })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": NewSearchForm()
        })

def site(request, entry):
    if util.get_entry(f"{entry}") == None:
        return render(request, "encyclopedia/error.html", {
            "site": entry,
            "form": NewSearchForm()
        })
    else:
        return render(request, "encyclopedia/site.html", {
            "title": entry,
            "site": markdown2.markdown(util.get_entry(f"{entry}")),
            "form": NewSearchForm()
        })

def new(request):
    if request.method == "POST":
        page_form = NewPageForm(request.POST)
        if page_form.is_valid():
            title = page_form.cleaned_data["title"]
            content = page_form.cleaned_data["content"]
            if util.get_entry(title) == None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("site", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/new_page_error.html", {
                    "site": title.lower(),
                    "form": NewSearchForm()
                })
        else:
            return render(request, "encyclopedia/new_page.html", {
                "page_form": page_form,
                "form": NewSearchForm()
            })
    else:
        return render(request, "encyclopedia/new_page.html", {
            "page_form": NewPageForm(),
            "form": NewSearchForm()
        })

def edit(request, title):
    if request.method == "POST":
        edit_form = NewEditForm(request.POST)
        if edit_form.is_valid():
            content = edit_form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("site", kwargs={'entry': title}))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "edit_form": edit_form,
                "form": NewSearchForm()
            })
    else:
        content = util.get_entry(f"{title}")
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "edit_form": NewEditForm(initial={'content': content}),
            "form": NewSearchForm()
        })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return  HttpResponseRedirect(reverse("site", kwargs={'entry': title}))
