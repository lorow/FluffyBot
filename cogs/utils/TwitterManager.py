import ujson

import tweepy


class TwitterStreamListener(tweepy.StreamListener):

    def __init__(self, eventManager):
        super().__init__()
        self.eventManager = eventManager

    def on_status(self, status):
        print(status)

    def on_data(self, raw_data):
        data = ujson.loads(raw_data)
        print(data['entities']['media'][0]['url'])

    def on_error(self, status_code):
        if status_code == 403:
            print("The request is understood, but it has been refused or access is not allowed. Limit is maybe reached")
            return False


class TwitterHandler(object):
    # Get access and key from another class
    def __init__(self, configManager, eventManager):
        self.streamListener = TwitterStreamListener(eventManager)

        self.consumer_key = configManager.get_field("consumer_key")
        self.consumer_secret = configManager.get_field("consumer_secret")
        self.access_token = configManager.get_field('access_token')
        self.access_secret = configManager.get_field('access_token')


        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.secure = True
        auth.set_access_token(self.access_token, self.access_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5,
                         retry_errors=5)
        self.my_stream = tweepy.Stream(auth=api.auth, listener=self.streamListener)

        print('listening....')
        print('----------------------------------')
        self.my_stream.filter(follow=['961690133618741250'], async=True)