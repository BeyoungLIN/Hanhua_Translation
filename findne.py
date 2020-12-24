import re


def find(path,label):
	pattern = re.compile(label+':(.*?)}}')
	list = []
	with open(path, 'r', encoding='utf-8') as f:
		lines = f.readlines()
		for line in lines:
			res = pattern.findall(line)
			if res:
				for ress in res:
					list.append(ress)
	list = set(list)
	print(label+'：')
	print()	
	for i in list:
		print(i)
	print('*'*30)
	print()
	return list

labels =['图样',  '人物', '地名', '日期', '官职']

for i in labels:	
#	find('/Users/Beyoung/Desktop/研一课件/翻译技术原理/2020级计算机辅助翻译课程竞赛/hanhua_copac_ner_gl_2M_full_ft_morelabels.txt', i)
#	find('/Users/Beyoung/Desktop/研一课件/翻译技术原理/2020级计算机辅助翻译课程竞赛/hanhua_test_ner_result_combined.txt', i)
	find('/Users/Beyoung/Desktop/研一课件/翻译技术原理/2020级计算机辅助翻译课程竞赛/hanhua_test_ner_result.txt', i)