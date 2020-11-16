但如果您能对本项目进行核心代码贡献/修复被认可，或是可以贡献超过5个指纹yaml并被认可，即可共享目前的指纹库。

## Usage
若在linux下使用，请给 rad_linux/ffuf_linux/hb_linux三个文件可执行权限

并且执行pip install安装依赖
```
python3 -m pip install requirements.txt
```
将指纹库yaml文件放入fingerprint文件夹内，执行check.py可进行yaml格式检查。

## 常用命令
```
python3 Frog-Fp.py win/linux -tL urls.txt
python3 Frog-Fp.py win/linux -dL ips.txt
```
输入的文本按行划分，支持ip/domain/CIDR格式

#yaml格式解析

GET,POST:
```
#name为yaml的标题，请以fp开头，以请求方法结尾，中间以-连接
name: fp-demo-get

#method目前支持GET,POST
method: GET

#目录采用list格式，可写多个
path: ["/","/login"]

#Header采用dict格式，可写入""留空，即采用chrome默认header
Header: {"Accept-Language":"zh-CN", "Content-Type": "text/javascript"}

#Cookie采用;分隔多个key=value，中间不要有空格
Cookie: key1=value1;key2=value2

#follow_redirects可赋值True或False，记得第一位字母大写
follow_redirects: True

#expression表达式采用python语句直接执行，requests请求的返回值为r
expression: |
      r.status_code == 200 and ('test' in str(r.headers) or 'test1' in r.content.decode())

#若请求方法为POST可加入data字段,格式为string
data: ''

```

MD5:
```
#name为yaml的标题，请以fp开头，以md5结尾
name: fp-demo-md5

#md5_path为文件路径，list格式，与md5的list一一对应
md5_path: ["/test.ico","/favicon.ico"]

#md5为对于path的md5值，与md5_path一一对应
md5: ["18b786ca7913a58cb8463f1a5feca293","ffaadddssa7913a58cb8463f1a5feca2"]

```

#config.py

```
#指纹识别代理(去掉井号)(dirfuzz,爬虫代理暂不支持)
proxies = {
	#"http":"http://127.0.0.1:8080",
	#"https":"http://127.0.0.1:8080",
}

#目录fuzz递归深度
recursion = 2

#目录fuzz超时(s)
fuzztime = 5

#指纹识别超时(s)
timeout = 5

#单个目标爬虫超时(s)
crawler_timeout = 600

#指纹识别线程数
threads = 100

#目录fuzz线程数
fuzz_t = 20

#web端口扫描超时
hb_time = 5

#端口扫描线程数
hb_t = 200

#端口扫描端口list
ports = "80,81,443,444,8000,8080,8088,8880,8443,18080,18443"

#仅基础扫描,此配置为True就不会进行爬虫与目录fuzz
only_basic = True

```
