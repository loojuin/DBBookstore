from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import Book
from .models import Customer

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

def register(request):
	template = loader.get_template('bookstore/register.html')
	context = None
	return HttpResponse(template.render(context))

def functionlog(request):
    errors = []
    if 'r' and 'q' in request.GET:
        q=request.GET['q']
        r = request.GET['r']
        if not q:
            errors.append('Enter a username.')
        elif not r: 
            errors.append('Enter password.')
        elif len(r) > 20:
            errors.append('Please enter at most 20 characters.')
        else:

            validuser = Customer.objects.filter(login_name=q ,pwd=r)
            user=Customer.objects.filter(login_name=q)
            return render(request, 'bookstore/login_results.html',
                {'user':user,'validuser': validuser, 'query': q})
    return render(request, 'bookstore/login_form.html',
        {'errors': errors})