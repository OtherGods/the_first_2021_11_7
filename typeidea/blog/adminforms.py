from django import forms

class PostAdminForm(forms.ModelForm):
	#这里是在自定义desc字段用来覆盖admin系统为我们的模型创建的ModelForm中的desc字段。
	desc = forms.CharField(widget = forms.Textarea,label = '摘要',required = False)


