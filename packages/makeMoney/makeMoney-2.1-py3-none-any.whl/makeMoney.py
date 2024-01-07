
from datetime import datetime
import pdb
import os



def get_info_list_dict(inputting_file_1):
    
    info_list_dict = {}
    all_colum_list = []
    
    with open(inputting_file_1) as f_inputting_file_1:
        
        title_list = f_inputting_file_1.readline().strip('\r\n').split('\t')
        for line in f_inputting_file_1:
            
            column_list = line.strip('\r\n').split('\t')
            
            if column_list[41] == '':
                continue            
            elif column_list[41][0] != 'A':
                continue

            all_colum_list.append(column_list)
            
            
            date = column_list[2]
            if ':' in date:
                date = date[:date.find(' ')] 
                
            convertible_debt_code = column_list[3]
            convertible_debt_name = column_list[4]
            stock_code = column_list[5]
            stock_name = column_list[6]
            
            date_format = "%Y/%m/%d"
            converted_date = datetime.strptime(date, date_format)#字符串转成时间格式
            date = converted_date.strftime(date_format)#时间格式转成字符串格式   

            if '!'in convertible_debt_name:
                convertible_debt_name = convertible_debt_name[:convertible_debt_name.find('!')]
            else:
                convertible_debt_name = convertible_debt_name
            
            key = date+'-'+convertible_debt_code+'-'+convertible_debt_name+'-'+stock_code+'-'+stock_name

            if key not in info_list_dict:
                info_list_dict[key] = [column_list]
            else:
                info_list_dict[key].append(column_list)
            # if column_list[0] == '130873':
                # pdb.set_trace()

    return info_list_dict, all_colum_list, title_list

    

def get_duplicated_lines(info_list_dict, all_colum_list, title_list):

    out = open('结果文件1-可转债数据库.csv-重复数据.xls', 'w')
    out.write('\t'.join(['重复数据是否相等', '标记', '重复次数']+title_list)+'\n')
    
    for key in info_list_dict:
        
        if len(info_list_dict[key]) > 1:
            
            if info_list_dict[key][0][2:] != info_list_dict[key][1][2:]:
                flag = '不相等'
            else:
                flag = '相等'
                
            for duplicated_line_list in info_list_dict[key]:
                line_list = [flag, key, str(len(info_list_dict[key]))] + duplicated_line_list
                
                out.write('\t'.join(line_list)+'\n')
                
    out.close()



def get_date_list(info_list_dict):
    
    date_list = []
    converted_date_list = []
    sorted_converted_date_list = []
    iteration_date_list = []
    
    for key in info_list_dict:
        
        key_list = key.split('-')
        
        date = key_list[0]
        
        date_list.append(date)
        
    out = open('结果文件2-日期中间数据验证.txt.xls', 'w')
    
    for date in date_list:
        
        date_format = "%Y/%m/%d"
        converted_date = datetime.strptime(date, date_format)
        converted_date_list.append(converted_date)
        #out.write(date+'\n')
        
    sorted_converted_date_list = sorted(converted_date_list)
    
    for date in sorted_converted_date_list:
        
        fmt = "%Y/%m/%d"
        iteration_date_list.append(date.strftime(fmt))#时间格式转成字符串格式
        #排序后没有去重的时间
    for date in iteration_date_list:
        
        out.write(date+'\n')
    out.close()

    return iteration_date_list
    
    

def get_date_infoList_dict(info_list_dict):
    
    date_infoList_dict = {}
    
    for key in info_list_dict:
        
        key_list = key.split('-')
        date = key_list[0]
        
        date_infoList_dict[date] = info_list_dict[key]
        
    return date_infoList_dict
    
    
def get_testingDay_rankList_dict(start_day, end_day, iteration_key_list, info_list_dict, file_name):

    temp_testing_day_list = []#有顺序的交易日期
    testingDay_rankList_dict = {}

    with open(file_name) as file_name:
        
        for line in file_name:
            
            name_list = line.split('-')
            date = name_list[0]
            
            #if date[:date.find('/')] == testing_year and date not in testing_day_list:
            if date not in temp_testing_day_list:
                temp_testing_day_list.append(date)
    
    start_index = temp_testing_day_list.index(start_day)
    end_index = temp_testing_day_list.index(end_day)
    
    testing_day_list= temp_testing_day_list[start_index:end_index+2]
    weight_list = [round(i*0.1, 2) for i in range(1, 11)]
    #balance_weight_list = [round(i*-0.1, 2) for i in range(1, 11)]
    
    for testing_day in testing_day_list:
    
        day_rank_list = []#第一天排名
        for key in iteration_key_list:
            
            key_list = key.split('-')
            date = key_list[0]
            year = date[:date.find('/')]
            
            if date == testing_day: #回测第一天的日期         
                
                info_list = info_list_dict[key][0]
                convertible_bond_price = round(float(info_list[9]), 10)
                premium_rate = round(float(info_list[16]), 10)  
                balance = round(float(info_list[21]), 10)
                 
                rank_list = []
                for N_1 in [convertible_bond_price*w for w in weight_list]:#可转债价格
                    
                    for N_2 in [premium_rate*w for w in weight_list]:#溢价率
                        
                        for N_3 in [balance*w for w in weight_list]:#余额
                            
                            rank = N_1+N_2#+N_3
                            rank_list.append(rank)
                            
                max_rank_value = max(rank_list)
                day_rank_list.append([key, max_rank_value])

        #sorted_day_rank_list = sorted(day_rank_list, key=lambda item: item[1], reverse=True)#排名降序
        sorted_day_rank_list = sorted(day_rank_list, key=lambda item: item[1])#升序
        
        testingDay_rankList_dict[testing_day] = sorted_day_rank_list
    
    return testingDay_rankList_dict, testing_day_list
    
    
    
def get_sorted_key_list(info_list_dict):

    key_list = []
    iteration_key_list = []
    
    for info_key in info_list_dict:
        
        info_key_list = info_key.split('-')
        date = info_key_list[0]

        date_format = "%Y/%m/%d"
        converted_date = datetime.strptime(date, date_format)#字符串转成时间格式
        
        line_key_list = [converted_date] + info_key_list[1:]

        
        key_list.append(line_key_list)
        
    sorted_key_list = sorted(key_list)
    
    out = open('结果文件3-循环时间验证.xls', 'w')
    file_name = '结果文件3-循环时间验证.xls'
    
    for line_list in sorted_key_list:
        
        fmt = "%Y/%m/%d"
        str_date = line_list[0].strftime(fmt)#时间格式转成字符串格式        
        
        sorted_key = str_date+'-'+line_list[1]+'-'+line_list[2]+'-'+line_list[3]+'-'+line_list[4]
        out.write(sorted_key+'\n')
        
        iteration_key_list.append(sorted_key)
    
    out.close()

    return iteration_key_list, file_name



def get_rank_key_list(day_rank_list):
    
    key_list = []
    
    for rank_list in day_rank_list:
        
        key = rank_list[0]
        key = key[key.find('-')+ 1:]
        key_list.append(key)
        
    return key_list
    
    

def mark_judgment(next_testing_day, testing_day, key, nextDay_key_price_dict):
   
    judge_key = next_testing_day +'-'+ key
    
    if judge_key in nextDay_key_price_dict:
        mark = '是'
    else:
        mark = '否'
    
    return mark
    
    
def get_buy_key_info_list(next_testing_day, tempDay_key_price_dict, testingDay_rankList, assets_sold_list):
    
    buy_key_info_list = testingDay_rankList[10:len(assets_sold_list)+20]#改1
    #buy_key_info_list = testingDay_rankList[3:len(assets_sold_list)+20]
    
    buy_money = 0
    
    for line_list in  assets_sold_list:
        
        money = line_list[2]
        buy_money+= money
        
    buy_num = len(assets_sold_list)
    
    temp_buy_list = []
    for buy_list in buy_key_info_list:
        
        buy_key = buy_list[0]
        buy_key = buy_key[buy_key.find('-')+1:]
    
        if next_testing_day+'-'+ buy_key not in tempDay_key_price_dict:
            continue
        else:
            temp_buy_list.append(buy_list)
    
    final_buy_info_list = temp_buy_list[:len(assets_sold_list)]
    
    return final_buy_info_list, buy_money, buy_num
    
    
# def get_newbuy_key_info_list(testingDay_rankList, assets_sold_list):
    
    # buy_key_info_list = testingDay_rankList[10:len(assets_sold_list)+10]
    
    # buy_money = 0
    
    # for line_list in  assets_sold_list:
        
        # money = line_list[2]
        # buy_money+= money
        
    # buy_num = len(assets_sold_list)

    # return buy_key_info_list, buy_money, buy_num
 
 
    
def get_soldKey_list(intersection_key_set, key_list, next_key_list):
    
    soldKey_list = []
    
    for key in key_list:
        
        if key not in next_key_list:
            soldKey_list.append(key)
            
    return soldKey_list
    
    
    
def output_result(iteration_date_list, day_key_price_dict, money, testingDay_rankList_dict, testing_day_list):

    deduplicated_iteration_date_list = []
    
    for iteration_date in iteration_date_list:
        if iteration_date not in deduplicated_iteration_date_list:
            deduplicated_iteration_date_list.append(iteration_date)


    out = open('结果文件4-回测交易结果.xls', 'w')
    title_list = ['轮动日期', '状态', '买入后资产', '相比前一天收益(%)', '交易日期', '买入日期','可转债名称', '买入价格', '买入时排名分数', '最大买入张数', '持仓/手', '买完后剩余金额']
    print(title_list)
    out.write('\t'.join(title_list)+'\n')
    
    tempKey_infoList_dict = {}#用来迭代计算每天的最新信息
    soldKey_set = set()#用来存卖出的可转债
    
    first_day = testing_day_list[0]
    all_left_money = 0
    num = 1

    for testing_day in testing_day_list[:-1]:#有顺序的交易日期

        if testing_day == first_day:  
            
            #buy_list = testingDay_rankList_dict[testing_day][:3]#第一天排名
            buy_list = testingDay_rankList_dict[testing_day][:10]#第一天排名改1
            key_list = get_rank_key_list(buy_list)#第一天排名处理
            #'123029-英科转债-300677.SZ-英科医疗'
            ######################################################################################
            testing_day_index = deduplicated_iteration_date_list.index(testing_day) 
            next_testing_day = deduplicated_iteration_date_list[testing_day_index + 1]            
            mark_list = []
            for key in key_list:
                mark = mark_judgment(next_testing_day, testing_day, key, day_key_price_dict[next_testing_day])#判断下一天该转债是否有交易信息
                mark_list.append(mark)
            if '否' in mark_list:
                print ([testing_day, '明天有可转债没有交易信息, 今天要卖出', '这部分代码没写，要补上'])
                out.write('\t'.join([testing_day, '明天有可转债没有交易信息, 今天要卖出', '这部分代码没写，要补上'])+'\n')
                pdb.set_trace()
            else:
                print ([testing_day, '目前持有的所有可转债在明天都有交易信息'])
                out.write('\t'.join([testing_day, '目前持有的所有可转债在明天都有交易信息'])+'\n')
            ######################################################################################
            #pdb.set_trace()
            for key_rank_list in buy_list:
                
                key, rank = key_rank_list
                price = day_key_price_dict[testing_day][key]
                #max_num = int(0.3*money/price)
                max_num = int(0.1*money/price)#改1
                num = int(max_num/10.0)
                left_money = 0.1*money - (num*10*price)
                
                trade_info_list = [testing_day, '买入', round(num*10*price, 10), 0, testing_day, testing_day, key, price, rank, max_num, num, left_money]
                tempKey = key[key.find('-')+1 : ]
                tempKey_infoList_dict[tempKey] = trade_info_list
                #{'123029-英科转债-300677.SZ-英科医疗': ['2021/01/04', '买入', 82000.0, 0, '2021/01/04', '2021/01/04', '2021/01/04-123029-英科转债-300677.SZ-英科医疗', 2050.0, 2051.66, 48, 4, 18000.0
                
                trade_info_list = [str(i) for i in trade_info_list]
                out.write('\t'.join(trade_info_list)+'\n')
                all_left_money+= float(trade_info_list[11])
                print (trade_info_list)
        else:
            next_rankList_list = testingDay_rankList_dict[testing_day][:10]#改1
            #next_rankList_list = testingDay_rankList_dict[testing_day][:3]
            next_key_list = get_rank_key_list(next_rankList_list)

            ##################################################################################################                
            testing_day_index = deduplicated_iteration_date_list.index(testing_day) 
            next_testing_day = deduplicated_iteration_date_list[testing_day_index + 1]            
            mark_list = []

            for key in next_key_list:
                mark = mark_judgment(next_testing_day, testing_day, key, day_key_price_dict[next_testing_day])#判断下一天该转债是否有交易信息
                mark_list.append(mark)                

            if '否' in mark_list:
                print ([testing_day, '明天有可转债没有交易信息, 今天要卖出'])
                out.write('\t'.join([testing_day, '明天有可转债没有交易信息, 今天要卖出'])+'\n')
            else:
                print ([testing_day, '目前持有的所有可转债在明天都有交易信息'])
                out.write('\t'.join([testing_day, '目前持有的所有可转债在明天都有交易信息'])+'\n')

            ##################################################################################################

            current_assets_list = []
            assets_sold_list = []
            
            if len(set(key_list) & set(next_key_list)) == 10:#改1
            #if len(set(key_list) & set(next_key_list)) == 3:
            
                line_info_list = [testing_day, '前后两天排名可能有变化，但依然是上一天的10支转债']
                print (line_info_list)
                out.write('\t'.join(line_info_list)+'\n')
                
                for key in next_key_list:

                    ###############################################################################################
                    #持有可转债的代码
                    judge_key = next_testing_day +'-'+ key
                    if judge_key in day_key_price_dict[next_testing_day]:

                        #tempKey_infoList_dict[tempKey] = trade_info_list

                        trade_info_list = tempKey_infoList_dict[key]#前一天的交易信息

                        current_price = day_key_price_dict[testing_day][testing_day+'-'+key]#
                        position = round(float(trade_info_list[10])*10*current_price, 10)#
                        rate = round((position - float(trade_info_list[2]))/float(trade_info_list[2]), 10)*100#
                        
                        current_info_list = [testing_day, '持有'] + [position, rate] + trade_info_list[4:]
                        current_assets_list.append(current_info_list)
                        current_info_list = [str(i) for i in current_info_list] 
                        print (current_info_list)
                        
                        tempKey_infoList_dict[key] = current_info_list
                        out.write('\t'.join(current_info_list)+'\n')
                        
                    ############################################################################################### 
                    #卖出可转债的代码
                    elif judge_key not in day_key_price_dict[next_testing_day]:
                        soldKey_set.add(key)
                        trade_info_list = tempKey_infoList_dict[key]#前一天的交易信息
                        current_price = day_key_price_dict[testing_day][testing_day+'-'+key]#
                        position = round(float(trade_info_list[10])*10*current_price, 10)#
                        rate = round((position - float(trade_info_list[2]))/float(trade_info_list[2]), 10)*100#
                        current_info_list = [testing_day, '卖出-明天无交易'] + [position, rate] + trade_info_list[4:]
                        #current_assets_list.append(current_info_list)
                        assets_sold_list.append(current_info_list)
                        current_info_list = [str(i) for i in current_info_list] 
                        print (current_info_list)                        
                        out.write('\t'.join(current_info_list)+'\n')
                        
                    else:
                        print ('有bug，请检查')
                        pdb.set_trace()
                        
                #持有、卖出后买入的代码
                if len(assets_sold_list) == 0:#前后两天排名有变化，但依然是上一天的10支转债时不买入
                    continue

                buy_key_info_list, buy_money, buy_num= get_buy_key_info_list(next_testing_day, day_key_price_dict[next_testing_day], testingDay_rankList_dict[testing_day], assets_sold_list)
                buy_money = buy_money + all_left_money
                all_left_money = 0
                #[['2021/01/05-113035-福莱转债-601865.SH-福莱特', 328.9097]]
                
                for buy_key_info_list in buy_key_info_list:
                    
                    key, rank = buy_key_info_list
                    price = day_key_price_dict[testing_day][key]
                    max_num = int((buy_money/buy_num)/price)
                    num = int(max_num/10.0)
                    left_money = buy_money/buy_num - (num*10*price)
                    all_left_money += left_money
                    
                    trade_info_list = [testing_day, '买入', round(num*10*price, 10), 0, testing_day, testing_day, key, price, rank, max_num, num, left_money]
                    current_assets_list.append(trade_info_list)
                    tempKey = key[key.find('-')+1 : ]
                    tempKey_infoList_dict[tempKey] = trade_info_list
                    #{'123029-英科转债-300677.SZ-英科医疗': ['2021/01/04', '买入', 82000.0, 0, '2021/01/04', '2021/01/04', '2021/01/04-123029-英科转债-300677.SZ-英科医疗', 2050.0, 2051.66, 48, 4, 18000.0
                    
                    trade_info_list = [str(i) for i in trade_info_list]
                    out.write('\t'.join(trade_info_list)+'\n')
                    print (trade_info_list)
                    
                
            elif len(set(key_list) & set(next_key_list)) == 0:
                print ('全部卖出', '重新轮动', 'check')
                pdb.set_trace()
            else:
                if len(key_list) != 10:#改1
                #if len(key_list) != 3:
                    print ('前一天的转债列表不等于10', '请检查')
                    pdb.set_trace()
                
                soldKey_list = get_soldKey_list(set(key_list) & set(next_key_list), key_list, next_key_list)
                
                #pdb.set_trace()
                for key in key_list:#当天可转债列表
                
                    judge_key = next_testing_day +'-'+ key
                    if key in (set(key_list) & set(next_key_list)) and judge_key in day_key_price_dict[next_testing_day]:#

                        trade_info_list = tempKey_infoList_dict[key]#前一天的交易信息
                        current_price = day_key_price_dict[testing_day][testing_day+'-'+key]#
                        position = round(float(trade_info_list[10])*10*current_price, 10)#
                        rate = round((position - float(trade_info_list[2]))/float(trade_info_list[2]), 10)*100#
                        
                        current_info_list = [testing_day, '持有'] + [position, rate] + trade_info_list[4:]
                        current_assets_list.append(current_info_list)
                        current_info_list = [str(i) for i in current_info_list] 
                        print (current_info_list)
                        
                        tempKey_infoList_dict[key] = current_info_list
                        out.write('\t'.join(current_info_list)+'\n')

                    elif key in (set(key_list) & set(next_key_list)) and judge_key not in day_key_price_dict[next_testing_day]:
                        #这个是卖出可转债的代码
                        ###################################################################################################
                        soldKey_set.add(key)
                        trade_info_list = tempKey_infoList_dict[key]#前一天的交易信息
                        current_price = day_key_price_dict[testing_day][testing_day+'-'+key]#
                        position = round(float(trade_info_list[10])*10*current_price, 10)#
                        rate = round((position - float(trade_info_list[2]))/float(trade_info_list[2]), 10)*100#
                        current_info_list = [testing_day, '卖出-明天无交易'] + [position, rate] + trade_info_list[4:]
                        #current_assets_list.append(current_info_list)
                        assets_sold_list.append(current_info_list)
                        current_info_list = [str(i) for i in current_info_list] 
                        print (current_info_list)                        
                        out.write('\t'.join(current_info_list)+'\n')
                    elif key in soldKey_list:
                        soldKey_set.add(key)

                        trade_info_list = tempKey_infoList_dict[key]#前一天的交易信息
                        current_price = day_key_price_dict[testing_day][testing_day+'-'+key]#
                        position = round(float(trade_info_list[10])*10*current_price, 10)#
                        rate = round((position - float(trade_info_list[2]))/float(trade_info_list[2]), 10)*100#
                        current_info_list = [testing_day, '卖出'] + [position, rate] + trade_info_list[4:]
                        #current_assets_list.append(current_info_list)
                        assets_sold_list.append(current_info_list)
                        current_info_list = [str(i) for i in current_info_list] 
                        print (current_info_list)                        
                        out.write('\t'.join(current_info_list)+'\n')                        
                        ###################################################################################################
                    else:
                        print ('请检查')
                        pdb.set_trace()
                #持有、卖出后买入的代码
                if len(assets_sold_list) == 0:#前后两天排名有变化，但依然是上一天的10支转债时不买入
                    continue
                buy_key_info_list, buy_money, buy_num= get_buy_key_info_list(next_testing_day, day_key_price_dict[next_testing_day], testingDay_rankList_dict[testing_day], assets_sold_list)
                buy_money = buy_money + all_left_money
                all_left_money = 0
                #[['2021/01/05-113035-福莱转债-601865.SH-福莱特', 328.9097]]
                
                for buy_key_info_list in buy_key_info_list:
                    
                    key, rank = buy_key_info_list
                    price = day_key_price_dict[testing_day][key]
                    max_num = int((buy_money/buy_num)/price)
                    num = int(max_num/10.0)
                    left_money = buy_money/buy_num - (num*10*price)
                    
                    trade_info_list = [testing_day, '买入', round(num*10*price, 10), 0, testing_day, testing_day, key, price, rank, max_num, num, left_money]
                    current_assets_list.append(trade_info_list)
                    tempKey = key[key.find('-')+1 : ]
                    tempKey_infoList_dict[tempKey] = trade_info_list
                    #{'123029-英科转债-300677.SZ-英科医疗': ['2021/01/04', '买入', 82000.0, 0, '2021/01/04', '2021/01/04', '2021/01/04-123029-英科转债-300677.SZ-英科医疗', 2050.0, 2051.66, 48, 4, 18000.0
                    
                    trade_info_list = [str(i) for i in trade_info_list]
                    out.write('\t'.join(trade_info_list)+'\n')
                    print (trade_info_list)                         
                        
            buy_list = next_rankList_list
            next_key_list = []
            for current_list in current_assets_list:
                
                key = current_list[6]
                next_key_list.append(key[key.find('-')+1:])

            key_list = next_key_list
            first_day = testing_day
        print ('#'*10)
        out.write('\t'.join(['###########'])+'\n')
        #pdb.set_trace()
    out.close()
    
    
def get_day_key_price_dict(testing_day_list, iteration_key_list, info_list_dict):

    day_key_price_dict = {}#{'2021/01/04': {'2021/01/04-110031-航信转债-600271.SH-航天信息': 106.31}
    
    for testing_day in testing_day_list:
        day_key_price_dict[testing_day] = {}
        
    
    for key in iteration_key_list:
        
        date = key.split('-')[0]
        price = round(float(info_list_dict[key][0][9]), 10)
        year = date[:date.find('/')]
        
        if date not in  testing_day_list:
            continue
        day_key_price_dict[date][key] = price
        #pdb.set_trace()
    return day_key_price_dict
    
    
    
def main():
    #Step<1>#inputting files
    inputting_file_1 = '附件1-可转债数据库-V2.txt'
    #money = int(input('请输入投资金额（如10000000）：').strip())
    #start_day = input('请输入买入日期（必须是交易日期），如2021/01/04：')
    #end_day = input('请输入结束日期（必须是交易日期），如如2021/12/31：')
    money = 500000#int(input('请输入投资金额（如10000000）：').strip())
    #start_day = '2021/01/04'#input('请输入买入日期（必须是交易日期），如2021/01/04：')
    #end_day = '2022/12/30'#input('请输入结束日期（必须是交易日期），如如2021/12/31：')    
    start_day = '2022/12/30'#input('请输入买入日期（必须是交易日期），如2021/01/04：')
    end_day = '2023/12/07'#input('请输入结束日期（必须是交易日期），如如2021/12/31：')    
    #step<2>basic data structure
    info_list_dict, all_colum_list, title_list = get_info_list_dict(inputting_file_1)
    
    #step<3>generating duplicated lines
    get_duplicated_lines(info_list_dict, all_colum_list, title_list)
    iteration_date_list = get_date_list(info_list_dict)
    iteration_key_list, file_name = get_sorted_key_list(info_list_dict)
    
    #date_infoList_dict = get_date_infoList_dict(info_list_dict)
    
    #step<4>calculating
    testingDay_rankList_dict, testing_day_list = get_testingDay_rankList_dict(start_day, end_day, iteration_key_list, info_list_dict, file_name)#测试年份
    day_key_price_dict = get_day_key_price_dict(testing_day_list, iteration_key_list, info_list_dict)
    output_result(iteration_date_list, day_key_price_dict, money, testingDay_rankList_dict, testing_day_list)
    pdb.set_trace()
    
    
if __name__ == '__main__':
    main()