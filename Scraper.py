import pandas as pd
from datetime import datetime
from datetime import date 

from time import sleep
from tqdm import tqdm, trange

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

from pyvirtualdisplay import Display
from xvfbwrapper import Xvfb

coins=['btc','eth','xrp','ltc','bch','tusd','mana','gnt','bat','dai']
URLs={}
for i in coins:
    URLs.update({i:'https://bitso.com/trade/market/'+i+'/mxn'})


## Functions

def readscreen(test=False, verbose=False, database=[],order='asc',limitedStop=False, stopLimit=0, breakIfError=False):
    try:
        # Getting candels tags
        tagsPath = driver.find_elements_by_tag_name('g')
        candels=[]
        for i in range(len(tagsPath)):
            if tagsPath[i].get_attribute("aria-label") != None and tagsPath[i].get_attribute("aria-label").find('Price')==0:
                #print(tagsPath[i].get_attribute("transform"), tagsPath[i].get_attribute("aria-label"))
                candels.append(tagsPath[i])
        print("\n",len(candels), 'Candels detected')

        #Checking every candel by moving arround
        nCandels = len(candels)
        
        if limitedStop==False:
            steps=nCandels
        else:
            steps=stopLimit
        
        
        for i in trange(steps):
            ok=False
            while ok==False:
                try:
                    action=ActionChains(driver)
                    if order == 'asc':
                        action.move_to_element(candels[i])
                    elif order == 'des':
                        action.move_to_element(candels[nCandels-i-1])
                    else:
                        print('ERROR: Non order detected, use asc or des')

                    action.perform()
                    #print(i, candels[i].get_attribute('aria-label'))

                    #Getting info of every candel

                    voltag=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div')
                    volume=voltag.text

                    boxtags = driver.find_elements_by_tag_name('b')
                    i_open=boxtags[0].text
                    i_low=boxtags[1].text
                    i_high=boxtags[2].text
                    i_close=boxtags[3].text

                    datetag=driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div[1]/div/div/div[2]/div[1]/div/div/div[2]/div')
                    date_str=datetag.text
                    i_date=datetime.strptime(date_str,'%b %d, %Y')

                    day=[i_date,i_open,i_low,i_high,i_close,volume] #Register integration

                    if test == False:
                        database.append(day)

                    if verbose == True:
                        print(day)
                        
                    ok=True
          
                except:
                    print('The Candel',i,'Fails when was tried to read it')
                    if breakIfError == True:
                        return 'Fail'
                    else:
                        ok=True
    
        return day[0].date() #Control date to finish the scanning of windows dates
    except:
            print('ERROR: Mayor Fail - Check the driver is initialized correctly')
   
def getScrollerPosition(si,sf):
    xi,yi=int(si[si.find('(')+1:si.find(',')]),int(si[si.find(',')+1:si.find(')')])
    xf,yf=int(sf[sf.find('(')+1:sf.find(',')]),int(sf[sf.find(',')+1:sf.find(')')])
    return xi,yi,xf,yf

def getScrollers():
    #Getting the tags of the  scrollers for time periods
    loaded=False
    while loaded == False:
        try:
            scroll_tags = driver.find_elements_by_tag_name('g') #The scrollers are over the tag 'g'
            scrollers=[]

            for i in range(len(scroll_tags)):
                role = scroll_tags[i].get_attribute("role") # Scrollers has the exlusive attribute 'role'
                if role != None:
                    #print(scrollers[i].get_attribute("role"), scrollers[i].get_attribute("transform"))
                    scrollers.append(scroll_tags[i])
            loaded=True
            if len(scrollers) == 2:
                print('Scroller elements load successfully')
            else:
                print('Something went wrong with the scrollers')
        except:
            print('Loading scrollers...')
    return scrollers

def scrap(zeroi=-17, zerof=38, max_tries=3,offseti=1 ,offsetf=1,driver=0, wait_loading_time=0,verbose_rs=False, database_rs=[]):
    
    sleep(wait_loading_time)
    #Checking where are the scrollers
    si=scrollers[0].get_attribute("transform")
    sf=scrollers[1].get_attribute("transform")

    xi,yi,xf,yf=getScrollerPosition(si,sf)

    step=zerof-zeroi

    it=0
    tries=0
    loaded= False
    
    # Movig the scrollers for time periods
    
    try:
        while loaded == False:
            print('Fitting the area to scan', end="")
            while (xi != zeroi+step*it or xf != zerof+step*it) and tries < max_tries:
                action=ActionChains(driver)
                action.drag_and_drop_by_offset(scrollers[0],zeroi+step*it-xi-offseti,0)
                action.drag_and_drop_by_offset(scrollers[1],zerof+step*it-xf+offsetf,0)
                action.perform()
                

                si=scrollers[0].get_attribute("transform")
                sf=scrollers[1].get_attribute("transform")
                xi,yi,xf,yf=getScrollerPosition(si,sf)
                sleep(1)
                tries+=1
                print('.',end="")
            
            print("")
            sleep(1)
            last_day=readscreen(database = database_rs, verbose=verbose_rs) ## Getting info function
            it+=1
            tries=0
            print('Iteracion: ',it)
            if last_day == date.today():
                print('Space completed in ',it,'iterations')
                loaded=True
    except:
        print('Space completed in ',it,'iterations [except]')
    print('Scrap function completed')
    
def save(name,database=[]):
    df=pd.DataFrame(database)
    df=df.drop_duplicates()
    df=df.reset_index()
    df.rename(columns={0:'date',1:'open',2:'low',3:'high',4:'close',5:'volume'},inplace=True)
    df=df.drop(columns='index')
    df.to_csv('./'+name+'-mxn.csv',index=False)

def loadWebpage(URL=''):
    print('Opening browser...')
    driver = webdriver.Firefox()
    print('Opening ',URL)
    driver.get(URL)
    sleep(5)
    print('Maximizing window...')
    driver.maximize_window()
    print('Scrolling into graph...')
    driver.execute_script("window.scrollTo(0, 200)")
    return driver

## Daily Scraper

vdisplay = Xvfb(width=2880, height=1800)
vdisplay.start()

for i in coins:
    # Revisar csv y obtener ultima fecha
    ok=False
    while ok==False:
        try:
            file=i+'-mxn.csv'
            data=pd.read_csv(file)
            lastdate=data.date[len(data)-1]

            #Sacar la diferencia entre el último registro y el día actual
            delta=(datetime.now()-datetime.strptime(lastdate,'%Y-%m-%d')).days +1

            updates=[]

            #Scraping Bitso
            driver = loadWebpage(URLs[i])
            scrollers = getScrollers()
            readError = readscreen(database=updates,order='des',limitedStop=True, stopLimit=delta, breakIfError=True)
            
            if readError =='Fail':
                raise NameError('Read Candel Error')
            
            driver.close()

            #Pasando las actualizaciones a un Data Frame de pandas
            ud=pd.DataFrame(updates)
            #Ordenando las actualizaciones
            ud=ud.sort_values(by=[0])
            ud=ud.reset_index(drop=True)
            #Colacando nombres a las columnas
            ud.rename(columns={0:'date',1:'open',2:'low',3:'high',4:'close',5:'volume'},inplace=True)
            #Pasando la fecha str para homogenizar
            ud.date=ud.date.apply(lambda x: x.date().strftime('%Y-%m-%d'))

            #Agregando las actualizaciones a la base de datos guardada
            data=data.append(ud)
            #Actualizando índices
            data=data.reset_index(drop=True)
            #Eliminando duplicados
            data.date=data.date.drop_duplicates(keep='last')
            data=data.dropna()
            #Actualizando índices
            data=data.reset_index(drop=True)
            #Guarando base actualizada
            save(i,data)
            print('Base de datos de ', i, '-mxn actualizada correctamente')
            print('-------------------------------------------------------')
            #Terminando while de aseguramiento
            ok=True

        except:
            print('No se actualizó ', i, '-mxn')
            try:
                driver.close()
            except:
                pass

vdisplay.stop()