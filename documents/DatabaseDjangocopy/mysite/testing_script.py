from bookstore.models import Opinion, Book

print Book.objects.all()[0].title
book_id = Book.objects.all()[0]
comment = Opinion.objects.filter(book=book_id).order_by("-score")

print comment[0].score, comment[0].txt
print comment[1].score, comment[1].txt
