import facebook
import urllib3, requests 


print(facebook.__version__)

class PP_facebook:
    
    __instance__ = None
    _graph = None
    _PP_PAGE_ID = '478092096063377'


    def __init__(self, token):
        if PP_facebook.__instance__ is None:
            PP_facebook.__instance__ = self
            self._graph = facebook.GraphAPI(access_token=token)
        else:
            raise Exception("PP_facebook is singleton!")

    @staticmethod
    def get_instance(token):
        if not PP_facebook.__instance__:
            PP_facebook(token)
        return PP_facebook.__instance__
    

    def publish_post(self, text='', image_path=''):
        self._graph.put_photo(image=open(image_path, 'rb'),
            message=text,
        )

    def get_message(self, post_id=''):
        complete_id = self._PP_PAGE_ID+'_'+post_id
        message = self._graph.get_objects(ids=[complete_id], fields='message')
        print(message[complete_id]['message'])

    def publish_feed(self):
        self._graph.put_object(
            parent_object= self._PP_PAGE_ID,
            connection_name="feed",
            message="Ciao, sto testando GraphAPI di facebook!",
        )


