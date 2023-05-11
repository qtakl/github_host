import traceback
import requests
import re
import os
import webbrowser
import json
hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
log_file_name = 'github_host_log.txt'
websites = ['github.com','github.global.ssl.fastly.net']

def search_ip(website):
    headers = {}
    res = requests.get('https://ip.tool.chinaz.com/' + website, headers = headers)
    ip = re.findall('''AiWenIpData\('([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})''', res.text)
    if not ip:
        raise Exception("ip查询异常")
    return ip[0]

def get_ips():
    ips = github520()
    if ips:
        return ips;
    for website in websites:
        ip_address = search_ip(website)
        ips.append(ip_address)
    return ips;

def github520():
    ips = []
    try:
        res = requests.get('https://raw.hellogithub.com/hosts.json').text
        res = json.loads(res)
        if res:
            global websites
            websites = []
            for ip_web in res:
                ips.append(ip_web[0])
                websites.append(ip_web[1])
    except Exception as e:
        pass
    return ips

def write_hosts(ips):
    hosts = ''
    with open(hosts_path, 'r') as f:
        for line in f.readlines():
            need_flg = True
            for website in websites:
               if line.find(website) >= 0 or line=='\n':
                   need_flg = False
                   break
            if need_flg:
                hosts += line
    with open(hosts_path, 'w', encoding = 'utf-8') as f:
        f.write(hosts)
        for i in range(0,len(websites)):
            f.write('\n' + ips[i]+' '+websites[i])  

def main():
    #如果日志存在则有错误或正执行中
    if os.path.exists(log_file_name):
        return
    #执行时创建日志防止重复执行，正常执行后删除
    with open(log_file_name, 'w') as f:
        f.write('github_host log:\n')
    try:
        write_hosts(get_ips())
    except Exception as e:
        with open(log_file_name, 'a') as f:
            f.write(traceback.format_exc())
    else:
        if os.path.exists(log_file_name):
            os.remove(log_file_name)
        try:
            webbrowser.register('edge',None,webbrowser.BackgroundBrowser(edge_path))
            webbrowser.get('edge').open('github.com')
        except Exception:
            webbrowser.open('github.com')
        
if __name__=="__main__":
    main()
        