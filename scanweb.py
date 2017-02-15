#-*-coding:utf-8-*-
'''
1. 将扫描对象网址保存在文本文件中，明确一种保存格式。
1. 将扫描对象网址保存在文本文件中，明确一种保存格式。
2. 主程序逐条读取文本文件中的记录，提取出网站名称和网站地址信息，
   对网址进行扫描，看该网站能否打开，并记录打开主页所需要的时间。
   生成扫描记录。
3. 显示扫描报告
   （1）本次扫描的详细信息
   序号 网站名称 网站地址 扫描结果  扫描日期、时间
   scan_Num
   site_name
   site_url
   site_status
   scan_date
   scan_time

   （2）本次扫描的总体信息
   扫描日期：     扫描时间：
   本次扫描网站  个，用时  秒
   其中：连接的    个，占%  。
		 较慢的    个，占%  。
		 极慢的    个，占%  。
		 无连接的  个，占%  。
'''

import urllib.request
from urllib.request import URLError, HTTPError
import time
import os,sys
import threading

#------------------------------------------------------------------------------
# get the url of website which will be to scanning from a txt file.
# Format of the TXT file:
# FORMAT1
#
# site1_name site1_url
# site2_name site2_url
# site3_name site3_url
# ....
# FORMAT2
#
# [libraries]
# site1_name site1_url
# site2_name site2_url
# site3_name site3_url
# ....
# [arts]
# site1_name site1_url
# site2_name site2_url
# site3_name site3_url
# ....
#------------------------------------------------------------------------------

def geturl():
	sitefile = '.\\scan.conf.txt'
	df = dict()
	f = open(sitefile,"r")
	a = f.readline().strip('\n')
	while 1:
		if a == '':
			break
		k, v = a.split('\t')
		df[k] = v
		a = f.readline().strip('\n')
	f.close()
	return df

#------------------------------------------------------------------------------
#urllib.request.urlopen() open a website by URL. the format of URL such as: 
#"http://www.ahwh.gov.cn/"
#------------------------------------------------------------------------------
def scanurl(url):
	t1 = time.time()
	try:
		p = urllib.request.urlopen(url)
	except HTTPError as e:
		if hasattr(e,"code"):
			return 1, e.code
		if hasattr(e,"reason"):
			return 1, 999
	except URLError as e:
		if hasattr(e,"code"):
			return 1, e.code
		if hasattr(e,"reason"):
			return 1, 999

	accesstime = time.time() - t1

	if p is None:
		p.close()
		return 1, accesstime
	else:
		p.close()
		return 0, accesstime

#------------------------------------------------------------------------------
def displayscanresult(rel):
	n = sn = dn = 0
	scanrel = []
	print("Scanning date and time: %s\n"%(time.ctime()))
	t1 = time.time()
	for a in rel:
		n = n + 1
		r, t = scanurl(rel[a])
		if r == 1:
			dn = dn + 1
		else:
			sn = sn + 1
		print ('%3d %s %d %0.03f'%(n,a,r,t))
		scanrel.append(str('%3d %s %d %0.03f'%(n,a,r,t)))
	t2 = time.time() - t1
	print("Total scanning sites:%d, Success: %d, Failed: %d, Used time: %d"
		%(len(rel), sn, dn, t2))
	return scanrel

#------------------------------------------------------------------------------
def savescanresult(r):
	logfilepath = os.getcwd()
	print("Save scanning result?(y/n)")
	nory = input('>')
	if nory == 'y':
		a = time.localtime()
		relstamp = str("%4d%02d%02d%02d%02d%02d"%(a.tm_year, a.tm_mon, a.tm_mday,
			a.tm_hour, a.tm_min, a.tm_sec))
		savefile = str(logfilepath + '\\' + 'scan' + relstamp + '.txt')
		f = open(savefile, "w")
		for i in r:
			f.write(i + '\n')
		f.close
		print("%s be saved successfully!"%savefile)
	else:
		print("Not to be saved!")
		return

#------------------------------------------------------------------------------
# 
#------------------------------------------------------------------------------
def scanstatistic():
	return 0

#------------------------------------------------------------------------------
def main():
	u = geturl()
	r = displayscanresult(u)
	savescanresult(r)

if __name__ == "__main__":
	main()
