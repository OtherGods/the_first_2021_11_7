from dal import autocomplete
from django import forms
#为了想要实现使用amrkdown形式编写内容而导入
#from ckeditor.widgets import CKEditorWidget
#为了想要实现使用amrkdown形式编写内容并且能上传图片而导入
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import Category,Tag,Post

class PostAdminForm(forms.ModelForm):
	#这里是在自定义desc字段用来覆盖admin系统为我们的模型创建的ModelForm中的desc字段。
	desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
	
	'''
	#这里配置的会报错，在页面中显示en.js:2 Uncaught TypeError: Cannot read property 'define' of undefined
	#我认为这是离我比较远的东西，所以注释了
	#接下来配置的是djnago-autocomplete-light，使用django-autocomplete-light提供的form层的组建来帮助我们更好的接
	#入后段的接口
	category = forms.ModelChoiceField(
		queryset=Category.objects.all(),
		widget=autocomplete.ModelSelect2(url='category-autocomplete'),
		label='分类',
	)
	tag = forms.ModelMultipleChoiceField(
		queryset=Tag.objects.all(),
		widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
		label='标签',
	)
	class Meta:
		model = Post
		fields = ('category','tag','title','desc','content','status')
	
	'''
	
	#这是配置ckeditor
	#这个content已经是经过处理后的HTML代码,同时还能够上传图片,相当于下面的content_ck
	#content = forms.CharField(widget = CKEditorUploadingWidget(),label = '正文',required = True)
	
	#content_ck和content_md是需要按照条件展示在页面中的，而content是在页面中隐藏的，是用来接受最终编辑内容的。
	#这个展示的条件是通过js来判断的。
	content_ck = forms.CharField(widget = CKEditorUploadingWidget(),label = '正文',required = False)
	content_md = forms.CharField(widget = forms.Textarea(),label = '正文',required = False)
	content = forms.CharField(widget = forms.HiddenInput(),required = False)
	
	class Meta:
		model = Post
		fields = (
			'category','tag','desc','title',
			'is_md','content','content_md','content_ck',
			'status'
		)

	def __init__(self,instance = None,initial = None,**kwargs):
		'''
			参数instance是某个模型类的实例
			参数initial是form表单中各个字段的初始值，也就是
			通过重新构造函数来设置initial，初始值会随着instance实例中的is_md参数变化而变化;
			因为在修改文章的时候需要把文章原来的内容展示出来【至于怎么使用数据库中的数据展示出来我就不知道了
			我在源码中没有找到对initial的详细设置】，但是文章所在的类Post中没有定义context_md和context_ck
			所需需要在initial中增加context_ck/content_md【通过instance类中的is_md字段来判断在initial中增加
			那个键值对】
		'''
		initial = initial or {}
		print('打印：/*-+/*-++-*/*-+--*/*********************************   initial：',initial)
		if instance:
			if instance.is_md:
				initial['content_md'] = instance.content
			else:
				initial['content_ck'] = instance.content
		super().__init__(instance = instance,initial = initial,**kwargs)

	def clean(self):
		is_md = self.cleaned_data.get('is_md')
		if is_md:
			content_field_name = 'content_md'
		else:
			content_field_name = 'content_ck'
		#把增加博客页面中展示出来的content_md或content_ck从cleaned_data中拿出来放到content中
		#因为在post所在的类中并没有定义这两个字段，他们只是用来展示在页面中；但是真正保存的是在Post类中
		#的context_html和context，所以需要把增加Post页面中展示出来的字段重赋值给context用来保存。
		content = self.cleaned_data.get(content_field_name)
		#如果用户在浏览器中的增加文章页面中使用的是makdown形式增加文章的话，那么在这里拿到的context就是用户在浏
		#览器中输入的原始数据的形式，，如果用户在浏览器中增加文章页面中使用的是另一种形式的话，那么这里拿到的context
		#就是html形式的【不是纯数据，而是包含标签的数据】
		
		if not content:
			self.add_error(content_field_name,'必填项！')
			return
		#向干净的数据中添加content，因为最后要使用instance.save来保存form表单中对应的model实例到数据库中
		self.cleaned_data['content'] = content
		return super().clean()
	class Media:
		js = ('js/post_editor.js',)	#这是自定义的js文件。
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
