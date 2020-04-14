from googlesearch import search as gsc
import requests
import re

def google_search(querry):
    return []
    return list(gsc(querry, tld="co.in", num=50, stop=50, pause=2))

def facebook_search(querry):
    response = requests.get('https://www.facebook.com/public/'+ querry)
    facebook_re = re.compile("href=\"https://www.facebook.com/[^/\"]+\"><span>[^<]+")
    links = facebook_re.findall(response.text)
    titles = {elem.split('<span>')[1]: elem.split('<span>')[0][6:-2] for elem in links}
    return titles


def search_routine(querry):

    results = {}
    try:
        results['facebook'] = facebook_search(querry)
    except Exception as e:
        print(e)


    return results

