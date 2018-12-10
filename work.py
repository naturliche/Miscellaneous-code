#! /usr/bin/python3
#coding=utf-8

def _open_file(filename):  #打开文件，返回所有单词list
	with open(filename,'r',encoding = 'ISO-8859-1') as f:   #编码方式不一样
		raw_words = f.read()
		low_words = raw_words.lower()   #字符串中所以大写字符变为小写
		words = re.findall("[a-z]+", low_words)   #正则re找到单词，返回的是列表
	return words
#刚开始encoding = 'utf-8'不成功，google后改为'ISO-8859-1'编码

#剔除常用单词（is am are do......）
def _filter_words(words): #载入未处理的所有单词列表和默认count值
	new_words = []
	exclude_list = ['am','are','my','is','the','to','in','and','on','it','that','as','of','have','you','with','for','by','they','their']
	for i in range(len(words)):
		if words[i] not in exclude_list and len(words[i]) > 1:
			new_words.append(words[i])
	return new_words


def trans(word):
	url = 'http://www.iciba.com/index.php?a=getWordMean&c=search&word=' + word
	req = requests.get(url)
	req.raise_for_status() #内部判断rstatus.code是否等于200
	info = req.json()
	data = info['baesInfo']['symbols'][0]   #[baesInfo]关于单词的多种形式
	assert info['baesInfo']['symbols'][0]   #[symbols]关于单词的发音以及各种形式的意思
	#去掉没有音标的单词                       #利用google插件jsonView格式化查看元素
	assert data['ph_am'] and data['ph_en']
	#去除没有词性的单词
	assert data['parts'][0]['part']
	ph_en = '英 [' + data['ph_en'] + ']'
	ph_am = '美 [' + data['ph_am'] + ']'
	ex = ''
	for part in data['parts']:
		ex += part['part'] + ';'.join(part['means']) + ';'
	return ph_en+ph_am, ex
'''
1.原主以上用的是try...except但我不会用，删除了
2.原主以上用了info，只要用插件就可以查看
以下，原主用的是数据库peewee，emmm我不会，所以没有选择保存在
数据库中，而是直接保存在csv文件中，然后用excel打开
'''


import requests
import re
import csv



TOP_NUM = 10
TARGET_FILE = '2016_12_2'


from collections import Counter #计时器
words1 = _open_file('G:/study/crawler/'+TARGET_FILE+'.txt')  #返回单词列表
words = _filter_words(words1)  
c = Counter(words) #list new_words
top_word = c.most_common(TOP_NUM)



csv_file_name = 'G:/study/crawler/'+TARGET_FILE+'.csv'
#写csv文件
with open(csv_file_name,'w',encoding='utf-8') as f:
	csv_file = csv.writer(f, delimiter = '|', quotechar = '"',quoting = csv.QUOTE_MINIMAL)
	for word,num in top_word:
		trans_res = trans(word)
		ph = trans_res[0]
		tr = trans_res[1]
		csv_file.writerow([word,num,ph,tr])
		print(">>> "+word)


