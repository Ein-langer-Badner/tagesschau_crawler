import requests as req
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from time import sleep


class TagesSchauArtikel:
    def __init__(self, topline, schlagzeile, kurzfassung, link):
        self.topline = topline
        self.schlagzeile = schlagzeile
        self.kurzfassung = kurzfassung
        self.link = link


def tages_leser(rubrik_url):
    url = rubrik_url
    sleep(1)
    return_list = []
    site = req.get(url)
    saved_site = BeautifulSoup(site.text, "html.parser")

    top_list = []
    head_list = []
    short_list = []
    link_list = []
    replace_lex = {
        "mehr": "", "sportschau.de": "", "wdr.de": "", "wdr": "",
        "sr.de": "", "audio": "", "ndr": "", "ardthek.de": "",
        "europamagazin": "", "rbb": "", "swr": "", "thek": "",
        "mdr": "", "hr": "", "br": "" , "sportschau": ""
    }

    for var1 in range(len(saved_site.select(".columns .teaser__shorttext"))):
        top_list.append(saved_site.select(".columns .teaser__topline")[var1].text.strip())
        head_list.append(saved_site.select(".columns .teaser__headline")[var1].text.strip())
        short_list.append(saved_site.select(".columns .teaser__shorttext")[var1].text.strip())
        link_list.append(saved_site.select(".teaser__link")[var1].attrs["href"])

    # Anpassung der Daten beginnt hier
    for var1 in range(len(short_list)):
        for key, value in replace_lex.items():
            short_list[var1] = short_list[var1].replace(key, value).strip()

    if "ARD-Programm" in top_list:
        short_list.pop(top_list.index("ARD-Programm"))
        head_list.pop(top_list.index("ARD-Programm"))
        link_list.pop(top_list.index("ARD-Programm"))
        top_list.pop(top_list.index("ARD-Programm"))

    if "tagesthemen" in head_list:
        top_list.pop(head_list.index("tagesthemen"))
        short_list.pop()
        link_list.pop(head_list.index("tagesthemen"))
        head_list.pop(head_list.index("tagesthemen"))

    link_list.pop()
    link_list.pop()
    new_link1 = urljoin(url, link_list[len(link_list) - 2])
    link_list.append(new_link1)

    new_link2 = urljoin(url, link_list[len(link_list) - 1])
    link_list.append(new_link2)
    # Anpassung der Daten endet hier

    for var1 in range(len(head_list)):
        title = head_list[var1].strip()
        topline = top_list[var1].strip()
        kurzfassung = short_list[var1].strip().split(". ")
        link = link_list[var1].strip()
        ausgabe = TagesSchauArtikel(topline, title, kurzfassung, link)
        return_list.append(ausgabe)
    return return_list


def rubriken_leser():
    # rubriken = ("/", "/inland/", "/ausland/", "/wirtschaft/", "/wissen/", "/faktenfinder/", "/investigativ/")
    rubriken = ("/")
    return_list = []
    url = "https://www.tagesschau.de"
    for rubrik in rubriken:
        rubrik_url = urljoin(url, rubrik)
        return_list += tages_leser(rubrik_url)
    return return_list


def csv_schreiber_tagesschau(nachrichten_eingabe):
    with open('nachrichten.csv', 'w', newline='', encoding='utf-8') as csvfile:
        newswriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for var1 in range(len(nachrichten_eingabe)):
            newswriter.writerow([nachrichten_eingabe[var1].schlagzeile])
            newswriter.writerow([nachrichten_eingabe[var1].topline])

            for line in nachrichten_eingabe[var1].kurzfassung:
                newswriter.writerow([line])

            newswriter.writerow([nachrichten_eingabe[var1].link])
            newswriter.writerow([])
            newswriter.writerow([])


def main():
    nachrichten = rubriken_leser()
    csv_schreiber_tagesschau(nachrichten)


if __name__ == "__main__":
    main()
