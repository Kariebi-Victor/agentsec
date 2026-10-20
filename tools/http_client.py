import httpx


def send_request(base_url, method, path, token=None):
    headers = {}

    if token: 
        headers["Authorization"] = f"Bearer {token}"
    
    with httpx.Client(timeout=10.0, follow_redirects=False) as client: 
        response = client.request(
            method.upper(),
            f"{base_url.rstrip('/')}/{path.lstrip('/')}",
            headers=headers,
        )

    try:
        body = response.json() 
    except ValueError: 
        body = response.text[:1000]
    
    return { 
        "status_code": response.status_code, 
        "body": body,
    }
    