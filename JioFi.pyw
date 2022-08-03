from pystray import MenuItem as item
import pystray
from PIL import Image
import threading
from time import sleep
import requests
from bs4 import BeautifulSoup

url = 'http://jiofi.local.html/cgi-bin/en-jio-4-1/mStatus.html'
noerror=True
def Refreshaction():
    status,per=get_bat_details()
    if noerror:
        cstatus='\n(plugged in)' if status else '\n(not plugged in)'
        image = Image.open("img/"+per+".png")
        icon.icon = image
        icon.title='JioFi Battery Status '+per+'%'+cstatus
    else:
        image = Image.open("img/0.png")
        icon.icon = image
        icon.title='JioFi Battery Status Unavailable'
    
    return
    
def Exitaction():
    icon.stop()
    
def get_bat_details():
    global noerror
    status=False
    per='0'
    try:
        t = requests.get(url)
        soup = BeautifulSoup(t.content,'html.parser')
        per = soup.findAll("label", {"id": "lDashBatteryQuantity"})[0].string
        cstatus = soup.findAll("label", {"id": "lDashChargeStatus"})[0].string
        if cstatus =='Discharging':
        	status=False
        else:
        	status=True

        noerror=True
        return status,per.replace('%','')
    except:
       noerror=False
       return status,per

image = Image.open("img/0.png")
menu = (item('Refresh', Refreshaction), item('Exit', Exitaction))
icon = pystray.Icon("JioFi Battery Status", image, "JioFi Battery Status Unavailable", menu)

class thread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
 
    def run(self):
        while(1):
            status,per=get_bat_details()
            if noerror:
                image = Image.open("img/"+per+".png")
                icon.icon = image
                cstatus='\n(plugged in)' if status else '\n(not plugged in)'
                icon.title='JioFi Battery Status '+per+'%'+cstatus
                if int(per) == 100:
                    if status:
                        icon.title='JioFi Battery Status '+per+'%'
                        icon.notify('Battery Fully Charged')
                        icon.title='JioFi Battery Status '+per+'%'+cstatus
                if int(per) < 15:
                    icon.title='JioFi Battery Status '+per+'%'
                    icon.notify('Battery Below 15%')
                    icon.title='JioFi Battery Status '+per+'%'+cstatus
            else:
                image = Image.open("img/0.png")
                icon.icon = image
                icon.title='JioFi Battery Status Unavailable'
            sleep(60)
 
thread1 = thread()
thread1.daemon = True
thread1.start()
icon.run()

   