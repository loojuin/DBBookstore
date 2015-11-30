from django.contrib import admin

# Register your models here.
from .models import Book
from .models import Customer

class BookAdmin(admin.ModelAdmin):
	
	list_display = ('title', 'author', 'isbn')

class CusAdmin(admin.ModelAdmin):
	list_display = ('login_name', 'given_name')

admin.site.register(Book, BookAdmin)
admin.site.register(Customer, CusAdmin)