from django.contrib import admin
from .models import Profile, Book, Message, Cart, Wishlist, Transaction, Rating, Reported

# Register your models here.
admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Message)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Transaction)
admin.site.register(Rating)
admin.site.register(Reported)