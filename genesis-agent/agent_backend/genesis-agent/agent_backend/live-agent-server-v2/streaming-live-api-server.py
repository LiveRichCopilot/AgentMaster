
import os
import asyncio
import json
import logging
from aiohttp import web, ClientSession, TCPConnector
import ssl
import certifi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

# Corrected model name as per user specification
MODEL_NAME = "gemini-live-2.5-flash-preview-native-audio"

class MultimodalStreamingServer:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_get('/ws', self.handle_websocket)
        # Removed all static file and index.html serving logic that caused the crash

    async def handle_websocket(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        logger.info("✅ Client connected for multimodal streaming")

        gemini_session = None
        gemini_ws = None

        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = TCPConnector(ssl=ssl_context)
            gemini_session = ClientSession(connector=connector)

            gemini_url = f"wss://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:streamGenerateContent?key={GOOGLE_API_KEY}"
            gemini_ws = await gemini_session.ws_connect(gemini_url)
            logger.info(f"✅ Connected to Gemini API: {MODEL_NAME}")

            setup_msg = {
                "setup": {
                    "model": f"models/{MODEL_NAME}",
                    "generation_config": {
                        "response_modalities": ["AUDIO"],
                        "input_audio_transcription": {},
                        "output_audio_transcription": {},
                    },
                    "multimodal_config": {"enabled": True},
                }
            }
            await gemini_ws.send_str(json.dumps(setup_msg))
            logger.info("📤 Sent multimodal setup to Gemini")

            setup_response = await gemini_ws.receive()
            if setup_response.type == web.WSMsgType.TEXT:
                response_data = json.loads(setup_response.data)
                if "setupComplete" in response_data or "setup" in response_data:
                    await ws.send_json({"type": "ready", "status": "Multimodal streaming ready"})
                    logger.info("✅ Multimodal setup complete")

            client_streamer = asyncio.create_task(self.stream_from_client(ws, gemini_ws))
            gemini_streamer = asyncio.create_task(self.stream_from_gemini(gemini_ws, ws))
            await asyncio.gather(client_streamer, gemini_streamer)

        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            await ws.send_json({"type": "error", "message": str(e)})
        finally:
            if gemini_ws: await gemini_ws.close()
            if gemini_session: await gemini_session.close()
            logger.info("🔌 Streaming session ended")

        return ws

    async def stream_from_client(self, client_ws, gemini_ws):
        try:
            async for msg in client_ws:
                if msg.type == web.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if "realtimeInput" in data and "mediaChunks" in data["realtimeInput"]:
                        streaming_msg = {"realtime_input": data["realtimeInput"]}
                        await gemini_ws.send_str(json.dumps(streaming_msg))
                    elif "clientContent" in data:
                        await gemini_ws.send_str(json.dumps(data))
                elif msg.type == web.WSMsgType.ERROR:
                    logger.error(f"Client streaming error: {client_ws.exception()}")
                    break
        except Exception as e:
            logger.error(f"Error in client streaming: {e}", exc_info=True)

    async def stream_from_gemini(self, gemini_ws, client_ws):
        try:
            async for msg in gemini_ws:
                if msg.type == web.WSMsgType.TEXT:
                    await client_ws.send_str(msg.data)
                elif msg.type == web.WSMsgType.ERROR:
                    logger.error(f"Gemini streaming error: {gemini_ws.exception()}")
                    break
        except Exception as e:
            logger.error(f"Error in Gemini streaming: {e}", exc_info=True)

    async def start(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        port = int(os.environ.get("PORT", 8080))
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"🎙️ Multimodal Streaming Server running on http://0.0.0.0:{port}")
        await asyncio.Event().wait()

async def main():
    server = MultimodalStreamingServer()
    await server.start()

if __name__ == "__main__":
    asyncio.run(main())
