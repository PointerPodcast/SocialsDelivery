import instabot
import os

class PP_instagram:
    
    __instance__ = None
    _bot = None

    _users_to_tag = [
        {'user_id': '339266895', 'x': 0.5, 'y': 0.1}, #Ale
	{'user_id': '48812384', 'x': 0.5, 'y': 0.5}, #Luca
	{'user_id': '1555356995', 'x': 0.5, 'y': 0.9} #Eug
    ]

    def __init__(self, token):
        if PP_instagram.__instance__ is None:
            PP_instagram.__instance__ = self
            self._bot = instabot.Bot()
            credentials = token.split(',')
            self._bot.login(
                username = credentials[0],
                password = credentials[1],
                use_cookie=True
            )
        else:
            raise Exception("PP_instagram is singleton!")

    @staticmethod
    def get_instance(token):
        if not PP_instagram.__instance__:
            PP_instagram(token)
        return PP_instagram.__instance__
    

    def _publish_post(self, text='', image_path=''):
        self._bot.upload_photo(image_path, text)

    #NOT WORKING. Instagram pretends 1080x1920 photo. 
    def _publish_story(self, image_path=''):
#        photo_data, photo_size = media.prepare_image(image_path, aspect_ratios=MediaRatios.reel)
        self._bot.upload_story_photo('/home/alessandro/Github/SocialsDelivery/cover_templates/test.jpg')

    def publish_post_and_story(self, text='', image_path=''):
        #self._publish_story(image_path)
        self._publish_post(text, image_path)
        #workaround to fix REMOVE_ME added by instabot
        os.rename(image_path+'.REMOVE_ME', image_path)


