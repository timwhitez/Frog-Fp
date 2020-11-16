import yaml
import requests
import os
yaml.warnings({'YAMLLoadWarning':False})


def get_yaml(yaml_file):
	# 打开yaml文件
	file = open(yaml_file, 'r', encoding="utf-8")
	file_data = file.read()
	file.close()

	# 将字符串转化为字典或列表
	raw_data = yaml.load(file_data)

	#处理name
	if type(raw_data['name']) == str:
		if raw_data['name'].split("-")[0] == "fp":
			if raw_data['name'].split("-")[-1] == "get" or raw_data['name'].split("-")[-1] == "post" or raw_data['name'].split("-")[-1] == "md5":
				pass
			else:
				print(yaml_file,"name字段格式错误")
		else:
			print(yaml_file,"name字段格式错误")
	else:
		print(yaml_file,"name字段格式错误")


	if raw_data['name'].split("-")[-1] != "md5":
		#处理cookie
		if raw_data['Cookie'] != "" and raw_data['Cookie'] != {""} and raw_data['Cookie'] != {"":""}:
			if type(raw_data['Cookie']) != str:
				print(yaml_file,"Cookie字段格式错误")
			else:
				if ";" in raw_data['Cookie']:
					for i in raw_data['Cookie'].split(";"):
						if "=" not in i:
							print(yaml_file,"Cookie字段格式错误")
				elif "=" not in raw_data['Cookie']:
					print(yaml_file,"Cookie字段格式错误")


		#处理Header
		if raw_data['Header'] != "" and raw_data['Header'] != {""} and raw_data['Header'] != {"":""}:
			if type(raw_data['Header']) != dict:
				print(yaml_file,"Header字段格式错误")

		#处理redirects
		if type(raw_data['follow_redirects']) != bool:
			print(yaml_file,"follow_redirects字段格式错误")
		
		#处理path
		if type(raw_data['path']) != list:
			print(yaml_file,"path字段格式错误")

		#处理method
		if raw_data['method'].lower() != "get" and raw_data['method'].lower() != "post":
			print(yaml_file,"method字段格式错误")

		#处理expression
		if type(raw_data['expression']) != str:
			print(yaml_file,"expression字段格式错误")
		if "\n" in raw_data['expression']:
			expression = raw_data['expression'].split("\n")[0]
		else:
			expression = raw_data['expression']
		
		if eval(expression) != True and eval(expression) != False:
			print(yaml_file,"expression字段格式错误")


		#处理data
		if raw_data['method'].lower() == "post":
			try:
				if type(raw_data['data']) != str:
					print(yaml_file,"data字段格式错误")
			except:
				pass
		
		md5 = []
		md5_path = []
	
	elif raw_data['name'].split("-")[-1] == "md5":
		if type(raw_data['md5_path']) != list:
			print(yaml_file,"md5_path字段格式错误")
		if type(raw_data['md5']) != list:
			print(yaml_file,"md5字段格式错误")
		for i in raw_data['md5']:
			if len(i)!= 32:
				print(yaml_file,"md5字段格式错误")
		if len(raw_data['md5_path']) != len(raw_data['md5']):
			print(yaml_file,"md5字段list对应关系错误")



r = requests.get("https://www.baidu.com", timeout=10)
yaml_list = os.listdir('fingerprint')
print("+++++++++++++++++++++++++checking+++++++++++++++++++++++++")
for y in yaml_list:
	print("checking -", y)
	get_yaml('fingerprint/'+y)
print("\ntotal checked:",len(yaml_list),"yaml files\n")
print("+++++++++++++++++++++++++finished+++++++++++++++++++++++++")
