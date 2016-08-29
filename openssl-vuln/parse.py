#!/usr/bin/env python3

#from urllib.request import urlopen # python3
from urllib2 import urlopen
import lxml.html 
from lxml.cssselect import CSSSelector
from functools import reduce

import numpy as np
from sklearn.cluster import Ward as WardAgglomeration

import rake
rake_object = rake.Rake('SmartStoplist.txt')

def summary(txt):
    keywords = rake_object.run(txt)
    return keywords


def get_summary(url):
    response = urlopen(url)
#    with urlopen(url) as response:
    root = lxml.html.parse(response).getroot()

    sel = CSSSelector('#GeneratedTable tr:nth-child(4) td')

    return summary(sel(root)[0].text.replace('\n', ' '))


def parse(url, N_clusters):
    response = urlopen(url)
#    with urlopen(url) as response:
    root = lxml.html.parse(response).getroot()

    sel = CSSSelector('dt a[href*="cve.mitre.org"]')

    hrefs = [el.get('href') for el in sel(root)]
    hrefs = sorted(hrefs)

    # get description and summarize it
    keywords = {}
    for i, h in enumerate(hrefs):
        print(i+1, len(hrefs))
        kwds = list(filter(lambda kw: kw[1]>1, get_summary(h)))
        keywords[h] = filter(lambda kw: kw[0] not in ['application crash', 'remote attackers'], kwds)

    all_kwds = reduce(lambda a,b: a+b, keywords.values())
    unique_keywords = sorted(set(list(map(lambda kw: kw[0], all_kwds))))

    # generate clustering matrix
    M = np.zeros([len(hrefs), len(unique_keywords)], dtype=float)
    for h, kwds in keywords.items():
        i = hrefs.index(h)
        for kw, score in kwds:
            j = unique_keywords.index(kw)
            M[i,j] = score

    C = WardAgglomeration(N_clusters)
    clusters = C.fit_predict(M)

    print(clusters)

    from matplotlib import pyplot as plt
    ax = plt.imshow(M, interpolation='nearest')
    plt.xticks(range(len(unique_keywords)), unique_keywords, rotation='vertical')
    plt.show()

    res = [
        {h: kwds for (h, kwds), cc in zip(keywords.items(), clusters)
          if cc == c}
        for c in range(N_clusters)
    ]
    return res


def main():
    url = 'https://www.openssl.org/news/vulnerabilities.html'
    clusters = parse(url, N_clusters=10)
    for C in clusters:
        print('===============================')
        for h, kwds in C.items():
            print(h)
            print('  '+'\n  '.join(map(lambda kw: kw[0], kwds)))
        print('===============================')


if __name__ == '__main__':
    main()

