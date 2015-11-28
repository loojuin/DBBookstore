from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Book
from .models import Customer

def index(request):
    return HttpResponse("Hello, world. You're at the bookstore index.")
# Create your views here.

def all_books(request):
	books = Book.objects.all()
	paginator = Paginator(books, 4)
	pagerange = paginator.page_range
	page = request.GET.get('page')
	try:
		booklist = paginator.page(page)
	except PageNotAnInteger:
		booklist = paginator.page(1)
	except EmptyPage:
		booklist = paginator.page(paginator.num_pages)

	template = loader.get_template('bookstore/index.html')
	context = RequestContext(request, {
		'booklist': booklist,
		'pagerange': pagerange,
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
	    errors = []
	    if 'pw' and 'userid' in request.GET:
	        userid=request.GET['userid']
	        pw = request.GET['pw']

	        if not userid:
	            errors.append('Enter a username.')

	        elif not pw: 
	            errors.append('Enter password.')

	        elif len(pw) > 20:
	            errors.append('Please enter at most 20 characters.')

	        else:
	            validuser = Customer.objects.filter(login_name=userid ,pwd=pw)
	            user=Customer.objects.filter(login_name=userid)
	            return render(request, 'bookstore/post_login.html', {'user':user,'validuser': validuser, 'query': userid})

	    return render(request, 'bookstore/login.html', {'errors': errors})

def register(request):
	template = loader.get_template('bookstore/register.html')
	context = None
	return HttpResponse(template.render(context))

