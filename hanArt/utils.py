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



def searchAll(articles,target,searchMethod,threshold=0.9):
    """
    输入文章集，目标句子，搜索方法和阈值，
    按照指定的搜索方法和阈值在文章集里搜索相似句子，
    输入articles是[[文章一],[文章二],[文章三]]的形式，
    target是字符串，searchMethod是搜索方法，threshold阈值默认是0.9
    """
    sims={}
    # for i,article in enumerate(tqdm(articles)):
    of = open('/Users/Beyoung/Desktop/研一课件/翻译技术原理/2020级计算机辅助翻译课程竞赛/hanhua_similarsentences.txt', 'a', encoding='utf-8')
    for i,article in enumerate(articles):
        # print(i, article)
        current_sims=None

        current_sims=searchMethod(article,target,threshold)
        if current_sims:
            sims.update({i:current_sims})
    if len(sims.values()) >= 20:
        print()
        print(target)
        of.writelines('原句：'+target)
        of.writelines('\n')
        print('出现次数：', len(sims.values()))
        of.writelines('出现次数：'+ str(len(sims.values())))
        of.writelines('\n')
        for key, value in sims.items():
            for value_1 in value:
                print(value_1)
                of.writelines(str(value_1))
                of.writelines('\n')
        print('*'*20)
        of.writelines('*'*20)
        of.writelines('\n')
        of.writelines('\n')


    return sims
    
    
    
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