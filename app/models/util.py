import os.path
import urllib.error
import urllib.request


def extract_media_from_tweets(tweets: list, threshold: int = 1):
    media_urls = list()
    for tweet in tweets:
        # 画像が無い場合にはスキップ
        if 'media' not in tweet['entities'].keys():
            continue
        # RT数が一定に届かない場合にはスキップ
        if tweet['favorite_count'] < threshold:
            continue
        # 画像のurlを保存
        for media in tweet['entities']['media']:
            media_urls.append(media['media_url_https'])
    return media_urls


def extract_userID(tweet):
    return tweet['user']['id']


def extract_tweetID(tweet):
    return tweet['id']


def save_image(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


def make_path(root, screen_name, url):
    name = os.path.basename(url)
    return os.path.join(root, screen_name, name)
