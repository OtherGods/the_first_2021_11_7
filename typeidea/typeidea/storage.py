from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadfile import InmemoryUploadeFile

from PIL import Image,ImageDraw,ImageFont

class WaterMarkStorage(FileSystemStorage):
	def save(self,name,content,max_length = None):
		if 'image' in content.content_type:
			#加水印
			image = self.watermark_with_text(content,'lxd6138.com','red')
			
			#把最终打上水印的图片对象Image转换为文件对象
			content = self.convert_image_to_file(image,name)
			
		return super().save(name,content,max_length = max_length)

	def convert_image_to_file(self,image,name):
		temp = BytesIO
		image.save(temp,format = 'PNG')
		file_size = temp.tell()
		return InMemoryUploadedFile(temp,None,name,'image/png',file_size,None)
	
	def watermark_with_text(self,file_obj,text,color,fontfamily = None):
		#打开我们传递的文件对象，将其转换为image对象，同时转换为RGB的格式。
		image = Image.open(file_obj).convert('RGBA')
		#准备向图片中画文字
		draw = ImageDraw.Draw(image)
		width,height = image.size
		margin = 10
		
		if fontfamily:
			font = ImageFont.truetype(fontfamily,int(height/20))
		else:
			font = None
		#计算要添加的文字宽度和高度
		textWidth,textHeight = draw.textsize(text,font)	
		#计算文字在图片中的位置
		x = (width - textWidth - margin) / 2		#计算横轴位置
		y = height - textHeight - margin		#计算纵轴位置
		#通过Pillow的ImageDraw向Image对象的指定位置上、画指定颜色、字体的文字
		draw.text((x,y),text,color,font)
		
		return image
		
