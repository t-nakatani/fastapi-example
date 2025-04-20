from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
import uvicorn

from config import config

app = FastAPI()


@app.post("/receive-stream")
async def receive_stream(request: Request):
    """
    クライアントからチャンク単位で送られてくるバイナリを受け取り、
    合計バイト数を最終的に JSON で返す例
    """
    total_bytes = 0

    # チャンクを非同期に受け取りつつ処理
    async for chunk in request.stream():
        # chunk は bytes
        total_bytes += len(chunk)
        # ここでパース／保存／加工などの処理を行える :contentReference[oaicite:6]{index=6}
        print(f"[server] received: {chunk}")
    return JSONResponse({"received_bytes": total_bytes})


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=config.port, reload=True)
