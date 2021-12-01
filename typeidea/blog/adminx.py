from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post,Category,Tag,Question

from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry
#这里的导入是xadmin要求的
import xadmin
from xadmin.layout import Row,Fieldset,Container
from xadmin.filters import manager
from xadmin.filters import RelatedFieldListFilter

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
	#在使用xadmin的时候当要处理inline的时候和admin的逻辑不太一直，需要通过form_layout来控制要展示的内容
	#，不过修改起来不复杂，只需要把fields修改为form_layout即可
	
	form_layout = (
		Container(
			Row('title','desc')
		)
	)
	extra = 1
	model = Post

	

#@admin.register(Category)
#这里是要使用自定义的站点
#@admin.register(Category,site = custom_site)
#这里是在xadmin中不能使用多个站点
@xadmin.sites.register(Category)
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
#这里是要使用自定义的站点
#@admin.register(Tag,site = custom_site)
@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerAdmin):
	list_display = ('name','status','created_time')
	fields = ('name','status')

"""	
#这里被注释掉的是django中admin中中自定义过滤类，由于要使用xadmin的原因
class CategoryOwnerField(admin.SimpleListFilter):
	'''自定义的过滤器只展示当前用户的分类'''
	title = '分类过滤器  根据不同的用户展示不同的分类'		#用来标识 标题 ，这个标题就是在页面中显示的过滤器的名字
	parameter_name = 'owner_category'		#这个是查询时url参数的名字；比如查询id为1的内容url后面的Query
								#部分是  ？owner_category=1
	
	def lookups(self,request,model_admin):
		'''
		    这里返回一个二维元组详细介绍看笔记
		    这里获取到的是当前登陆用户创建的分类，在	blog/Category模型类的定义中有User字段，所以在保存
		    分类的同时也保存了作者，所以不同的登陆用户看到的分类过滤器是不同的。		
		'''
		l = Category.objects.filter(owner = request.user).values_list('id','name')
		return l
		
	def queryset(self,request,queryset):
		'''
		根据url Query 的内容返回列表页数据，比如如果URL最后的QUery是 ?owner_category=1，那么这里拿
		到的self.value()就是1，此时会根据1来过滤 queryset ，这里的queryset是列表页所有战士数据的合集及post
		的数据集
		'''
		category_id = self.value()
		print("************************",category_id)
		print('************************',queryset)
		if category_id:
			return queryset.filter(category = category_id)
		return queryset
	
"""
#这是对xadmin配置的自定义过滤器,跟之前的admin中的自定义的过滤器的作用一样。
class CategoryOwnerField(RelatedFieldListFilter):
	@classmethod
	def test(cls,field,request,params,model,admin_view,field_path):
		'''
		这个方法的作用是确认字段是否需要被当前的过滤器处理。
		'''
		return field.name == 'category'
		
	def __init__(self,field,request,params,model,model_admin,field_path):
		super().__init__(field,request,params,model,model_admin,field_path)
		#重新获取lookup_choices，根据owner过滤,这个lookup_choices默认情况下【也就是在父类中】是查询所有的数据
		self.lookup_choices = Category.objects.filter(owner = request.user).values_list('id','name')
#把我们自定义的过滤器注册到管理器中，并且设置优先权，这样才会在页面加在的时候使用我们定义的这个过滤器。
manager.register(CategoryOwnerField,take_priority = True)
	



#@admin.register(Post)
#这里是要使用自定义的站点
#@admin.register(Post,site = custom_site)
@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerAdmin):
	#指向blog中的adminforms.py中为覆盖对desc字段的默认而设置的自定义的类，用来修改对desc字段的默认设置。
	form = PostAdminForm


	#在django企业实战开发一书中在下面的list_display列表中还有多对多子段，但是我实际编写后发现不能在里面
	#添加这个多对多字段，在印象笔记中也说到了。
	list_display = ['title','status','created_time','operator','owner']
	list_display_links = []
	
	
	#这里设置的两个过滤器第一个是无论当前登陆的用户是谁都会将Category类中存的每行记录展示出来，
	#第二个元素是按照当前登陆的用户来展示当前用户下设置的分类有哪些，这种方式才是合理的。
	#list_filter = ['category',CategoryOwnerField]
	#这里注释掉admin中定义的过滤器用的列表，把自定义的过滤器从list_filter中去掉了;这里不是自定义的filter类而是字段名。
	list_filter = ['category']
	
	search_fields = ['title','category__name']

	actions_on_top = True
	actions_on_bottom = True

	save_on_top = True
	'''
	#注释掉这里是因为xadmin的需要
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
			#'classes':('collapse',),	#不知道这里发生了什么事情，在页面中点击展开之后连‘展开’这两
							#个子都没有了，把这个classes家在基础配置中也是同样的结果，不知所以
			'classes':('wide'),	#这里的代码是在django企业开发实战书中写的【我忘记它是在那里配置的】
			'fields':('tag',),
		}),

	)
	'''

	form_layout = (
		Fieldset(
			'基础信息',
			Row('title','category'),
			'status',
			'tag',
		),
		Fieldset(
			'内容信息',
			'desc',
			'is_md',			
			'content_ck',
			'content_md',
			'content',
		),
	)
	
	

#在django企业开发实战教材中的122页中说这样可以配置多对多字段，但是我没有试成功
#	filter_herizontal	= ('tag',)
	filter_vertical = ('tag',)

	def operator(self,obj):
		'''
		这个方法的作用是在展示文章列表页面中添加一个链接用来提供调转到编辑页面的链接
		
		参数obj的作用：这个参数是固定的，就是当前行对象，列表页中的每一行数据都对应数据表中的一条数据，也对
		应Model的一个实例
		
		'''
		#将原来默认的站点修改之后在这里就需要重写
		#reverse("admin:blog_post_change",args = (obj.id,))
		print('==================================%s========================'%type(obj))
		print('==================================%s========================'%obj)	
		return format_html(
			'<a href="{}">编辑</a>',	
			#这里是对admin的配置在xadmin中要被注释掉
			#reverse('cus_admin:blog_post_change',args = (obj.id,))
			reverse('xadmin:blog_post_change',args = (obj.id,))		
		)

	operator.short_description = '操作'	


	#xadmin使用的是django.forms.widget.Media这个对象,Django中定义
	#的admin会自动转为django.forms.widgets.Media对象
	class Media:
		css = {
			'all':("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),		
		}
		js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)	
	
	
#这里是要使用自定义的站点
#@admin.register(LogEntry,site = custom_site)
#@xadmin.sites.register(LogEntry)
#class LogEntryAdmin(object):
#	list_display = ['object_repr','object_id','action_flag','user','change_message']
#xadmin中自带了日志功能，所以把我们的日记代码注释掉就可以了。



#这里是要使用自定义的站点
#@admin.register(Question,site = custom_site)
@xadmin.sites.register(Question)
class QuestionAdmin(object):
	fields = ['question_text','pub_date',]
	list_display = ['question_text','pub_date',]




