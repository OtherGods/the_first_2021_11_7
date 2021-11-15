from django.shortcuts import render,HttpResponse
from django.views.generic import ListView
from blog.views import CommonViewMixin
from .models import Link

# Create your views here.

def links(request):
	return HttpResponse('links')


#这个类是用来作友链的
class LinkListView(CommonViewMixin,ListView):
	queryset = Link.objects.filter(status = Link.STATUS_NORMAL)
	template_name = 'config/links.html'
	context_object_name = 'link_list'
	
