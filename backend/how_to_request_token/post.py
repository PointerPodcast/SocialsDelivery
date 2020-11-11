import requests


#profile_id = 'idBfR6bf7d'
organization_id = '42331509'

access_token = 'AQWDYOtsQBaHKiLU2NpkvRkc5-T4Y8sK2DcS8EJvHg4qDHI0XxPmnbLWSHEpdbjbN5a8strU26jfYdtjcG3DXlDjPfSG6Hda0XJrcrLcdtu_O_qdmW8Sf2OYJboYsQWJ14mwwKgLGQo1skU4iPk3q2n3e14kkD-q605GfAGpDUm5AGLg2oFq0l2p4PLo2wBAdkCBbPfM6X77-NuGAlKAL4p6BrsXKEyI4ojxYPKRY3LSSHBDD2ks44Slk7-TD_jDvfJ44H3sCLyGh4dbWBfOYH3M6lDEsG3ZrLN3keLvO6Y4AHYu6qICbbww9H9HR1n2QZCCR4__Po9mDa6lSPG8hOrCCMGPHA'
#access_token = 'AQULx69xq9KpLNOP_Iu4fw-31pYX-_Wprw57EkH3pOsCSZaJiq3R2Im6yOKHyX40Hap3cOyIP06oKeRViApIbtJ3aZKqKdH986_WkRBt3iouRiTyJ7wlqPXX6Gxq2jXQ5r55tR6H4bz2YRpNV4O4AOwiCftRgHIlUMiZgbu1UH6HySM3DXEjBDo7LKtCSv094XjxDtPH1X7PaxPMQZh73nWM8C8A7SXnp0DkTUZYN5xN_RdndvqpBdcTcWX4T7RAcyekZZ2UjMYNWjc8xs88Nj54u2ahJVBgknSTv3DCFR8Nq-p1-mHag7SUlX8BS3e6LAO2jvQiAUnQIL4GTrq0wmaDQyhOcQ'

url = "https://api.linkedin.com/v2/ugcPosts"

headers = {'Content-Type': 'application/json',
           'X-Restli-Protocol-Version': '2.0.0',
           'Authorization': 'Bearer ' + access_token}


post_data = {
    #"author": "urn:li:person:"+profile_id,
    "author": "urn:li:organization:"+organization_id,
    "lifecycleState": "PUBLISHED",
    "specificContent": {
        "com.linkedin.ugc.ShareContent": {
            "shareCommentary": {
                "text": "Hello World! This is my first Share on LinkedIn!!"
            },
            "shareMediaCategory": "NONE"
        }
    },
    "visibility": {
        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
}

response = requests.post(url, headers=headers, json=post_data)

print(response)
