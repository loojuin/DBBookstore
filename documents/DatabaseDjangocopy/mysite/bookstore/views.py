from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login

from .models import Book
from .models import Customer
from .models import Opinion

user = None
def index(request):
	return HttpResponse("Hello, world. You're at the bookstore index.")

def all_books(request):
	books = Book.objects.all()
	paginator = Paginator(books, 8)
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
	comment = Opinion.objects.filter(book=book).order_by("-score")[:3]

	template = loader.get_template('bookstore/book.html')
	if request.user.is_authenticated():
		cus = Customer.objects.get(login_name=request.user.username)
		c = Opinion.objects.filter(book=book, customer=cus)
		user_comment = c[0] if len(c)!=0 else None
		print user_comment

	context = RequestContext(request, {
		'book' : book, 
		'comments':comment,
		'user': user,
		'user_comment': user_comment
		})
	return HttpResponse(template.render(context))

def add_comment(request, book_id):
	if request.method == "POST":
		if request.user.is_authenticated():
			text = request.POST["comment"]
			book = Book.objects.get(isbn = book_id)
			cus = Customer.objects.get(login_name=request.user.username)
			c = Opinion.objects.filter(book=book, customer=cus)
			if len(c)==0:
				Opinion(book=book, txt=text, score=0, customer=cus).save()
				print "comment saved"
		else: 
			"""
			TODO: 
			if user is not authenticated, there should be a page saying: 
			please login to comment on the book
			"""
			pass

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def rate_comment(request, book_id, commenter):
	"""
	TODO
	1. check if authenticated
	2. check if it's user's own comment
	3. check if user has rated this comment already
	4. save rating in 
	"""
	if request.method == "POST":
		pass

def view_login(request):
	errors = []
	userid = request.POST.get("userid", False)
	pw = request.POST.get("pw", False)
	user = authenticate(username=userid, password=pw)
	if user is not None:
		if user.is_active:
			print "login"
			login(request, user)
			template = loader.get_template('bookstore/post_login.html')
			context = RequestContext(request, {'query': userid, 'validuser': user})
			return HttpResponse(template.render(context))
	else: 
		template = loader.get_template('bookstore/login.html')
		context = RequestContext(request, {'errors': errors})
		return HttpResponse(template.render(context))


def logout(request):
	"""
	TODO: someone finish this please
	logout button are already inside the templates
	"""

def register(request):
	"""
	TODO: 
	1. create new User element(username password)
	2. create new Customer 
	"""
	template = loader.get_template('bookstore/register.html')
	context = None
	return HttpResponse(template.render(context))

