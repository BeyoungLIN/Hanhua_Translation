import re
import text2vec



def loadDataFromText(filePath):
    """
    load data from text file, return a list
    """
    with open(filePath,'r') as f:
        contents=f.readlines()

    return contents



def para2Sentence(para):
    """
    convert paragraph to sentence, using ！？。... as separator
    """
    para = re.sub('([。；，！？\?])([^”’])', r"\1\n\2", para)  # 单字符断句符
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)  # 英文省略号
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)  # 中文省略号
    para = re.sub('([。！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    para = para.rstrip()  # 段尾如果有多余的\n就去掉它
    # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
    
    return para.split("\n")



def searchAndSort(article,target,show_all=True,threshold=0.05):
    """
    
    """
    search_sim = text2vec.SearchSimilarity(corpus=article) #对每一句话进行相似度计算
    result=[[element,article[index]] for index,element in enumerate(search_sim.get_scores(query=target))]
    result=sorted(result,key=lambda x:x[0],reverse=True) #按相似度从高到低排序
    
    if not show_all:
        result_new=[]
        temp_sum=0
        for r in result:
            temp_sum+=r[0]
        for i,r in enumerate(result):
            if r[0]/temp_sum>=threshold:
                result_new.append(r)
        result=result_new
    return result