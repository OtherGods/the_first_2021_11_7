from django.shortcuts import redirect
from django.views.generic import TemplateView
from .forms import CommentForm
from comment.models import Comment

# Create your views here.


class CommentView(TemplateView):
	http_method_name = ['post']
	template_name = 'comment/result.html'
	
	def post(self,request,*args,**kwargs):
		comment_form = CommentForm(request.POST)
		target = request.POST.get('target')
		
		if comment_form.is_valid():
			instance = comment_form.save(commit = False)
			instance.target = target		
			#虽然模型类中的target字段没有在页面中展示出来，但是在页面中的url就对应着模型类中的target字段

			instance.save()
			succeed = True
			return redirect(target)	
		else:
			succeed = False
		context = {
			'succeed':succeed,
			'form':comment_form,
			'target':target,
		}
		return self.render_to_response(context)
		





