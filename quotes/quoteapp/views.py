from datetime import datetime
from threading import Thread
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from django.conf import settings
from .forms import TagForm, QuoteForm, AuthorForm
from .models import Tag, Author, Quote
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from . import scraping_ as sc

# Create your views here.

QUOTES_COUNT = 5


def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, QUOTES_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/index.html', {'quotes': quotes, "page_obj": page_obj})


def find_quotes_by_tag(request, tag_id):
    quotes = Quote.objects.filter(tags=tag_id).all()
    paginator = Paginator(quotes, QUOTES_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/index.html', {'quotes': quotes, 'filter': Tag.objects.filter(id=tag_id).first(), "page_obj": page_obj})


def find_quotes_by_user(request, user_id):
    quotes = Quote.objects.filter(user=user_id).all()
    paginator = Paginator(quotes, QUOTES_COUNT)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'quoteapp/index.html', {'quotes': quotes, 'filter': User.objects.filter(id=user_id).first(), "page_obj": page_obj})


@login_required
def user_quotes(request):
    quotes = Quote.objects.filter(user=request.user).all()
    return render(request, 'quoteapp/user_quote.html', {'quotes': quotes})


@login_required
def tag(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quoteapp/tag.html', {'form': form, 'tags': tags})
        else:
            return render(request, 'quoteapp/tag.html', {'form': form, 'tags': tags})

    return render(request, 'quoteapp/tag.html', {'form': TagForm(), 'tags': tags})


@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)

            choice_author = Author.objects.filter(fullname__in=request.POST.getlist('authors')).first()
            new_quote.author = choice_author
            new_quote.save()
            new_quote.user = request.user
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag_ in choice_tags.iterator():
                new_quote.tags.add(tag_)
            new_quote.save()
            return redirect(to='quoteapp:userquote')
        else:
            errors = ('Invalid data',)
            return render(request, 'quoteapp/add_quote.html',
                          {"tags": tags, "authors": authors, 'form': form, 'errors': errors})

    return render(request, 'quoteapp/add_quote.html', {"tags": tags, "authors": authors, 'form': QuoteForm()})


@login_required
def quote_edit(request, quote_id):
    tags = Tag.objects.all()
    authors = Author.objects.all()
    db_quote = Quote.objects.filter(pk=quote_id).first()

    if request.method == 'POST':
        new_quote = request.POST.get('quote')
        new_author = Author.objects.filter(fullname__in=request.POST.getlist('authors')).first()
        new_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
        quote = Quote.objects.filter(pk=quote_id, user=request.user)
        quote.update(quote=new_quote, author=new_author)

        quote = Quote.objects.get(id=quote_id, user=request.user)
        quote.tags.clear()
        for tag_ in new_tags.iterator():
            quote.tags.add(tag_)

        return redirect(to='quoteapp:userquote')
    return render(request, 'quoteapp/edit_quote.html',
                  {"tags": tags, "authors": authors, 'form': QuoteForm(initial={'quote': db_quote.quote}),
                   'quote': db_quote})


@login_required
def quote_delete(request, quote_id):
    quote = Quote.objects.filter(pk=quote_id, user=request.user)
    quote.delete()
    return redirect(to='quoteapp:userquote')


@login_required
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quoteapp:main')
        else:
            errors = ('Invalid or exist data',)
            return render(request, 'quoteapp/author.html', {'form': form, 'errors': errors})

    return render(request, 'quoteapp/author.html', {'form': AuthorForm()})


def author_detail(request, author_id):
    author_ = get_object_or_404(Author, pk=author_id)
    return render(request, 'quoteapp/author_view.html', {"author": author_})


def scrap(request):
    for url_ in sc.get_urls():
        sc.spider(url_)
    sc.quoters
    sc.authors
    print('All done!')
    for author_ in sc.authors:
        try:
            author_born_date = datetime.strptime(author_['born_date'], '%B %d, %Y')
            db_author = Author(fullname=author_['fullname'],
                               born_location=author_['born_location'],
                               born_date=author_born_date,
                               description=author_['description'],
                               )
            db_author.save()
        except:
            pass

    for quote_ in sc.quoters:
        tags = quote_['tags']
        for tag_ in tags:
            try:
                db_tag = Tag(name=tag_)
                db_tag.save()
            except:
                pass
            try:
                db_quote = Quote(quote=quote_['quote'],
                                 author=Author.objects.filter(fullname=quote_['author']).first()
                                 )
                db_quote.save()
                choice_tags = Tag.objects.filter(name__in=tags)
                for tag_iterator in choice_tags.iterator():
                    db_quote.tags.add(tag_iterator)
                db_quote.save()
            except:
                pass

    print('Data was scrapped and added to data base!')

@login_required
def add_via_scrapping(request, ):
    th = Thread(target=scrap, args=(request,))
    th.start()
    return render(request, 'quoteapp/scrapping.html', {})
