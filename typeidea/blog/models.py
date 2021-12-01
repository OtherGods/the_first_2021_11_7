#from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import mistune
#导入的这个cached_property的作用是帮我们把返回的数据绑定到实例上，不用每次访问都回去执行tags函数中的代码
from django.utils.functional import cached_property
from django.utils import timezone
import datetime

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
	
	#这个字段在数据库中保存的是增加文章页面中content_ck或cotent_md中的内容，如果是页面中显示的是content_ck那么这个
	#content中保存的是html形式的正文内容【也就是页面中显示的内容是被处理过的原始数据<可能是前端中处理的>】，如果页面
	#中显示的是content_md，那么这个content中保存的是原始的数据【没有被处理的】
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
	
	#这个自段用来统计某篇文章被访问了多少次【这个字段应该防止同一个用户在极短时间内多次刷同一篇文章的页面】
	pv = models.PositiveIntegerField(default = 1)
	#同一个用户一天内多次访问同一篇文章，那么这个uv字段只增加一次。
	uv = models.PositiveIntegerField(default = 1)
	
	#用来判断在xadmin中新增文章的时候使用的是markdown还是django-ckeditor
	is_md = models.BooleanField(default = True,verbose_name = 'markdown语法')

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
		'''
		如果用户在浏览器中是通过markdown形式增加Post的话那么context_html中保存的数据就是执行了mistune.markdown之后的
		形式的数据，如果用户在浏览器中是通过ckeditor形式编写的Post那么context_html中保存的数据就和context中的数据一致。
		'''
		if self.is_md:
			self.content_html = mistune.markdown(self.content)
		else:
			self.content_html = self.content
		super().save(*args,**kwargs)
		
	@cached_property
	def tags(self):
		"""
			这个方法是在书的9.6.2中添加的，在django的官方文档中说这个cached_property是用来缓存用的，
			将被这个装饰器装饰的方法的结果缓存起来。但是我还是第一次使用不太熟悉。
		"""
		return ','.join(self.tag.values_list('name',flat = True))


#将会被用来测试的类
class Question(models.Model):

	question_text = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('data published')

	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	










