#!/usr/bin/python3
# coding: utf-8
import subprocess
import os
import simplejson
import time
import config

#获取时间戳
def gettime():
	t = time.strftime("%m-%d_%H-%M-%S", time.localtime())
	return str(t)

#写入
def wFile(file,str):
	tn = gettime()
	if ":" in file:
		file = file.replace(":","_")
	try:
		f = open("tmp/history/"+file + "_" + tn +".txt",'a')
		f.write(str)
		f.write('\n')
	finally:
		f.close()

def rad_crawler(rad_bin,target):
	uList = []
	name = target.split("://")[1]
	try:
		name = name.split("/")[0]
	except:
		pass
	try:
		os.remove("tmp/rad_output.json")
	except:
		pass
	cmd = ["./rad/"+rad_bin, "-t", target, "-json", "tmp/rad_output.json", "--no-banner","-c","rad/rad_config.yml"]
	print('\nCrawling '+target+"...")
	try:
		output = subprocess.check_output(cmd, timeout=config.crawler_timeout)
	except Exception as e:
		#print(e)
		if "time out" in str(e):
			print("crawling timeout...")
			pass
		else:
			print(e)
			return uList
	
	#print("Finished")
	file_err = False
	with open("tmp/rad_output.json") as f:
		try:
			result_json = simplejson.load(f)
		except:
			file_err = True
			pass
	if file_err == True:
		with open("tmp/rad_output.json") as f:
			try:
				result_json = simplejson.loads(f.read()+"]")
			except:
				print("json解析失败")
				return uList

	for u in result_json:
		url_split = []
		url_list = []
		try:
			urls = u['URL']
			if "?" in urls:
				urls = urls.split("?")[0]
			url_split.append(urls.split("://")[0])
			for ul in range(len((urls.split("://")[1]).split("/"))):
				url_split.append(urls.split("://")[1].split("/")[ul])
				if ul == 3:
					break
			url = url_split[0]+"://" + url_split[1]
			url_list.append(url)
			if len(url_split) > 2:
				for i in range(len(url_split)-2):
					i = i + 2
					if url_split[i] == "":
						break
					url = url +"/"+ url_split[i]
					url_list.append(url)
			uList.extend(url_list)
		except:
			continue
	uList = list(set(uList))
	for url0 in uList:
		wFile(name,url0)
	return uList