import time
import requests

from config import config


def generate_chunks():
    """
    1秒ごとに文字列をチャンクとして生成するジェネレータ。
    bytes もしくは str が yield されれば requests は自動で chunked request とみなします。
    """
    for i in range(1, 11):
        chunk = f"chunk #{i}\n"
        print(f"[client] sending: {chunk.strip()}")
        yield chunk.encode("utf-8")
        time.sleep(1)


if __name__ == "__main__":
    url = f"http://localhost:{config.port}/receive-stream"
    headers = {
        # Content-Length を指定しないことで、requests が chunked transfer encoding を自動付与します :contentReference[oaicite:0]{index=0}
        "Content-Type": "application/octet-stream",
        # 明示的に指定してもよいが、不要です:
        # "Transfer-Encoding": "chunked",
    }
    resp = requests.post(
        url,
        data=generate_chunks(),
        headers=headers,
        timeout=20,  # 必要に応じて調整
    )

    # サーバーからの最終レスポンスを表示
    print("[client] response status:", resp.status_code)
    print("[client] response JSON:", resp.json())
