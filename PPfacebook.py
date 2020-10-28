import facebook
import urllib3, requests 

class PP_facebook:
    
    __instance__ = None
    _graph = None
    _PP_PAGE_ID = '478092096063377'
    _token = 'EAAmsCa9pfl0BAJeBg4y5LDmvZCe3VUmE5C6NBH7HWGwFKH2ojWTbZALxPo0wgw5Gtcdirs6XPU4ZC6FTfDTv7vD7Kl7O6LjOO1Gg1ZA2LrleovX8fy7hzfnOIrMG088lmHZABQG3ZCv7oGez7TPs4a9BLDhlISeGw573iffZBSmPIRd7ZBXd4F6z0godQ23mID4rDjSsYheG2wZDZD'


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
    

    def publish(self, text='', image_path=''):
        self._graph.put_photo(image=open('/home/alessandro/Pictures/ancient.jpg', 'rb'),
                message='Look at this cool photo!')

    def get_message(self, post_id=''):
        complete_id = self._PP_PAGE_ID+'_'+post_id
        message = self._graph.get_objects(ids=[complete_id], fields='message')
        print(message[complete_id]['message'])



#IDPAGE_IDPOST
'''
'''

'''
graph.put_object(
    parent_object=PP_PAGE_ID,
    connection_name="feed",
    message="Ciao, sto testando GraphAPI di facebook!",
)
'''

