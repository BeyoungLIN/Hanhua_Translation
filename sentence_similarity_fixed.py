from tqdm import tqdm

# from hanArt.utils import loadDataFromText
from hanArt.utils import searchAll, dynamicSearch
from utils import *


def alltxtpieces(filepath, testnum):
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

    all_text_new = list(set(all_text[:testnum]))
    all_text = all_text_new

    return all_text


all_text = alltxtpieces('./hanhua_jt_fin_test.txt', 300)

sims = []

descriptions = loadDataFromText('./hanhua_jt_fin_test.txt')
outputpath = '/Users/Beyoung/Desktop/研一课件/翻译技术原理/2020级计算机辅助翻译课程竞赛/hanhua_similarsentences_dynamic_95_rmdup_300.txt'

# for para_i in range(50):
# for para_i in tqdm(range(50)):
for para_i in tqdm(range(len(all_text))):
    # current_sims = searchAndShow(all_text[para_i + 1:], all_text[para_i], False, 0.05)
    # target='建鼓，上有羽葆，两侧有小鼓' #目标句子
    searchAll(descriptions, all_text[para_i], searchMethod=dynamicSearch, threshold=0.93, outputpath=outputpath)
    # searchAll(descriptions, target,searchMethod=fixedSearch,threshold=0.95)
