import json
from requests_oauthlib import OAuth1Session


class TwitterAPI(object):
    def __init__(
            self,
            consumer_key, consumer_secret,
            access_token, access_token_secret):
        self.api = OAuth1Session(
            consumer_key, consumer_secret, access_token, access_token_secret)

    def get_user_id(self, screen_name: str):
        url = "https://api.twitter.com/1.1/users/show.json"
        params = {'screen_name': screen_name}
        res = self.api.get(url, params=params)
        user_id = json.loads(res.text)['id']
        return user_id

    def get_tweets(
            self, screen_name: str,
            since_id: int = None, limit: int = 1000):
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {
            'screen_name': screen_name,
            'exclude_replies': True,
            'include_rts': False
        }
        if since_id is None:
            params['count'] = limit
        else:
            params['since_id'] = since_id
        res = self.api.get(url, params=params)
        return json.loads(res.text)
