#from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import mistune

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

	class Meta:
		#这里是是设置模型对象的直观名称，用于在各种打印、页面展示等场景。
		verbose_name = '分类'
	
	def __str__(self):
		return self.name

	@classmethod
	def get_navs(cls):
		categories = cls.objects.filter(status = cls.STATUS_NORMAL)	
		nav_categories = []
		normal_categories = []
		for cate in categories:
			if cate.is_nav:
				nav_categories.append(cate)
			else:
				normal_categories.append(cate)
		return {
			'nav_categories':nav_categories,
			'categories':normal_categories,
		}

	
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

	def __str__(self):
		return self.name


	
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
	#用来存储makedown处理后的正文内容
	content_html = models.TextField(verbose_name = '正文html代码',blank = True,editable = False)	
	
	status = models.PositiveIntegerField(default = STATUS_NORMAL,choices = STATUS_ITEMS,verbose_name = '状态')

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

	category = models.ManyToManyField(Category,verbose_name = '分类')
	tag = models.ManyToManyField(Tag,verbose_name = '标签')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------


#	owner = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name = '作者',on_delete = models.CASCADE)
	owner = models.ForeignKey(User,verbose_name = '作者',on_delete = models.CASCADE)
	
	created_time = models.DateTimeField(auto_now_add = True,verbose_name = '创建时间')
	
	#这两个字段用来处理文章的访问量。【至于为什么用两个字段来处理我就不太清楚了】
	pv = models.PositiveIntegerField(default = 1)
	uv = models.PositiveIntegerField(default = 1)
	

	class Meta:
		verbose_name = verbose_name_plural = '文章'
		ordering = ['-id'] 	#根据id进行降序排列
	

	def __str__(self):
		return self.title

	
	@staticmethod
	def get_by_tag(tag_id):
		try:
			tag = Tag.objects.get(id = tag_id)
		except Tag.DoesNotExist:
			tag = None
			post_list = []
		else:
			post_list = tag.post_set.filter(status = Post.STATUS_NORMAL)\
				.prefetch_related('owner','category')
		return post_list,tag
	
	@staticmethod
	def get_by_category(category_id):
		try:
			category = Category.objects.get(id = category_id)
		except Category.DoesNotExist:
			category = None
			post_list = []
		else:
			post_list = category.post_set.filter(status = Post.STATUS_NORMAL)\
				.prefetch_related('owner','category')
		
		return post_list,category
	
	@classmethod
	def latest_posts(cls):
		queryset = cls.objects.filter(status = cls.STATUS_NORMAL)
		return queryset
		
	@classmethod
	def hot_posts(cls):
		return cls.objects.filter(status = cls.STATUS_NORMAL).order_by('-pv')


	def save(self,*args,**kwargs):
		self.content_html = mistune.markdown(self.content)
		super().save(*args,**kwargs)














