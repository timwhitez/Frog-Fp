#指纹识别代理(dirfuzz,爬虫代理暂不支持)
proxies = {
	#"http":"http://127.0.0.1:8080",
	#"https":"http://127.0.0.1:8080",
}

#目录fuzz递归深度
recursion = 2

#目录fuzz超时(s)
fuzztime = 3

#指纹识别超时(s)
timeout = 5

#单个目标爬虫超时(s)
crawler_timeout = 1000

#指纹识别线程数
threads = 200

#目录fuzz线程数
fuzz_t = 20

#web端口扫描超时
hb_time = 3

#端口扫描线程数
hb_t = 500

#端口扫描端口list
ports = "80,443,8080,8443"

#仅基础扫描
only_basic = False

#深度扫描进行爬虫
deep_crawl = False
