from django.contrib import admin
from kolkata.models import KolkataPost,KolkataBlogComment

# Register your models here.
admin.site.register((KolkataBlogComment))

@admin.register(KolkataPost)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js=('tinyinject.js',)