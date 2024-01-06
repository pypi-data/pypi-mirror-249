import aiohttp

apikey = None
model = None

def setup(key):
    global apikey
    apikey = key
    
def model(modell):
    global model
    model = modell

async def request(user_id=None, user_name=None, message):
    
    global apikey
    request_headers = {'Authorization': apikey}
    async with aiohttp.ClientSession() as session:
        global model
        api_url = 'http://us3.techstar.host:55565/request'
        request_data = {'message': message,'message-author-id': user_id,'message-author-user': user_name,'model': model }
                        
        async with session.post(api_url, json=request_data, headers=request_headers) as response:
            api_response = await response.json()
            return api_response
