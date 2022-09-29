import re
def extract_outline_info(raw_data):
    result = {}
    line4 = 0
    try:
        for item in raw_data:
            if str(item['text']).rfind('No') != -1:
                result['Number1'] = str(item['text'])[:7]
                result['Number2'] = str(item['text'])[8:]
                
            elif str(item['text']).isnumeric() == True and len(str(item['text']))> 5:
                if len(str(item['text']))== 8:
                    result['Number1'] = str(item['text'])
                elif len(str(item['text']))== 10:
                    result['Number2'] = str(item['text'])
            if str(item['text']).rfind('收款人') != -1:
                result['receive_man']  = str(item['text'])[4:]
            elif str(item['text']).rfind('复核') != -1:   
                result['check_man']  = str(item['text'])[3:]
                line4 = item['text_region'][0][1]
            elif str(item['text']).rfind('开票人') != -1:
                result['open_man']  = str(item['text'])[4:]     
            elif str(item['text']).rfind('年') != -1:
                p = str(item['text']).rfind('年')-4
                result['date']  = str(item['text'])[p:]
    except:
        print('Extract Outline Info Routin Error')
        return {}
    return result,line4
def is_valid_crypto(pwd):
    chars = set('0123456789*-+/<>')
    return all(c in chars for c in pwd)
def extract_crypto_info(primary_data):
    result = ""
    first_line_posx = 0
    first_line_posy = 0
    try:
        for item in primary_data:
            if str(item['text']).isdigit() == False and is_valid_crypto(str(item['text'])) == True and len(str(item['text'])) > 5:
                if first_line_posx == 0: 
                        first_line_posx = item['text_region'][0][1]
                        first_line_posy = item['text_region'][0][0]
                result +=  str(item['text'])
    except:
           print('Extract Crypto Info Routin Error')
           return ''        
    return result,first_line_posx,first_line_posy
def sortFun(e):
    return e['pos']
def get_row_items(line_pos,data):
    result = []
    try:
        for item in data:
            if item['text_region'][0][1]  > line_pos - 10 and item['text_region'][0][1] <line_pos + 10 :
                    result.append({'text' :item['text'] ,'pos' : item['text_region'][0][0]})  
    except:
        print('Get Row Items Routin Error')
        return []
    result.sort(key = sortFun)
    return result
def extract_table_info(primary_data):
    second_line_pos = 0
    result = []
    try:
        for item in primary_data:
            if str(item['text']).rfind('%') != -1:
                if second_line_pos == 0: second_line_pos = item['text_region'][0][1]
                result.append(get_row_items(item['text_region'][0][1],primary_data))
    except:
        print('Extract Table Info Routin Error')
        return []
    return result,second_line_pos
def extract_table_head_info(line1,line2,primary_data):
    result = []
    try:
        for item in primary_data:
            if item['text_region'][0][1] > line1 and item['text_region'][0][1] < line2 and is_valid_crypto(str(item['text'])) == False and len(item['text']) > 5 :
                result.append({'text':item['text'],'pos':item['text_region'][0][1]})
        result.sort(key=sortFun)
    except:
        print('Extract Table Head Info Routin Error')
        return []
    if len(result) == 0: return []
    if result[0]['pos'] - line1 > 20: result.insert(0,{'text':'','pos':line1})
    return result
def get_money_value(primary_data):
    result = []
    line3 = 0
    try:
        for item in primary_data:
            if item['text'].rfind('￥') != -1:
                if line3 == 0:
                    line3 = item['text_region'][0][1]
                result.append(item['text'][(item['text'].rfind('￥')+1):])
    except:
        print('Get Money Routin Error')
        return []
    return result,line3
def extract_table_foot_info(line1,line2,line3,primary_data):
    result = []
    try:
        for item in primary_data:
            if item['text_region'][0][1] > line1 and item['text_region'][0][1] <line2 and  item['text_region'][0][0] <line3:
                    result.append({'text':item['text'],'pos':item['text_region'][0][1]})
    except:
        print('Extract_Table_Foot_InFo Routin Error')
        return []
    result.sort(key=sortFun)
    return result
def get_table_data(raw_data,primary_data):
    crypto_data,line1,line5 = extract_crypto_info(primary_data)
    money_data,line3 = get_money_value(primary_data)
    top_left_data,line4 = extract_outline_info(raw_data)
    table_body,line2 = extract_table_info(primary_data)
    table_foot = extract_table_foot_info(line3-10,line4-20,line5,primary_data)
    table_head = extract_table_head_info(line1-10,line2-30,primary_data)
    result = {}
    result['crypto'] = crypto_data
    result['money'] = money_data
    result['root_data'] = top_left_data
    result['table_body'] = table_body
    result['receiver_data'] = table_foot
    result['sender_data'] = table_head
    print(result)
    return result
#print(raw_data)
# raw_data = torch.load('Data1.txt')
# primary_data = torch.load('Data2.txt')
# get_table_data(raw_data,primary_data)