from bookstore.models import Customer

users = ["Yuna", "Nalia", "Diana", "Bojack", "Carolyn", "Taub", "Peanutbutter", "Vincent", "Owl", "Amy"]
p = 123456
credit = 1234123423452345

for user in users:
	p += 1
	credit += 1
	c = Customer(login_name=user, given_name=user, surname=user+"ski", pwd="password"+user, 
			phoneno = p, credit_card = credit, address = "Changi South Ave 1"
			)
	c.save()

print len(Customer.objects.all())

