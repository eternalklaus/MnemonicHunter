#!/usr/bin/python
#-*- coding: utf-8 -*-
import requests
import re
import sys
from bs4 import BeautifulSoup

def lowercase(line):
    return line.lower()

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
    		colomnContent = lowercase(colomnContent)
    		# 딕셔너리 어펜드
    		resdic[colomnNames[i]].append(colomnContent)
    return resdic

def parseargv(sysargv):
	whitelist = []
	startfrom = 1 # 디폴트로다가는 url 1부터 시작한다. 
	mode = 'default'

	for str in sysargv:
		if str == '--whitelist':
			mode = '--whitelist'
			continue
		elif str == '--startfrom':
			mode = '--startfrom'
			continue
		
		if mode == '--whitelist':
			whitelist.append(str)
		elif mode == '--startfrom':
			startfrom = int(str)

	return  whitelist, startfrom

if __name__=="__main__":

	if len(sys.argv) < 3:
		print "Usage)"
		print "    python MnemonicHunter.py [OptionName] [Str1] [Str2] [...]"
		print ""
		print "Options)"
		print "    --whitelist : specifies the string to be included from searching"
		print "    --startfrom : specifies the page number of c9x.me/x86 to start searching"

		print ""
		print "Example)"
		print "     python MnemonicHunter.py --whitelist 'imm316' 'imm32'"
		print "     python MnemonicHunter.py --whitelist 'r/m16' --startfrom '292' "
		print ""
		sys.exit()
	
	whitelist, startfrom = parseargv(sys.argv)
	print ''
	print "whitelist : {}".format(whitelist)
	print ''
	
	for i in range(startfrom,333): 
		# print i
		url = 'https://c9x.me/x86/html/file_module_x86_id_{}.html'.format(i)
		resdic = html2dictionary(url)
		
		for i in xrange(len(resdic['Mnemonic'])):
			select  = 'no' # 디폴트 셋팅
			content = resdic['Mnemonic'][i]
			content = content.replace(',',' ')
			content = content.replace('(',' ')
			content = content.replace(')',' ')
			content = content.replace(':',' ')
			content = content.replace('&',' ')
			content = content.replace('*',' ')
			content = content.split(' ')
			for w in whitelist:
				for c in content: # 'ADC', 'r/m32', 'r16' 에 대해서 모두 검사
					if w == c:
						select = 'yes'
			
			if select == 'yes': # 살아남았다면
				print resdic['Mnemonic'][i].ljust(70) + ' : ' + resdic['Opcode'][i]

		for i in xrange(len(resdic['Opcode'])):
			'nothing to do'

		for i in xrange(len(resdic['Description'])):
			'nothing to do'
	
