"""typeidea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path,path
from django.conf.urls import url
from blog import views
from typeidea.custom_site import custom_site

#from blog.views import post_list,post_detail
from config.views import links
#代替了上面的post_list,post_detail函数
from blog.views import IndexView,CategoryView,TagView,PostDetailView,SearchView,AuthorView
from config.views import LinkListView
from comment.views import CommentView
from blog.rss import LatestPostFeed
from blog.sitemap import PostSitemap
from django.contrib.sitemaps import views as sitemap_views
from django.views.generic import TemplateView
#xadmin
import xadmin
#django-autocomplete-light
from .autocomplete import CategoryAutocomplete,TagAutocomplete

#上传文件
from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static 


urlpatterns = [
	#url('super_admin/', admin.site.urls,name = 'super-admin'),
	#url('admin/', custom_site.urls,name = 'admin'),
	url('xadmin/', xadmin.site.urls,name = 'xadmin'),
	url('test1/', views.test1),

	url(r'^$', IndexView.as_view(),name = 'index'),
	url(r'^category/(?P<category_id>\d+)/$',CategoryView.as_view(),name = 'category-list'),
	url(r'^tag/(?P<tag_id>\d+)/$',TagView.as_view(),name = 'tag-list'),
	url(r'^post/(?P<post_id>\d+).html/$',PostDetailView.as_view(),name = 'post-detail'),
	url(r'^links/$',LinkListView.as_view(),name = 'links'),
	url(r'^search/$',SearchView.as_view(),name = 'search'),
	url(r'^author/(?P<owner_id>\d+)/$',AuthorView.as_view(),name = 'author'),
	url(r'^comment/$',CommentView.as_view(),name = 'comment'),
	#配置RSS 和 sitemap
	url(r'rss|feed/',LatestPostFeed(),name = 'rss'),
	url(r'^sitemap\.xml$',sitemap_views.sitemap,{'sitemaps':{'posts':PostSitemap}}),
	url(r'^test10/$',TemplateView.as_view(template_name = 'test10.html')),
	
	#配置django-autocomplete-light
	#re_path(r'^category-autocomplete/',CategoryAutocomplete.as_view(),name = 'category-autocomplete'),
	#re_path(r'^tag-autocomplete/',TagAutocomplete.as_view(),name = 'tag-autocomplete'),
	
	path('category-autocomplete/',CategoryAutocomplete.as_view(),name = 'category-autocomplete'),
	path('tag-autocomplete/',TagAutocomplete.as_view(),name = 'tag-autocomplete'),
	url(r'^ckeditor/',include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)













