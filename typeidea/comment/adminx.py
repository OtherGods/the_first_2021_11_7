from django.contrib import admin

from .models import Comment

import xadmin
# Register your models here.


#@admin.register(Comment)
#class CommentAdmin(admin.ModelAdmin):
#xadmin需要的配置
@xadmin.sites.register(Comment)
class CommentAdmin:
	list_display = ('target','nickname','content','website','created_time')





















