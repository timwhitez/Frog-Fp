#!/usr/bin/python3
# coding: utf-8
import subprocess
import os
import sys
import config

def hb_scan(hb_bin,file):
	try:
		os.remove("tmp/hb_output.txt")
	except:
		pass
	cmd = ["./hb/"+hb_bin, "-f", file, "-o", "tmp/hb_output.txt", "-p", config.ports, "-random", "-redirect", "-timeout", str(config.hb_time), "-code", "200", "-t", str(config.hb_t)]
	try:
		print("Starting Port Scan")
		rsp=subprocess.Popen(cmd)
		output, error = rsp.communicate()
	except Exception as e:
		print(e)
		print("端口扫描出错，请检查输入文件以及hb文件夹内二进制文件")
		sys.exit(1)
	print("Port Scanning Finished\n")
	print(r"***************************************************************************************")