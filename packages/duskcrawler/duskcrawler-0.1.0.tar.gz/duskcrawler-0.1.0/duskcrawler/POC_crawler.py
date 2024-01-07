from lxml.etree import HTML
from requests import get
import textwrap
import pandas as pd

# Data for future use if User want data on his computer as file
data_url = []
data_date = []
data_text = []
data_par1 = []
data_par2 = []
data_par3 = []
data_par4 = []
data_par5 = []
data_par6 = []

# Crawling process

def process_page(page_url: str):
    print(f"Start page: {page_url}")
    response = get(page_url)
    tree = HTML(response.text)
    # Retrieving links from main page
    for page_link in tree.xpath(
        "//a[contains(@class, 'horo-card border-rad-4 px-1 pt-15 pb-2 text-center')]/@href"
        ):
        full_page_url = page_link
        print("")
        print(f"Article link: {full_page_url}")
        data_url.append(page_link)
        response1 = get(page_link)
        tree1 = HTML(response1.text)
        # Retrieving date from retrieved links
        for date in tree1.xpath(
            "//span[contains(@id, 'content-date')]/text()"
                ):
            print(str("\033[1m" + date + "\033[0m"))
            data_date.append(date)
            print("")
            # Retrieving "Daily Horoscope" content from retrieved links
        for text in tree1.xpath(
            "//span[contains(@style, 'font-weight: 400')]/text()" # //div[contains(@id, 'content')]/p/text()????
            ):
            data_text.append(text)
            print(textwrap.fill(text))
        print("")
        # Retrieving titles from retrieved links
        for title1 in tree1.xpath(
            "//h4[contains(@class, 'header-container mb-1 mb-md-15')]/text()"
            ):
            # Required to compare strings from titles
            tt1 = title1.__str__().strip()
            tt2 = tree1.xpath("//h4[contains(text(), 'Daily Food Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            tt3 = tree1.xpath("//h4[contains(text(), 'Daily Home Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            tt4 = tree1.xpath("//h4[contains(text(), 'Daily Dog Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            tt5 = tree1.xpath("//h4[contains(text(), 'Daily Teen Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            tt6 = tree1.xpath("//h4[contains(text(), 'Daily Cat Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            tt7 = tree1.xpath("//h4[contains(text(), 'Daily Bonus Horoscope')]/text()").__str__().strip("['\\n ").strip(" \\n']").strip()
            # Compares titles and based on the result prints specific data to that title
            if tt1 == tt2:
                par1 = tree1.xpath("//div[contains(@id, 'content-food')]/text()")
                par1 = par1.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par1))
                data_par1.append(par1)
            elif tt1 == tt3:
                par2 = tree1.xpath("//div[contains(@id, 'content-home')]/text()")
                par2 = par2.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par2))
                data_par2.append(par2)
            elif tt1 == tt4:
                par3 = tree1.xpath("//div[contains(@id, 'content-dog')]/text()")
                par3 = par3.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par3))
                data_par3.append(par3)
            elif tt1 == tt5:
                par4 = tree1.xpath("//div[contains(@id, 'content-teen')]/text()")
                par4 = par4.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par4))
                data_par4.append(par4)
            elif tt1 == tt6:
                par5 = tree1.xpath("//div[contains(@id, 'content-cat')]/text()")
                par5 = par5.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par5))
                data_par5.append(par5)
            elif tt1 == tt7:
                par6 = tree1.xpath("//div[contains(@id, 'content-bonus')]/text()")
                par6 = par6.__str__().strip('["\\n ').strip(' \\n"]').strip("['\\n ").strip(" \\n']").strip()
                print("\033[1m" + title1 + "\033[0m")
                print(textwrap.fill(par6))
                data_par6.append(par6)
            else:
                print("error")
try:
    process_page("https://www.astrology.com/horoscope/daily.html")
except Exception as e:
    print("Timed out")

#  Saving crawled information in dataset
dataset = {
    "URL": data_url,
    "Date": data_date,
    "Daily horoscope": data_text,
    "Daily Food Horoscope": data_par1,
    "Daily Home Horoscope": data_par2,
    "Daily Dog Horoscope": data_par3,
    "Daily Teen Horoscope": data_par4,
    "Daily Cat Horoscope": data_par5,
    "Daily Bonus Horoscope": data_par6
}
# Generating dataFrame
file = pd.DataFrame(dataset)
# User prompt if they want to save the data as a file on their computer
while True:
    prompt1 = input("Would you like for the data to be saved on your computer?").lower()
    if prompt1 == "yes":
        with open("Daily_Horoscope", "w") as f:
            # using explode to turn one row into multiple rows
            file = file.explode("URL")
            # Saving formatted data to .csv file with separation
            file.to_csv(f, sep = '\t', index=False)
        print("File saved as 'Daily_Horoscope' in .csv format")
        break
    elif prompt1 == "no":
        print("T_T")
        break
    else:
        print("whaa?")
        print("Answer must be a 'yes' or a 'no' ")

