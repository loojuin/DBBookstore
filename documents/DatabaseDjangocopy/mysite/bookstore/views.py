from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Book
from .models import Customer
from .models import Opinion
from .models import Rate
from .models import Ord
from .models import Cart


from django.db.models import Sum

import datetime
def search_bar(request,type,query_input):
	if type=='Book_title':
		Book.objects.filter(title__contains=query_input).values()
	elif type=='Author':
		Book.objects.filter(author__contains=query_input).values()
	elif type=='Publisher':
		Book.objects.filter(pubisher__contains=query_input).values()
	elif type=='Subject':
		Book.objects.filter(subject__contains=query_input).values()
	elif type=='Isbn':
		Book.objects.filter(isbn__contains=query_input).values()
	else:
		pass




def view_search(request, authors_input,publisher_input,title_input,subject_input,isbn_input,sorted_year,sorted_score):
	"""
	TODO:
	Users may search for books, by asking conjunctive
	queries on the authors, and/or publisher, and/or title, and/or subject. 
	Your system should allow the user to specify that the results are to be 
	sorted a) by year, or b) by the average score of the feedbacks.
	"""
	"""
	average score of feedback
	conjunctive function
	multiple authors
	isbn & book
	"""

	"""
	if title given --> isbn
	"""
	isbn_title=list(Book.objects.filter(title=title_input).values('isbn'))



	search_publisher=list(Book.objects.filter(publisher=publisher_input).values())
	search_author=list(Book.objects.filter(author=authors_input).values())
	search_title=list(Book.objects.filter(title=title_input).values())
	search_isbn=list(Book.objects.filter(isbn=isbn_input).values())
	search_subject=list(Book.objects.filter(sbj=subject_input).values())
	average_score=Opinion.objects.filter(book=isbn_input).aggregate(Avg('score'))

	"""
	this lines below should suffice
	dynamic input Eg, if type 'Ste' , authors such as Stephen Hawking & Stephen King will appear
	"""
	results=Book.objects.filter(author__contains=authors_input,publisher__contains=publisher_input , title__contains=title_input,subject__contains=subject_input,isbn__contains=isbn_input).values()
	output_results=list(results)
	if sorted_year==True:
		sorted_year_results=list(results.order_by('-yr'))
	elif sorted_score==True:
		feedback_isbn=results.values('isbn')
		for i in feedback_isbn:
			sorted_score=Opinion.objects.filter(book=i['isbn']).aggregate(Avg('score'))
	else:
		return results

	# template = loader.get_template('bookstore/profile.html')
	# context = RequestContext(request, {
	# 	'profile' : profile, 
	# 	'orders': orders,
	# 	'feedbacks': feedbacks,
	# 	})

	# return HttpResponse(template.render(context))

def useful_feedbacks(request, number_of_comments):
	"""
	TODO: 
	For a given book, a user could ask for the top n most useful feedbacks.
 	The value of n is user-specified (say, 5, or 10). The usefulness of a 
	feedback is its average usefulness score.
	"""
	pass

def add_book(request, book_id):
	customer = Customer.objects.get(login_name=request.user.username)
	book = Book.objects.get(isbn = book_id)
	qty = request.POST["qty"]
	price = book.price * float(qty)
	Cart(customer=customer, book=book, qty=qty, price=price).save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def remove_book(request, book_id):
	item = Cart.objects.get(book = book_id)
	item.delete()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def view_cart(request):
	cart_items = Cart.objects.filter(customer=request.user.username)
	total_price = cart_items.aggregate(Sum('price'))


	template = loader.get_template('bookstore/cart.html')
	context = RequestContext(request, {
		'cart_items' : cart_items,
		'total_price': total_price
	})
	return HttpResponse(template.render(context))


# Working on it: Loo Juin
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


# Working on it: Loo Juin
#
# Shows a page displaying the:
# - m most popular books (in terms of copies sold in this month)
# - m most popular authors
# - m most popular publishers
def show_statistics(request):
	m = 10

	def pop_books(ordbooks):
		counts = {}
		for ordbook in ordbooks:
			try:
				counts[ordbook.book.isbn] += ordbook.qty
			except KeyError:
				counts[ordbook.book.isbn] = ordbook.qty
		ranks = [(c, counts[c]) for c in counts.keys()]
		ranks = sorted(ranks, key = lambda entry: entry[1], reverse = True)
		if len(ranks) <= m:
			return ranks
		else:
			return ranks[0:m]

	def pop_authors(ordbooks):
		counts = {}
		for ordbook in ordbooks:
			try:
				counts[ordbook.book.author] += ordbook.qty
			except KeyError:
				counts[ordbook.book.author] = ordbook.qty
		ranks = [(c, counts[c]) for c in counts.keys()]
		ranks = sorted(ranks, key = lambda entry: entry[1], reverse = True)
		if len(ranks) <= m:
			return ranks
		else:
			return ranks[0:m]

	def pop_publishers(ordbooks):
		counts = {}
		for ordbook in ordbooks:
			try:
				counts[ordbook.book.publisher] += ordbook.qty
			except KeyError:
				counts[ordbook.book.publisher] = ordbook.qty
		ranks = [(c, counts[c]) for c in counts.keys()]
		ranks = sorted(ranks, key = lambda entry: entry[1], reverse = True)
		if len(ranks) <= m:
			return ranks
		else:
			return ranks[0:m]

	now = datetime.datetime.now()
	books = OrdBook.objects.filter(oid__timestmp__year = now.year) #.filter(oid__timestmp__month = now.month)

	pop_books = pop_books(books)
	pop_authors = pop_authors(books)
	pop_publishers = pop_publishers(books)

	template = loader.get_template('bookstore/stats.html')
	context = RequestContext(request, {
		"pop_books": pop_books,
		"pop_authors": pop_authors,
		"pop_publishers": pop_publishers
	})
	return HttpResponse(template.render(context))


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
	book_in_cart = Cart.objects.filter(book = book_id).exists()

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
		'user_comment': user_comment,
		'in_cart': book_in_cart,
		})
	return HttpResponse(template.render(context))

def user_record(request,user_name):
	profile=Customer.objects.get(login_name=user_name)
	orders=list(Ord.objects.filter(customer=user_name))
	feedbacks=list(Opinion.objects.filter(customer=user_name))
	feedback_books = []
	

	template = loader.get_template('bookstore/profile.html')
	context = RequestContext(request, {
		'profile' : profile, 
		'orders': orders,
		'feedbacks': feedbacks,
		})

	return HttpResponse(template.render(context))

def view_orders(request):
	template = loader.get_template('bookstore/orders.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))

def add_comment(request, book_id):
	if request.method == "POST":
		if request.user.is_authenticated():
			text = request.POST["comment"]
			rating = request.POST["rating"]
			book = Book.objects.get(isbn = book_id)
			cus = Customer.objects.get(login_name=request.user.username)
			c = Opinion.objects.filter(book=book, customer=cus)
			if len(c)==0:
				Opinion(book=book, txt=text, score=rating, customer=cus).save()
				print "comment saved"
		else: 
			"""
			TODO: 
			if user is not authenticated, there should be a page saying: 
			please login to comment on the book
			"""
			pass

	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def rate_comment(request, book_id, username):
	comment_author = username
	if request.method == "POST":
		if request.user.is_authenticated():
			rating = request.POST["rating"]			
			if comment_author != request.user.username:
				cus = Customer.objects.filter(login_name=comment_author)[0]
				rater = Customer.objects.filter(login_name=request.user.username)[0]
				b = Book.objects.filter(isbn=book_id)
				op = Opinion.objects.filter(book = b, customer=cus)[0]
				old_rating = Rate.objects.filter(rater=rater, opinion=op)
				if len(old_rating) == 0:
					newrating = Rate(rater=rater, opinion=op, rating=rating)
					newrating.save()
					print "new rating saved! "+ rating   
					"""
					TODO:
					notify the user the rating is successful/unsuccessful
					Don't think this is graded though
					"""
			else:
				print "don't rate your own comments!"
		else:
			print "user is not logged in!"
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	

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

