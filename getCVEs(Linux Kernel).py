#coding=utf-8
from bs4 import BeautifulSoup
import requests
import lxml
from lxml import etree

'''
获取关于Linux Kernel的CVE漏洞列表，包括漏洞CVE编号，影响Linux kernel内核版本号，漏洞评分
每个漏洞将CVE编号作为一个文件夹，同时将其写入一个总的txt文件中去，其中的version.txt记录受影响的内核版本号，score.txt记录漏洞评分，patch.txt记录该CVE漏洞对应的补丁的内容
爬取网站：https://nvd.nist.gov/vuln/search/results?form_type=Basic&results_type=overview&query=linux+kernel&search_type=all&startIndex=0
         https://www.cvedetails.com/vulnerability-list/vendor_id-33/product_id-47/Linux-Linux-Kernel.html
从获取的CVE漏洞列表提取出每个CVE编号，运行patchFinder获得其对应的补丁，将补丁内容添加到patch.txt中（最好有统一的格式）
'''
def parse_page(url):
    '''
    返回url的XPath解析对象
    '''
    html=requests.get(url).text
    selector = etree.HTML(html)
    return selector

def get_cve_list(url, file_path):
    '''
    从网页中爬取所有CVE列表，将结果存入文件“cve_list.txt”中
    '''
    cve_num=parse_page(url).xpath("/html/body/table/tr[2]/td[2]/div/div[6]/b/text()")
    print("cve_num: ",cve_num)     #cve_num是总共的Linux kernel相关的CVE漏洞数量  2347
    
    cve_list_file=open(file_path,"a")
    cve_flag=0  #表示现阶段已抓取的CVE数目,用于判断是否所有的CVE漏洞名称都已经被爬取，用于退出循环
    page=1
    while(True):
        if(cve_flag>=int(cve_num[0])):
            break    
        #url1=r"https://www.cvedetails.com/vulnerability-list.php?vendor_id=33&product_id=47&version_id=&page="+str(page)+r"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=2346&sha=544260ec3a86a7e17f8b02b39d6342815d8d4bd5"
        url1 =r"https://www.cvedetails.com/vulnerability-list.php?vendor_id=1224&product_id=15031&version_id=&page="+str(page)+r"&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=0&order=1&trc=1858&sha=dad84f9c3747d02e86132c2ca5dc09a296cdf556"
        cve_name=parse_page(url1).xpath("/html/body/table/tr[2]/td[2]/div/div[5]/table/tr[@class='srrowns']/td[2]/a/text()")
        
        string=""
        for i in cve_name:
            string=string+i+"\n"
            
        cve_list_file.write(string)
        cve_flag+=len(cve_name)
        print("cve_flag: ",cve_flag,"   page: ",page,"    cve_name[-1]:",cve_name[-1])
        page+=1
        
    cve_list_file.close()
    print("OK..")

url = r"https://www.cvedetails.com/vulnerability-list/vendor_id-1224/product_id-15031/Google-Chrome.html"
file_path = r"f:\chrome_cve.txt"
get_cve_list(url,file_path)
