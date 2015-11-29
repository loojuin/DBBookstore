from bookstore.models import Opinion, Book, Customer

customer = [2,3,4,5,6,7,8,9,10,11]
scores = [23, 9, 12, 2, 3, 19, 30, 0, 12, 5]
text = ["an invaluable resource … takes the reader step by step…",
		"among the best … refreshing in its specificity", 
		"relentlessly logical … fresh and forceful", 
		"a wealth of great advice… clear, succinct, robust … compact and accessible",
		"I recommend to anyone with an ambition to succeed",
		"Pretty mediocre, I could have written it myself",
		"Painstakingly average. My son throw up all over it",
		"Kinda hard to read",
		"inspiring, engaging and very useful… different and refreshing… excellent and I thoroughly recommend it to anyone",
		"This is the best book I've ever read"
		]

for c in customer:
	book1 = Book.objects.all()[1]
	cus = Customer.objects.all()[c]
	o = Opinion(book=book1, customer=cus, score=scores[c-2], txt=text[c-2])
