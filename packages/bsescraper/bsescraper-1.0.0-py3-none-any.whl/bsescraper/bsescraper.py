import requests
import pandas as pd

version="1.0.0"
description="A Python library to scrape data from BSE India website"
functions=["get_corporate_ann","GainerLoserDataMarket","GainerLoserDataGroup","get_index","get_stock_data","get_code","top_turnovers","dataframe","save"]

headers ={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/87.0.4280.66 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.bseindia.com/corporates/ann.html',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'TE': 'Trailers',  
}

def get_corporate_ann(code,category,startdate,enddate):
    try:
        cat = ['Board Meeting','Company Update','Corp. Action','AGM/EGM','New Listing','Results','Others']
        announcements = []
        startdate = str(startdate)[6:10]+str(startdate)[3:5]+str(startdate)[0:2]
        enddate = str(enddate)[6:10]+str(enddate)[3:5]+str(enddate)[0:2]
        url = f"https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat={category}&strPrevDate={str(startdate)}&strScrip={str(code)}&strSearch=P&strToDate={str(enddate)}&strType=C&subcategory=-1"
        req = requests.get(url,headers=headers)
        length = len(req.json()['Table'])
        for i in range(length):
            temp={}
            headlines = req.json()['Table'][i]['HEADLINE']
            temp['Headline'] = headlines
            subject = req.json()['Table'][i]['NEWSSUB']
            temp['Subject'] = subject
            date = req.json()['Table'][i]['NEWS_DT']
            temp['Date'] = date[0:10]
            announcements.append(temp)
        return announcements
    except Exception as e:
        print("Error: "+str(e))  

def GainerLoserDataMarket(type,order):
    try:
        market = []
        url = f"https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype={type}&IndxGrp=AllMkt&IndxGrpval=AllMkt&orderby={str(order)}"
        req = requests.get(url,headers=headers)
        length = len(req.json()['Table'])
        for i in range(length):
            temp={}
            sec = req.json()['Table'][i]['scrip_cd']
            temp['Security Code'] = sec
            name = req.json()['Table'][i]['scripname']
            temp['Security Name'] = name
            openrate = req.json()['Table'][i]['openrate']
            temp['Open Rate'] = openrate
            highrate = req.json()['Table'][i]['highrate']
            temp['High Rate'] = highrate
            lowrate = req.json()['Table'][i]['lowrate']
            temp['Low Rate'] = lowrate
            ltp = req.json()['Table'][i]['ltradert']
            temp['LTP'] = ltp
            change = req.json()['Table'][i]['change_val']
            temp['Change'] = change
            changeper = req.json()['Table'][i]['change_percent']
            temp['Change Percent'] = changeper
            date = req.json()['Table'][i]['dt_tm'][0:10]
            temp['Date'] = date
            market.append(temp)
        return market
    except Exception as e:
        print("Error: "+str(e))
    
def GainerLoserDataGroup(type,group,order):
    try:
        market = []
        url = f"https://api.bseindia.com/BseIndiaAPI/api/MktRGainerLoserData/w?GLtype={type}&IndxGrp=group&IndxGrpval={group}&orderby={str(order)}"
        req = requests.get(url,headers=headers)
        length = len(req.json()['Table'])
        for i in range(length):
            temp={}
            sec = req.json()['Table'][i]['scrip_cd']
            temp['Security Code'] = sec
            name = req.json()['Table'][i]['scripname']
            temp['Security Name'] = name
            openrate = req.json()['Table'][i]['openrate']
            temp['Open Rate'] = openrate
            highrate = req.json()['Table'][i]['highrate']
            temp['High Rate'] = highrate
            lowrate = req.json()['Table'][i]['lowrate']
            temp['Low Rate'] = lowrate
            ltp = req.json()['Table'][i]['ltradert']
            temp['LTP'] = ltp
            change = req.json()['Table'][i]['change_val']
            temp['Change'] = change
            changeper = req.json()['Table'][i]['change_percent']
            temp['Change Percent'] = changeper
            date = req.json()['Table'][i]['dt_tm'][0:10]
            temp['Date'] = date
            market.append(temp)
        return market
    except Exception as e:
        print("Error: "+str(e))

def get_index(category):
    try:
        cat = ["MCB","S&I","THE","STR","SUS","VOL","COM","GOV","COR","MOM"]
        url = f"https://api.bseindia.com/BseIndiaAPI/api/MktCapBoard/w?cat={str(cat.index(category)+1)}&type=2"
        req = requests.get(url,headers=headers)
        length = len(req.json()['Table'])
        index = []
        for i in range(length):
            temp={}
            name = req.json()['Table'][i]['IndexName']
            temp['Index Name'] = name
            openrate = req.json()['Table'][i]['I_Open']
            temp['Open Rate'] = openrate
            highrate = req.json()['Table'][i]['High']
            temp['High Rate'] = highrate
            lowrate = req.json()['Table'][i]['Low']
            temp['Low Rate'] = lowrate
            currentval = req.json()['Table'][i]['Curvalue']
            temp['Current Value'] = currentval
            chg = req.json()['Table'][i]['Chg']
            temp['Change'] = chg
            chg_per = req.json()['Table'][i]['ChgPer']
            temp['Change Percentage'] = chg_per
            week52_high = req.json()['Table'][i]['Week52High']
            temp['52 Week High'] = week52_high
            week52_low = req.json()['Table'][i]['Week52Low']
            temp['52 Week Low'] = week52_low
            mktcap = req.json()['Table'][i]['MKTCAP']
            temp['Market Cap'] = mktcap
            mktcap_perc = req.json()['Table'][i]['MktcapPerc']
            temp['Market Cap Percentage'] = mktcap_perc
            net_turn = req.json()['Table'][i]['NET_TURN']
            temp['Net Turnover'] = net_turn
            turnover_perc = req.json()['Table'][i]['TurnoverPerc']
            temp['Turnover Percentage'] = turnover_perc
            index.append(temp)
        return index
    except Exception as e:
        print("Error: "+str(e))

def get_stock_data(code,startdate,enddate):
    try:
        startdate = str(startdate)
        enddate = str(enddate)
        sdd=startdate[0:2]
        smm=startdate[3:5]
        syyyy=startdate[6:10]
        edd = enddate[0:2]
        emm = enddate[3:5]
        eyyyy = enddate[6:10]
        url = f"https://api.bseindia.com/BseIndiaAPI/api/StockpricesearchData/w?MonthDate={sdd}%2F{smm}%2F{syyyy}&Scode={str(code)}&YearDate={edd}%2F{emm}%2F{eyyyy}&pageType=0&rbType=D"
        req = requests.get(url,headers=headers)
        length = len(req.json()['StockData'])
        stock = []
        for i in range(length):
            temp={}
            dates = req.json()['StockData'][i]['Dates']
            temp['Date'] = dates
            qe_open = req.json()['StockData'][i]['qe_open']
            temp['Open'] = qe_open
            qe_high = req.json()['StockData'][i]['qe_high']
            temp['High'] = qe_high
            qe_low = req.json()['StockData'][i]['qe_low']
            temp['Low'] = qe_low
            qe_close = req.json()['StockData'][i]['qe_close']
            temp['Close'] = qe_close
            weighted_price = req.json()['StockData'][i]['WeightedPrice']
            temp['Weighted Price'] = weighted_price
            no_of_shrs = req.json()['StockData'][i]['no_of_shrs']
            temp['Number of Shares'] = no_of_shrs
            no_trades = req.json()['StockData'][i]['no_trades']
            temp['Number of Trades'] = no_trades
            net_turnov = req.json()['StockData'][i]['net_turnov']
            temp['Net Turnover'] = net_turnov
            delivery_qty = req.json()['StockData'][i]['Delivery_Qty']
            temp['Delivery Quantity'] = delivery_qty
            perc_del_qty = req.json()['StockData'][i]['Perc_Del_Qty']
            temp['Percentage Delivery Quantity'] = perc_del_qty
            spread_high_low = req.json()['StockData'][i]['SpreadHighLow']
            temp['Spread High-Low'] = spread_high_low
            spread_open_close = req.json()['StockData'][i]['SpreadOpenClose']
            temp['Spread Open-Close'] = spread_open_close
            stock.append(temp)
        return stock
    except Exception as e:
        print("Error: "+str(e))
        

def get_code(name):
    try:
        url = f"https://api.bseindia.com/BseIndiaAPI/api/ListofScripData/w?Group=&Scripcode=&industry=&segment=Equity&status="
        req = requests.get(url,headers=headers)
        length = len(req.json())
        for i in range(length):
            if req.json()[i]['Scrip_Name']==name:
                return int(req.json()[i]['SCRIP_CD'])
    except Exception as e:
        print("Error: "+str(e))

def top_turnovers(num):
    try:
        url = "https://api.bseindia.com/BseIndiaAPI/api/GetMktData/w?ordcol=TT&strType=AllMkt&strfilter=All"
        req = requests.get(url,headers=headers)
        length = len(req.json()['Table'])
        turnovers = []
        for i in range(num):
            temp = {}
            scrip_cd = req.json()['Table'][i]['scrip_cd']
            temp['Code'] = scrip_cd
            scripname = req.json()['Table'][i]['scripname']
            temp['Name'] = scripname
            scrip_grp = req.json()['Table'][i]['scrip_grp']
            temp['Group'] = scrip_grp
            openrate_scrip = req.json()['Table'][i]['openrate']
            temp['Open'] = openrate_scrip
            highrate_scrip = req.json()['Table'][i]['highrate']
            temp['High'] = highrate_scrip
            lowrate_scrip = req.json()['Table'][i]['lowrate']
            temp['Low'] = lowrate_scrip
            ltradert = req.json()['Table'][i]['ltradert']
            temp['Last'] = ltradert
            prevdayclose = req.json()['Table'][i]['prevdayclose']
            temp['Previous Day Close'] = prevdayclose
            change_val = req.json()['Table'][i]['change_val']
            temp['Change Value'] = change_val
            change_percent = req.json()['Table'][i]['change_percent']
            temp['Change Percentage'] = change_percent
            index_code = req.json()['Table'][i]['index_code']
            temp['Index Code'] = index_code
            trd_val = req.json()['Table'][i]['trd_val']
            temp['Trade Value'] = trd_val
            trd_vol = req.json()['Table'][i]['trd_vol']
            temp['Trade Volume'] = trd_vol
            nooftrd = req.json()['Table'][i]['nooftrd']
            temp['Number of Trades'] = nooftrd
            trend = req.json()['Table'][i]['trend']
            temp['Trend'] = trend
            dt_tm = req.json()['Table'][i]['dt_tm']
            temp['Date and Time'] = dt_tm[0:10]
            turnovers.append(temp)
        return turnovers
    except Exception as e:
        print("Error: "+str(e))

def dataframe(dictionary):
    df = pd.DataFrame(dictionary)
    return df
def save(df,name):
    df.to_csv(f"{name}.csv",index=False)
    return "Saved"
def version():
    print("Version: "+version)
def description():
    print("Description: "+description)
def functions():
    for i in functions:
        print(i)