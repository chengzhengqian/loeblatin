from bs4 import BeautifulSoup
import requests
import re


def get_div_with_class(s, cn):
    return s.findAll("div", {"class": cn})


def get_latin(s):
    return _remove_all_attrs(get_div_with_class(s, "verso")[0])


def get_eng(s):
    return _remove_all_attrs(get_div_with_class(s, "recto")[0])


def _remove_all_attrs(soup):
    '''remove all attrs include root node and javascripts'''
    [x.extract() for x in soup.findAll('script')]
    [x.extract() for x in soup.findAll('span', {"class", "marginNote"})]
    [x.extract() for x in soup.findAll('span', {"class", "lineNumber"})]

    soup.attrs = {}
    for tag in soup.find_all(True):
        tag.attrs = {}
    return soup


def next_page_url(soup):
    for i in soup.findAll("a"):
        if(i.text == "Next Page"):
            return i.attrs["href"]
    return ""


def get_soup(url):
    url_r = requests.get(url)
    url_r.encoding = "utf-8"
    soup = BeautifulSoup(url_r.text, 'html.parser')
    return soup


def clear_files(files):
    for i in files:
        with open(i, "w+") as f:
            f.write("  ")


def download_from(url_base="https://www.loebclassics.com", url_loc="/view/virgil-aeneid/1916/pb_LCL063.263.xml?result=2&rskey=XbeKad"):
    url = url_base + url_loc
    name = "Aenied"
    file_eng = "../files/%s_eng.html" % name
    file_latin = "../files/%s_latin.html" % name
    file_total = "../files/%s_total.html" % name
    is_stop = False
    clear_files([file_eng, file_latin, file_total])
    while(not is_stop):
        soup = get_soup(url)
        div_latin = get_latin(soup)
        div_eng = get_eng(soup)
        with open(file_eng, "a") as f:
            f.write(str(div_eng))

        with open(file_latin, "a") as f:
            f.write(str(div_eng))

        with open(file_total, "a") as f:
            f.write(str(div_latin))
            f.write(str(div_eng))
        next_url_loc = next_page_url(soup)
        if(next_url_loc == ""):
            is_stop = True
        else:
            url = url_base + next_url_loc
        print("start new url", url)


if __name__ == "__main__":
    download_from()
