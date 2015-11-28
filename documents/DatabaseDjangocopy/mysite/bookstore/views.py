from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Book

def index(request):
    return HttpResponse("Hello, world. You're at the bookstore index.")
# Create your views here.

def all_books(request):
	booklist = Book.objects.all()
	template = loader.get_template('bookstore/index.html')
	context = RequestContext(request, {
		'booklist': booklist,
		})
	return HttpResponse(template.render(context))

def book(request, book_id):
	book = Book.objects.get(isbn = book_id)
	template = loader.get_template('bookstore/book.html')
	context = RequestContext(request, {
		'book' : book,
		})
	return HttpResponse(template.render(context))

def login(request):
	template = loader.get_template('bookstore/login.html')
	context = None
	return HttpResponse(template.render(context))