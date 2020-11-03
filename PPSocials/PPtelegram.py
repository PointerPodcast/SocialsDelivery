import telegram

class PP_telegram:
    
    __instance__ = None

    _bot = None
    _chat_id = None

    def __init__(self, token):
        if PP_telegram.__instance__ is None:
            PP_telegram.__instance__ = self
            credentials = token.split(',')
            try:
                self._bot = telegram.Bot(token=credentials[0])
                self._chat_id = credentials[1]
                print(" > Telegram: Authentication OK")
            except:
                print(" > Telegram: unable to login.")
                raise Exception("Unable to login in Telegram")

    @staticmethod
    def get_instance(token):
        if not PP_telegram.__instance__:
            PP_telegram(token)
        return PP_telegram.__instance__
    
    def publish_post(self, text='', image_path=''):
        self._bot.send_photo(
            self._chat_id,
            photo = open(image_path, 'rb'),
            caption = text
        )
        print(" >> Telegram: published!")
