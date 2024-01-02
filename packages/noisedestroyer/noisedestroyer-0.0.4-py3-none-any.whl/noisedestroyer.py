import httpx
import aiofiles
from typing import Any, Dict, Optional, Tuple
import aiohttp

noise_destroyer = "https://www.noisedestroyer.com"


async def do_request(token, method, url, query=None, body=None):
    async with aiohttp.ClientSession() as session:
        # response = await client.request(
        #     url,
        #     method=method,
        #     content=body,
        #     query=query,
        #     headers={
        #         "token": token,
        #         "content-type": "application/octet-stream"
        #     },
        # )

        # use aiohttp
        response = await session.request(
            method=method,
            url=url,
            data=body,
            params=query,
            headers={
                "token": token,
                "content-type": "application/octet-stream"
            },
        )
        return_value = None
        try:
            return_value = await response.json()
        except:
            try:
                return_value = await response.text()
            except:
                pass
    
        # if 2XX
        if response.status // 100 == 2:
            return return_value, None
        else:
            if return_value == "" or return_value is None:
                return None, response
            return None, ValueError(return_value)
            

async def remove_background_noise(token: str, data, ouput_format="aac") -> Tuple[Optional[Dict[str, Any]], Optional[Exception]]:
    url = f"{noise_destroyer}/api/v1/background-noise-removal?outputFormat={ouput_format}"
    if not token or token == "":
        return None, ValueError("token is required")
    if not data:
        return None, ValueError("data is required")
    
    file = None
    try:
        if isinstance(data, str):
            async with aiofiles.open(data, mode="rb") as f:
                return await do_request(token, "POST", url, body=f)
        else:
            return await do_request(token, "POST", url, body=data)
    except Exception as err:
        return None, err
    finally:
        try:
            if file is not None and isinstance(data, str):
                await file.close()
        except:
            pass

def remove_background_noise_sync(token: str, data: str, ouput_format="aac") -> Tuple[Optional[Dict[str, Any]], Optional[Exception]]:
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(remove_background_noise(token, data, ouput_format))

async def get_status(token, guid):
    url = f"{noise_destroyer}/api/v1/file-status/{guid}"
    return await do_request(token, "GET", url)

def get_status_sync(token, guid):
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_status(token, guid))

async def download(url, output_path=None):
    # if no output path, return bytes, otherwise stream to file
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if output_path is None:
                    return await response.read(), None
                else:
                    with open(output_path, "wb") as f:
                        async for chunk in response.content.iter_chunked(4096):
                            f.write(chunk)
                    return True, None
    except Exception as err:
        return None, err
    
def download_sync(url, output_path=None):
    import asyncio
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(download(url, output_path))
