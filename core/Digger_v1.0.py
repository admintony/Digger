__author__="AdminTony"

import optparse,requests,re,threading,sys

lock = threading.Lock()

headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

#存放结果的list
result=[]

def crew(url):
    res = requests.get(url,headers=headers)
    #style="text-decoration:none;">(.*?)<b>.*?</b>/&nbsp;</a>
    re_ = re.compile(r'style="text-decoration:none;">(.*?)<b>.*?</b>/')
    result_=re_.findall(res.text)
    global result
    lock.acquire()
    result+=result_
    lock.release()
    print("[+] 正在抓取 "+str(result))

#线程启动函数
def run(start,end,domain):
    for i in range(start,end+1):
        url="https://www.baidu.com/s?wd=inurl:"+domain+"&pn="+str(i*10)+"&oq=inurl:"+domain
        crew(url)

def main():

    #定义接受的参数
    opt = optparse.OptionParser()
    opt.add_option('--domain', action='store', dest="domain", type="string", help="Parent Domain !")
    opt.add_option('-p', '--page', action="store", dest="page_num", type="int", help="Page number From Baidu !")
    opt.add_option('--thread', action="store", dest="thread_num", default=5, type="int", help="The thread number")
    (options, args) = opt.parse_args()
    if (len(sys.argv) < 4):
        print('''* by:AdminTony
* QQ:78941695    
[+] usage:
[+] e.g.%s --domain=ParentDomain -p PageNum [--thread=5]
        '''%sys.argv[0])
        sys.exit()
    domain = options.domain
    #资源分配
    tmp = int(options.page_num/options.thread_num)
    y = options.page_num%options.thread_num
    thread_list=[]
    for i in range(options.thread_num):
        if i==0:
            start=0
            end = start+tmp-1
        elif i<options.thread_num-1:
            start=end+1
            end = start+tmp-1
        else:
            start=end+1
            end = start+tmp-1+y
        thread = threading.Thread(target=run,args=(start,end,domain))
        thread.start()
        thread_list.append(thread)
    for thread in thread_list:
        thread.join()

    #结果去重
    result_s = set(result)
    with open("result.txt","w+") as file:
        for u in result_s:
            file.write(u+domain+"\n")
            print("[+] 正在保存结果 ",u+domain)
    print("[+] 任务已经完成！\n[+] 结果已经保存在当前目录下的result.txt了。")

if __name__ == '__main__':
    main()
