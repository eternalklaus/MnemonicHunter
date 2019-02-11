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
    colomnnames = []

    for e in tablelines:
    	ths = e.find_all('th')
    	tds = e.find_all('td')

    	for i in xrange(len(ths)):
    		# 칼럼이름 리스트화
    		colomnnames.append(removebrackets(str(ths[i])))
    		# 딕셔너리 초기화
    		resdic[colomnnames[i]] = []

    	for i in xrange(len(tds)):
    		# 컨텐츠 스트립
    		colomnContent = removebrackets(str(tds[i]))
    		colomnContent = lowercase(colomnContent)
    		# 딕셔너리 어펜드
    		resdic[colomnnames[i]].append(colomnContent)
    return resdic

def parseargv(sysargv):
	search = [] # TODO: 이거 이름을 화이트리스트가 아니라 search 로 바꺼야딩 ㅎ 
	startfrom = 1  # 디폴트로다가는 url 1부터 시작한다. 
	colomnname = '' 

	mode = ''
	for str in sysargv:
		if str == '--search':
			mode = '--search'
			continue
		elif str == '--startfrom':
			mode = '--startfrom'
			continue
		elif str == '--colomnname':
			mode = '--colomnname'
			continue

		if mode == '--search':
			search.append(str)
		elif mode == '--startfrom':
			startfrom = int(str)
		elif mode == '--colomnname':
			colomnname = str

	for i in xrange(len(search)):
		search[i] = lowercase(search[i]) # DS, ds 헷갈리니깐 걍 다 소문자로 획일화하자
	return  search, startfrom, colomnname

def exitproc():
	print "Usage)"
	print "    python MnemonicHunter.py [OptionName] [Str1] [Str2] [...]"
	print ""
	print "Options)"
	print "    --search  : specifies the string to be included from searching"
	print "    --colomnname : specifies the colomn name. Mnemonic/Opcode/Description"
	print "    --startfrom  : specifies the page number of c9x.me/x86 to start searching (Optional)"
	print ""
	print "Example)"
	print "     python MnemonicHunter.py --search 'imm316' 'imm32' --colomnname 'Mnemonic' --startfrom '292'"
	print ""
	sys.exit()


if __name__=="__main__":

	if len(sys.argv) < 3:
		exitproc()

	search, startfrom, colomnname = parseargv(sys.argv)
	
	if len(search) is 0:
		print '[!] Searching string is Null!'
		print ''
		exitproc() 
	if colomnname == '':
		print '[!] Invalid colomnname'
		print ''
		exitproc()
	if colomnname not in ['Mnemonic', 'Opcode', 'Description']:
		print '[!] Invalid colomnname'
		print ''
		exitproc()

	for i in range(startfrom,333): 
		url = 'https://c9x.me/x86/html/file_module_x86_id_{}.html'.format(i)
		resdic = html2dictionary(url)
		
		for i in xrange(len(resdic[colomnname])):
			select  = 'no' # 디폴트 셋팅
			content = resdic[colomnname][i]
			content = content.replace(',',' ')
			content = content.replace('(',' ')
			content = content.replace(')',' ')
			content = content.replace(':',' ')
			content = content.replace('&',' ')
			content = content.replace('*',' ')
			content = content.split(' ')
			for w in search:
				for c in content: # 'ADC', 'r/m32', 'r16' 에 대해서 모두 검사
					if w == c:
						select = 'yes'
			
			if select == 'yes': # 살아남았다면
				print resdic['Mnemonic'][i].ljust(70) + ' : ' + resdic['Opcode'][i].ljust(30) + ' ' + resdic['Description'][i]


