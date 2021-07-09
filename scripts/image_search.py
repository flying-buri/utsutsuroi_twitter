#/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import json
import keys
from requests_oauthlib import OAuth1Session

class Search():
    def image_search(self):
        #API認証情報
        CK = keys.CK
        CS = keys.CS
        AT = keys.AT
        ATS = keys.ATS
        twitter = OAuth1Session(CK,CS,AT,ATS)

        #API取得
        search = "https://api.twitter.com/1.1/search/tweets.json"

        # 画像を保存するディレクトリ
        folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../images")
        print(folder_path)
        path = os.path.exists(folder_path)
        if not path:
            os.mkdir(folder_path)

        # ツイートの取得設定
        num = 10
        keyword = '#VRChatワールド紹介' + ' -filter:retweets'
        params = {'q' : keyword, 'count' : num}
        req = twitter.get(search, params = params)
        image_num = 0

        if req.status_code == 200:
            # ツイートの画像を取得
            tweets = json.loads(req.content)
            print(tweets)
            for tweet in tweets['statuses']:
                if 'media' in tweet['entities']:
                    urls = tweet['entities']['media']
                    media_urls = urls[0]['media_url']
                    downloads = twitter.get(media_urls).content
                    # 画像を保存
                    file_name = '{0:03d}'.format(image_num) + '.jpg'
                    file_path = folder_path + '/' + file_name
                    images = open(file_path, 'wb')
                    images.write(downloads)
                    images.close()
                    image_num += 1

        else:
            print("ERROR: %d" % req.status_code)

if __name__ == '__main__':
    Search().image_search()
