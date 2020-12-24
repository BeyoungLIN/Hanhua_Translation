from text2vec import *
import numpy as np
from tqdm import tqdm
from hanArt.utils import loadDataFromText
from hanArt.utils import fixedSearch,searchAll
from utils import *

'''
target='建鼓，上有羽葆，两侧有小鼓' #目标句子
searchAll(descriptions,target,searchMethod=fixedSearch,threshold=0.9)
descriptions=loadDataFromText('./hanhua_jt_fin.txt')
'''


def alltxtpieces(filepath):
    """
    load data from text file, return a list of all sentences of the file
    """
    all_text = []
    with open(filepath, 'r') as f:
        lines = f.readlines()

    for i in lines:
        pieces = re.split(r'[。！？：；‘’“”\n]', i)
        # pieces = re.split(r'([，。！？：、‘’“”])', i) #加()保留分隔符
        for j in pieces:
            if j != '':
                all_text.append(j)
    return all_text


all_text = alltxtpieces('./hanhua_jt_fin_test.txt')

sims = []


def searchAndShow(article, target, show_all=True, threshold=0.05):
    """

    """
    search_sim = text2vec.SearchSimilarity(corpus=article)  # 对每一句话进行相似度计算
    result = [[element, article[index]] for index, element in enumerate(search_sim.get_scores(query=target))]
    # print(result)
    # result = sorted(result, key=lambda x: x[0], reverse=True)  # 按相似度从高到低排序

    if not show_all:
        result_new = []
        # temp_sum = 0
        for r in result:
            # temp_sum = r[0]
            if r[0] >= threshold:
                result_new.append(r)
        result = result_new
        # print(result)

    temp_max = [0, '']
    scoreandsent = []
    for r in result:
        if r[0] >= temp_max[0]:
            temp_max = r
            # scoreandsent.append(r)
    for r in result:
        mark = r[0]/temp_max[0]
        if mark > 0.8: # 此处可以调相似度阈值
            scoreandsent.append(r)

    if len(scoreandsent) > 40:
        print()
        print(target)
        print('最相似句子:', temp_max)
        print('出现频率', len(scoreandsent))
        for i in scoreandsent:
            print(i)
        print('*' * 20)

    result = scoreandsent
        # for i, r in enumerate(result):
        #     print(i,r)
        #     if i >= threshold:
        #         result_new.append(r)
        # result = result_new
    return result



# for para_i in range(50):
for para_i in tqdm(range(16308)):
    # print(len(all_text))
    # for para_j in range(para_i + 1, 6):
    # para_
    # print(all_text[para_i], '相似句子，相似度')
    # corpus = [all_text[para_i], all_text[para_j]]
    # print(corpus)
    # search_sim = SearchSimilarity(corpus=corpus)
    # print(all_text[para_j], 'scores:', search_sim.get_scores(query=all_text[para_i]))
    current_sims = None
    # if para_j in ['', ' ', '\n', '\r', '\r\n']:
    #     continue
    # sentences = para2Sentence(para_j)
    # print(all_text[para_i])
    current_sims = searchAndShow(all_text[para_i + 1:], all_text[para_i], False, 0.05)
    # if current_sims:
    #     sims.append(current_sims)
        # try:
        #     current_sims = searchAndSort(para_j, para_i, False, 0.1)
        #     if current_sims:
        #         sims.append(current_sims)
        # except:
        #     pass
# print(sims)
# sim = Similarity()
# s = Similarity().get_score(all_text[para_i], all_text[para_j])
# print(raw[para_j], s)
# sims.append((all_text[para_j], s))
# print(len(all_text))
