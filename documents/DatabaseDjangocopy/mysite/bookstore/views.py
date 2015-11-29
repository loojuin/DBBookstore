from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login

from .models import Book
from .models import Customer
from .models import Opinion

def index(request):
	return HttpResponse("Hello, world. You're at the bookstore index.")
# Create your views here.

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
	print comment[0].customer.login_name
	context = RequestContext(request, {
		'book' : book, 
		'comments':comment
		})
	return HttpResponse(template.render(context))

def add_comment(request, book_id):
	if request.method == "POST":
		text = request.POST["comment"]
		book = Book.objects.get(isbn = book_id)
		cus = Customer.objects.all()[11]
		Opinion(book=book, txt=text, score=0, customer=cus).save()
		print text
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def rate_comment(request, book_id, commenter):
	if request.method == "POST":
		pass

def view_login(request):
	errors = []
	userid = request.POST.get("userid", False)
	pw = request.POST.get("pw", False)
	print userid
	print pw
	user = authenticate(username=userid, password=pw)
	if user is not None:
		print user
		if user.is_active:
			print "login"
			login(request, user)
			template = loader.get_template('bookstore/post_login.html')
			context = RequestContext(request, {'query': userid})
			return HttpResponse(template.render(context))
	else: 
		template = loader.get_template('bookstore/login.html')
		context = RequestContext(request, {'errors': errors})
		return HttpResponse(template.render(context))

	"""

		if 'pw' and 'userid' in request.GET:
				userid=request.GET['userid']
				pw = request.GET['pw']
				print userid 
				print pw

				if not userid:
						errors.append('Enter a username.')

				elif not pw: 
						errors.append('Enter password.')

				elif len(pw) > 20:
						errors.append('Please enter at most 20 characters.')

				else:
					user = authenticate(username=userid, password=pw)
				if user is not None:
					print "login"
						if user.is_active:

					login(request, user)
					print "lanalana"
						#validuser = Customer.objects.filter(login_name=userid ,pwd=pw)
						#user=Customer.objects.filter(login_name=userid)
					return render(request, 'bookstore/post_login.html', {'query': userid})
	"""


def register(request):
	template = loader.get_template('bookstore/register.html')
	context = None
	return HttpResponse(template.render(context))

