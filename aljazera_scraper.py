import json
import urllib.request
import http
import gzip
from time import sleep

def add_headers(req: urllib.request.Request):
    headers = [
        ("Accept", "*/*"),
        ("Accept-Encoding", "gzip, deflate, br, zstd"),
        ("Accept-Language", "en-US,en;q=0.9"),
        ("Content-Type", "application/json"),
        ("Cookie", ""),
        ("Dnt", "1"),
        ("If-None-Match", 'W/"458-ZxEDpx4QaV6gmwMdN3eljeOps4A"'),
        ("Original-Domain", "www.aljazeera.com"),
        ("Referer", ""),
        ("Sec-Ch-Ua", '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'),
        ("Sec-Ch-Ua-Mobile", "?0"),
        ("Sec-Ch-Ua-Platform", '"Linux"'),
        ("Sec-Fetch-Dest", "empty"),
        ("Sec-Fetch-Mode", "cors"),
        ("Sec-Fetch-Site", "same-origin"),
        ("User-Agent", "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"),
        ("Wp-Site", "aje"),
    ]
    for header_key, header_value in headers:
        req.add_header(header_key, header_value)

def decode_response(res: http.client.HTTPResponse):
    return json.loads(gzip.decompress(res.read()).decode('utf-8'))

def try_get(req: urllib.request.Request, trials: int = 10):
    num_retries = 0
    while num_retries < trials:
        sleep(0.1)  # Seems that AJ rate limits our code, so we need to tone it down a bit
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                decoded_response = decode_response(response)
                if decoded_response is None:
                    print(f'[{num_retries+1}/{trials}] Timed out, retrying...')
                    continue

                return decoded_response
        except urllib.error.URLError as e:
            if e.errno == 104:
                print(f'[{num_retries+1}/{trials}] Failed to connect, retrying...')
                num_retries += 1
                continue
        except Exception as e:
            print(e)
            num_retries += 1
            continue

def get_live_update_post_ids(live_update_name: str):
    request = urllib.request.Request(
        f'https://www.aljazeera.com/graphql?wp-site=aje&operationName=SingleLiveBlogChildrensQuery&variables=%7B%22postName%22%3A%22{live_update_name}%22%7D&extensions=%7B%7D')

    add_headers(request)
    response_data = try_get(request)
    return response_data['data']['article']['children']

def get_post_data(post_id: int):
    url = f'https://www.aljazeera.com/graphql?wp-site=aje&operationName=LiveBlogUpdateQuery&variables=%7B%22postID%22%3A{post_id}%2C%22postType%22%3A%22liveblog-update%22%2C%22preview%22%3A%22%22%2C%22isAmp%22%3Afalse%7D&extensions=%7B%7D'
    request = urllib.request.Request(url)
    add_headers(request)
    return try_get(request)

def get_aljazeera_headlines(link_id, header_short_link_id):
    header_short_link="https://aje.io/"+header_short_link_id+"?update="
    filtered_posts=[]
    post_ids=get_live_update_post_ids(link_id)
    for post_id in post_ids:
        try:
            post = get_post_data(post_id)['data']['posts']['title']
            link=header_short_link+str(post_id)
            filtered_posts.append({'link': link, 'headline': post})
        except:
            pass
    return filtered_posts

def example():
    print(get_aljazeera_headlines("israels-war-on-gaza-live-thousands-could-die-in-days-as-israel-blocks-aid", "k5c04g"))

