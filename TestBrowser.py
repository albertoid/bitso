# Test script to open and read browser with a vritual display and selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from xvfbwrapper import Xvfb

vdisplay = Xvfb(width=2880, height=1800)
vdisplay.start()


coins=['btc','eth','xrp','ltc','bch','tusd','mana','gnt','bat','dai']
URLs={}
for i in coins:
    URLs.update({i:'https://bitso.com/trade/market/'+i+'/mxn'})

print('Opening browser...')
driver = webdriver.Firefox()
print('Opening ',URLs['btc'])
driver.get(URLs['btc'])
print(driver.name)


driver.close()

vdisplay.stop()