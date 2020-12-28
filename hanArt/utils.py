import re
import text2vec
from tqdm import tqdm



sim=text2vec.Similarity()



def loadDataFromText(filePath):
    """
    load data from text file, return a list
    """
    with open(filePath,'r') as f:
        contents=f.readlines()

    return contents



def para2Sentence_1(para):
    """
    以大单位分句，每个分句可能包含小句
    """
    para = re.sub('([。；？！])([^”’])', r"\1\n\2", para)  # 单字符断句符
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    
    return para.split("\n")



def para2Sentence(para):
    """
    以最小单位分句
    """
    para = re.sub('([。；，！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    
    return para.split("\n")



def searchAll(articles,target,searchMethod,threshold=0.9, outputpath=''):
    """
    输入文章集，目标句子，搜索方法和阈值，
    按照指定的搜索方法和阈值在文章集里搜索相似句子，
    输入articles是[[文章一],[文章二],[文章三]]的形式，
    target是字符串，searchMethod是搜索方法，threshold阈值默认是0.9
    """
    sims={}
    # for i,article in enumerate(tqdm(articles)):
    of = open(outputpath, 'a', encoding='utf-8')
    for i,article in enumerate(articles):
        # print(i, article)
        current_sims=None

        current_sims=searchMethod(article,target,threshold)
        if current_sims:
            sims.update({i:current_sims})
    if len(sims.values()) >= 50:
        print()
        print(target)
        of.writelines('原句：'+target)
        of.writelines('\n')
        print('出现次数：', len(sims.values()))
        of.writelines('出现次数：'+ str(len(sims.values())-1))
        of.writelines('\n')
        for key, value in sims.items():
            if key != 0:
                # value_light =
                for value_1 in value:
                    print(value_1)
                    of.writelines(str(value_1))
                    of.writelines('\n')
        print('*'*20)
        of.writelines('*'*20)
        of.writelines('\n')
        of.writelines('\n')


    return sims



def sentenceParse(sentence):
    sentences=para2Sentence(sentence)
    sentencePart=len(sentences)
    if sentencePart==1:
        return [sentences]
    elif sentencePart==2:
        return [
            sentences,
            [sentence]
        ]
    elif sentencePart==3:
        return [
            sentences,
            [sentence],
            [sentences[0],sentences[1]+sentences[2]],
            [sentences[0]+sentences[1],sentences[2]]
        ]
    elif sentencePart==4:
        return [
            sentences,
            [sentence],
            [sentences[0]+sentences[1],sentences[2],sentences[3]],
            [sentences[0],sentences[1]+sentences[2],sentences[3]],
            [sentences[0],sentences[1],sentences[2]+sentences[3]],
            [sentences[0]+sentences[1]+sentences[2],sentences[3]],
            [sentences[0],sentences[1]+sentences[2]+sentences[3]]
        ]
    elif sentencePart==5:
        return [
            sentences,
            [sentence],
            [sentences[0]+sentences[1],sentences[2],sentences[3],sentences[4]],
            [sentences[0],sentences[1]+sentences[2],sentences[3],sentences[4]],
            [sentences[0],sentences[1],sentences[2]+sentences[3],sentences[4]],
            [sentences[0],sentences[1],sentences[2],sentences[3]+sentences[4]],
            [sentences[0]+sentences[1]+sentences[2],sentences[3],sentences[4]],
            [sentences[0],sentences[1]+sentences[2]+sentences[3],sentences[4]],
            [sentences[0],sentences[1],sentences[2]+sentences[3]+sentences[4]],
            [sentences[0]+sentences[1]+sentences[2]+sentences[3],sentences[4]],
            [sentences[0],sentences[1]+sentences[2]+sentences[3]+sentences[4]]
        ]
    else:
        return [sentences] #如果句子太长，就直接按最小单位拆分并返回



def dynamicSearch(article,target,threshold=False):
    """
    输入文章和目标句子，动态分句子。
    之后计算每句话和目标句子的相似度，相似度会归一化。
    默认输出所有句子以及其相似度，如果设置了threshold，只输出相似度>=threshold的句子。
    """

    global sim
    result=[]

    bigSentences=para2Sentence_1(article)
    for sentence in bigSentences:
        pattern=sentenceParse(sentence)
        result+=findLocalMax(pattern,target)
    if threshold!=False:
        new_result=[]
        for r in result:
            if r[1]>=threshold:
                new_result.append(r)
        result=new_result

    return result



def findLocalMax(pattern,target,debug=False):
    """
    输入一堆句子，通常是一个句子不同句长的组合。
    返回包含最大相似句子的那个pattern以及其分句对应概率
    """
    probs=[]
    for p in pattern:
        probs_temp=[]
        for parts in p:
            probs_temp.append(sim.get_score(target,parts))
        probs.append(probs_temp)

    if debug:
        return [
            [pattern[i],probs[i]] for i in range(len(pattern))
        ]
    else:
        probs_max=[max(i) for i in probs]
        max_prob=max(probs_max)
        index_max=probs_max.index(max_prob)
        return [[pattern[index_max][i],c] for i,c in enumerate(probs[index_max])]

    
    
def fixedSearch(article,target,threshold=False):
    """
    输入文章和目标句子，按照最小单位分句。
    之后计算每句话和目标句子的相似度，相似度会归一化。
    默认输出所有句子以及其相似度，如果设置了threshold，只输出相似度>=threshold的句子。
    """
    
    global sim
    probs=[]
    
    sentenceInArticle=para2Sentence(article)
    # print(sentenceInArticle)
    # sentenceInArticle=article
    for sentence in sentenceInArticle:
        # print(sentence)
        probs.append(sim.get_score(target,sentence))
    result=[[sentenceInArticle[index],element] for index,element in enumerate(probs)]
    # result=sorted(result,key=lambda x:x[1],reverse=True) #按相似度从高到低排序
    if threshold!=False:
        new_result=[]
        for r in result:
            if r[1]>=threshold:
                new_result.append(r)
                # print(r)
        result=new_result
    # for r in result:
    #     print(r)
        print(r)

    
    return result

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
        mark = r[0] / temp_max[0]
        if mark > 0.8:  # 此处可以调相似度阈值
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