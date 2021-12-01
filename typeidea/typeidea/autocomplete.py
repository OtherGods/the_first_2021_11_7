#有这个模块的原因是在增加一片文章的时候，如果分类【category】所在的表中的数据过多的话，在打开增加文章的页面的时候就会花费很长
#时间，因为在打开这个增加文章的页面的时候要一次性的把所有的分类【这个分类是文章所在的表的外键】加载到页面中，生成一个select标签，
#但是这个select标签只有用户在选择分类的时候才会用到，所以可以把加载分类的时间放到用户选择分类的时候而不是把加载分类的时间放在
#显示增加文章页面的时间中。
#这个模块的作用是解决上面说道的问题；配置所需要的自动补全接口，可以把这个模块理解为自动补全View层

#同时这个模块中的代码还可以解决作者在增加文章的时候看见别人创建的分类和标签的问题

from dal import autocomplete
from blog.models import Category,Tag

class CategoryAutocomplete(autocomplete.Select2QuerySetView):

	def get_queryset(self):
		'''
		这里的这个方法是用来处理数据源的
		'''	
		if not self.request.user.is_authenticated:  #这里的self.request.user是在中间件中被设置的，如果服务端
									 #中没有检索到user，那么就返回一个匿名用户【AnonymousUser】。
			return Category.objects.none()
		qs = Category.objects.filter(owner = self.request.user).order_by('name')

		if self.q:#书中书这个self.q的值是url参数上传递过来的值
			#这里的self.q是在dal包中相关的源码中设置的。
			qs = qs.filter(name__istartswith = self.q)
		return qs

class TagAutocomplete(autocomplete.Select2QuerySetView):
	
	def get_queryset(self):
		'''
		这里的这个方法是用来处理数据源的
		'''	
		if not self.request.user.is_authenticated:
			return Tag.objects.none()
		qs = Tag.objects.filter(owner = self.request.user).order_by('name')

		if self.q:	#书中书这个self.q的值是url参数上传递过来的值
			qs = qs.filter(name__istartswith = self.q)
		return qs

