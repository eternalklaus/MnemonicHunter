#!/usr/bin/python
#-*- coding: utf-8 -*-
import requests
import re
import sys
from bs4 import BeautifulSoup

def removebrackets(str):
	while True:
		if '<' in str and '>' in str:
			idx1 = str.index('<')
			idx2 = str.index('>')
			str = str.replace(str[idx1:idx2+1],'')
		else:
			break
	return str


def html2dictionary(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    table      = soup.find_all('table',{'class':'box'}) # <table class="box"></table>
    tablelines = table[0].find_all('tr')

    resdic = {}
    colomnNames = []

    for e in tablelines:
    	ths = e.find_all('th')
    	tds = e.find_all('td')

    	for i in xrange(len(ths)):
    		# 칼럼이름 리스트화
    		colomnNames.append(removebrackets(str(ths[i])))
    		# 딕셔너리 초기화
    		resdic[colomnNames[i]] = []

    	for i in xrange(len(tds)):
    		# 컨텐츠 스트립
    		colomnContent = removebrackets(str(tds[i]))
    		# 딕셔너리 어펜드
    		resdic[colomnNames[i]].append(colomnContent)
    return resdic

def parseargv(sysargv):
	whitelist = []
	blacklist = []
	mode = 'default'
	for str in sysargv:
		if str == '--blacklist':
			mode = '--blacklist'
			continue
		elif str == '--whitelist':
			mode = '--whitelist'
			continue

		if mode == '--blacklist':
			blacklist.append(str)
		elif mode == '--whitelist':
			whitelist.append(str)

	return blacklist, whitelist

if __name__=="__main__":

	if len(sys.argv) < 3:
		print "Usage)"
		print "    python MnemonicHunter.py [OptionName] [Str1] [Str2] [...]"
		print ""
		print "Options)"
		print "    --blacklist : specifies the string to be excluded from searching"
		print "    --whitelist : specifies the string to be included from searching"
		print ""
		print "Example)"
		print "     python MnemonicHunter.py --blacklist 'r/m32' --whitelist 'IMM' "
		print ""
		sys.exit()
	
	blacklist, whitelist = parseargv(sys.argv)
	print ''
	print "blacklist : {}".format(blacklist)
	print "whitelist : {}".format(whitelist)
	print ''
	
	#blacklist 부터 필터링하고나서, whitelist 매치되는넘들을 추가함.
	for i in range(1,333): 
		url = 'https://c9x.me/x86/html/file_module_x86_id_{}.html'.format(i)
		resdic = html2dictionary(url)
		
		for i in xrange(len(resdic['Mnemonic'])):
			select  = 'yes' # 디폴트 셋팅
			for b in blacklist:
				if b in resdic['Mnemonic'][i]:
					select = 'no'
			for w in whitelist:
				if w not in resdic['Mnemonic'][i]:
					select = 'no'
			if select == 'yes': # 살아남았다면
				print resdic['Mnemonic'][i]


		for i in xrange(len(resdic['Opcode'])):
			'nothing to do'

		for i in xrange(len(resdic['Description'])):
			'nothing to do'
	
