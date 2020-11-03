from linkedin import linkedin


class PP_linkedin:
    
    __instance__ = None


    def __init__(self, token):
        if PP_linkedin.__instance__ is None:
            PP_linkedin.__instance__ = self
            #raise Exception("Unable to login in Telegram")
        else:
           # return PP_linkedin.__instance__

    @staticmethod
    def get_instance(token):
        if not PP_linkedin.__instance__:
            PP_linkedin(token)
        return PP_linkedin.__instance__
    
