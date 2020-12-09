#!/usr/bin/python3
# coding: utf-8
import subprocess
import os
import sys
import config

def ffuf_dir(ffuf_bin,url):
	print("fuzzing ",url)
	li = []
	cmd = ["./ffuf/"+ffuf_bin, "-u", url+"/FUZZ", "-timeout", str(config.fuzztime), "-ac", "-r", "-t", str(config.fuzz_t), "-s","-recursion","-recursion-depth", str(config.recursion), "-w", "ffuf/dict.txt", "-o", "tmp/fuzz_tmp.csv", "-of", "csv"]
	try:
		output = subprocess.check_output(cmd)
	except Exception as e:
		print(e)
		#print("fuzz目录出错")
		return li

	#读结果
	with open("tmp/fuzz_tmp.csv", 'r') as f:
		next(f)
		for text in f.readlines():
			if text != "":
				li.append(text.split(",")[1])
	print("fuzz_results:",len(li))
	return li
