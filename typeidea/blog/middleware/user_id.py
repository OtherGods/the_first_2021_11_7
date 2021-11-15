import uuid

USER_KEY = 'uid'
TEN_YEARS = 60*60*24*365*10

class UserIDMiddleware:
	def __init__(self,get_response):
		self.get_response = get_response
	def __call__(self,request):
		uid = self.generate_uid(request)
		request.uid = uid
		print('在请求的时候已经给请求生成了一个uid。。。。。。。。。。。。。：',uid,'***********')

		response = self.get_response(request)
		
		response.set_cookie(USER_KEY,uid,max_age = TEN_YEARS,httponly = True)
		print('在返回响应的时候给响应设置了cookies，键是字符串’uid值’对是uid对应的值')

		return response
	def generate_uid(self,request):
		try:
			"""前面已经给客户端的cookie设置了时间，只要没有超过时间，客户端发送的请求都会包含这个cookie
				所以，在这个try内只要用户发送来的请求中包含cookie，就不会报错，只是把request中的
				cookie读到内存中并且赋值给uid。
			"""    
			print('打印缓存中的cookies******************',request.COOKIES)
			uid = request.COOKIES[USER_KEY]
		except KeyError:
			uid = uuid.uuid4().hex
		return uid
		
