import requests
from get_html import getItems, getSource
from bs4 import BeautifulSoup
import yaml
import os

def search(target_url, contains_text=None, exclude_text=None, limit_num=10):

    source = getItems(target_url)
    soup = BeautifulSoup(source, "html.parser")
    #print(soup)
    #print("---------------------------------------------------------------------")

    items = soup.select("li", limit=limit_num)

    results = []
    check_duplicate_urls = []
    for item in items:
        #print("---------------------------------------------------------------------")
        #print(item)

        # Get URL
        soup_url = BeautifulSoup(str(item), "html.parser")
        url = "https://jp.mercari.com" + str(soup_url.select_one("a").get("href"))
        print(url)
        check_duplicate_urls.append(url)
    
    urls = diff(check_duplicate_urls, os.getcwd() + "/merucari/diff.txt")

    for url in urls:
        #Item Details
        details_source = getSource(url)
        soup_details = BeautifulSoup(details_source, "html.parser")

        #Get Title
        title = str(soup_details.select_one(".mer-spacing-b-2").get("title-label"))
        print(title)

        # Get Price
        price = str(soup_details.select_one('[data-testid="price"]').get("value"))
        print(price)

        # Get Description
        description = soup_details.select_one('mer-show-more').get_text()
        #print(description)

        # メルカリ特有の「OO様専用」を除外
        if "専用" in title:
            continue

        if contains_text == None and exclude_text == None:
            results.append({"url": url, "price": price, "title": title})
            continue

        if exclude_text != None:
            exclude = False
            for text in exclude_text:
                if text in title:
                    exclude = True
                elif text in description:
                    exclude = True
            if exclude == True:
                continue
        
        if contains_text != None:
            already_append = False
            for text in contains_text:
                if already_append == False:
                    if text in title:
                        results.append(
                            {"url": url, "price": price, "title": title})
                        already_append = True
                    elif text in description:
                        results.append(
                            {"url": url, "price": price, "title": title})
                        already_append = True
        else:
            results.append({"url": url, "price": price, "title": title})

    return results

def diff(new_id, save_path):
    try:
        with open(save_path, "r", encoding="utf-8") as f:
            checklists = [s.strip() for s in f.readlines()]
    except Exception:
        checklists = [" "]

    with open(save_path, mode="w", encoding="utf=8") as f:  # 上書きする
        f.write("\n".join(new_id))

    return list(set(new_id) - set(checklists))

def webhook(url, content):
    main_content = {
        "content": content
    }
    requests.post(url, main_content)

def loadConfig():
    config = {"timespan": 30, "include_text": [], "exclude_text": []}
    try:
        with open('config.yml', encoding="utf-8") as file:
            load_config = yaml.safe_load(file.read())
    except FileNotFoundError:
        print("エラー、設定ファイルが見つかりませんでした。デフォルトの設定を使用します。")
        return config
    try:
        config["timespan"] = load_config["timespan"]
        if load_config["include_text"] == None:
            config["include_text"] = []
        else:
            config["include_text"] = load_config["include_text"]
        if load_config["exclude_text"] == None:
            config["exclude_text"] = []
        else:
            config["exclude_text"] = load_config["exclude_text"]
    except Exception:
        print("エラー、設定ファイルの記述が間違っています。")
    return config
