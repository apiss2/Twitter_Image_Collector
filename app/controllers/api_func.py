import os
import shutil
import logging

from app.models import util
from app.models.user import User
from app.models.twitter import TwitterAPI
import settings

logger = logging.Logger(__name__)
twitter = TwitterAPI(
    settings.CONSUMER_KEY,
    settings.CONSUMER_SECRET,
    settings.ACCESS_TOKEN,
    settings.ACCESS_TOKEN_SECRET)


def registration(user_id, screen_name, latest_tweet_id, threshold):
    # ユーザーオブジェクトを作成
    user = User(
        user_id=user_id,
        screen_name=screen_name,
        latest_checked_tweet=latest_tweet_id,
        threshold=threshold)
    user.save()


def delete_user(request):
    '''
    監視するユーザー登録処理を行う関数
    '''
    screen_name = request.form["userID"]
    # TODO: 成功判定を行う
    if "delete_entire_folder" in request.form.keys():
        if request.form["delete_entire_folder"] == "on":
            dir_name = os.path.join(settings.SAVE_ROOT, screen_name)
            shutil.rmtree(dir_name)
        else:
            # TODO: エラー処理
            return 502
    User.delete_user(screen_name)
    return 200


def registration_user(request):
    '''
    監視するユーザー登録処理を行う関数
    '''
    screen_name = request.form["userID"]
    threshold = request.form["threshold"]
    # screen_name
    if screen_name == "":
        logger.error(f"action=regist_user info=Empty_Value_Error(screen_name)")
        return 502
    # threshold
    try:
        threshold = int(threshold)
    except ValueError as e:
        logger.warning(f"action=regist_user info={e}")
        threshold = 100
    # 重複するユーザーがいる場合にはエラー
    if User.get_user(screen_name) is not None:
        logger.error(f"action=regist_user info=User_Duplication_Error")
        return 502

    # 画像を取得する
    tweets = twitter.get_tweets(screen_name)
    if not len(tweets) > 0:
        # 基本的にツイートが取得できる前提なので、該当ツイートが無い場合はエラー扱いにする
        logger.error('action=api_regist_user info=Tweets_Not_Found_Error')
        return 502
    # 画像を保存するフォルダを作成
    os.makedirs(os.path.join(settings.SAVE_ROOT, screen_name), exist_ok=True)
    # 画像を保存
    urls = util.extract_media_from_tweets(tweets, threshold=threshold)
    for url in urls:
        save_path = util.make_path(settings.SAVE_ROOT, screen_name, url)
        util.save_image(url, save_path)

    # ツイートから情報を取得する
    user_id = util.extract_userID(tweets[0])
    latest_tweet_id = util.extract_tweetID(tweets[0])
    registration(user_id, screen_name, latest_tweet_id, threshold)

    return 200


def registration_from_file(request):
    '''
    監視するユーザー登録処理を行う関数
    '''
    raise NotImplementedError