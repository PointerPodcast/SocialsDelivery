import requests

organization_id = '42331509'

access_token = 'AQWDYOtsQBaHKiLU2NpkvRkc5-T4Y8sK2DcS8EJvHg4qDHI0XxPmnbLWSHEpdbjbN5a8strU26jfYdtjcG3DXlDjPfSG6Hda0XJrcrLcdtu_O_qdmW8Sf2OYJboYsQWJ14mwwKgLGQo1skU4iPk3q2n3e14kkD-q605GfAGpDUm5AGLg2oFq0l2p4PLo2wBAdkCBbPfM6X77-NuGAlKAL4p6BrsXKEyI4ojxYPKRY3LSSHBDD2ks44Slk7-TD_jDvfJ44H3sCLyGh4dbWBfOYH3M6lDEsG3ZrLN3keLvO6Y4AHYu6qICbbww9H9HR1n2QZCCR4__Po9mDa6lSPG8hOrCCMGPHA'


headers = {'Content-Type': 'application/json',
           'X-Restli-Protocol-Version': '2.0.0',
           'Authorization': 'Bearer ' + access_token
           }

def registerUpload():
    url = 'https://api.linkedin.com/v2/assets?action=registerUpload'
    register_data = {
        "registerUploadRequest": {
            "owner": "urn:li:organization:"+organization_id,
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
        response = requests.post(url, headers=headers, json=register_data)
        response.raise_for_status()
        json_data = response.json()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)

    linkedin_url = json_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    digital_media = json_data['value']['asset']
    print(response)
    return linkedin_url, digital_media

def uploadImage(linkedin_url, file_path):
    headers = {
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': 'Bearer ' + access_token
           }
    try:
        response = requests.put(linkedin_url, headers=headers, data=open(file_path, 'rb'))
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)
    return True

def publishRichMedia(digital_media, text):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    post_data = {
        "author": "urn:li:organization:"+organization_id,
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
        response = requests.post(url, headers=headers, json=post_data)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise Exception(err)
    return True



file_path = './blackhole.jpg'
text = 'Hi a tutti'
linkedin_url, digital_media = registerUpload()
if uploadImage(linkedin_url, file_path):
    publishRichMedia(digital_media, text)
