from linkedin_v2 import linkedin

'''
APPLICATON_KEY    = '77jpfeat9zvo6p'
APPLICATON_SECRET = 'Z7ExiOcp5QLqivrY'


RETURN_URL = 'https://pointerpodcast.it/auth/linkedin/callback'

authentication = linkedin.LinkedInAuthentication(
                    APPLICATON_KEY,
                    APPLICATON_SECRET,
                    RETURN_URL
                )

print (authentication.authorization_url)
'''


access_token = 'AQWpnmOUjGShzQzPfXbRnj4p4gnzUa6BH4wMv3_B07jobBzzin3q5woXve9BFSw_Z2ahMAUX5SQzmXbCEg6uWh40-Xefrt13rQGfxFXKgc2bL0aWkEEGpVHhzMipNt8FJQXiY7ii4dAsiy08OM1Bt3S166GGl0Bleyj0pkpyUMEMt8mrsM9r48PacgxwlYtxg59Q9NFpgJN-tONv0b5ng5APDYZ0aNayUi6XCu4peqyYNe8ydBAy1sf5Gq-POkmll491x6TDjWEbLoz2MhyZvqS_RMDfPPJ7GwDRApR62q7PhTOruTPnGkVJMbe08-3SbviCq9rqI2j5J9riIldx23OILjgEIA'

application = linkedin.LinkedInApplication(token=access_token)

g = application.get_profile()
print(g)
