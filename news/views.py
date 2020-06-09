import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

# Create your views here.
###################################################################################
#Scrape website and create database
def scrape(request):
    res = requests.get('https://bitcoinist.com/category/bitcoin/')
    soup = BSoup(res.text, 'html.parser')
    main = soup.select('.featured-image')[6:]
    for data in main:
        link = data.get('href')
        title = data.get('title')
        image_src = data.find('img')['src']
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        new_headline.save()
    return redirect('../')

##############################################################################
#Serve stored database object
def news_list(request):
    headlines = Headline.objects.all().order_by('-id')[:12:-1]
    context = {
        'object_list': headlines
    }
    return render(request, 'news/home.html', context)

###############################################################################

