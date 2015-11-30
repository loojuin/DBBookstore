from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Book
from .models import Customer
from .models import Opinion
from .models import Ord
from .models import OrdBook

def view_search(request):
	"""
	TODO:
	Users may search for books, by asking conjunctive
	queries on the authors, and/or publisher, and/or title, and/or subject. 
	Your system should allow the user to specify that the results are to be 
	sorted a) by year, or b) by the average score of the feedbacks.
	"""
	pass

def useful_feedbacks(request, number_of_comments):
	"""
	TODO: 
	For a given book, a user could ask for the top n most useful feedbacks.
 	The value of n is user-specified (say, 5, or 10). The usefulness of a 
	feedback is its average usefulness score.
	"""
	pass

def order_book(request):
	"""
	TODO:
	add a book order to shopping cart without a checkout
	"""
	pass

def view_cart(request):
	template = loader.get_template('bookstore/cart.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def recommendation(request):
	"""
	TODO:
	Book recommendation: Like most e-commerce websites, when a user orders a 
	copy of book A, your system should give a list of other suggested books. 
	Book  B is suggested, if there exist a user  X that bought both  A and  B. 
	The suggested books should be sorted on decreasing sales count (i.e., most 
		popular first); count only sales to users like  X (i.e. the users who bought both  A and  B).
	"""
	pass

def show_statistics(request):
	"""
	TODO:
	the list of the m most popular books (in terms of copies sold in this month)
	the list of m most popular authors
	the list of m most popular publishers
	"""
	pass

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
	user_comment = None
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

def user_record(request,user_name):
	profile=Customer.objects.get(login_name=user_name)
	orders=list(Ord.objects.filter(customer=user_name).values())
	feedbacks=list(Opinion.objects.filter(customer=user_name).values())

	template = loader.get_template('bookstore/profile.html')
	context = RequestContext(request, {
		'profile' : profile, 
		'orders': orders,
		'feedbacks': feedbacks,
		})

	return HttpResponse(template.render(context))

def user_record_2(request,user_name):
	if request.user.is_authenticated():
		surname=Customer.objects.filter(login_name=user_name).values().first()['surname']
		given_name=Customer.objects.filter(login_name=user_name).values().first()['given_name']
		address=Customer.objects.filter(login_name=user_name).values().first()['address']
		credit_card=Customer.objects.filter(login_name=user_name).values().first()['credit_card']
		phoneno=Customer.objects.filter(login_name=user_name).values().first()['phoneno']
		number_of_ords=len(list(Ord.objects.filter(customer=user_name).values()))
		for i in range(number_of_ords):
			oid_value=list(Ord.objects.filter(customer=user_name).values())[i]['oid']
			status=list(Ord.objects.filter(customer=user_name).values())[i]['stat']
			time_stamp=list(Ord.objects.filter(customer=user_name).values())[i]['timestmp']
			isbn_value=OrdBook.objects.filter(oid=oid_value).values().first()['book_id']
			qty=OrdBook.objects.filter(oid=oid_value).values().first()['qty']
			book_name=Book.objects.filter(isbn=isbn_value).values().first()['title']
			book_author=Book.objects.filter(isbn=isbn_value).values().first()['author']
			book_publisher=book_name=Book.objects.filter(isbn=isbn_value).values().first()['publisher']
			book_desc=book_name=Book.objects.filter(isbn=isbn_value).values().first()['desc']
		number_of_feedbacks=len(Opinion.objects.filter(customer=user_name).values())
		for i in range(number_of_feedbacks):
			book_name_feedback_isbn=list(Opinion.objects.filter(customer=user_name).values())[i]['book_id']
			book_name_feedback=Book.objects.filter(isbn=book_name_feedback_isbn).values().first()['title']
			score=list(Opinion.objects.filter(customer=user_name).values())[i]['score']
			txt=list(Opinion.objects.filter(customer=user_name).values())[i]['txt']	
			
			template = loader.get_template('bookstore/post_login.html')
			context = RequestContext(request, {'query': userid, 'validuser': user})
			return HttpResponse(template.render(context))
	else: 
		template = loader.get_template('bookstore/login.html')
		context = RequestContext(request, {'errors': errors})
		return HttpResponse(template.render(context))

def view_orders(request):
	template = loader.get_template('bookstore/orders.html')
	context = RequestContext(request, {})
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


def view_logout(request):
	"""
	TODO: someone finish this please
	logout button are already inside the templates
	"""
	if request.user.is_authenticated():
		logout(request)
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def register(request):
	if request.method == "POST":
		
		username = request.POST["username"]
		password = request.POST["password"]
		first = request.POST["firstname"]
		last = request.POST["lastname"]
		addr = request.POST["address"]
		phone = request.POST["phone"]
		credit = request.POST["credit"] 

		User.objects.create_user(username=username, password=password).save()
		Customer(login_name=username, 
		given_name=first,
		surname=last,
		pwd=password, phoneno=phone, credit_card=credit,
		address=addr).save()
		#saved successfully, redirect to log in page
		
		template = loader.get_template('bookstore/login.html')
		context = RequestContext(request, {'errors': []})
		return HttpResponse(template.render(context))

	template = loader.get_template('bookstore/register.html')
	context = None
	return render(request, 'bookstore/register.html')
	#return HttpResponse(template.render(context))

