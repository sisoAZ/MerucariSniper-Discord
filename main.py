import os
merucari_url = os.environ["url"]
webhook_url = os.environ['webhook']

#-------------------------------------
from merucari_lib import search
from merucari_lib import webhook
from merucari_lib import loadConfig
from time import sleep
import keep_alive

config = loadConfig()

timespan = config["timespan"]
include_text = config["include_text"]
exclude_text = config["exclude_text"]

if len(include_text) == 0:
    include_text = None

if len(exclude_text) == 0:
    exclude_text = None

if os.path.exists(os.getcwd() + "/merucari/diff.txt") == False:
    os.makedirs(os.getcwd() + "/merucari")

print("---------------------")
print(f"チェック間隔 -> {timespan}分ごと")
print(f"含むキーワード -> {include_text}")
print(f"除外するキーワード -> {exclude_text}")
keep_alive.keep_alive()

while True:
    results = search(merucari_url, include_text, exclude_text, 10)
    for result in results:
        webhook(webhook_url, f"{result['price']}円 {result['title']}\n{result['url']}")
        print(result)
    sleep(60 * timespan)
