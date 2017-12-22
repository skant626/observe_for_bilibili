import jieba
import re
import os
import nltk

#src = "weibodata//2017-04-23//tieba"
#savepath = "tieba_sentence.txt"
def textwashing(src,savepath):
	try:
		savecontent = open(savepath,'w')
		i = 0
		while i<999:
			i = i+1
			if os.path.exists(str(src)+str(i)+".txt"):
				content = open(str(src)+str(i)+".txt",'r')
				strings = ""
				texts = content.readline()
				while texts != "":
					pattern = re.compile(u"[\u4e00-\u9fa5]+") 
					texts =pattern.findall(texts)
					print(texts)
					for text in texts:
						savecontent.write(str(text)+"\n")
					texts = content.readline()
					print("texts:",texts)
	except Exception as e:
		print(e)
def stopwords(src):
	texts = open(src)
	words = texts.readline()
	st = []
	#pattern = re.compile(u"[\u4e00-\u9fa5]+") 
	while words != "":
		#words =pattern.findall(words)
		words = words[:-1]
		if words != []:
			st.append(words)
		words = texts.readline()
	print(st)
	return st
def fenci(sentence):
	seg_list = jieba.lcut(sentence)
	return seg_list[:-1]

#textwashing(src,savepath)
sentence_src = "danmu.txt" 
stopwords_src = "stopwords1.txt"
newcontentsrc = "danmu_cipin.txt"
sentences = open(sentence_src,"r")
sentence = sentences.readline()
st = stopwords(stopwords_src)
newcontent = open(newcontentsrc,"w")
all_words = []
while sentence != "":
	seg_list = fenci(sentence)
	for word in seg_list:
		if word in st:
			seg_list.remove(word)
	#print(seg_list)
	all_words.extend(seg_list)
	sentence = sentences.readline()
a = {}
#print(all_words)
n = len(all_words)


a = nltk.FreqDist(all_words)
print(a)
#for j,element in enumerate(all_words):
#	print("计算词频:")
#	print(str(j/(n+0.0))+"%")
#	if all_words.count(element)>1:
#		a[element] = all_words.count(element)
#print(a)
a = sorted(a.items(),key=lambda item:item[1],reverse = True)
for i in a:
	newcontent.write(i[0]+" "+str(i[1])+'\n')
