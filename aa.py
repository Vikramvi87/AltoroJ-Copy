from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    if flow.request.pretty_url.startswith("https:demo.testfire.net"):
        print("API Call:", flow.request.pretty_url)
