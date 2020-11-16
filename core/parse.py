import yaml
yaml.warnings({'YAMLLoadWarning':False})

def get_yaml(yaml_file):
	#初始化
	HD = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
		   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
	cookies = {}
	data = ""

	# 打开yaml文件
	file = open(yaml_file, 'r', encoding="utf-8")
	file_data = file.read()
	file.close()

	# 将字符串转化为字典或列表
	raw_data = yaml.load(file_data)

	#处理name
	yaml_name = raw_data['name']

	if yaml_name.split("-")[-1] != "md5":
		#处理cookie
		if raw_data['Cookie'] != "" and raw_data['Cookie'] != {""} and raw_data['Cookie'] != {"":""}:
			if ";" in raw_data['Cookie']:
				for q in raw_data['Cookie'].split(";"):
					c1 = q.split("=")[0]
					c2 = q.split("=")[1]
					cookies[c1] = c2
			else:
				c1 = raw_data['Cookie'].split("=")[0]
				c2 = raw_data['Cookie'].split("=")[1]
				cookies[c1] = c2


		#处理Header
		if raw_data['Header'] != "" and raw_data['Header'] != {""} and raw_data['Header'] != {"":""}:
			HD.update(raw_data['Header'])

		#处理redirects
		if raw_data['follow_redirects'] == True:
			fRe = True
		else:
			fRe = False
		
		#处理path
		paths = raw_data['path']

		#处理method
		Method = raw_data['method'].lower()

		#处理expression
		if "\n" in raw_data['expression']:
			expression = raw_data['expression'].split("\n")[0]
		else:
			expression = raw_data['expression']

		#处理data
		if raw_data['method'].lower() == "post":
			try:
				data = raw_data['data']
			except:
				pass
		
		md5 = []
		md5_path = []
	
	elif yaml_name.split("-")[-1] == "md5":
		md5_path = raw_data['md5_path']
		md5 = raw_data['md5']
		fRe = False
		Method = "get"
		paths = ""
		expression = ""

	return yaml_name,cookies,HD,fRe,paths,Method,expression,data,md5_path,md5
