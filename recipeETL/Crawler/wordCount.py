import re, sys, json

from cleanQty import qtyCleaner
from cleanIngred import ingredCleaner

folders = ["低脂","生酮","低醣","沙拉","高蛋白","健身","高纖"]

cntTotal = 0
cntProcs = 0
foodList = []
foodFreq = {}

nClean = int(sys.argv[1])  if len(sys.argv) > 1 else 4
bVerb  = bool(sys.argv[2]) if len(sys.argv) > 2 else False

def load_ID(path):
    ID_file = path
    ID_dict = set()
    try:
        with open(ID_file, "r", encoding='utf-8') as f:
            for line in f:
                ID_dict.add(line.replace('\n', ''))
    except:
        print('No excluding list loaded.')
    return ID_dict

ignore_IDs = load_ID('ID_exclude.txt')
skip_IDs = set()

iCleaner = ingredCleaner()
qCleaner = qtyCleaner()

def procIngrdent(food_ID, ingreds, bVerb=bVerb, nClean=nClean):
    global foodList, foodFreq, cntTotal
    global iCleaner

    x = {}     # to avoid change ingreds in for-loop
    for food, qty in ingreds.items():  # 抓出"食譜"中的所有 key 和 值
        if nClean:
            nfood = iCleaner.clean(food_ID, food, bVerb=bVerb, nClean=nClean)
            qty_unit = qCleaner.clean(food_ID, qty, bVerb=bVerb)
        else:
            qty_unit = qty
            nfood    = food

        if iCleaner.checkSkip(food_ID, nfood, qty_unit, bVerb=True) > 0:
            skip_IDs.add(food_ID)
            # continue

        # 計算食材出現詞頻
        if nfood in foodList:
            foodFreq[nfood] += 1
        else:
            foodFreq[nfood] = 1
        foodList.append(nfood)
        #print(food) # 所有食材
        x[nfood] = qty_unit
    return x

xf1 = open('./clr-Long.txt', 'w', encoding='utf-8')
xf2 = open('./clr-Short.txt', 'w', encoding='utf-8')
for i in folders:
    with open(f'{i}/{i}.txt', 'r', encoding='utf-8') as f:
        for line in f:              # 使用迴圈方式一條一條抓
            data = json.loads(line)

            cntTotal += 1
            food_ID = data['food_ID']
            if food_ID not in ignore_IDs:
                data['推讚數'] = qCleaner.parseNumber(data['推讚數'])
                data['瀏覽數'] = qCleaner.parseNumber(data['瀏覽數'])
                data['份數']   = qCleaner.parseNumber(data['份數'])
                data['食譜']   = procIngrdent(food_ID, data['食譜'], bVerb=bVerb, nClean=nClean)
                cntProcs += 1
                xf1.write(json.dumps(data, ensure_ascii=False)+'\n')
                xf2.write(json.dumps({'id':food_ID, 'ingredents':data['食譜']}, ensure_ascii=False)+'\n')
xf1.close()
xf2.close()

skipA, skipB, skipC = iCleaner.getSkip()
print(f"少許:{len(skipA)}\nList:{skipA}\n\n適量:{len(skipB)}\nList:{skipB}\n\n空白:{len(skipC)}\nList:{skipC}\n")
print(f'To Skip:{len(skip_IDs)}\nList:{skip_IDs}')

print(len(foodList)) # 總共多少食材
print(cntTotal, cntProcs) # 總共幾個食譜


# 詞頻轉成表格
import pandas as pd
df = pd.DataFrame.from_dict(foodFreq, orient='index', columns=['詞頻']) # 將字典轉為表格

# df = df.sort_index(ascending=False)
# df.to_csv("照食材順序排的food_frequency_2.0.csv", encoding="utf-8-sig")

df = df.sort_values(by='詞頻', ascending=False) # 照"詞頻"這欄的值，由大到小做排列 ascending=False
df.to_csv("照詞頻順序排的food_frequency_2.0.csv", encoding="utf-8-sig")
