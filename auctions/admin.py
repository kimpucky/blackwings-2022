from django.contrib import admin
from .models import *



# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)

@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    ordering = ('-user',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'comment')
    ordering = ('-listing','-commentdate',)