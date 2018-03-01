from django.contrib import admin
from .models import Article, Victor
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    # 规定在每条数据详细页面显示的内容
    fieldsets = [
        ('标题', {'fields': ['title']}),
        ('作者', {'fields': ['author']}),
        ('内容', {'fields': ['context']}),
    ]
    # 规定在预览数据库页面显示的内容
    list_display = ('title', 'author', 'pub_date')


class VictorAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'sex', 'user_email')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Victor, VictorAdmin)
