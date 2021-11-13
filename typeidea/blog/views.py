from django.shortcuts import render,HttpResponse
from .models import Tag,Post,Category
from config.models import SideBar
from django.views.generic import DetailView
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin


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



class CommonViewMixin(ContextMixin):
#class CommonViewMixin:
	"""
		获取通用数据，例如导航栏、侧边栏、底部导航。
	"""
	def get_context_data(self,**kwargs):
		"""
			A default context mixin that passes the keyword arguments received by
			get_context_data() as the template context.
			在书中这个类没有继承自ContextMixin，但是如果没有继承自这个类的话下面的super是怎么来的？

					
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
	paginate_by = 5
	context_object_name = 'post_list'
	template_name = 'blog/list.html'


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#这里是分类列表页对应的类和标签列表页对应的类
class CategoryView(IndexView):
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		category_id = self.kwargs.get('category_id')
		category = get_object_or_404(Category,pk = category_id)
		context.update({
			'category':category,
		})
		return context
	def get_queryset(self):
		"""
			重写queryset，根据分类过滤
		"""
		queryset = super().get_queryset()
		category_id = self.kwargs.get('category_id')	#这里的kwargs不知道哪里来的
		print('********************************',queryset.filter(category = category_id),'****************')
		print("************************打印self.kwargs：",self.kwargs)
		return queryset.filter(category = category_id)
	
class TagView(IndexView):
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



class PostDetailView(CommonViewMixin,DetailView):
	"""
		替代上面的post_detail函数
		这个类的作用是用来展示一片文章的具体内容的，所以不需要继承那么多的东西。
	"""
	queryset = Post.latest_posts()
	template_name = 'blog/detail.html'
	context_objects_name = 'post'
	pk_url_kwarg = 'post_id'




	





