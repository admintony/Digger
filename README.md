# Digger 
从百度爬取子域名

## 0.更新说明

在这段时间的使用过程中，发现了V1.0版本一些设计不够友好，还需要一些人力来辅助，所以进行了算法优化更新，这次都更新了什么：

* 1.优化算法，不再需要用户输入page_num，而是对页面中“下一页”识别判断是否为最后一页。

* 2.支持存活检测，--status 选项，支持用户自定义存活状态码，默认为all即不进行存活检测


新版本的用法也有些不同了，下面是新版本的用法介绍：

python diiger2.0.py --domain=swust.edu.cn [--status=200,404,403,401] [--thread=10]

```options
Options:
  -h, --help           show this help message and exit
  --domain=DOMAIN      父域名！[必须参数]
  --thread=THREAD_NUM  线程数！[可选，默认为5]
  --status=STATUS      存活检测状态码，默认不进行存活检测！输入状态码以","隔开[可选，默认不进行存活检测]
```
## 1.目录

```bash
###########
├── Readme.md               // 帮助文档 
├── Digger V2.0             // Digger v2.0版本
│   ├── Digger v2.0.py      // Digger v2.0版本主程序
├── core                    // 核心代码存放目录
│   ├── Digger_v1.0.py      // Digger v1.0版本主程序
```

## 2.设计目的：

子域名在渗透中起着很重要的作用，子域名挖掘工具很多，比如Seay法师写的那款暴力枚举的子域名挖掘工具。但是在挖掘过程中，我发现Seay写的那款，对于那些收录较高的站点，挖掘效率很低，甚至还会卡死。因此自己写了一款基于百度搜索语法的子域名挖掘工具，适用于收录高的站点。

## 3.用法

Blog：http://47.95.206.199/?p=408

```html
usage:
e.g.main.py --domain=ParentDomain -p PageNum [--thread=5]
# --domain 填写父域名如：admintony.top
# -p       填写要爬行的页数，页数过大会重新重新爬第一页，所以建议百度搜索inurl:domain后再填写页数
# --thread 参数可选，默认为5
```
