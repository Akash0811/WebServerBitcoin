from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from datetime import timedelta
import bs4,requests,re,os

from .models import Alert

# Time String
now = datetime.utcnow()
now += timedelta(hours=5 , minutes=30)
date_string = now.strftime('%d/%m/%y')
time_string = now.strftime('%H.%M')


# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello!'*times,'Please go to /db to know the price')


def db(request):
    
    # Go to Webpage
    webpage = requests.get('https://www.coindesk.com/price/bitcoin')
    
    # Raise exception if there is an error
    if webpage.status_code != requests.codes.ok:
        raise Exception("Error while downloading webpage")
    
    # Copy price text from html
    parser = bs4.BeautifulSoup(webpage.text,'html.parser')
    elemsPrice = parser.select('#export-chart-element > div > section > div.coin-info-list.price-list > div:nth-child(1) > div.data-definition > div')
    
    # Extract the price
    string1 = str(elemsPrice).replace(',','')  # Replace commas in price
    NumRegex = re.compile(r'\d+.\d+')
    num = NumRegex.findall(string1)
    
    # Add the entry to the table
    alert = Alert(d1 = date_string,
                  t1 = time_string,
                  price = num[0])
    alert.save()

    alerts = Alert.objects.all()

    return render(request, "db.html", {"alerts": alerts})
