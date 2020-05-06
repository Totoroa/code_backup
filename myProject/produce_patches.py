"""利用北交的代码，将爬取到的补丁链接中对应的补丁下载到本地"""
import os
import re
import random
import time
import bs4
import shutil
from bs4 import BeautifulSoup
from distutils.filelist import findall
import requests

import Repository

patches_file=r"D:\test1\nvd_kernel_patches"  #补丁文件存储路径
#user_agent_list = [
    #"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322"
    #"; .NET CLR 2.0.50727)",
    #"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.5"
    #"0727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    #"Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR"
    #" 1.1.4322; .NET CLR 2.0.50727)",
    #"Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    #"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3"
    #".5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    #"Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SL"
    #"CC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .N"
    #"ET CLR 1.1.4322)",
    #"Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50"
    #"727; InfoPath.2; .NET CLR 3.0.04506.30)",
    #"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko,"
    #" Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    #"Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) "
    #"Arora/0.6",
    #"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/"
    #"2.1.1",
    #"Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kap"
    #"iko/3.0",
    #"Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    #"Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazeha"
    #"kase/0.5.6",
    #"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0"
    #".963.56 Safari/535.11",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) "
    #"Chrome/19.0.1036.7 Safari/535.20",
    #"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
#]

def parse_page(url,try_times=5,sleep_time=10,**kwarg):
    '''
    返回url的response
    '''
    try_times_count = try_times
    while try_times>0:
        try:
            response=requests.get(url,**kwarg)
            response.raise_for_status()
            #selector=etree.HTML(response.text)
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, ssl.SSLError,
                    requests.exceptions.HTTPError, requests.exceptions.InvalidSchema,
                    requests.exceptions.MissingSchema):
            try_times_count -= 1
            time.sleep(sleep_time)
        else:
            break
    else:
        return None
    return response

#def requests_get_content(url, **kwarg):
    #response = requests_get(url, **kwarg)
    #if response:
        #content = response.content
        #response.close()
        #return content
    #else:
        #return None
    
#def requests_get(url, try_times=5, sleep_time=10, **kwarg):
    #try_times_count = try_times
    #while try_times_count > 0:
        #try:
            #response = requests.get(url, **kwarg)
            #response.raise_for_status()
        #except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError, ssl.SSLError,
                #requests.exceptions.HTTPError, requests.exceptions.InvalidSchema,
                #requests.exceptions.MissingSchema):
            #try_times_count -= 1
            #time.sleep(sleep_time)
        #else:
            #break
    #else:
        ## print('\r\033[1;31mFail(' + str(try_times) + " Times):" + url + '\033[0m')
        #return None
    #return response

#def append_file_with_eol(save_path, string, encoding=None):
    #with open(save_path, 'a', encoding=encoding, errors='ignore') as file:
        #file.write(string + '\n')

def get_patch_link(path):    #从文件中提取出补丁链接，path举例：D:\test1\nvd_linux_kernel_multiProcess\CVE-2006-2272-source.txt
    file=open(path,"r")
    pre_urls=file.readlines()    #待处理的补丁链接
    links=[]
    file.close()
    for index in range(0,len(pre_urls),2):
        if pre_urls[index][-1]=='\n':
            pre_urls[index]=pre_urls[index][:-1]
        if re.search(r"^https://github\.com/", pre_urls[index]):
            links.append(pre_urls[index].replace(".patch",""))
        elif re.search(r"source.codeaurora.org",pre_urls[index]):
            links.append(pre_urls[index].replace("/patch/","/commit/"))
        links.append(pre_urls[index])
    return links
    
def get_score(cve):    #得到cve对应的评分，并写入相应文件
    cve_info_url = ("https://nvd.nist.gov/vuln/detail/" + cve)
    save_dir=os.path.join(patches_file, cve)   #save_dir举例：D:\test1\nvd_kernel_patches\CVE-2016-4557\，最后的cve编号可变
    if os.path.exists(save_dir):
        print("patches exists !")
        return True
    os.makedirs(save_dir)   
    content = etree.HTML(parse_page(cve_info_url, timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)}).text)
    cvssv3=content.xpath("//span[@data-testid='vuln-cvssv3-base-score']/text()")
    cvssv2=content.xpath("//span[@data-testid='vuln-cvssv2-base-score']/text()")
    f_score=open(os.path.join(save_dir,score.txt),"w")
    f_score.write("cvssv3:")
    for i in cvssv3:
        f_score.write(i)
    f_score.write("cvssv2:")
    for j in cvssv2:
        f_score.write(j)
    f_score.close()

def save_bm_code_in_github_com(hyperlink, save_path):
    if os.path.exists(save_path):
        os.remove(save_path)
    content = Repository.requests_get_content(hyperlink, timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_td in soup.select(
                'table.highlight.tab-size.js-file-line-container td.blob-code.blob-code-inner.js-file-line'):
            Repository.append_file_with_eol(save_path, tag_td.get_text())
        return True
    return False

def save_patch_in_github_com(hyperlink, cve):
    save_dir=os.path.join(patches_file,cve)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)    
    content = Repository.requests_get_content(hyperlink, timeout=10, headers={'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        for tag_div_diff in soup.select(
                'div.js-diff-progressive-container '
                'div.file.js-file.js-details-container.Details.show-inline-notes'):
            vuln_file_name = ''
            for tag_a in tag_div_diff.select('div.file-header.js-file-header div.file-info a.link-gray-dark'):
                vuln_file_name = tag_a.get_text().strip().replace('/', '#~')
            for tag_a in tag_div_diff.select('div.file-actions a.btn.btn-sm.tooltipped.tooltipped-nw'):    #保存漏洞文件
                bm_code_hyperlink = 'https://github.com' + tag_a['href']
                if not save_bm_code_in_github_com(bm_code_hyperlink, os.path.join(save_dir, '(BM)' + vuln_file_name)):
                    print('\r\033[1;31mFail:(BM)' + vuln_file_name + '\033[0m')
                    return False
            for tag_table in tag_div_diff.select(    
                    'div.js-file-content.Details-content--shown table.diff-table.tab-size'):
                Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name), re.sub(r'\n+', r'\n', tag_table.get_text()))
        return True
    return False

def save_patch_in_git_kernel_org(hyperlink, cve):
    save_dir=os.path.join(patches_file,cve)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    text = Repository.requests_get_content(hyperlink, timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)})
    if text:
        soup = bs4.BeautifulSoup(text.replace(b'<br/>', b'\n').replace(b'<br>', b'\n'), 'lxml')
        for tag_table in soup.select('div#cgit div.content table.diff'):
            if tag_table['summary'] == 'diff':    #补丁所在的位置
                vuln_file_name = ''
                has_vuln_file_name = False
                for tag_div in tag_table.select('div'):
                    if 'head' in tag_div['class']:
                        vuln_file_name_list = []
                        bm_and_am_code_hyperlink_list = []
                        for tag_a in tag_div.select('a'):
                            vuln_file_name_list.append(tag_a.get_text().strip())    #获取漏洞对应的文件名（新的和旧的）
                            bm_and_am_code_hyperlink_list.append("https://git.kernel.org" + tag_a['href'])
                        if len(vuln_file_name_list) != 2 or len(bm_and_am_code_hyperlink_list) != 2:
                            has_vuln_file_name = False
                            continue
                        vuln_file_name = vuln_file_name_list[0].replace('/', '#~')
                        has_vuln_file_name = True
                        Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),tag_div.get_text())   #将补丁文件存在#~文件中
                                                        
                        #将未打补丁的旧文件写入（BM）文件
                        if not Repository.save_tag_code_from_html(
                                bm_and_am_code_hyperlink_list[0],
                                os.path.join(save_dir, '(BM)' + vuln_file_name)
                        ):
                            print('\r\033[1;31mFail:(BM)' + vuln_file_name + '\033[0m')
                            return False
                        #将打了补丁的新文件写入（AM）文件
                        if not Repository.save_tag_code_from_html(
                                bm_and_am_code_hyperlink_list[1],
                                os.path.join(save_dir, '(AM)' + vuln_file_name)
                        ):
                            print('\r\033[1;31mFail:(AM)' + vuln_file_name + '\033[0m')
                            return False
                    elif has_vuln_file_name:    #将补丁文件存在#~文件中
                        Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                        tag_div.get_text())
            return True
    return False

def save_patch_in_patchwork_kernel_org(hyperlink, cve):
    save_dir=os.path.join(patches_file,cve)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    content = Repository.requests_get_content(hyperlink, timeout=10, headers={'User-Agent': random.choice(Repository.user_agent_list)})
    if content:
        soup = bs4.BeautifulSoup(content, 'lxml')
        has_vuln_file_name = False
        vuln_file_name = ''
        for tag_span in soup.select('div#content div.patch pre.content span'):
            if 'p_header' in tag_span['class']:
                match = re.match('diff\s+--git\s+a/(.*?)\s+b/(.*)', tag_span.get_text().strip(), re.I)
                if match:
                    vuln_file_name = match.group(1).replace('/', '#~')
                    has_vuln_file_name = True
                    Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                    tag_span.get_text())
                elif has_vuln_file_name:
                    Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                    tag_span.get_text())
            elif has_vuln_file_name:
                Repository.append_file_with_eol(os.path.join(save_dir, vuln_file_name),
                                                tag_span.get_text())
        return True
    return False

def save_patch_in_codeaurora_org(hyperlink,cve):
    save_dir=os.path.join(r"D:\tt",cve)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    html=etree.HTML(parse_page(hyperlink, timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)}).text)
    diff_element=html.xpath("/html/body/div[2]/div[1]/table[@summary='diff']")
    if diff_element:
        diff_element=diff_element[0]
        vuln_file_name=""
        for element in diff_element.xpath(".//div"):
            if element.xpath("./@class")==['head']:
                vuln_file_name=element.xpath("./a[1]/text()")[0].replace('/', '#~')
                Repository.append_file_with_eol(os.path.join(save_dir,vuln_file_name),'\n'.join(element.xpath(".//text()")))
                bm_file_context=''.join(etree.HTML(parse_page("https://source.codeaurora.org"+element.xpath("./a[1]/@href")[0], timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)}).text).xpath("/html/body/div[2]/div[2]/table/tr/td[2]/pre/code/div[@class='highlight']//text()"))
                Repository.append_file_with_eol(os.path.join(save_dir,'(BM)'+vuln_file_name),bm_file_context)
                am_file_context=''.join(etree.HTML(parse_page("https://source.codeaurora.org"+element.xpath("./a[2]/@href")[0], timeout=10,headers={'User-Agent': random.choice(Repository.user_agent_list)}).text).xpath("/html/body/div[2]/div[2]/table/tr/td[2]/pre/code/div[@class='highlight']//text()"))
                Repository.append_file_with_eol(os.path.join(save_dir,'(AM)'+vuln_file_name),am_file_context)
            else:
                Repository.append_file_with_eol(os.path.join(save_dir,vuln_file_name),''.join(element.xpath(".//text()")))
        return True
    return False    

if __name__=="__main__":
    file_list=os.listdir(r"D:\test1\nvd_linux_kernel_multiProcess")
    print("total_number:",len(file_list))
    i=0
    for name in file_list:    #name举例：CVE-2006-2272-source.txt
        cve=name[:-11]
        file_path=os.path.join(r"D:\test1\nvd_linux_kernel_multiProcess",name)    #file_path举例：D:\test1\nvd_linux_kernel_multiProcess\CVE-2006-2272-source.txt
        patch_links=get_patch_link(file_path)   #提取出文件中的cve编号的链接
        for patch_link in patch_links:
            if re.search(r"github\.com",patch_link):
                save_patch_in_github_com(patch_link,cve)
            elif re.search(r"git\.kernel\.org",patch_link):
                save_patch_in_git_kernel_org(patch_link, cve)            
            elif re.search(r"patchwork\.kernel\.org",cve):
                save_patch_in_patchwork_kernel_org(patch_link,cve)
            elif re.search(r"source\.codeaurora\.org",cve):
                save_patch_in_codeaurora_org(patch_link,cve)
        get_score(cve)   #爬取并存储对应cve的评分
        i=i+1
        print("第%d个"%i,"共%d个"%len(file_list))
    print("OK..")