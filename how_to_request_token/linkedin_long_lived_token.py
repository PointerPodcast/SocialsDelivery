from linkedin_v2 import linkedin

APPLICATON_KEY    = '77jpfeat9zvo6p'
APPLICATON_SECRET = 'Z7ExiOcp5QLqivrY'

RETURN_URL = 'https://localhost:8000'


authentication = linkedin.LinkedInAuthentication(
                    APPLICATON_KEY,
                    APPLICATON_SECRET,
                    RETURN_URL,
                    linkedin.PERMISSIONS.enums.values()
                )

print (authentication.authorization_url)
'''
authentication.authorization_code = '#############################################'
result = authentication.get_access_token()

print ("Access Token:", result.access_token)
print ("Expires in (seconds):", result.expires_in)
'''
