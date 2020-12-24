import numpy as np
from tqdm import tqdm
from hanArt.utils import loadDataFromText
from hanArt.utils import fixedSearch,searchAll
from utils import *



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


descriptions=loadDataFromText('./hanhua_jt_fin_test.txt')
# lines = descriptions

# for para_i in range(50):
for para_i in tqdm(range(50)):
    # current_sims = None
    # current_sims = searchAndShow(all_text[para_i + 1:], all_text[para_i], False, 0.05)
    # target='建鼓，上有羽葆，两侧有小鼓' #目标句子
    # print(all_text[para_i])
    searchAll(descriptions, all_text[para_i],searchMethod=fixedSearch,threshold=0.9)
    # searchAll(descriptions, target,searchMethod=fixedSearch,threshold=0.95)
    # print(searchAll(descriptions, target,searchMethod=fixedSearch,threshold=0.95))

