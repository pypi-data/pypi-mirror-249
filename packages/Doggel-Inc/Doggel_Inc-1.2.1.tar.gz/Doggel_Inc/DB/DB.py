import aiohttp

apikey = None
node = None
db_id = None

def setup(key, dbid):
    global apikey
    apikey = key
    global db_id
    db_id = dbid
    
def node(nodee):
    global node
    node = nodee

async def request(action, line, value=None):
    
    global apikey
    request_headers = {'Authorization': apikey}
    async with aiohttp.ClientSession() as session:
        global node
        global db_id
        api_url = f'http://us3.techstar.host:55567/{node}/{db_id}'
        request_data = {'action': action,'line': line,'value': value }
                        
        async with session.post(api_url, json=request_data, headers=request_headers) as response:
            api_response = await response.json()
            return api_response
