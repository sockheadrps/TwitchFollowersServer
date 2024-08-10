# FastAPI Followers API Server
![img](resp.png)

## Overview

The **FastAPI Followers Server** is a FastAPI-based web service designed to retrieve and return the list of followers for a given Twitch broadcaster. The endpoint requires various parameters, including access token, client ID, client secret, and broadcaster username, so for that reason this tool should not be exposed on the internet, rather used as an internal API service for your application.

## Features

- **Fetch Followers:** Retrieve a complete list of followers for a specified Twitch broadcaster.
- **Handle Pagination:** Automatically manage pagination to ensure all followers are fetched.
- **Returns JSON:** Provides the follower data in JSON format.


**Query Parameters:**

- `access_token` (string, required): Your Twitch OAuth access token.
- `client_id` (string, required): Your Twitch client ID.
- `username` (string, required): The Twitch username of the broadcaster.
- `returns_per_page` (integer, optional): The number of followers to return per page. Default is 100.

### Example Request

```http
POST /followers?access_token=abc123&client_id=your_client_id&username=exampleuser&returns_per_page=50 HTTP/1.1
Host: yourapi.example.com
Content-Type: application/json
```


## Prerequisites

- Python 3.7 or higher
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- [httpx](https://www.python-httpx.org/) (HTTP client for asynchronous requests)
- [pydantic](https://pydantic-docs.helpmanual.io/) (Data validation and settings management)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sockheadrps/TwitchFollowersServer.git
