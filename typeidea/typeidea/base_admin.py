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
		'''
		保存用户在编辑页面中添加的数据的同时保存被添加的post是那个作者
		'''
		obj.owner = request.user
		return super(BaseOwnerAdmin,self).save_model(request,obj,form,change)



