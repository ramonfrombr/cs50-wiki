from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django import forms
from markdown2 import Markdown
from random import randrange
from . import util

markdowner = Markdown()

class SearchPageForm(forms.Form):
    q = forms.CharField(label="Search")

class NewPageForm(forms.Form):
    page_title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        'form': SearchPageForm(),
        "entries": util.list_entries()
    })

def page(request, page):

    page_content = util.get_entry(page)

    if page_content:
        page_content = markdowner.convert(util.get_entry(page))
        return render(request, "encyclopedia/page.html", {'form': SearchPageForm(), 'page': page,'page_content': page_content})
    else:
        return render(request, "encyclopedia/404.html", {'form': SearchPageForm()})

def search(request):
    if request.method == 'POST':

        form = SearchPageForm(request.POST)

        if form.is_valid():
            
            page_content = util.get_entry(form.cleaned_data['q'])

            if page_content:
                return HttpResponseRedirect(reverse('page', args=[form.cleaned_data['q']]))
            else:
                possible_pages = [page for page in util.list_entries() if form.cleaned_data['q'] in page]

                return render(request, "encyclopedia/search.html", {'form': SearchPageForm(), 'possible_pages': possible_pages})

def new_page(request):

    if request.method == 'POST':

        form = NewPageForm(request.POST)

        if form.is_valid():

            util.get_entry(form.cleaned_data['page_title'])

            util.save_entry()

            if form.cleaned_data['page_title'] in util.list_entries():
                return HttpResponseRedirect(reverse("not_allowed"))
            else:
                util.save_entry(form.cleaned_data['page_title'], form.cleaned_data['content'])

                return HttpResponseRedirect(reverse("page", args=form.cleaned_data['page_title']))
            

    return render(request, 'encyclopedia/new_page.html', {'form': SearchPageForm(),'new_page_form': NewPageForm})


def edit_page(request, page):

    if request.method == 'POST':

        form = EditPageForm(request.POST)

        if form.is_valid():

            util.save_entry(page, form.cleaned_data['content'])

            return HttpResponseRedirect(reverse("page", args=page))
    
    default_data = {'content': util.get_entry(page)}

    form = EditPageForm(default_data)

    return render(request, 'encyclopedia/edit_page.html', {'edit_page_form': form, 'page': page})


def random_page(request):

    random_index = randrange(len(util.list_entries()))

    random_page = util.list_entries()[random_index]

    return HttpResponseRedirect(reverse("page", args=[random_page]))


def not_allowed(request):
    return render(request, 'encyclopedia/403.html')