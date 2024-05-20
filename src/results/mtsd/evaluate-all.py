import json
import numpy as np
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_fscore_support
import json
import glob
import os     
import sys
LABEL2IDX={'FAVOR':1,'AGAINST':0,'NEUTRAL':2}

def extract(pred,f):
    pred = pred.lower()
    pred=pred.lower().split('the attitude of the sentence')[-1] 
    pred = pred.lower().split('final answer')[-1].replace('favor or against','')
    if 'trump' in f:
        if 'favor' in pred and not 'against' in pred and not 'neutral' in pred:
            return 'FAVOR'
        elif 'against' in pred  and not 'favor' in pred and not 'neutral' in pred:
            return 'AGAINST'
        elif 'neutral' in pred  and not 'favor' in pred and not 'against' in pred:
            return 'NEUTRAL'
        else:
            # print(pred)
            # aa=input()
            return 'AGAINST'
    elif 'hillary' in f:
        if 'favor' in pred and not 'against' in pred and not 'neutral' in pred:
            return 'FAVOR'
        elif 'against' in pred  and not 'favor' in pred and not 'neutral' in pred:
            return 'AGAINST'
        elif 'neutral' in pred  and not 'favor' in pred and not 'against' in pred:
            return 'NEUTRAL'
        else:
            # print(pred)
            # aa=input()
            return 'AGAINST'
    elif 'bernie' in f:
        if 'favor' in pred and not 'against' in pred and not 'neutral' in pred:
            return 'FAVOR'
        elif 'against' in pred  and not 'favor' in pred and not 'neutral' in pred:
            return 'AGAINST'
        elif 'neutral' in pred  and not 'favor' in pred and not 'against' in pred:
            return 'NEUTRAL'
        elif 'towards Bernie Sanders is likely against' in pred:
            return 'AGAINST'
        else:
            # print(pred)
            # aa=input()
            return 'AGAINST'
    elif 'ted' in f:
        if 'favor' in pred and not 'against' in pred and not 'neutral' in pred:
            return 'FAVOR'
        elif 'against' in pred  and not 'favor' in pred and not 'neutral' in pred:
            return 'AGAINST'
        # elif 'neutral' in pred  and not 'favor' in pred and not 'against' in pred:
        #     return 'NEUTRAL'
        else:
            # print(pred)
            # aa=input()
            return 'AGAINST'
ll=[]        
with open('./predix.text','r') as f:
    for line in f.readlines():
        # print(line.strip())
        ll.append(line.strip())
        # aa=input()
print(ll)
# PATH='./result/dvc003_acc10-2_'
# path='./result/'
# for file in glob.glob(os.path.join(path,"*test_trump_th_2way.json")):
#     file_name=os.path.basename(file)
#     print(file_name)
#     INPUT=path +file_name
all_results=[]
FILES=['test_trump_th','test_hillary_th','test_trump_tt','test_ted_tt','test_bernie_hb','test_hillary_hb']
for l in ll:
    all_res=[]
    PATH="./"+l
    for f in FILES:
        print(f)
        labels=[]
        predicts=[]
        
        test_file = open(PATH + f+'_2way.json', 'r', encoding='utf-8')
        test_data = json.load(test_file)
        for idx, test_case in enumerate(test_data):
            if test_case['Answer'] =='NEUTRAL':
                continue
            # print(test_case['Answer'])
            # print(test_case['Predict'])
            labels.append(LABEL2IDX[test_case['Answer']])
            predicts.append(LABEL2IDX[extract(test_case['Predict'],f)])

        # print(f1_score(labels,predicts,average='macro'))
        # print(f1_score(labels,predicts,average='micro'))
        
        result = precision_recall_fscore_support(np.array(labels), np.array(predicts), average=None, labels=[0,1,2], zero_division=0)
        # print(result)
        print((result[2][0]+result[2][1])/2) # average F1 score of Favor and Against
        all_res.append((result[2][0]+result[2][1])/2)
    
    all_results.append(l+"DT-HC :%.4f"%((all_res[0]+all_res[1])/2))
    all_results.append(l+"DT-TC :%.4f"%((all_res[2]+all_res[3])/2))
    all_results.append(l+"HC-BS :%.4f"%((all_res[4]+all_res[5])/2))
    print('---'*10)
    print("DT-HC :%.4f"%((all_res[0]+all_res[1])/2))
    print("DT-TC :%.4f"%((all_res[2]+all_res[3])/2))
    print("HC-BS :%.4f"%((all_res[4]+all_res[5])/2))

    print('---'*10)
    print("Avg of All :%.4f"%((((all_res[0]+all_res[1])/2)+((all_res[2]+all_res[3])/2)+((all_res[4]+all_res[5])/2))/3))

with open('00out3.json','w') as ff:
    json.dump(all_results,ff,indent=4)