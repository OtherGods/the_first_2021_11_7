from django import template

from comment.forms import CommentForm
from comment.models import Comment

register= template.Library()


@register.inclusion_tag('comment/block.html')
def comment_block(target):


	"""
		在需要使用评论的地方使用自定义的标签{% comment_block request.path %}
		这里的参数request.path就是传递给这个标签的tagret，这个url是展示某篇文章详情的url，所记就可以将评论和
		某篇文章相结合起来；当这个reqeust.path是友链的路径的时候，就可以将评论和友链页面连接起来【注意：这里是
		友链页面，不是对单铬友链，只是评论友链页面】
		这种方式可以代替blog/views.py中的PostDetailView类中的get_by_target方法。
	"""


	return {
		'target':target,
		'comment_form':CommentForm(),
		'comment_list':Comment.get_by_target(target),
	}


