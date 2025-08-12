import asyncio, json, random, time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = """
<html><body>
<h3>Stock Ticker (Simulado)</h3>
<div id='log'></div>
<script>
  const ws = new WebSocket(`ws://${location.host}/ws`);
  ws.onmessage = (ev) => {
    const data = JSON.parse(ev.data);
    document.getElementById('log').innerText = JSON.stringify(data);
  };
</script>
</body></html>
"""

@app.get('/')
def index():
    return HTMLResponse(HTML)

@app.websocket('/ws')
async def ws(ws: WebSocket):
    await ws.accept()
    price = 100.0
    try:
        while True:
            price += random.uniform(-1.0, 1.5)
            payload = {'symbol':'ACME', 'price': round(price,2), 'ts': time.time()}
            await ws.send_text(json.dumps(payload))
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
