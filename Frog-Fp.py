#!/usr/bin/python3
# coding: utf-8
import requests
from core import parse,banner,hb,rad,ffuf
import config
import argparse
import sys
import os
import logging
import hashlib
logging.captureWarnings(True)
from random import shuffle
from concurrent.futures import ThreadPoolExecutor,wait, ALL_COMPLETED

raw_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
		   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

hb_bin = 'hb_linux'
rad_bin = "rad_linux"
ffuf_bin = "ffuf_linux"

fileL = []

sec_flag = False

#设置两种系统
def getsys(sys0):
	global hb_bin
	global rad_bin
	global ffuf_bin
	if sys0.lower() == 'linux':
		hb_bin = 'hb_linux'
		rad_bin = "rad_linux"
		ffuf_bin = "ffuf_linux"
	if sys0.lower() == 'win':
		hb_bin = 'hb_win.exe'
		rad_bin = "rad_win.exe"
		ffuf_bin = "ffuf_win.exe"


#读取文件输出list
def readf(fname):
	li = []
	try:
		f = open(fname)
		for text in f.readlines():
			data1 = text.strip('\n')
			if data1[-1] == "/":
				data1 = data1[:-1]
			if data1 != '':
				li.append(data1)
	except:
		return None
	finally:
		f.close()
	return li


#写入
def wFile(str):
	try:
		f = open("fp_results.txt",'a')
		f.write(str)
		f.write('\n')
	finally:
		f.close()


def getmd5(body):
		m2 = hashlib.md5()
		m2.update(body)
		return m2.hexdigest()


#指纹扫描
def run(url,yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5,type_F):
	global sec_flag
	global fileL
	if type_F == "second" and sec_flag == True:
		return
	flag = 0
	if yaml_name.split("-")[-1] != "md5":
		for i in paths:
			if (i == "/" or i == "") and HD == raw_headers and cookies == {} and Method == "get":
				continue
			else:
				url_tar = url + i
				if Method == "get":
					try:
						r = requests.get(url_tar, headers=HD, cookies = cookies, timeout=config.timeout, verify=False, allow_redirects=fRe, proxies = config.proxies)
						if eval(expression):
							print("        "+yaml_name + ": "+url_tar)
							wFile(yaml_name + ": "+url_tar)
							flag = 1
							break
					except:
						pass
				elif Method == "post":
					try:
						r = requests.post(url_tar, headers=HD, cookies = cookies, data = datas, timeout=config.timeout, verify=False, allow_redirects=fRe, proxies = config.proxies)
						if eval(expression):
							print("        "+yaml_name + ": "+url_tar)
							wFile(yaml_name + ": "+url_tar)
							flag = 1
							break
					except:
						pass
	elif yaml_name.split("-")[-1] == "md5":
		for i in range(len(md5_path)):
			url_tar = url + md5_path[i]
			if Method == "get":
				try:
					r = requests.get(url_tar, headers=HD, timeout=config.timeout, verify=False, allow_redirects=fRe, proxies = config.proxies)
					r_md5 = getmd5(r.content)
					if r_md5 == md5[i] and r.status_code == 200:
						print("        "+yaml_name + ": "+url_tar)
						wFile(yaml_name + ": "+url_tar)
						flag = 1
						break
				except:
					pass
	if flag == 1 and type_F == "first":
		fileL.remove(url)
	elif flag == 1 and type_F == "second":
		sec_flag = True

#根目录指纹扫描
def run_root(url,type_F):
	global sec_flag
	global fileL
	if type_F == "second" and sec_flag == True:
		return
	try:
		r = requests.get(url, headers=raw_headers, timeout=config.timeout, verify=False, allow_redirects=True, proxies = config.proxies)
	except:
		return
	#一次请求根目录判断多个yml
	for y in yaml_list:
		yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5 = parse.get_yaml("fingerprint/"+y)
		if yaml_name.split("-")[-1] != "md5" and "/" in paths and Method == "get" and fRe == True:
			if eval(expression):
				print("        "+yaml_name + ": "+url)
				wFile(yaml_name + ": "+url)
				#if type_F == "first":
					#fileL.remove(url)
				if type_F == "second" and sec_flag == False:
					sec_flag = True
				return
	
	try:
		r = requests.get(url, headers=raw_headers, timeout=config.timeout, verify=False, allow_redirects=False, proxies = config.proxies)
	except:
		return
	#一次请求根目录判断多个yml
	for y in yaml_list:
		yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5 = parse.get_yaml("fingerprint/"+y)
		if yaml_name.split("-")[-1] != "md5" and "/" in paths and Method == "get" and fRe == False:
			if eval(expression):
				print("        "+yaml_name + ": "+url)
				wFile(yaml_name + ": "+url)
				#if type_F == "first":
					#fileL.remove(url)
				if type_F == "second" and sec_flag == False:
					sec_flag = True
				return



if __name__ == '__main__':
	os.system('')
	banner.banner()
	if len(sys.argv) != 4:
		print('\n')
		print("Usage: python3 Frog-Fp.py win/linux -tL urls.txt")
		print("Usage: python3 Frog-Fp.py win/linux -dL ips.txt")
		exit()
	else:
		parser = argparse.ArgumentParser() 
		parser.add_argument('os', help='win/linux')
		parser.add_argument('-tL', help='urls', default='')
		parser.add_argument('-dL', help='domains', default='')
		args = parser.parse_args()

	#根据系统设置二进制文件名
	getsys(args.os)

	#读取yaml文件夹
	yaml_list = os.listdir('fingerprint')
	print("fingerprint list:\n")
	for y in yaml_list:
		print("    ",y)
	print("\ntotal:",len(yaml_list),"yaml files\n")
	shuffle(yaml_list)

	#输入url的情况
	if args.tL != "":
		file = args.tL
	#输入domain/ip/cidr的情况用hb进行端口发现
	elif args.dL != "":
		domainfile = args.dL
		hb.hb_scan(hb_bin,domainfile)
		file = "tmp/hb_output.txt"

	#将初始url读入list
	fileL = readf(file)

	#判断是否仅进行基础扫描
	if config.only_basic == True:
		print("only_basic == True 仅进行基础扫描\n")

	#基础指纹扫描
	print("Basic scanning ",len(fileL),"urls...")

	type_F = "first"
	#针对根路径进行一次检测
	with ThreadPoolExecutor(max_workers=config.threads) as pool:
			all_task = [pool.submit(run_root,url,type_F) for url in fileL]
			wait(all_task, return_when=ALL_COMPLETED)

	#解析yaml文件
	for y in yaml_list:
		shuffle(fileL)
		#print("        ",y)
		yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5 = parse.get_yaml("fingerprint/"+y)
		#逐个url去请求
		with ThreadPoolExecutor(max_workers=config.threads) as pool:
			all_task = [pool.submit(run,url,yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5,type_F) for url in fileL]
			wait(all_task, return_when=ALL_COMPLETED)
		#print("        Done\n")


	print("Basic Scan Finished\n")

	#判断是否需要进行深度扫描
	if config.only_basic == True or fileL == []:
		exit()

	print("Start Crawling&Deepscan ",len(fileL),"urls...")

	#爬虫,逐个url
	crawler_res = []
	crawlerL = []
	for url in fileL:
		crawlerL = rad.rad_crawler(rad_bin,url)
		if crawlerL != []:
			crawler_res.extend(crawlerL)
			crawlerL.clear()

		#dirfuzz目录发现
		fuzzL = ffuf.ffuf_dir(ffuf_bin,url)

		#补充爬虫(速度太慢，暂时抛弃)
		'''
		if fuzzL != []:
			for x in fuzzL:
				if x not in crawler_res:
					crawlerL = rad.rad_crawler(rad_bin,x)
					if crawlerL != []:
						crawler_res.extend(crawlerL)
						crawlerL.clear()
		'''
		if fuzzL != []:
			crawler_res.extend(fuzzL)
			fuzzL.clear()

		print(len(crawler_res),"crawling results in ./tmp/history/")
		
		#深度指纹扫描
		type_F = "second"
		sec_flag = False

		if crawler_res != []:
			#去重
			crawler_res = list(set(crawler_res))
			#爬虫结果打乱
			shuffle(crawler_res)
			print("Deep scanning ",len(crawler_res),"urls...")

			#针对爬虫后的根路径进行一次检测
			with ThreadPoolExecutor(max_workers=config.threads) as pool:
					all_task = [pool.submit(run_root,url,type_F) for url in crawler_res]
					wait(all_task, return_when=ALL_COMPLETED)


			for y in yaml_list:
				#print("        ",y)
				yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5 = parse.get_yaml("fingerprint/"+y)
				#逐个url去请求
				with ThreadPoolExecutor(max_workers=config.threads) as pool:
					all_task = [pool.submit(run,url,yaml_name,cookies,HD,fRe,paths,Method,expression,datas,md5_path,md5,type_F) for url in crawler_res]
					wait(all_task, return_when=ALL_COMPLETED)
				#print("        Done\n")

		#清除爬虫结果的list,进入下次循环
		crawler_res.clear()

	print("\nCrawling&Deepscan All Finished\n")
	try:
		os.remove("tmp/rad_output.json")
	except:
		pass
	try:
		os.remove("tmp/hb_output.txt")
	except:
		pass
