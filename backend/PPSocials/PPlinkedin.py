import requests

class PP_linkedin:
    
    __instance__ = None

    _organization_id = None
    _access_token = None

    _headers_register_publish = None
    _headers_upload = None

    _url_registerUpload = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    _url_ugcPosts = 'https://api.linkedin.com/v2/ugcPosts'

    def __init__(self, token):
        if PP_linkedin.__instance__ is None:
            PP_linkedin.__instance__ = self
            credentials = token.strip().split(',')
            self._organization_id = credentials[0]
            self._access_token = credentials[1]
            self._headers_register_publish = {
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0',
                'Authorization': 'Bearer ' + self._access_token
               }
            self._headers_upload = {
                'X-Restli-Protocol-Version': '2.0.0',
                'Authorization': 'Bearer ' + self._access_token
               }

            try:
                self._registerUpload()
                print(" > Linkedin: Authentication OK")
            except:
                print(" > Linkedin: unable to login.")
                raise Exception("Unable to login in Linkedin")

    @staticmethod
    def get_instance(token):
        if not PP_linkedin.__instance__:
            PP_linkedin(token)
        return PP_linkedin.__instance__
    

    def _registerUpload(self):
        register_data = {
            "registerUploadRequest": {
                "owner": "urn:li:organization:"+self._organization_id,
                "recipes": [
                    "urn:li:digitalmediaRecipe:feedshare-image"
                ],
                "serviceRelationships": [
                    {
                        "identifier": "urn:li:userGeneratedContent",
                        "relationshipType": "OWNER"
                    }
                ],
                "supportedUploadMechanism":[
                    "SYNCHRONOUS_UPLOAD"
              ]
            }
        }
        try:
            response = requests.post(self._url_registerUpload,
                                     headers=self._headers_register_publish,
                                     json=register_data)
            response.raise_for_status()
            json_data = response.json()
        except requests.exceptions.HTTPError as err:
            raise Exception(err)

        linkedin_url = json_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        digital_media = json_data['value']['asset']
        print(response)
        return linkedin_url, digital_media

    def _uploadImage(self, linkedin_url, image_path):
        try:
            response = requests.put(linkedin_url,
                                    headers=self._headers_upload,
                                    data=open(image_path, 'rb'))
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        return True


    def _publishRichMedia(self, digital_media, text):
        post_data = {
            "author": "urn:li:organization:"+self._organization_id,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "media": [
                        {
                            "media": digital_media,
                            "status": "READY",
                            "title": {
                                "text": "Black Hole"
                            }
                        }
                    ],
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        try:
            response = requests.post(self._url_ugcPosts,
                                     headers=self._headers_register_publish,
                                     json=post_data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        return True

    def publish_post(self, text='', image_path=''):
        linkedin_url, digital_media = self._registerUpload()
        if self._uploadImage(linkedin_url, image_path):
            self._publishRichMedia(digital_media, text)
