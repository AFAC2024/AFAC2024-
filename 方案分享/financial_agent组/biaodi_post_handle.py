import json
import pandas as pd
import difflib
import pdb

def is_subset_of_chars(str1, str2):
    return set(str1).issubset(set(str2))

def longest_common_substring(s1, s2):
    s2 = s2.replace("股份","").replace("ST","").replace("st","")
    if s1==s2:
        return 100
    m, n = len(s1), len(s2)
    # 创建一个二维数组，用于存储最长公共子串的长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    longest = 0  # 存储最长公共子串的长度
    end = 0  # 当前最长公共子串的结束位置
    
    # 填充dp数组
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > longest:
                    longest = dp[i][j]
                    end = i
            else:
                dp[i][j] = 0
    
    # 根据最长长度从s1中截取最长公共子串
    return len(s1[end - longest: end])

def match_ent(x,biao_type):
    if not x:
        return None
    if biao_type=="股票":
        standard_name = data_stock
    elif biao_type=="基金":
        standard_name = data_fund
    
    if len(x)>4:
        biao_type = "基金"
    x = norm_q(x)
    x_len = len(x)
    candidate = difflib.get_close_matches(x,standard_name,n=100,cutoff=0.0001)
    if not candidate:
        return None
    back_up = candidate[0]
    candidate = [y for y in candidate if is_subset_of_chars(x,y)]
    candidate = [(y,longest_common_substring(x,y[:x_len])) for y in candidate]
    candidate = sorted(candidate,key=lambda y:y[1],reverse=True)
    candidate = [y for y,_ in candidate]
    candidate = sorted(candidate,key=lambda y:len(y)==3,reverse=False)
    candidate = sorted(candidate,key=lambda y:"股份" in y,reverse=True)
    candidate = sorted(candidate,key=lambda y:"A" in y,reverse=True)
    candidate = sorted(candidate,key=lambda y:x in y,reverse=True)
    if candidate:
        return candidate[0]
    else:
        return None
   
def norm_q(x):
    x = x.replace("基金","").replace("ETF","交易型开放式指数证券投资基金").replace("大摩","摩根").replace("HGS","沪港深")
    x = x.replace("公司","").replace("环保","").replace("中融","国联")
    return x

def ac(x,y):
    return is_subset_of_chars(x,y)

cn = 0
data_stock = pd.read_excel('raw_data/标准名.xlsx',sheet_name='股票标准名')
data_fund = pd.read_excel('raw_data/标准名.xlsx',sheet_name='基金标准名')
data_stock = data_stock['标准股票名称'].to_list()
data_fund = data_fund['标准基金名称'].to_list()
standard = data_stock+data_fund
test_qs = pd.read_excel("raw_data/test_b_without_label.xlsx")["query"].to_list()
sup_dic = json.load(open("data/sup_dic.json","r"))
submit = [line.strip() for line in open("api_post.jsonl","r")]
tmp = [json.loads(line.strip()) for line in open("data/ner_result.jsonl","r")]
dic = {x["query"]:x["parse"]["entity"] for x in tmp}

assert len(test_qs)==len(submit)

with open("finanal_submit_file.jsonl","w") as f:
    for item,q in zip(submit,test_qs):
        try:
            item = json.loads(item)
        except:
            f.write("{}\n".format(item))
            continue
        apis = item["relevant APIs"]
        if len([x for x in apis if x["api_name"]=="查询代码"])>0:
            assert apis[0]["api_name"]=="查询代码"
            assert len(apis[0]["required_parameters"][0])==1
            old_biaodi = apis[0]["required_parameters"][0][0]
            parse_data = dic[q]
            if len(parse_data)==0:
                f.write("{}\n".format(json.dumps(item,ensure_ascii=False)))
                continue
            biaodi_type = apis[0]["tool_name"][:2]
            if parse_data[0] in sup_dic and old_biaodi==sup_dic[parse_data[0]][0][0]:
                f.write("{}\n".format(json.dumps(item,ensure_ascii=False)))
                continue
            new_biaodi = match_ent(parse_data[0],biaodi_type)
            if old_biaodi not in standard and new_biaodi:
            # if old_biaodi!= new_biaodi and new_biaodi:
                cn+=1
                # print("{}\t{}\t{}".format(parse_data[0],old_biaodi,new_biaodi))
                apis[0]["required_parameters"][0][0] = new_biaodi
                item["relevant APIs"] = apis
                f.write("{}\n".format(json.dumps(item,ensure_ascii=False)))
                continue
                
        f.write("{}\n".format(json.dumps(item,ensure_ascii=False)))

