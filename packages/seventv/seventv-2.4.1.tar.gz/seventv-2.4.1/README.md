# seventv - an asynchronous Python API-wrapper for 7tv
[7tv.app](https://7tv.app)

This API-wrapper makes use of the 7tv API (v3) to make it possible to get emotes, details about them, and soon some more things the API supports.

To get emotes by search query, the wrapper uses the GraphQL endpoint ```https://7tv.io/v3/gql``` because it seems to currently be the only working one for searching emotes. 

<sub>this project is not associated with or owned by 7tv or it's developers<sub>

# Installation
## How to install:
```
pip install seventv
```
### requires:
```
aiohttp
```

# Usage
To search for an emote and make use of the search results, do the following (asynchronously):
- create a class instance of sevenTV
- await the ```.emote_search``` method with your search query string and optional filters
- don't forget to close the session at some later point, using ```.close()```.

Example usage:
```
import asyncio
import seventv

async def myFunctionSearchEmote():
    mySevenTvSession = seventv.seventv()
    # initialize an instance of the seventv() class. this must happen in an asynchronous context

    emotes = await mySevenTvSession.emote_search("pepe", case_sensitive=True)
    # searches for "pepe", using the optional filter "case_sensitive"
    
    myEmote = emotes[2] # get the third emote from the search results
    print(myEmote)
    print(myEmote.host_url) # get the url from the emote object
    
    await mySevenTvSession.close() # later close the session

asyncio.run(getemote())
```
Sample output: third Emote object in results; host_url:
```
Emote(id: 60a304efac2bcb20ef20fa89, name: pepeMeltdown, owner_username: supernoahtv, host_url: //cdn.7tv.app/emote/60a304efac2bcb20ef20fa89)
//cdn.7tv.app/emote/60a304efac2bcb20ef20fa89
```

The output from a search is an array with the Emote objects inside.
Each emote contains the following properties:
- id
- name
- owner_username
- host_url

_Sidenote: Keep in mind that to use the actual emote-image using the url, you must write it as url like this:_
```
host_url = //cdn.7tv.app/emote/60a304efac2bcb20ef20fa89 # url you get from the api
https:host_url/2x.webp
```
_Emotes are stored on 7tv in different sizes, usually ranging from 1x.webp to 4x.webp. Not every emote might have every size though, so look it up or go with x2 or x3 which the majority of emotes have._

_About closing sessions: initializing a session with seventv.sevent() creates an aiohttp session. This session should be closed by calling .close() at some point. Not doing so will cause a warning like this:_ 
```
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x7fd2b06469b0>
```
_Closing/reopening it after every request does avoid the warning, but is not very efficent. It would be optimal to close the session when the service/code that uses it stops._

### Currently available search filters (optional):

| filter                         | meaning | default value |     
| ---------------------------------------------- | -------- | --------------- | 
| searchterm | search for specific emotes by text string      | empty string, which can be left this way and still works             |
| limit (int) | how many emotes are contained in the response      | 12             |     
| page (int) | which page from the search results to return      | 1             | 
| case_sensitive (bool) | whether or not upper-/lowercase letters are treated differently or will not be distinguished   | False |     
| animated (bool) |only return animated emotes in search results          | False                 |     
| exact_match (bool) | only return emotes that exactly match the search query | False   |
| query     | you can chose what data exactly to request (WIP). options: "all", "url" for only the host_url | "all"         |


planned to be added functionality: 
- get an emote by it's id
- more options for the gql query