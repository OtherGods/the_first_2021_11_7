from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
	'''
	django-rest-framework的作用等同于Django中的View+Form
	'''
	class Meta:
		model = Post
		fields = ['title','category','desc','content_html','created_time']
		
