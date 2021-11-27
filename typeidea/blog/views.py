from django.shortcuts import render,HttpResponse
from .models import Tag,Post,Category
from config.models import SideBar
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin
from django.db.models import Q,F
from comment.forms import CommentForm
from comment.models import Comment
from datetime import date
from django.core.cache import cache

# Create your views here.


def test1(request):
	import sys

	print("******打印路径*********:",sys.path)
	return HttpResponse('OK')

'''
def post_list(request,category_id = None,tag_id = None):

	tag = None
	category = None
	if tag_id:
		post_list,tag = Post.get_by_tag(tag_id)
	elif category_id:
		post_list,category = Post.get_by_category(category_id)
	else:
		post_list = Post.latest_posts()
	context = {
		'category':category,
		'tag':tag,
		'post_list':post_list,
		'sidebars':SideBar.get_all()
	}
	context.update(Category.get_navs())
	return render(request,'blog/list.html',context = context)
'''	


'''	
def post_detail(request,post_id):
	"""	
	return render(request,'blog/detail.html',context = {'name':'post_detail'})
	"""

	try:
		post = Post.objects.get(id = post_id)
	except Post.DoesNotExist:
		post = NOne
	context = {
		'post':post,
		'sidebars':SideBar.get_all(),
	}
	context.update(Category.get_navs())
	return render(request,'blog/detail.html',context = context)
'''


class CommonViewMixin:
	"""
		获取通用数据，例如导航栏、侧边栏、底部导航。
	"""
	def get_context_data(self,**kwargs):
		"""
			A default context mixin that passes the keyword arguments received by
			get_context_data() as the template context.
			这个类没有继承一个父类，但是这个类的子类的另一个父类有
			get_context_data方法，所以这个方法实际上是执行这个类的子类的另一个父类的get_context_data方法
		"""
		context = super().get_context_data(**kwargs)
		context.update({
			'sidebars':SideBar.get_all(),
		})
		context.update(Category.get_navs())
		return context


class IndexView(CommonViewMixin,ListView):
	"""
		这是首页内容的类，继承了上面获取通用数据的类。
	"""
	queryset = Post.latest_posts()  #这里得到的是所有的文章
	paginate_by = 1
	context_object_name = 'post_list'
	template_name = 'blog/list.html'


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#这里是分类列表页对应的类和标签列表页对应的类
class CategoryView(IndexView):
	'''
	这个类覆盖了父类IndexView中的数据源queryset【get_queryset方法】以及_context_data方法。
	在Indexew类中展示的是所有的文章列表，但是在这个类中是展示用户在url中输入的分类对应的文章列表
	'''
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		category_id = self.kwargs.get('category_id')
		category = get_object_or_404(Category,pk = category_id)
		context.update({
			'category':category,
		})
		#这个context中封装了好多数据，包括分页，polt_list等等，但是不知道在那里使用了这个context
		return context
	def get_queryset(self):
		"""
			重写queryset，根据分类过滤
		"""
		queryset = super().get_queryset()
		category_id = self.kwargs.get('category_id')
		return queryset.filter(category = category_id)
	
class TagView(IndexView):
	'''
	这个类覆盖了父类IndexView中的数据源queryset【get_queryset方法】以及_context_data方法。
	在Indexew类中展示的是所有的文章列表，但是在这个类中是展示用户在url中输入的标签对应的文章列表
	'''
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		tag_id = self.kwargs.get('tag_id')
		tag = get_object_or_404(Tag,pk = tag_id)
		context.update({
			'tag':tag,
		})
		return context
	
	def get_queryset(self):
		"""重写queryset，根据标签过滤"""
		queryset = super().get_queryset()
		tag_id = self.kwargs.get('tag_id')
		return queryset.filter(tag__id = tag_id)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#这里是搜索功能对应的类

class SearchView(IndexView):
	'''
	注意：这里是继承自IndexView类，这个IndexView类会展示所有的文章，但是由于这里是搜索文章，所以就需要修改数据源
	，这里的这个SearchView类的用法和上面按照标签和分类展示文章的类的租用一样，都是通过修改数据源，并且修改上下文
	来操作展示给用户的数据有哪些。	  
	'''

	def get_context_data(self,**kwargs):
		context = super().get_context_data()
		context.update({
			'keyword':self.request.GET.get('keyword','')
		})
		return context
		
	def get_queryset(self):
		"""
			这里的查询功能是按照title和desc查询的
		"""
		queryset = super().get_queryset()
		keyword = self.request.GET.get('keyword')
		if not keyword:
			return queryset
		return queryset.filter(Q(title__icontains = keyword) | Q(desc__icontains = keyword))


class AuthorView(IndexView):
	def get_queryset(self):
		queryset = super().get_queryset()
		author_id = self.kwargs.get('owner_id')
		return queryset.filter(owner_id = author_id)


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#这个类的作用使用来展示文章详情的
class PostDetailView(CommonViewMixin,DetailView):
	"""
		这个类的作用是用来展示一片文章的具体内容以及文章的评论
	"""

	queryset = Post.latest_posts()
	template_name = 'blog/detail.html'
	context_objects_name = 'post'
	pk_url_kwarg = 'post_id'			#这个post_id对应与urls.py中的url(r'^post/(?P<post_id>\d+).html/$',..)
							#post_id;
							#这个属性的作用是设置在DetailView源码的父类的get_object方法中
							#用到的：pk = self.kwargs.get(self.pk_url_kwarg)，
							#【这里的self.kwargs是在View类中的setup方法中设置的，
							#这里的self.kwargs对应的值是用户在浏览器中输入的url中的关键字参数
							#也就是对应在urls.py中的urlpatterns中的url第一个参数为
							#r'^post/(?P<post_id>\d+).html/$'  中的关键字参数post_id和
							#用户在浏览器中输入的参数匹配的字典】，pk得到的值就是kwargs字典中
							#键post_id对应值.



	'''
	#由于添加评论的时候直接象下面这样写耦合性太高，所以要把获取评论的内容以及提交评论的表但抽象出来作为一个插件随插随用
	#所以注释掉这里，重新写了一个自定义的标签，在这个自定义的标签中获取评论内容，和提交评论的表单。自定义标签在
	#comment包下的templatetags中。

	#这个方法的作用是用来将某篇文章对应的评论添加到上下文context中，但是之后优化了代码，将获取评论的方式
	#转换成一个标签，随用随插，这样就可以即在文章详情的时候展示评论，也可以在展示友情链接的时候展示评论
	#【虽然我还不知道这个友情链接是干什么用的】
	def get_context_data(self,**kwargs):
		"""
			这个方法我在源码中看到大部分都是在get方法中调用的【用来获取上下文】
			这里是为了给上下文对应的字典中添加评论相关的内容
		"""
		context = super().get_context_data(**kwargs)	#在源码中这个方法还会去调用父类【在现在这种情况
										#下源码该方法所在类的父类是ContextMixin】中
										#的get_context_data方法
		context.update({
			'comment_form':CommentForm,	
			#都没有实例化就直接使用,居然也能得到一个空的form表单

			'comment_list':Comment.get_by_target(self.request.path),
			#因为是在文章详情也面上展示评论的，选取评论的时候可以根据文章的id进行选取，而文章的id在页面所在的url
			#也就是可以通过request.path获得。
		})
		return context
	'''

	'''
	#这种方式是用来作统计用的，每当有用户访问某篇文章的时候，就会给该文章的pv、uv增加1，但是这种方式不好，在django企
	#业开发实战中说过原因，用下面的get方法代替它
	def get(self,request,*args,**kwargs):
		response = super().get(request,*args,**kwargs)
		Post.objects.filter(pk = self.object.id).update(pv = F('pv')+1,uv = F('uv')+1)
		
		#调试用
		from django.db import connection
		print(connection.queries)
		return response
	'''		
	def get(self,request,*args,**kwargs):
		response = super().get(request,*args,**kwargs)	
		self.handle_visited()
		return response

	def handle_visited(self):
		"""
			user_id.py文件中的UserIDMiddleware类中的__call__方法是给客户端设置cookie，也就是让cookie
			【这个保存在客户端浏览器中的cookie是uid】保存在客户端的浏览器上，而这里是把根据uid而生成的一些值
			保存在服务端的缓存中，并且设置了时间；
			每当用户查看某篇文章的详情的时候，会向服务端发送一个请求，在首先进入web应用的中间件中，在中间件
			中判断用户发送来的request中的cookies中是否有uid这个键，如果没有的话，那么该用户就是第一次访问
			这篇文章，会给这个用户生成一个uid【并且在最后返回response的时候将这个uid保存到cookie中】，将这
			个uid存到request中，按着中间件的流程往下执行，一直到这里【视图类中】，在这里会将uid包装一下，
			分别保存在pv_key和uv_key中，之后将这两个变量保存在缓存中，并设置保存时间，目的是防止某个用户【
			假设这个用户是用户A，访问的是文章 P】打开文章详情页面后一直刷新从而产生没有意义的文章被访问次
			数，只有当服务的缓存中没有了这个包装了uid的pv_key和uv_key之后A用户访问文章P才可以被认为是正常
			的文章被访问次数。
		"""
		increase_pv = False
		increase_uv = False
		uid = self.request.uid
		pv_key = 'pv:%s:%s'%(uid,self.request.path)
		uv_key = 'uv:%s:%s:%s'%(uid,str(date.today()),self.request.path)
		print('++++++++++++++++++++++++++%s---%s+++++++++++++++++++++++++++++'%(pv_key,uv_key))
		if not cache.get(pv_key):
			increase_pv = True
			cache.set(pv_key,1,1*60)  #1分钟有效
		if not cache.get(uv_key):
			increase_uv = True
			cache.set(uv_key,1,24*60*60)  #24小时有效
		print('++++++++++++++++++++++++++%s---%s+++++++++++++++++++++++++++++'%(increase_pv,increase_uv))
		if increase_pv and increase_uv:
			#在下面用到的self.object包含的是该视图正在操作的对象【可以去看源码，它的值是由于
			#SingleObjectMixin父类中的get_object方法返回的】
			Post.objects.filter(pk = self.object.id).update(pv = F('pv')+1,
						uv = F('uv')+1)
		elif increase_pv:
			Post.objects.filter(pk = self.object.id).update(pv = F('pv')+1)
		elif increase_uv:
			Post.obejcts.filter(pk = self.object.id).update(uv = F('uv')+1)
















