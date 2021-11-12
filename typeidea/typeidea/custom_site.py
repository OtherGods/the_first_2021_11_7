from django.contrib.admin import AdminSite


#Djnago提供的admin.site模块实际上是django.contrib.admin.AdminSite类的一个实例
#所以我们可以自己定义一个site	？？？


#用自定义的行为设置自己的管理站点
class CustomSite(AdminSite):
	site_header = 'Typeidea'
	site_title = 'Typeidea管理后台'
	index_title = '首页'

#注意：这里在实例化CustomSite类的时候传递了一个name参数，当在业务层使用reverse反解这个站点的时候就会用到这个参数，
custom_site = CustomSite(name = 'cus_admin')
