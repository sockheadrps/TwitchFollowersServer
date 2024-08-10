from fastapi import FastAPI, HTTPException
import asyncio
import aiohttp
import logging

app = FastAPI()


async def fetch_followers_page(session, access_token, client_id, broadcaster_id, cursor, returns_per_page=100):
    """Fetch a page of followers for a given broadcaster ID."""
    url = f'https://api.twitch.tv/helix/channels/followers?broadcaster_id={broadcaster_id}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id,
        'Content-Type': 'application/json'
    }
    params = {'after': cursor, 'first': returns_per_page} if cursor else {}

    async with session.get(url, headers=headers, params=params) as response:
        if response.status != 200:
            raise HTTPException(status_code=response.status,
                                detail="Failed to fetch followers")
        return await response.json()


async def get_followers(session, access_token, client_id, broadcaster_id, returns_per_page=100):
    """Get all followers for a given broadcaster ID, handling pagination."""
    all_followers = []
    cursor = None
    tasks = []

    # Fetch the first page to determine total followers
    first_page = await fetch_followers_page(session, access_token, client_id, broadcaster_id, cursor, returns_per_page)

    if 'data' not in first_page or not first_page['data']:
        logging.error(
            "No followers found or 'data' field missing in the first page response.")
        return all_followers

    total_followers = first_page.get('total', 0)
    all_followers.extend(first_page['data'])
    cursor = first_page.get('pagination', {}).get('cursor')

    logging.info(
        f"Fetched {len(first_page['data'])} followers. Total: {total_followers}")

    # Create tasks for fetching remaining pages concurrently
    while cursor:
        task = asyncio.create_task(fetch_followers_page(
            session, access_token, client_id, broadcaster_id, cursor))
        tasks.append(task)

        # Fetch cursor for the next page
        next_page = await fetch_followers_page(session, access_token, client_id, broadcaster_id, cursor, returns_per_page=100)
        cursor = next_page.get('pagination', {}).get('cursor')

        if len(all_followers) >= total_followers:
            logging.info("All followers fetched.")
            break

    # Run tasks concurrently and gather results
    pages = await asyncio.gather(*tasks)
    for page in pages:
        if 'data' in page and page['data']:
            all_followers.extend(page['data'])
            logging.info(f"Fetched {len(page['data'])} followers.")

    logging.info(f"Total followers fetched: {len(all_followers)}")
    return all_followers


async def get_broadcaster_id(session, access_token, client_id, username):
    """Get the broadcaster ID for a given username."""
    url = f'https://api.twitch.tv/helix/users?login={username}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Client-Id': client_id
    }

    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            raise HTTPException(status_code=response.status,
                                detail="Failed to fetch broadcaster ID")
        user_data = await response.json()
        if 'data' in user_data and user_data['data']:
            return user_data['data'][0]['id']
        else:
            raise HTTPException(status_code=404, detail="Username not found")


@app.post("/followers")
async def get_twitch_followers(access_token: str, client_id: str, username: str, returns_per_page: int = 100):
    async with aiohttp.ClientSession() as session:
        broadcaster_id = await get_broadcaster_id(session, access_token, client_id, username)
        followers = await get_followers(session, access_token, client_id, broadcaster_id, returns_per_page)
        return {"followers": followers}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
