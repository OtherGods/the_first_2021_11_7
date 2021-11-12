from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post,Category,Tag

from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


"""

在本系统中的admin.py中凡是继承了一个Modeldmin的类，都是想要对admin进一步的定制，比如下面的展示出模型类中的
什么字段，修改的时候展示什么字段，使用过滤器查找等等。

使用默认的行为的方式：     admin.site.register(模型类名)
使用自定制的行为的方式：   admin.site.register(模型类名，自定制的Modeldmin类的子类),或者使用下面的装饰器的形式。
"""


# Register your models here.

class PostInline(admin.TabularInline):
	"""
	对应于CategoryAdmin类中的inlines，但是会报错	
	"""
	fields = ('title','desc')
	extra = 1
	model = Post
	

#@admin.register(Category)
@admin.register(Category,site = custom_site)
class CategoryAdmin(BaseOwnerAdmin):
	
	#不知道为什么这里去掉注释就会报错，显示的错误和Post与Category类的外键有关	
	#官方文档中给出的例子也只是一个外键关系
	#inlines = [PostInline,]	
	
	list_display = ('name','status','is_nav','created_time','post_count')
	fields = ('name','status','is_nav')
	

	def post_count(self,obj):
		return obj.post_set.count()
	post_count.short_description = '文章数量'



#@admin.register(Tag)
@admin.register(Tag,site = custom_site)
class TagAdmin(admin.ModelAdmin):
	list_display = ('name','status','created_time')
	fields = ('name','status')

	

class CategoryOwnerField(admin.SimpleListFilter):
	"""自定义的过滤器只展示当前用户的分类"""
	title = '分类过滤器  根据不同的用户展示不同的分类'
	parameter_name = 'owner_category'
	
	def lookups(self,request,model_admin):
		"""
		    这里返回一个二维元组详细介绍看笔记
		    这里获取到的是当前登陆用户创建的分类，在	blog/Category模型类的定义中有User字段，所以在保存
		    分类的同时也保存了作者，所以不同的登陆用户看到的分类过滤器是不同的。		
		"""
		l = Category.objects.filter(owner = request.user).values_list('id','name')
		return l
		
	def queryset(self,request,queryset):
		category_id = self.value()
		print("************************",category_id)
		print('************************',queryset)
		if category_id:
			return queryset.filter(category = category_id)
		return queryset
	




#@admin.register(Post)
@admin.register(Post,site = custom_site)
class PostAdmin(BaseOwnerAdmin):
	#指向blog中的adminforms.py中为覆盖对desc字段的默认而设置的自定义的类，用来修改对desc字段的默认设置。
	form = PostAdminForm


	#在django企业实战开发一书中在下面的list_display列表中还有多对多子段，但是我实际编写后发现不能在里面
	#添加这个多对多字段，在印象笔记中也说到了。
	list_display = ['title','status','created_time','operator','owner']
	list_display_link = []
	
	
	#这里设置的两个过滤器第一个是无论当前登陆的用户是谁都会将Category类中存的每行记录展示出来，
	#第二个元素是按照当前登陆的用户来展示当前用户下设置的分类有哪些，这种方式才是合理的。
	list_filter = ['category',CategoryOwnerField]
	search_fields = ['title','category__name']

	actions_on_top = True
	actions_on_bottom = True

	save_on_top = True

	#fields = (
	#	('category','title'),
	#	'desc',
	#	'status',
	#	'content',
	#	'tag',
	#	)

	fieldsets = (

		('基础配置',{
			'description':'基础配置描述',
			'fields':(
				('title','category'),
				'status',			
			),	
		}),
		('内容',{
			'fields':(
				'desc',
				'content',			
			),	
		}),
		('额外信息',{
			'classes':('collapse',),
			'fields':('tag',),
		})

	)
#在django企业开发实战教材中的122页中说这样可以配置多对多字段，但是我没有试成功
#	filter_herizontal	= ('tag',)
	filter_vertical = ('tag',)

	def operator(self,obj):
		#将原来默认的站点修改之后在这里就需要重写
		#reverse("admin:blog_post_change",args = (obj.id,))	
		return format_html(
			'<a href="{}">编辑</a>',	
			reverse('cus_admin:blog_post_change',args = (obj.id,))		
		)

	operator.short_description = '操作'
	

	class Media:
		css = {
			'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),		
		}
		js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

@admin.register(LogEntry,site = custom_site)
class LogEntryAdmin(admin.ModelAdmin):
	list_display = ['object_repr','object_id','action_flag','user','change_message']







