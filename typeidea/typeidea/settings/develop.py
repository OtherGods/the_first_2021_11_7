from .base import *  #NOQA

DEBUG = True

DATABASES = {
	#'default': {
	#	'ENGINE': 'django.db.backends.sqlite3',
	#	'NAME': BASE_DIR / 'db.sqlite3',
	#},
	'default':{
		'ENGINE':'django.db.backends.mysql',
		'NAME':'typeidea_db_2',
		'USER':'root',
		'PASSWORD':'271441',
		'HOST':'127.0.0.1',
		'PORT':3306,
		'CONN_MAX_AGE':100,
		'OPTIONS':{'charset':'utf8mb4'},
		
		'TEST':{
			'NAME':'mytestdatabase',		#这是单元测试要用到的数据库
			'CHARSET':'UTF8',
			'COLLATION':'utf8_general_ci',
		},
	},
	
}

