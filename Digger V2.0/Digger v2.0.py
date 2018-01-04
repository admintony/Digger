__author__="AdminTony"

"""
Digger v2.0 更新说明:
    1.优化算法，不再需要用户输入page_num
    2.支持存活检测，--status 选项，支持用户自定义存活状态码，默认为all即不进行存活检测
"""

import optparse,requests,re,threading,sys

#=============全局变量声明区=============
headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

#线程锁
lock = threading.Lock()
#存放结果的list
result=[]
#page_num
page_num=0
#最后一页标识符
ack = 0

#存活检测用的list
alive_list=[]
#=============全局变量声明结束===========

def crew(url):
    keyword = 'class="n">下一页&gt;</a>'
    res = requests.get(url,headers=headers)
    #style="text-decoration:none;">(.*?)<b>.*?</b>/&nbsp;</a>
    re_ = re.compile(r'style="text-decoration:none;">(.*?)<b>.*?</b>/')
    result_=re_.findall(res.text)
    print("[+] 正在抓取 "+str(result_))
    if keyword not in res.text:
        global ack
        ack = 1
    return result_

#线程启动函数
def run(domain):
    while True:
        #判断是否是最后一页
        if ack == 1:
            break
        #改变page_num写在爬行前面，防止在线程A爬行时，线程B也爬行同样任务
        lock.acquire()
        global page_num
        page = page_num
        page_num +=1
        lock.release()
        url="https://www.baidu.com/s?wd=inurl:"+domain+"&pn="+str(page*10)+"&oq=inurl:"+domain
        result_=crew(url)
        #将result_拼接到结果中
        lock.acquire()
        global result
        result += result_
        lock.release()


# V2.0 更新：存活检测使用到的生成器
def Generator(result_set):
    for res in result_set:
        yield res

#V2.0 更新：存活检测
def is_alive(url,status):
    try:
        res = requests.get(url,headers=headers,timeout=5)
        res_code = str(res.status_code)
        if res_code in status:
            lock.acquire()
            alive_list.append(url)
            lock.release()
            print("[+] %s 存活，状态码为 %s"%(url,res_code))
        else:
            print("[+] %s 不存活，状态码为 %s"%(url,res_code))
    except:
        print("[+] %s 不存活，无法连接！"%url)


#V2.0 更新：存活检测线程启动函数
def run_alive(domain,status,gen):
    while True:
        try:
            url = gen.__next__()
            if "https://" in url:
                pass
            elif "http://" in url:
                pass
            else:
                url = "http://"+url
        except:
            break
        url_=url+domain
        is_alive(url_,status)

def rm_portal(url):
    return url.split("//")[-1]

def main():

    #定义接受的参数
    opt = optparse.OptionParser()
    opt.add_option('--domain', action='store', dest="domain", type="string", help="父域名！")
    opt.add_option('--thread', action="store", dest="thread_num", default=5, type="int", help="线程数！")
    opt.add_option('--status',action="store",dest="status",type="string",help="存活检测状态码，默认不进行存活检测！")
    (options, args) = opt.parse_args()
    if (len(sys.argv) < 2):
        print('''* by:AdminTony
* QQ:78941695    
[+] usage:
[+] e.g.python %s --domain=ParentDomain [--thread=5] [--status=200,403,401,500,404]
        '''%sys.argv[0])
        sys.exit()

    #线程启动
    threads = []
    for i in range(options.thread_num):
        thread = threading.Thread(target=run,args=(options.domain,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    result_set = set(result)
    if options.status:
        status = options.status.split(",")
        #存活检测
        print("[+] 抓取完成，正在进行存活检测....")
        gen = Generator(result_set)
        threads = []
        for i in range(options.thread_num):
            thread = threading.Thread(target=run_alive,args=(options.domain,status,gen))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        #alive_list rm_portal
        result_f = list(map(rm_portal,alive_list))
    else:
        result_f=list(map(lambda url: url+options.domain, result_set))

    with open("Digger_V2.0_result.txt","w+") as file:
        for u in result_f:
            file.write(u+"\n")
            print("[+] 正在保存结果 ",u)
    print("[+] 任务已经完成！\n[+] 结果已经保存在当前目录下的Digger_V2.0_result.txt了。")




if __name__ == '__main__':
    main()
