import requests
from io import BytesIO
from PIL import Image
import re
import urllib.request
import urllib.parse

urlOuo = 'Base url where the captcha happend'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'
head = {'Host': 'www.google.com',
    'User-Agent': UA,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': urlOuo}
    
def ResolveCaptcha(body):
    headers = {UA}

    captchaScrap = re.findall('value="8"><img class="fbc-imageselect-payload" src="(.+?)"',str(body))

    text = re.search('<div class="rc-imageselect.+?">.+?<strong>(.+?)</strong>',str(body)).group(1)

    c = re.search('method="POST"><input type="hidden" name="c" value="(.+?)"',str(body)).group(1)
    k = re.search('k=(.+?)" alt=',str(body)).group(1)
    params = {
        "c": c,
        "k": k,
    }
    query_string = urllib.parse.urlencode( params )

    url = 'https://www.google.com'+str(captchaScrap[0]) + "?" + query_string
    print('\n' + url)

    headers = {
        'Host': 'www.google.com',
        'User-Agent': UA,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length':str(len(params))}

    r = requests.get(url)
    i = Image.open(BytesIO(r.content)).show()
    response = input('Select all images representing '+text+'. Type from 1 to 9 (add space between all number ): ')

    allNumber = [int(s) for s in re.findall('([0-9])',str(response))]
    responseFinal = ""
    for rep in allNumber:
        responseFinal = responseFinal + '&response='+str(int(rep)-1)

    r = requests.post(urlBase, data='c='+c+responseFinal, headers=headers)
    return re.search('<textarea dir="ltr" readonly>(.+?)<',str(r.text)).group(1)

WebSiteKey = 'Recaptcha\'s key of the website'
urlBase  = 'https://www.google.com/recaptcha/api/fallback?k='+WebSiteKey
r = requests.get(urlBase, headers=head)

gToken = ResolveCaptcha(r.text)
print('Token final de Recaptcha : '+gToken)
