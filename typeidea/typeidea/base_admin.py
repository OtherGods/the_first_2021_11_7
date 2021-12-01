'''
#这里注释掉导入和继承是因为使用xadmin的要求，并且xadmin不支持多个site的配值
from django.contrib import admin

class BaseOwnerAdmin(admin.ModelAdmin):

"""
	1、用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
	2、用来针对queryset过滤当前用户的数据
	"""
	exclude = ('owner',)
	

	def get_queryset(self,request):
		print("\r\n**************\r\n----------------\r\n++++++++++++\r\n//////////////\r\n")
		qs = super(BaseOwnerAdmin,self).get_queryset(request)
		return qs.filter(owner = request.user)


	def save_model(self,request,obj,form,change):
		"""
		保存用户在编辑页面中添加的数据的同时保存被添加的post是那个作者
		"""
		obj.owner = request.user
		return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)

'''
class BaseOwnerAdmin:
	"""
	1、用来自动补充文章、分类、标签、侧边栏、友链这些Model的owner字段
	2、用来针对queryset过滤当前用户的数据

	在xadmin中把上面两个方法的名字以及方法的参数做了修改，因为在xadmin中需要的参数传递的数据
	都可以通过self对象获得，比如说：self.request,self.new_obj,另外如果是修改数据可以通过self.org_obj来获得
	修改之前的数据对象。
	
	"""
	exclude = ('owner',)
	
	
	def get_list_queryset(self):	
		print('调用了get_list_queryset方法：-----------------------------------------------————————')	
		request = self.request
		qs = super().get_list_queryset()
		return qs.filter(owner = request.user)


	def save_models(self):
		print('调用了save_model方法：+++++++++++++++++++++++++++++++++++++')
		'''
		保存用户在编辑页面中添加的数据的同时保存被添加的post是那个作者
		'''
		self.new_obj.owner = self.request.user
		return super().save_models()



