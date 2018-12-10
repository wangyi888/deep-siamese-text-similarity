# coding:utf-8
'''
author:wangyi
'''

import json
import random
import thulac
import re

def create_sentence_pair(inf,law_inf,stop_inf,outf):
    stops = []
    for line in open(stop_inf,encoding='utf-8').readlines():
        stops.append(line.strip())
    laws = [line.strip().split('    ')[1] for line in open(law_inf,encoding='utf-8').readlines()]
    out = open(outf,'w',encoding='utf-8')
    with open(inf,encoding='utf-8') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            line = json.loads(line)
            fact = line['fact'].strip()
            fact = re.sub('\d(\.|、)','',fact)
            fact = re.sub('(某\d|\d某)','某',fact)
            fact = re.sub('（[一二三四五六七八九]）','',fact)
            fact = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，：；《 》。？、~@#￥%……&*（）]+', "", fact)

            fact = re.sub('[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日[0-9]{1,2}时许'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日.*?[0-9]{1,2}时许'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日.*?午'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日晚上'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日晚'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日凌晨'
                          '|[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日'
                          '|[0-9]{4}年[0-9]{1,2}月份到[0-9]{1,2}月份'
                          '|[0-9]{4}年[0-9]{1,2}月'
                          '|[0-9]{4}年', '<TIME>', fact)
            # 替换所有的18岁以下年龄为<CHILD>标识,替换所有的18岁以上为<AUDLT>标识
            fact = re.sub(r'(?<!\d)(1[8-9]|[2-9]\d|[1-9]\d\d)岁', '<AUDLT>', fact)
            fact = re.sub(r'(?<!\d)([1-9]|1[1-7]|未满.*?)岁', '<CHILD>', fact)

            # 替换金额
            fact = re.sub(r'(?<!\d)(\d|[1-9]\d|[1-9]\d\d)(\.\d{0,2}){0,1}余?元', '<ONE>', fact)
            fact = re.sub(r'(?<!\d)(1\d\d\d)(\.\d{0,2}){0,1}余?元', '<TWO>', fact)
            fact = re.sub(r'(?<!\d)(2\d\d\d)(\.\d{0,2}){0,1}余?元', '<THREE>', fact)
            fact = re.sub(r'(?<!\d)([3-4]\d\d\d)(\.\d{0,2}){0,1}余?元', '<FOUR>', fact)
            fact = re.sub(r'(?<!\d)([5-9]\d\d\d)(\.\d{0,2}){0,1}余?元', '<FIVE>', fact)
            fact = re.sub(r'(?<!\d)(1\d\d\d\d)(\.\d{0,2}){0,1}余?元', '<SIX>', fact)
            fact = re.sub(r'(?<!\d)(1|一)(\.\d{0,2}){0,1}余?万余?元', '<SIX>', fact)
            fact = re.sub(r'(?<!\d)([2-4]\d\d\d\d)(\.\d{0,2}){0,1}余?元', '<SEVEN>', fact)
            fact = re.sub(r'(?<!\d)([2-4]|[二两三四])(\.\d{0,2}){0,1}余?万余?元', '<SEVEN>', fact)
            fact = re.sub(r'(?<!\d)(5\d\d\d\d)(\.\d{0,2}){0,1}余?元', '<EIGHT>', fact)
            fact = re.sub(r'(?<!\d)(5|五)(\.\d{0,2}){0,1}余?万余?元', '<EIGHT>', fact)

            fact = re.sub(r'(?<!\d)([6-9]\d\d\d\d|[1-9]\d\d\d\d\d)(\.\d{0,2}){0,1}余?元', '<NINE>', fact)
            fact = re.sub(r'(?<!\d)([6-9]|[六七八九])(\.\d{0,2}){0,1}余?万余?元', '<NINE>', fact)
            fact = re.sub(r'(?<![二三四五六七八九])十余?万余?元', '<NINE>', fact)
            fact = re.sub(r'(?<![二三四五六七八九])十[一二三四五六七八九]余?万余?元', '<NINE>', fact)
            fact = re.sub(r'(?<!\d)([1-9]\d)(\.\d{0,2}){0,1}余?万余?元', '<NINE>', fact)
            fact = re.sub(r'(?<!\d)([二三四五六七八九])(\.\d{0,2}){0,1}十余?万余?元', '<NINE>', fact)
            fact = re.sub(r'(?<!\d)([二三四五六七八九])(\.\d{0,2}){0,1}十[一二三四五六七八九]余?万余?元', '<NINE>', fact)
            fact = re.sub(r'((?<!\d)\d(?!\d)|(?<!\d)\d\d(?!\d)|(?<!\d)\d\d\d(?!\d))','<NUM>',fact)
            fact = re.sub('的(?!确)','',fact)
            #fact = re.sub(stops,得得得'',fact)
            query = thu.cut(fact,text=True).replace(' <', '').replace('<', '').replace('> ', '').replace('>', '').split(' ')
            query = ' '.join([q for q in query if q not in stops])
            relevant_articles = line['meta']['relevant_articles']
            ans = []
            for ra in relevant_articles:
                ra = int(ra)
                laws[ra-1] = re.sub('（[一二三四五六七八九]）', '', laws[ra - 1])
                laws[ra-1] = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】；《 》：“”！，。？、~@#￥%……&*（）]+', "", laws[ra-1])
                #laws[ra-1] = re.sub(stops,'',laws[ra-1])
                txt = thu.cut(laws[ra-1],text=True).split(' ')
                txt = ' '.join([t for t in txt if t not in stops])
                ans.append(txt)
            #ans = [thu.cut(laws[ra-1],text=True) for ra in relevant_articles]
            neg_samples = [laws[i] for i in range(len(laws)) if i+1 not in relevant_articles]
            for j in range(len(ans)):
                out.write(query+'\t'+ans[j]+'\t'+'1'+'\n')
                ns = neg_samples[random.randint(0,len(neg_samples)-1)]
                ns = re.sub('（[一二三四五六七八九]）', '', ns)
                ns = re.sub('[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，：；《 》。？、~@#￥%……&*（）]+', "",ns)
                #ns = re.sub(stops,'',ns)
                txt = thu.cut(ns,text=True).split(' ')
                txt = ' '.join([t for t in txt if t not in stops])
                out.write(query+'\t'+txt+'\t'+'0'+'\n')
                out.flush()
            print(i)

if __name__ == '__main__':

    thu = thulac.thulac(seg_only=True)
    base_dir = '/home/nlp/pySpace'
    inf = base_dir + '/match_law/datasets/gamedatas/train.json'
    law_inf = base_dir + '/match_law/datasets/clean_xing_law_1.txt'
    stop_inf = base_dir+'/deep-siamese-text-similarity/datasets/stopwords.txt'
    outf = base_dir+'/deep-siamese-text-similarity/datasets/datas.txt'
    create_sentence_pair(inf,law_inf,stop_inf,outf)
