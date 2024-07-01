import aiohttp
import os
import hashlib
import base64


async def authenticate():
    body = {'email': os.environ.get("IRACING_USERNAME"), 'password': await encode_pw()}
    async with aiohttp.ClientSession() as session:
        async with session.post('https://members-ng.iracing.com/auth', data=body) as response:
            cookies = {c.key: c.value for c in session.cookie_jar}
            return cookies
            #print(await response.text())
            
async def encode_pw():
    username = os.environ.get("IRACING_USERNAME")
    password = os.environ.get("IRACING_PASSWORD")
    
    initialHash = hashlib.sha256((password + username.lower()).encode('utf-8')).digest()
    hashInBase64 = base64.b64encode(initialHash).decode('utf-8')
    return hashInBase64