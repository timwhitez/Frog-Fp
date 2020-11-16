- 本人github的项目可能目前主要分为两大类，🐸Frog系列为自动化扫描方向，🐶Doge系列为免杀及内网渗透方向

- 本系列命名为Frog可能是因为这种生物的寿命长 🐸 🤓 +1s 

- Frog-Fp为Frog系列第三个项目🐸，写的有点累了

## 序
```
1.关于自动化的设计，难点在于经验如何转化为程序的逻辑

2.大规模攻防对抗初期拼的是"以漏洞找资产的能力"

3.个人能力有限，精力有限，此项目的完成过程中非常纠结
```
# 🐸Frog-Fp

Frog-Fp批量深度指纹识别，采用python3实现，具体实现流程如下所示：

```
不开启深度扫描:

input: domain/ip/cidr-->web端口发现-->浅层指纹识别

input: url-->浅层指纹识别

开启深度扫描:

input: domain/ip/cidr-->web端口发现-->浅层指纹识别-->爬虫 && dir fuzz-->目录过滤与去重-->深度指纹识别

input: url-->初次指纹识别-->爬虫 && dir fuzz-->目录过滤与去重-->深度指纹识别

```
指纹库采用yaml格式进行解析, 需自行添加, 支持get,post,md5三种方式进行识别, 指纹库不公开, 具体格式见demo

web端口发现使用[c26root/hb](https://github.com/c26root/hb), 爬虫使用[chaitin/rad](https://github.com/chaitin/rad), 目录fuzz使用[ffuf/ffuf](https://github.com/ffuf/ffuf)

支持ip/domain/CIDR输入

## about

在大规模红蓝对抗中，不触发waf拦截的指纹识别是比较好的自动化切入点。

尤其是在手上有了一部分0day后，深度的指纹识别框架能提升"以漏洞找资产的能力"。

此框架的构思基于个人的一部分打点经验，有很多不足之处，开源是希望大家一起完善起来。

对于我个人来说，我是不太想公开指纹库的，但是如果你能对本项目进行核心代码贡献/修复，或是可以贡献超过5个指纹yaml，即可共享目前我写的指纹库。

## Usage
若在linux下使用，请给 rad_linux/ffuf_linux/hb_linux三个文件可执行权限

并且执行pip install安装依赖
```
python3 -m pip install requirements.txt

```
## 常用命令
```
python3 Frog-Fp.py win/linux -tL urls.txt

python3 Frog-Fp.py win/linux -dL ips.txt
```
输入的文本按行划分，支持ip/domain/CIDR格式
