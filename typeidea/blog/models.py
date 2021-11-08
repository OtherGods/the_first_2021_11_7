#from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),
		(STATUS_DELETE,'删除'),
	)
	name = models.CharField(max_length = 50,verbose_name = '名称')
	status = models.PositiveIntegerField(default = STATUS_NORMAL,choices = STATUS_ITEMS,verbose_name = '状态')
	is_nav = models.BooleanField(default = False,verbose_name = '是否为导航')

#	owner = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete = models.CASCADE)
	owner = models.ForeignKey(User,verbose_name = '作者',on_delete = models.CASCADE)
	created_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	class Meat:
		#这里是是设置模型对象的直观名称，用于在各种打印、页面展示等场景。
		verbose_name = verbose_name_plural = '分类'
	
class Tag(models.Model):
	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),	
		(STATUS_DELETE,'删除'),
	)
		
	name = models.CharField(max_length = 10,verbose_name = '名称')
	status = models.PositiveIntegerField(default = STATUS_NORMAL,choices = STATUS_ITEMS,verbose_name = '状态')
	
#	owner = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete = models.CASCADE)
	owner = models.ForeignKey(User,verbose_name = '作者',on_delete = models.CASCADE)
	
	created_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	
	class Meta:
		verbose_name = verbose_name_plural = '标签'
	
class Post(models.Model):
	STATUS_NORMAL = 1
	STATUS_DELETE = 0
	STATUS_DRAFT = 2
	STATUS_ITEMS = (
		(STATUS_NORMAL,'正常'),	
		(STATUS_DELETE,'删除'),
		(STATUS_DRAFT,'草稿'),
	)
	title = models.CharField(max_length = 255,verbose_name = '标题')
	desc = models.CharField(max_length = 1024,blank = True,verbose_name = '摘要')
	content = models.TextField(verbose_name = '正文',help_text = '正文必须为MarkDown的格式')
	status = models.PositiveIntegerField(default = STATUS_NORMAL,choices = STATUS_ITEMS,verbose_name = '状态')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

	category = models.ManyToManyField(Category,verbose_name = '分类')
	tag = models.ManyToManyField(Tag,verbose_name = '标签')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

#	owenr = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete = models.CASCADE)
	owenr = models.ForeignKey(User,verbose_name = '作者',on_delete = models.CASCADE)
	
	created_name = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	
	class Meta:
		verbose_name = verbose_name_plural = '文章'
		ordering = ['-id'] 	#根据id进行降序排列
	


























