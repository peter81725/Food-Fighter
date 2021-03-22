import re

class ZhcnSynonym():
    _cnChar = list("仼优兰刴发咸国圣块坚塩头姜嫰岛庄徳择掦无柠榄殻温湿炼猕现瑶盐筛籮类緑红绿苹荀荞葱蓝蔴蕯虾记调辢过选酱针铃铝铺锦门韮须饺马鱼鲍鲜鳯鸡麦黄黒龙⽔")
    # 必需手動修改 '姜'->'薑', '籮'->'蘿', '荀'->'筍', 並加上 '⽔'->'水', 單一個字 convertZ.exe 無整轉換出我們要的繁體字 twChar
    _twChar = list("任優蘭剁發鹹國聖塊堅鹽頭薑嫩島莊德擇揚無檸欖殼溫濕煉獼現瑤鹽篩蘿類綠紅綠蘋筍蕎蔥藍麻薩蝦記調辣過選醬針鈴鋁鋪錦門韭須餃馬魚鮑鮮鳳雞麥黃黑龍水")

    # '干' 不單一字轉, 改用詞
    _cn2twWord = {
        '豆乾': '豆干',
        '魚乾': '魚干',
        '梅乾': '梅干',
        '菜乾': '菜干',
        '肉乾': '肉干',
        '乾果': '干果',
        # '干貝': '乾貝',
        '葡萄乾': '葡萄干',
        '芥末': '芥苿',
        '豆豉': '豆鼓',
        '伍斯特辣醬': '喼汁',
        '豬鍵子': '豬𦟌肉',
        '牛鍵': '牛𦟌肉',
        '豬鍵': '豬𦟌',
        '牛鍵': '牛𦟌',
        # '伊籐': '伊藤',
        '蘿蔔': '萝卜',
        '菠蘿': '菠萝',
        '麵粉': '面粉',
        '麵包': '面包',
        '龍鬚麵': '龍須面',
        '義大利':'意大利',
        '義式': '意式',
        }

    _ChiSym1 = [
        '（','［','〔','﹝','【','「','＜','〈','《','『',
        '）','］','〕','﹞','】','」','＞','〉','》','』',
        '／','％','’','　','＊','*','•','◆','￼','。',
        ':', '；', ',', '，' ]
    _ChiSym2 = [
        '(', '[', '[', '[', '[', '[', '[', '[', '[', '[',
        ')', ']', ']', ']', ']', ']', ']', ']', ']', ']',
        '/', '%', "'", '',  '',  '',  '',  '', '', '',
        '：', '：', '、', '、' ]

    def _cvtChar(self, ch):
        if ch in self._cnChar:
            return self._twChar[self._cnChar.index(ch)]
        return ch

    def parseWord(self, line):
        line = "".join([self._cvtChar(ch) for ch in line]).strip()
        # Loop until no more cnWords
        while True:
            for twW, cnW in self._cn2twWord.items():
                if cnW in line:
                    line = line.replace(cnW, twW)
                    # break
            else:
                break
        return line


    def _cvtSym(self, ch):
        if ch in self._ChiSym1:
            return self._ChiSym2[self._ChiSym1.index(ch)]
        return ch

    def parseSymbol(self, line):
        return "".join([self._cvtSym(ch) for ch in line]).strip()


class EngSynonym():
    # 可以直接刪掉名字的品牌
    # 會處理後面的 空白
    _brandList = [
        'bodykey',
        'bragg',
        # "mozzarella",
        'iherb',
        'costco',
        'classico',
        'pb2',
        'sweet relish',
        'granola',
        'zespri',
        'spark shake',
        'sparkshake',
        'real salt',
        's&b',
        # 's&b ',
        'redlentil',
        'ikea',
        'roquette',
        'kewpie',

    ]

    # 用於 英翻中 並刪除重覆, 故需要多個 '譯名'
    # 1st: 用於 英翻中 (無中文)
    # 2nd~: 用於 刪除重覆, 即直接將英文刪除.
    # 之後 還要用 typoSyn 將用詞統一
    # 注意: 英文請全部用小寫
    Synonym = {
        # 品牌
        'bocconcini':   ['博康奇尼'],
        'havarti':      ['哈瓦蒂'],
        'havati':       ['哈瓦蒂'],
        'mascarpone':   ['馬斯卡彭', '馬斯卡朋'],
        'mozzarella':   ['莫札瑞拉'],
        'ricotta':      ['瑞可達起司'],
        'tabasco':      ['塔巴斯科'],
        'Ankang':       ['AK安康'],
        'special k':        ['家樂氏'],
        'specialk':         ['家樂氏'],
        'mozzarella cheese':['莫札瑞拉起司'],
        'mozzarellachease': ['莫札瑞拉起司'],
        # 食材
        # 'cream cheese': ['奶油乳酪'],
        'almond flour': ['杏仁粉'],
        'almond meal':  ['杏仁'],
        'almond':       ['杏仁'],
        'apple cider vinegar':  ['蘋果醋'],
        'apple vinegar':        ['蘋果醋'],
        'apple':        ['蘋果'],
        'applejuice':   ['蘋果果汁'],
        'arborio rice': ['阿柏里歐米'],
        'arborio':      ['阿柏里歐'],
        'aubergine':    ['茄子'],
        'avocado oil':  ['酪梨油'],
        'avocado':      ['酪梨'],
        'avocados':     ['酪梨'],
        'baby corn':    ['玉米筍'],
        'baby leaf':    ['貝比生菜'],
        'baby spinach': ['嫩菠菜'],
        'bacon':        ['培根'],
        'bagel':        ['貝果'],
        'baking powder':['泡打粉'],
        'baking soda':  ['小蘇打粉', '蘇打粉'],
        'bakingsoda':   ['小蘇打粉'],
        'basi':         ['羅勒'],
        'basil':        ['羅勒', '羅勒葉'],
        'basils':       ['蘿勒'],
        'bay leave':    ['月桂葉'],
        'bbq sauce':    ['烤肉醬'],
        'beet':         ['甜菜'],
        'beetroot':     ['甜菜根'],
        'beets':        ['甜菜'],
        'black pepper': ['黑胡椒', '黑椒'],
        'blackpepper':  ['黑胡椒'],
        'blue cheese':  ['藍莓芝士'],
        'boiled potato':['熟馬鈴薯', '熟薯'],
        'broad beans':  ['蠶豆'],
        'caeyne pepper':    ['卡宴辣椒'],
        'cajun':            ['肯瓊'],
        'cakeflour':        ['低筋麵粉'],
        'cannellini bean':  ['白腰豆'],
        'capsicum':     ['甜椒'],
        'carrot':       ['紅蘿蔔'],
        'carrots':      ['紅蘿蔔'],
        'cheese':       ['起司', '起士'],
        'cherrytomato': ['櫻桃茄'],
        'chia seed':    ['奇亞籽'],
        'chilli':       ['辣椒'],
        'cilantro':     ['香菜'],
        'cinnamon':     ['玉桂粉'],
        'coconut cream':['椰漿'],
        'coconut flour':['椰子粉'],
        'cooking spray':['烹飪噴霧'],
        'coriander':    ['香菜'],
        'cottage':      ['茅屋芝士'],
        'couscous':     ['庫斯庫斯', '小米'],
        'creamcheese':  ['奶油乳酪', '忌廉起司', '忌廉芝士'],
        'cucumber':     ['小黃瓜'],
        'cumin':        ['孜然', '小茴香'],
        'cumin seed':   ['小茴香籽'],
        'curly parsley':['洋香芹'],
        'dill':         ['時蘿'],
        'double espresso':  ['義式濃縮咖啡'],
        'egg':              ['雞蛋', '蛋'],
        'erythritol':       ['赤藻糖醇'],
        'feta cheese':      ['菲達起司', '費達起司', '菲達乳酪'],
        'feta':             ['菲達', '費塔', '菲達起司'],
        'fish sause':       ['魚露'],
        'flaxseed meal':    ['亞麻籽粉'],
        'fresh flat-leaf parsley': ['新鮮洋香菜'],
        'fresh rosemary':   ['新鮮迷迭香'],
        'fennel':           ['茴香'],
        'garbanzo bean':    ['鷹嘴豆'],
        'garlic':       ['大蒜'],
        'ghee':         ['酥油', '無水奶油'],
        'greek':        ['希臘'],
        'green apple':  ['青蘋果'],
        'green onions': ['綠蔥'],
        'greenpeace':   ['豌豆'],
        'haloumi':      ['哈羅米'],
        'ham':          ['火腿'],
        'hersheys cocoa':   ['無糖純可可粉'],     # 去品牌名
        'himalayan salt':   ['玫瑰鹽'],
        'hummus':           ['鷹嘴豆泥'],
        'horseradish':  ['辣根'],
        'jalapeno':     ['墨西哥辣椒'],
        'kewpie bb':    ['BB'],
        'ketchup':      ['番茄醬'],
        'kidney bean':  ['白腰豆'],
        'lemon juice':  ['檸檬汁'],
        'lemon':        ['檸檬'],
        'lemongrass':   ['香茅'],
        'lettuce':      ['萵苣', '羅馬生菜'],
        'lime juice':   ['檸檬汁'],
        'lime leave':   ['檸檬葉'],
        'marsala wine': ['馬沙拉酒'],
        'masala':       ['瑪撒拉'],
        'maydanoz':     ['香菜'],
        'mayonnaise':   ['美乃茲'],
        'mazurella cheese': ['馬自瑞拉起司'],
        'meat masala':      ['瑪撒拉香料'],
        'milk':         ['牛奶'],
        'mixed nuts':   ['混合堅果'],
        'mustard':      ['芥末'],
        'oatbran':      ['燕麥麩'],
        'oats':         ['燕麥'],
        'oil':          ['蔬菜油', '油'],
        'olive oil':    ['橄欖油'],
        'onion':        ['洋蔥'],
        'or couscous':  ['or小米'],
        'orbalsamic':   ['or義大利香黑'],
        'paprika':      ['甜椒粉', '紅甜椒粉', '煙燻紅椒粉'],
        'pasta':        ['義大利麵'],
        'peas':         ['青豆'],
        'pepper':       ['胡椒'],
        'persil':       ['巴西里', '巴西裏', '巴西裡'],
        'pickled':      ['醃瓜類'],
        'pinksalmon':   ['罐頭鮭魚'],
        'potato':       ['馬鈴薯'],
        'potatoes':     ['馬鈴薯'],
        'psyllium husk':['洋車前子'],
        'quinoa':       ['藜麥'],
        'radish':       ['小紅蘿蔔'],
        'red capsicum': ['紅椒'],
        'red onion':    ['紅洋蔥'],
        'roma tomato':  ['小番茄'],
        'salsa sauce':  ['莎莎醬'],
        'salt':         ['鹽'],
        'seaweed':      ['海苔'],
        'see weed':     ['海苔'],
        'small vine':       ['小番茄'],
        'smallgreenapple':  ['青蘋果小'],
        'sour cream':   ['酸奶油', '酸奶'],
        'sourcream':    ['酸奶油', '酸忌廉'],
        'stevia':       ['甜菊'],
        'sugar':        ['糖'],
        'sungold':      ['黃金'],
        'swedish shrimp':   ['瑞典蝦'],
        'sweet marsala wine':   ['瑪薩拉酒', '甜馬沙拉酒'],
        'sweetener':        ['甘味劑'],
        'tumeric':          ['薑黃'],
        'thyme':            ['百里香'],
        'tomato':           ['番茄'],
        'tomatoe':          ['番茄'],
        'unsalted butter':  ['無鹽奶油'],
        'vanilla extract':  ['香草精'],
        'vanillaextract':   ['香草精'],
        'vinegar':          ['醋'],
        'w pepper pw':      ['白胡椒粉'],
        'walnut':           ['核桃'],
        'wasabi':           ['山葵', '山葵醬'],
        'water':            ['水'],
        'whipping cream':   ['淡奶油'],
        'white sugar':      ['白糖'],
        'wholewheatflour':  ['全麥麵粉'],
        'worcestershire':   ['伍斯特辣醬'],
        'ylw capsicum':     ['黃椒'],
        'young coconut':    ['椰青'],
        'zucchini':         ['櫛瓜', '翠玉瓜'],

        # '': [''],
        # '': [''],
        # '': [''],
        # '': [''],
    }
    def __init__(self):
        pass

    def replaceBrand(self, value):
        pass


    _rgx7 = re.compile(r'([\u3001\u4e00-\u9fa5\uFF01-\uFF5E]+)')
    # _rgx8 = re.compile(r'\(?([a-z][a-z& ]+)\)', re.I)
    _rgx8 = re.compile(r'([a-z][a-z2& ]+)', re.I)
    _rgx9 = re.compile(r'\((?:[\u4e00-\u9fa5]*)?\s*([a-z][a-z2& ]+)(?:[\u4e00-\u9fa5]*)?\)', re.I)


    def _searchMore(self, idx, vstr):
        if idx > vstr.find('(') > 0:
            mat = self._rgx9.search(vstr)
            return '' if not mat else mat.group(1)
        else:
            mat = self._rgx8.search(vstr[idx:])
            return '' if not mat else mat.group(1)


    def replaceTran(self, vstr):

        # if '牛番茄or大番茄tomato' in vstr:
        #     print('1')
        sidx = 0
        midx = 0
        while True:
            mat = self._rgx8.search(vstr[sidx:])
            if not mat:     break

            word = mat.group(1).strip().lower()
            # if '牛番茄or大番茄tomato' in vstr:
            #     print('1')
            if word in self._brandList:
                return vstr.replace(self._searchMore(midx, vstr), '')
            if word in self.Synonym:
                trans = self.Synonym[word]
                for tran in trans:
                    if tran in vstr:
                        return vstr.replace(self._searchMore(midx, vstr), '')
                else:
                    return vstr.replace(self._searchMore(midx, vstr), trans[0])
            sidx += mat.end(0)
            midx = sidx + mat.start(0)
        return vstr


class TypoSyn():
    # 注意1: 不會處理字尾空白. 意思是有時必需加空白才會拿掉
    # value list 大寫會自動轉小寫
    typoDict = {
        '塔巴斯科辣椒醬': ['tabasco醬', 'tabasco辣醬', 'tabasco辣椒調味醬', 'tabasco'],
        '奶油乳酪': ['乳酪cream cheese', '乳脂cream cheese', '忌廉起司', '忌廉芝士', 'cream cheese'],
        '酸奶油': ['酸忌廉'],
        '異麥芽寡糖粉': ['vitafiber異麥芽寡糖粉'],
        '膳食纖維粉': ['vitafiber'],
        '牛番茄': ['大肉茄番茄'],
        '奶酪乾': ['jerky 起司'],
        '家樂氏原味香脆麥米片': ['家樂氏麥米片', '家樂氏原味米麥片', '家樂氏原味麥米片', '家樂氏香脆麥米片原味', '家樂氏香脆麥米片'],
        '義大利香黑醋': ["義大利黑醋", "balsamico", "香油酢(balsamic vinegar)", "balsamic 醋",
                "balsamico 葡萄酒醋", "義大利香黑醋", "巴薩米克黑醋", "義式香醋balsamic",
                "巴沙米可醋 balsamic vinegar", "balsamico紅酒醋", "黑醋 balsamic vinegar",
                "義式黑醋", "巴薩米可醋balsamic", "義式黑醋", "巴薩米克醋balsamic", 'balsamique',
                "黑醋balsamic", "balsamic醬", "紅酒醋(balsamic)", "balsamico(紅酒醋)",
                "義大利甜醋balsamicvinegar", 'balsamic vinegar'],
        '巴薩米克': ["巴薩米克(balsamico)", "巴沙米可", "巴沙米克", "巴沙米哥", "巴塞米",
                "巴撒米可", "巴撒米克", "巴薩米可", "巴薩米克", "巴薩米"],
        '香芹': ['香草 parsley', '香草 parsley', '歐芹', '歐芹parsley', '香芹parsley', '香菜parsley'],
        '莫札瑞拉':['馬扎瑞拉', '馬自瑞拉', '馬芝瑞拉', '馬茲瑞拉', '馬茲摩拉', '馬茲羅拉', '馬蘇里拉',
                '莫扎瑞拉', '莫左瑞拉', '莫札瑞拉', '莫札雷拉', '莫拉瑞拉', '莫茲瑞拉', '莫薩里拉',
                '瑪芝瑞拉', '瑪茲瑞拉'],
        '布拉塔': ['水牛乳酪  burrata  mozzarella'],
        '菲達起司': ['菲達乳酪', '費他乳酪', '費塔起司', '費達起司', '費塔乳酪'],
        '黃金奇異果': ['zespri sun gold奇異果'],
        '低卡可樂':   ['zero 可樂'],
        '藜麥':      ['quinoa藜米'],
        '帕馬森乾酪':   ['parmigiano起司'],
        '桂冠沙拉 light':  ['桂冠light沙拉', '桂冠沙拉light', '桂冠沙拉 light', '沙拉 light醬', '沙拉醬Light', 'light沙拉醬'],
        '蝴蝶麵':      ['義大利麵bowtiepasta'],
        '奧勒岡葉':    ['乾牛至oregano'],
        '水管麵':      ['義大利麵gigantoni'],
        '鷹嘴豆':      ['chickpea', '罐頭豆chick peas'],
        '煙燻辣椒':   ['辣椒醬chipotle', '煙燻辣椒chipotle', 'Chipotle 煙燻辣椒'],
        '越南春捲皮':   ['越南米紙springrollskin'],
        '黃芥未醬': ['第戎芥末醬 Dijon Mustard', '黃芥末醬 dijon'],
        '頂級初榨橄欖油': ['橄欖油extra virgin', '橄欖油dxtraVirgin', 'ex橄欖油', 'extra virgin橄欖油',
                    'extra virgin olive oil', 'extra olive virgin oil', 'DOP頂級初榨橄油'],
        'OmniPork ':  ['omnipork'],
        'MyProtein ': ['myprotein ', 'myprotein'],
        # '低卡可樂': ['zero', '纖維可樂'],
        # '汽水': ['雪碧'],
        '起司': ['起士', '芝士'],
        '小卷': ['小捲'],
        '帆立貝': ['凡立貝'],
        '燻雞': ['燻g'],
        '雞蛋': ['g蛋'],
        '春捲': ['春卷'],
        '綠捲': ['綠卷'],
        '蘿蔓': ['羅曼', '蘿曼'], 
        '蘿美': ['羅美', '美蘿心'],
        '芫荽': ['芫茜', '鹽須'],
        '番茄': ['蕃茄', '西紅柿'],
        '番荽': ['蕃荽', '胡妥', '胡荽'],
        # '梨子': ['雪梨'],
        # '檸檬': ['青寧', '台灣好田'],
        # '芒果': ['青芒'],
        # '草莓': ['士多啤梨'],
        # '柚子': ['文旦'],
        # '奇異果': ['猕猴桃'],
        '苜宿芽': ['暮宿芽', '目蓿芽'],
        '蔓越莓': ['蔓越梅', '蔓樾莓', '蔓岳莓'],
        '核桃': ['胡桃'],
        # '杏仁': ['南北杏', '南杏'],
        '葵花籽': ['葵花子'],
        '大麻籽': ['大麻子'],
        # '亞麻': ['胡麻'],
        '亞麻籽': ['亞麻子'],
        '奇亞籽': ['奇亞子', '奇芽籽', '奇芽子', '奇牙籽', '奇牙子'],
        '奧勒岡': ['奧利岡', '俄力岡'],
        # '穀片': ['穀物片'],
        '庫斯庫斯': ['庫司庫司'],
        '玉米': ['玉蜀黍'],
        '番薯': ['蕃薯', '甘薯', '甘藷', '地瓜', '沙葛'],
        '蒔蘿': ['洋茴香'],
        '車前': ['前車'],
        '芥末': ['芥苿'],
        '芥末籽': ['芥末子', '芥末仔'],
        '莎莎醬': ['salsa醬'],
        '馬斯卡彭': ['馬斯卡朋', '馬斯卡邦'],
        '凱撒': ['凱薩', '凱薩琳'],
        '鹽': ['塩', '盬', '塩巴', '鹽巴'],
        '煉乳': ['煉奶', '練奶', '炼奶'],
        '橄欖': ['橄榄', '橄㰖', '橄欄'],
        '薄菏': ['簿荷', '薄盒'],
        '藍莓': ['藍黴'],
        '煙燻': ['煙熏'],
        '荸薺': ['荸齊'],
        '蒟蒻': ['蒟篛'],
        '巴西里': ['巴西利', '巴西裏', '巴西裡'],
        '蘇打': ['梳打'],
        '花椰菜': ['西蘭花'],
        '香吉士': ['香桔士'],
        '蛤蜊': ['蛤蠣', '蛤利', '蛤仔'],
    }

    def __init__(self):
        self._lookup = {}
        for item, values in self.typoDict.items():
            # if '起司' == item:
            #     print('1')
            for val in values:
                self._lookup[val.lower()] = item
        self._lookup = sorted(self._lookup.items(), key=lambda x:len(x[0]), reverse=True)

    def replaceTypo(self, value):
        # if '焦糖乳清' in value:
        #     print('1')
        lowerV = value.lower()
        count = 0
        while True:
            for typo, key in self._lookup:
                if typo in lowerV:
                    lowerV = lowerV.replace(typo, key)
                    count += 1
            else:
                break
        if count > 0:
            return lowerV
        return value

class groupSyn():
    # 別名 或 同一類食材
    Synonym = [
        "蔘鬚",
        "黃耆",
        "熟地",
        "甘草",
        "枸杞",

        "伏特加",
        "白蘭地",
        "威士忌",
        "低卡可樂",
        "可樂",
        "汽水",
       ["優格"],
        "養樂多",
        "冰淇淋",
       ["黃布丁", "布丁"],

        "海鮮",
        "小卷",
        "軟絲",
        "牡蠣",
        "干貝",
        "扇貝",
        "昆布",
        "明太子",
        "火鍋料",
       ["魚翅", "北海翅"],
       ["鮭魚", "鱒澳鱸"],
       ["鰻魚", "蒲燒鰻"],

       ["小卷", "小管", "鎖管", "中卷", "透抽"],
       ["牡蠣", "蚵仔", "生蠔", "蠔"],
       ["干貝", "瑤柱", "帶子粒"],
       ["鮮貝", "帶子", "沙插", "騷蛤"],
       ["扇貝", "凡立貝", "帆立貝"],
        "漢堡排",
        "排骨",
        "叉燒",
       ["豬肉", "火鍋片"],
       ["雞胸肉", "金豐盛", "燻雞"],
        "雞蛋",
       ["高蛋白", "protein"],
       ["羊肉", "羊排"],
        "肉乾",

       ["麵", "雁门清高黑苦荞全麦龙须面"],
       ["麵包", "漢堡包", "軟法", "餐包", "銀絲卷", "三文治方", "新英格蘭堡", "義美馬芬堡", "馬芬堡", "義美馬芬"],
        "饅頭",

       ["麵皮", "餛飩皮"],
       ["春捲皮"],
       ["塔皮", "派皮"],

       ["乾酪", "帕馬森"],
       ["乳酪", "起司", "瑞可達", "博康奇尼", "莫札瑞拉", "馬斯卡彭", "布拉塔", "哈瓦蒂"],
       ["無鹽奶油", "忌廉", "動鮮"],
       ["鮮奶油"],
       ["淡奶油"],
       ["低脂起司", "低脂莫札瑞拉"],
       ["奶油"],
       ['酥油', '無水奶油'],

       ["餅乾", "OREO", "洋芋片", "樂事原味波卡", "浪味仙", "奇多"],
       ["巧克力", "Hersheys", "COCO"],

       ["蔬菜", "綠橡木葉", "時蔬", "冰山綠火焰", "韭黃", "青花苔", "大陸妹", "花椰菜", "過貓"],
        "綠卷",
        "豆芽菜",
        "九層塔",
        "胡蘿蔔",
       ["蘿蔓", "蘿美"],
        "羅望子",
       ["豆芽菜", "銀芽"],
       ["九層塔", "蘿勒"],
       ["胡蘿蔔", "紅蘿絲", "紅蘿蔔", "甘荀"],

       ["香菜", "芫荽"],
       ["洋香菜", "番荽"],

       ["大番茄", "牛番茄"],
       ["小番茄", "車厘茄", "聖女番茄", "櫻桃茄"],
        "蘋果",
       ["鳳梨", "蘿菠"],
        "草莓",
        "梨子",
        "榴槤",
        "檸檬",
        "櫻桃",
        "波羅蜜",
        "芒果",
        "李子",
        "柚子",
        "桑葚",
        "石榴",
        "奇異果",
        "酪梨",
        "栗子",
        "蔓越梅",

       ["果乾", "蔓越梅乾"],
       ["梅子", "烏梅", "梅乾"],

        "堅果",
        "葵花籽",
        "核桃",
        "杏仁",
        "大麻籽",
        "亞麻籽",
        "奇亞籽",
       ["麥片", "穀片"],

       ['小米', '庫斯庫斯'],
        "玉米",
        "甘薯",
        "荸薺",
        "菱角",
        "蓮藕",
        "蓮子",
        "芋頭",
        "天貝",
        "千張",
        "洋芋",
       ["蒟蒻絲", "魔芋面", "魔芋麵", "芋絲", "蒟蒻", "寒天"],
       ["辣木", "青汁"],
       ["洋芋", "馬鈴薯"],
       ["白木耳", "銀耳", "雪耳"],

        "鷹嘴豆",
        "蠶豆",

        "蒔蘿",
       ["食用花", "花片", "茉莉", "鼠尾草"],
        "甜菊",
        "梔子花",
        "香蜂草", 
        "斑蘭",
        "薄菏",
        "番紅花",
       ["香莢蘭", "雲呢拿"],

       ["發粉", "泡打粉"],
        "尾冬骨",
       ["明膠", "洋菜", "吉利丁", "果凍粉", "膠粉"],
       ["木耳", "銀耳"],
        "松茸",
        "松露",
        "玉子燒",
        "紅珊瑚",
       ["發泡錠","維他命C"],
        "腐皮",

        "奧勒岡",
       ["車前子", "洋車前"],
       ["香料", "葛縷子", "葫蘆巴", "香莢蘭"],
       ["孜然", "小茴香"],
        "茴香",
        "香茅",
        "紫蘇",
        "月桂",
        "八角", 
        "蒔蘿",
        "丁香",
        "卡菲萊姆葉",

        "山葵",
        "辣根",

       ["美乃滋", "KEPIE"],
        "莎莎醬",

       ["調味料", "滷汁包", "風味料", "鮮味炒手", "自然鮮", "滷包"],
       ["高湯塊", "麻辣鍋底"],
       ["味精", "味素"],
       ["醋", "巴薩米克醋", "義大利香黑醋"],
       ["醬料", "老乾媽"],
       ["醬油", "滷汁"],
       ["山葵", "綠芥末", "哇沙米"],
        "蔭豉",
        "破布子",
        "龍眼蜜",
        ]

    def __init__(self):
        self.dict = {}
        # dicN = {}
        for item in self.Synonym:
            if isinstance(item, list):
                self.dict[item[0]] = item[:]
                ## Todo: 字串長的先作, 再作短字串
                # for i in item:
                #     ilen = str(len(i)).zfill(2)
                #     if not ilen in dicN:
                #         dicN[ilen]=[[i,item[0]]]
                #     else:
                #         dicN[ilen].append([i,item[0]])
            else:
                self.dict[item] = [item]
        # self.dicN = [dicN[i] for i in keys()]


    def lookup(self, item, values):
        for sym in values:
            if sym == item:
                return True, False
            elif sym in item:
                return True, True
        else:
            return False, False
    
    def lookups(self, item, item_norm):
        for key, values in self.dict.items():
            bFind, bAppend = self.lookup(item_norm, values)
            if bFind:
                if bAppend or item_norm != item:
                    self.dict[key].append(item)
                # if item_norm != item:
                #     print('1')
                break
        else:
            print('NG', item)
