import tweepy

class PP_twitter:
    
    __instance__ = None

    _api = None

    def __init__(self, token):
        if PP_twitter.__instance__ is None:
            PP_twitter.__instance__ = self
            credentials = token.split(',')
            auth = tweepy.OAuthHandler(credentials[0], credentials[1])
            auth.set_access_token(credentials[2], credentials[3])
            self._api = tweepy.API(auth)
            try:
                self._api.verify_credentials()
                print(" > Twitter: Authentication OK")
            except:
                print(" > Twitter: unable to login.")
                raise Exception("Unable to login in Twitter")

    @staticmethod
    def get_instance(token):
        if not PP_twitter.__instance__:
            PP_twitter(token)
        return PP_twitter.__instance__
    
    def publish_post(self, text='', image_path=''):
        self._api.update_with_media(
            image_path,
            status = text
        )
        print(" >> Twitter: published!")
