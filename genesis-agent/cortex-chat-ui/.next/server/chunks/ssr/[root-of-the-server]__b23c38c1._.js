module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/utils/encoding.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * Encodes an ArrayBuffer into a Base64 string.
 * This is used for sending binary audio data over the WebSocket (as JSON).
 */ __turbopack_context__.s([
    "arrayBufferToBase64",
    ()=>arrayBufferToBase64,
    "base64ToArray",
    ()=>base64ToArray
]);
function arrayBufferToBase64(buffer) {
    let binary = "";
    const bytes = new Uint8Array(buffer);
    const len = bytes.byteLength;
    for(let i = 0; i < len; i++){
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}
function base64ToArray(base64) {
    const binaryString = window.atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for(let i = 0; i < len; i++){
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/hooks/useLiveConnection.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "useLiveConnection",
    ()=>useLiveConnection
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$utils$2f$encoding$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/utils/encoding.ts [app-ssr] (ecmascript)");
;
;
const RECORDER_WORKLET_PATH = "/audio-recorder-worklet.js";
const PLAYER_WORKLET_PATH = "/audio-player-worklet.js";
const FRAME_CAPTURE_INTERVAL_MS = 250;
function useLiveConnection() {
    const [connectionState, setConnectionState] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])("idle");
    const [latestTextMessage, setLatestTextMessage] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [eventLog, setEventLog] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])([]);
    const wsRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const mediaStreamRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const videoElementRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const canvasElementRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const videoLoopRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const audioPlayerContextRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const audioPlayerNodeRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const audioRecorderContextRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const audioRecorderNodeRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const sendMessage = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((data)=>{
        if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
            wsRef.current.send(JSON.stringify(data));
        }
    }, []);
    const startVideoFrameCapture = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        if (videoLoopRef.current) clearInterval(videoLoopRef.current);
        videoLoopRef.current = setInterval(()=>{
            const video = videoElementRef.current;
            const canvas = canvasElementRef.current;
            if (!video || !canvas || video.readyState < video.HAVE_METADATA) {
                return;
            }
            const { videoWidth, videoHeight } = video;
            canvas.width = videoWidth;
            canvas.height = videoHeight;
            const context = canvas.getContext("2d");
            if (!context) return;
            context.drawImage(video, 0, 0, videoWidth, videoHeight);
            const frameDataUrl = canvas.toDataURL("image/jpeg", 0.8);
            const base64Data = frameDataUrl.split(",")[1];
            sendMessage({
                mime_type: "image/jpeg",
                data: base64Data
            });
        }, FRAME_CAPTURE_INTERVAL_MS);
    }, [
        sendMessage
    ]);
    const stopVideoFrameCapture = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        if (videoLoopRef.current) {
            clearInterval(videoLoopRef.current);
            videoLoopRef.current = null;
        }
    }, []);
    const sendTextMessage = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((text)=>{
        if (!text || text.trim() === "") return;
        sendMessage({
            "mime_type": "text/plain",
            "data": text
        });
        const userEvent = {
            id: crypto.randomUUID(),
            author: 'user',
            is_partial: false,
            turn_complete: true,
            parts: [
                {
                    type: 'text',
                    data: text
                }
            ]
        };
        setEventLog((prevLog)=>[
                ...prevLog,
                userEvent
            ]);
    }, [
        sendMessage
    ]);
    const setupAudioRecording = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(async (stream)=>{
        const recorderContextOptions = {
            sampleRate: 16000
        };
        const audioTracks = stream.getAudioTracks();
        if (audioTracks.length === 0) {
            console.warn("No audio tracks found in the stream. Skipping audio recording setup.");
            return;
        }
        if (!audioRecorderContextRef.current) {
            audioRecorderContextRef.current = new AudioContext(recorderContextOptions);
        }
        const audioCtx = audioRecorderContextRef.current;
        if (audioCtx.state === 'suspended') {
            await audioCtx.resume();
        }
        try {
            await audioCtx.audioWorklet.addModule(RECORDER_WORKLET_PATH);
        } catch (e) {
            console.error("Error adding audio recorder worklet module", e);
            return;
        }
        const micSourceNode = audioCtx.createMediaStreamSource(stream);
        const workletNode = new AudioWorkletNode(audioCtx, "audio-recorder-processor");
        workletNode.port.onmessage = (event)=>{
            if (event.data.type === 'audio_data') {
                const pcmDataBuffer = event.data.buffer;
                const base64Data = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$utils$2f$encoding$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["arrayBufferToBase64"])(pcmDataBuffer);
                sendMessage({
                    mime_type: "audio/pcm",
                    data: base64Data
                });
            } else if (event.data.type === 'speech_start') {
                audioPlayerNodeRef.current?.port.postMessage({
                    type: 'flush'
                });
            }
        };
        micSourceNode.connect(workletNode);
        audioRecorderNodeRef.current = workletNode;
        console.log("Audio recorder worklet setup complete.");
    }, [
        sendMessage
    ]);
    const setupAudioPlayback = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(async ()=>{
        const playerContextOptions = {
            sampleRate: 24000
        };
        if (!audioPlayerContextRef.current) {
            audioPlayerContextRef.current = new AudioContext(playerContextOptions);
        }
        const audioCtx = audioPlayerContextRef.current;
        if (audioCtx.state === 'suspended') {
            await audioCtx.resume();
        }
        try {
            await audioCtx.audioWorklet.addModule(PLAYER_WORKLET_PATH);
            const playerNode = new AudioWorkletNode(audioCtx, "audio-player-processor");
            playerNode.connect(audioCtx.destination);
            audioPlayerNodeRef.current = playerNode;
            console.log("Audio player worklet setup complete.");
        } catch (error) {
            console.error("Error setting up audio player worklet:", error);
        }
    }, []);
    const connect = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(async (videoEl, canvasEl, userId, source)=>{
        setConnectionState("connecting");
        setLatestTextMessage(null);
        setEventLog([]);
        videoElementRef.current = videoEl;
        canvasElementRef.current = canvasEl;
        try {
            let stream;
            if (source === 'screen') {
                const screenStream = await navigator.mediaDevices.getDisplayMedia({
                    video: {
                        width: 1280,
                        height: 720
                    },
                    audio: false
                });
                let micStream = null;
                try {
                    micStream = await navigator.mediaDevices.getUserMedia({
                        audio: true,
                        video: false
                    });
                } catch (micErr) {
                    console.error("Could not get microphone audio:", micErr);
                }
                if (micStream && micStream.getAudioTracks().length > 0) {
                    stream = new MediaStream([
                        ...screenStream.getVideoTracks(),
                        ...micStream.getAudioTracks()
                    ]);
                } else {
                    stream = screenStream;
                }
            } else {
                stream = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: {
                        width: 1280,
                        height: 720
                    }
                });
            }
            mediaStreamRef.current = stream;
            videoEl.srcObject = stream;
            videoEl.play();
            const ws = new WebSocket(`wss://cortex-os-1096519851619.us-central1.run.app/ws/voice`);
            wsRef.current = ws;
            ws.onopen = ()=>{
                console.log("WebSocket connection opened.");
                setConnectionState("connected");
                setupAudioRecording(stream);
                setupAudioPlayback();
                startVideoFrameCapture();
            };
            ws.onmessage = (event)=>{
                const agentEvent = JSON.parse(event.data);
                for (const part of agentEvent.parts){
                    if (part.type === "audio/pcm") {
                        const audioDataBytes = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$utils$2f$encoding$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["base64ToArray"])(part.data);
                        audioPlayerNodeRef.current?.port.postMessage({
                            type: 'audio_data',
                            buffer: audioDataBytes.buffer
                        }, [
                            audioDataBytes.buffer
                        ]);
                    }
                }
                if (agentEvent.output_transcription) {
                    setLatestTextMessage(agentEvent.output_transcription.text);
                }
                if (agentEvent.input_transcription && agentEvent.input_transcription.is_final) {
                    const finalUserEvent = {
                        id: crypto.randomUUID(),
                        author: 'user',
                        is_partial: false,
                        turn_complete: true,
                        parts: [
                            {
                                type: 'text',
                                data: agentEvent.input_transcription.text
                            }
                        ]
                    };
                    setEventLog((prevLog)=>[
                            ...prevLog,
                            finalUserEvent
                        ]);
                }
                const finalParts = agentEvent.parts.filter((p)=>p.type === 'text' || p.type === 'function_call' || p.type === 'function_response');
                if (finalParts.length > 0 && !agentEvent.is_partial) {
                    const finalAgentEvent = {
                        id: crypto.randomUUID(),
                        author: 'agent',
                        is_partial: false,
                        turn_complete: agentEvent.turn_complete,
                        parts: finalParts
                    };
                    setEventLog((prevLog)=>[
                            ...prevLog,
                            finalAgentEvent
                        ]);
                }
                if (agentEvent.turn_complete) {
                    setLatestTextMessage(null);
                }
            };
            ws.onclose = ()=>{
                console.log("WebSocket connection closed.");
                disconnect();
            };
            ws.onerror = (error)=>{
                console.error("WebSocket error:", error);
                setConnectionState("error");
                disconnect();
            };
        } catch (error) {
            console.error("Failed to get user media:", error);
            setConnectionState("error");
        }
    }, [
        connectionState,
        setupAudioRecording,
        startVideoFrameCapture,
        setupAudioPlayback
    ]);
    const disconnect = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])(()=>{
        setConnectionState("closing");
        wsRef.current?.close();
        wsRef.current = null;
        stopVideoFrameCapture();
        audioRecorderContextRef.current?.close();
        audioRecorderNodeRef.current?.port.close();
        audioRecorderContextRef.current = null;
        audioRecorderNodeRef.current = null;
        audioPlayerContextRef.current?.close();
        audioPlayerNodeRef.current?.port.close();
        audioPlayerContextRef.current = null;
        audioPlayerNodeRef.current = null;
        mediaStreamRef.current?.getTracks().forEach((track)=>track.stop());
        mediaStreamRef.current = null;
        if (videoElementRef.current) {
            videoElementRef.current.srcObject = null;
        }
        setConnectionState("closed");
        console.log("Disconnected and cleaned up all resources.");
    }, [
        stopVideoFrameCapture
    ]);
    return {
        connectionState,
        latestTextMessage,
        eventLog,
        connect,
        disconnect,
        sendTextMessage
    };
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "SidePanel",
    ()=>SidePanel
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$bot$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Bot$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/bot.js [app-ssr] (ecmascript) <export default as Bot>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$user$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__User$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/user.js [app-ssr] (ecmascript) <export default as User>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Code$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/code.js [app-ssr] (ecmascript) <export default as Code>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$terminal$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Terminal$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/terminal.js [app-ssr] (ecmascript) <export default as Terminal>");
;
;
const EventPartCard = ({ part, author })=>{
    const isAgent = author !== 'user';
    switch(part.type){
        case 'text':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: `text-sm ${isAgent ? 'text-gray-200' : 'text-white font-medium'}`,
                children: part.data
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                lineNumber: 35,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0));
        case 'function_call':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "mt-2 bg-gray-900 rounded p-2 text-xs cursor-pointer",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        className: "font-medium text-yellow-400 flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Code$3e$__["Code"], {
                                className: "w-4 h-4"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                lineNumber: 43,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            "Function Call: ",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-yellow-200",
                                children: part.data.name
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                lineNumber: 44,
                                columnNumber: 28
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 42,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "mt-2 p-2 bg-black rounded overflow-x-auto text-gray-300",
                        children: JSON.stringify(part.data.args, null, 2)
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 46,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                lineNumber: 41,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0));
        case 'function_response':
            return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("details", {
                className: "mt-2 bg-gray-900 rounded p-2 text-xs cursor-pointer",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("summary", {
                        className: "font-medium text-purple-400 flex items-center gap-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$terminal$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Terminal$3e$__["Terminal"], {
                                className: "w-4 h-4"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                lineNumber: 55,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            "Function Response: ",
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-purple-200",
                                children: part.data.name
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                lineNumber: 56,
                                columnNumber: 32
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 54,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("pre", {
                        className: "mt-2 p-2 bg-black rounded overflow-x-auto text-gray-300",
                        children: JSON.stringify(part.data.response, null, 2)
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 58,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                lineNumber: 53,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0));
        default:
            return null;
    }
};
const SidePanel = ({ events })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "space-y-4",
        children: events.map((event)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex gap-3",
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: `flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${event.author === 'user' ? 'bg-gradient-to-r from-pink-500/20 to-cyan-500/20' : 'bg-gray-800/50'}`,
                        children: event.author === 'user' ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$user$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__User$3e$__["User"], {
                            className: "w-5 h-5"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                            lineNumber: 78,
                            columnNumber: 15
                        }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$bot$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Bot$3e$__["Bot"], {
                            className: "w-5 h-5"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                            lineNumber: 80,
                            columnNumber: 15
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 74,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "flex-1 bg-gray-800 rounded-lg p-3 space-y-2",
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                className: "text-sm font-semibold capitalize text-white",
                                children: event.author
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                lineNumber: 85,
                                columnNumber: 13
                            }, ("TURBOPACK compile-time value", void 0)),
                            event.parts.map((part, pIndex)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(EventPartCard, {
                                    part: part,
                                    author: event.author
                                }, pIndex, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                                    lineNumber: 89,
                                    columnNumber: 15
                                }, ("TURBOPACK compile-time value", void 0)))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                        lineNumber: 84,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, event.id, true, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
                lineNumber: 72,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0)))
    }, void 0, false, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>Home
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$hooks$2f$useLiveConnection$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/hooks/useLiveConnection.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$video$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Video$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/video.js [app-ssr] (ecmascript) <export default as Video>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Mic$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic.js [app-ssr] (ecmascript) <export default as Mic>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/loader-circle.js [app-ssr] (ecmascript) <export default as Loader2>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$x$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__X$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/x.js [app-ssr] (ecmascript) <export default as X>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$monitor$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Monitor$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/monitor.js [app-ssr] (ecmascript) <export default as Monitor>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$camera$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Camera$3e$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/camera.js [app-ssr] (ecmascript) <export default as Camera>");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$SidePanel$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/src/components/SidePanel.tsx [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
const SourceModal = ({ onSelect, onClose })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "bg-gray-800 rounded-lg shadow-2xl p-8 max-w-sm w-full relative",
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                    onClick: onClose,
                    className: "absolute top-4 right-4 text-gray-400 hover:text-white",
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$x$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__X$3e$__["X"], {
                        className: "w-6 h-6"
                    }, void 0, false, {
                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                        lineNumber: 29,
                        columnNumber: 11
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                    lineNumber: 25,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                    className: "text-2xl font-semibold mb-6 text-center",
                    children: "Choose your video source"
                }, void 0, false, {
                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                    lineNumber: 31,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "flex flex-col gap-4",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>onSelect("camera"),
                            className: "flex items-center justify-center gap-3 px-6 py-4 bg-blue-600 hover:bg-blue-700 rounded-lg text-lg font-semibold transition-all duration-200",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$camera$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Camera$3e$__["Camera"], {
                                    className: "w-6 h-6"
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 39,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                "Use Camera"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 35,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>onSelect("screen"),
                            className: "flex items-center justify-center gap-3 px-6 py-4 bg-gray-700 hover:bg-gray-600 rounded-lg text-lg font-semibold transition-all duration-200",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$monitor$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Monitor$3e$__["Monitor"], {
                                    className: "w-6 h-6"
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 46,
                                    columnNumber: 13
                                }, ("TURBOPACK compile-time value", void 0)),
                                "Share Screen"
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 42,
                            columnNumber: 11
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                    lineNumber: 34,
                    columnNumber: 9
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
            lineNumber: 24,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
function Home() {
    const { connectionState, latestTextMessage, eventLog, connect, disconnect } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$hooks$2f$useLiveConnection$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useLiveConnection"])();
    const videoRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const canvasRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const scrollContainerRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const [userId] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(()=>`client_${crypto.randomUUID()}`);
    const [showSourceModal, setShowSourceModal] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const [activeSource, setActiveSource] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const isStreaming = connectionState === "connected";
    const isConnecting = connectionState === "connecting";
    const handleStartStream = (source)=>{
        setShowSourceModal(false);
        if (videoRef.current && canvasRef.current) {
            setActiveSource(source);
            connect(videoRef.current, canvasRef.current, userId, source);
        } else {
            console.error("Video or Canvas refs are not set.");
        }
    };
    const handleStopStream = ()=>{
        disconnect();
        setActiveSource(null);
    };
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (scrollContainerRef.current) {
            scrollContainerRef.current.scrollTop = scrollContainerRef.current.scrollHeight;
        }
    }, [
        eventLog
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("main", {
        className: "flex flex-col h-screen w-full",
        children: [
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("canvas", {
                ref: canvasRef,
                className: "hidden"
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                lineNumber: 99,
                columnNumber: 7
            }, this),
            showSourceModal && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(SourceModal, {
                onSelect: handleStartStream,
                onClose: ()=>setShowSourceModal(false)
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                lineNumber: 102,
                columnNumber: 9
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "flex-1 overflow-hidden",
                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "h-full grid grid-cols-1 md:grid-cols-2 gap-6 p-6 [grid-template-rows:minmax(0,1fr)]",
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "bg-gray-900 border border-gray-700 rounded-lg shadow-lg flex flex-col p-6 gap-4 overflow-hidden",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                    className: "text-xl font-semibold",
                                    children: "Video Feed"
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 112,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    className: "relative w-full aspect-video bg-black rounded-lg overflow-hidden border border-gray-700",
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("video", {
                                            ref: videoRef,
                                            autoPlay: true,
                                            muted: true,
                                            playsInline: true,
                                            className: `
                  w-full h-full object-cover
                  ${activeSource === 'camera' ? 'transform -scale-x-100' : ''}
                `
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                            lineNumber: 114,
                                            columnNumber: 15
                                        }, this),
                                        !isStreaming && !isConnecting && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "absolute inset-0 bg-black/50 flex flex-col items-center justify-center z-10",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$video$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Video$3e$__["Video"], {
                                                    className: "w-16 h-16 text-gray-400"
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                    lineNumber: 126,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "mt-2 text-gray-300",
                                                    children: "Video feed is offline"
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                    lineNumber: 127,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                            lineNumber: 125,
                                            columnNumber: 17
                                        }, this),
                                        isConnecting && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "absolute inset-0 bg-black/50 backdrop-blur-sm flex flex-col items-center justify-center z-10",
                                            children: [
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Loader2$3e$__["Loader2"], {
                                                    className: "w-16 h-16 text-blue-400 animate-spin"
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                    lineNumber: 132,
                                                    columnNumber: 19
                                                }, this),
                                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                                    className: "mt-4 text-lg",
                                                    children: "Connecting..."
                                                }, void 0, false, {
                                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                    lineNumber: 133,
                                                    columnNumber: 19
                                                }, this)
                                            ]
                                        }, void 0, true, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                            lineNumber: 131,
                                            columnNumber: 17
                                        }, this),
                                        isStreaming && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                            className: "absolute top-4 left-4 z-20",
                                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                                className: "flex items-center gap-2 bg-red-600 px-3 py-1 rounded-full text-sm font-medium animate-pulse",
                                                children: [
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Mic$3e$__["Mic"], {
                                                        className: "w-4 h-4"
                                                    }, void 0, false, {
                                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                        lineNumber: 139,
                                                        columnNumber: 21
                                                    }, this),
                                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                                                        children: "LIVE"
                                                    }, void 0, false, {
                                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                        lineNumber: 140,
                                                        columnNumber: 21
                                                    }, this)
                                                ]
                                            }, void 0, true, {
                                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                                lineNumber: 138,
                                                columnNumber: 19
                                            }, this)
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                            lineNumber: 137,
                                            columnNumber: 17
                                        }, this)
                                    ]
                                }, void 0, true, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 113,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 111,
                            columnNumber: 11
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                            className: "bg-gray-900 border border-gray-700 rounded-lg shadow-lg flex flex-col p-6 gap-4",
                            children: [
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("h2", {
                                    className: "text-xl font-semibold",
                                    children: "Transcript"
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 148,
                                    columnNumber: 13
                                }, this),
                                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    ref: scrollContainerRef,
                                    className: "flex-1 overflow-y-auto pr-2",
                                    children: eventLog.length === 0 ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                        className: "flex flex-col items-center justify-center h-full text-gray-500",
                                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                                            children: "Start a conversation to see the transcript."
                                        }, void 0, false, {
                                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                            lineNumber: 153,
                                            columnNumber: 19
                                        }, this)
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                        lineNumber: 152,
                                        columnNumber: 17
                                    }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$src$2f$components$2f$SidePanel$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["SidePanel"], {
                                        events: eventLog
                                    }, void 0, false, {
                                        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                        lineNumber: 156,
                                        columnNumber: 17
                                    }, this)
                                }, void 0, false, {
                                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                    lineNumber: 150,
                                    columnNumber: 13
                                }, this)
                            ]
                        }, void 0, true, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 147,
                            columnNumber: 11
                        }, this)
                    ]
                }, void 0, true, {
                    fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                    lineNumber: 109,
                    columnNumber: 9
                }, this)
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                lineNumber: 108,
                columnNumber: 7
            }, this),
            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("footer", {
                className: "w-full p-4 flex justify-center items-center gap-4 bg-gray-900 border-t border-gray-700",
                children: !isStreaming && !isConnecting ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: ()=>setShowSourceModal(true),
                            className: "p-4 bg-gray-700 hover:bg-gray-600 rounded-full text-white transition-all",
                            "aria-label": "Start recording",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__Mic$3e$__["Mic"], {
                                className: "w-6 h-6"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                lineNumber: 172,
                                columnNumber: 15
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 167,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "text-gray-400",
                            children: "Click the icon to start recording"
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 174,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
                            onClick: handleStopStream,
                            className: "p-4 bg-red-600 hover:bg-red-700 rounded-full text-white transition-all",
                            "aria-label": "Stop recording",
                            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$x$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__$3c$export__default__as__X$3e$__["X"], {
                                className: "w-6 h-6"
                            }, void 0, false, {
                                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                                lineNumber: 185,
                                columnNumber: 15
                            }, this)
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 180,
                            columnNumber: 13
                        }, this),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            className: "text-gray-400",
                            children: isConnecting ? "Connecting..." : "Recording in progress..."
                        }, void 0, false, {
                            fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                            lineNumber: 187,
                            columnNumber: 13
                        }, this)
                    ]
                }, void 0, true)
            }, void 0, false, {
                fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
                lineNumber: 164,
                columnNumber: 7
            }, this)
        ]
    }, void 0, true, {
        fileName: "[project]/Agent master /genesis-agent/cortex-chat-ui/src/app/page.tsx",
        lineNumber: 98,
        columnNumber: 5
    }, this);
}
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
;
else {
    if ("TURBOPACK compile-time falsy", 0) //TURBOPACK unreachable
    ;
    else {
        if ("TURBOPACK compile-time truthy", 1) {
            if ("TURBOPACK compile-time truthy", 1) {
                module.exports = __turbopack_context__.r("[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)");
            } else //TURBOPACK unreachable
            ;
        } else //TURBOPACK unreachable
        ;
    }
} //# sourceMappingURL=module.compiled.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].ReactJsxDevRuntime; //# sourceMappingURL=react-jsx-dev-runtime.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)", ((__turbopack_context__, module, exports) => {
"use strict";

module.exports = __turbopack_context__.r("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/module.compiled.js [app-ssr] (ecmascript)").vendored['react-ssr'].React; //# sourceMappingURL=react.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/shared/src/utils.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "hasA11yProp",
    ()=>hasA11yProp,
    "mergeClasses",
    ()=>mergeClasses,
    "toCamelCase",
    ()=>toCamelCase,
    "toKebabCase",
    ()=>toKebabCase,
    "toPascalCase",
    ()=>toPascalCase
]);
const toKebabCase = (string)=>string.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
const toCamelCase = (string)=>string.replace(/^([A-Z])|[\s-_]+(\w)/g, (match, p1, p2)=>p2 ? p2.toUpperCase() : p1.toLowerCase());
const toPascalCase = (string)=>{
    const camelCase = toCamelCase(string);
    return camelCase.charAt(0).toUpperCase() + camelCase.slice(1);
};
const mergeClasses = (...classes)=>classes.filter((className, index, array)=>{
        return Boolean(className) && className.trim() !== "" && array.indexOf(className) === index;
    }).join(" ").trim();
const hasA11yProp = (props)=>{
    for(const prop in props){
        if (prop.startsWith("aria-") || prop === "role" || prop === "title") {
            return true;
        }
    }
};
;
 //# sourceMappingURL=utils.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/defaultAttributes.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>defaultAttributes
]);
var defaultAttributes = {
    xmlns: "http://www.w3.org/2000/svg",
    width: 24,
    height: 24,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round",
    strokeLinejoin: "round"
};
;
 //# sourceMappingURL=defaultAttributes.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/Icon.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>Icon
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$defaultAttributes$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/defaultAttributes.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/shared/src/utils.js [app-ssr] (ecmascript)");
;
;
;
const Icon = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["forwardRef"])(({ color = "currentColor", size = 24, strokeWidth = 2, absoluteStrokeWidth, className = "", children, iconNode, ...rest }, ref)=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createElement"])("svg", {
        ref,
        ...__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$defaultAttributes$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"],
        width: size,
        height: size,
        stroke: color,
        strokeWidth: absoluteStrokeWidth ? Number(strokeWidth) * 24 / Number(size) : strokeWidth,
        className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["mergeClasses"])("lucide", className),
        ...!children && !(0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["hasA11yProp"])(rest) && {
            "aria-hidden": "true"
        },
        ...rest
    }, [
        ...iconNode.map(([tag, attrs])=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createElement"])(tag, attrs)),
        ...Array.isArray(children) ? children : [
            children
        ]
    ]));
;
 //# sourceMappingURL=Icon.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "default",
    ()=>createLucideIcon
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/shared/src/utils.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$Icon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/Icon.js [app-ssr] (ecmascript)");
;
;
;
const createLucideIcon = (iconName, iconNode)=>{
    const Component = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["forwardRef"])(({ className, ...props }, ref)=>(0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createElement"])(__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$Icon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
            ref,
            iconNode,
            className: (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["mergeClasses"])(`lucide-${(0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toKebabCase"])((0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toPascalCase"])(iconName))}`, `lucide-${iconName}`, className),
            ...props
        }));
    Component.displayName = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$shared$2f$src$2f$utils$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["toPascalCase"])(iconName);
    return Component;
};
;
 //# sourceMappingURL=createLucideIcon.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/video.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Video
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5",
            key: "ftymec"
        }
    ],
    [
        "rect",
        {
            x: "2",
            y: "6",
            width: "14",
            height: "12",
            rx: "2",
            key: "158x01"
        }
    ]
];
const Video = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("video", __iconNode);
;
 //# sourceMappingURL=video.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/video.js [app-ssr] (ecmascript) <export default as Video>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Video",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$video$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$video$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/video.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Mic
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M12 19v3",
            key: "npa21l"
        }
    ],
    [
        "path",
        {
            d: "M19 10v2a7 7 0 0 1-14 0v-2",
            key: "1vc78b"
        }
    ],
    [
        "rect",
        {
            x: "9",
            y: "2",
            width: "6",
            height: "13",
            rx: "3",
            key: "s6n7sd"
        }
    ]
];
const Mic = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("mic", __iconNode);
;
 //# sourceMappingURL=mic.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic.js [app-ssr] (ecmascript) <export default as Mic>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Mic",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$mic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/mic.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/loader-circle.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>LoaderCircle
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M21 12a9 9 0 1 1-6.219-8.56",
            key: "13zald"
        }
    ]
];
const LoaderCircle = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("loader-circle", __iconNode);
;
 //# sourceMappingURL=loader-circle.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/loader-circle.js [app-ssr] (ecmascript) <export default as Loader2>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Loader2",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$loader$2d$circle$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/loader-circle.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/x.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>X
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M18 6 6 18",
            key: "1bl5f8"
        }
    ],
    [
        "path",
        {
            d: "m6 6 12 12",
            key: "d8bk6v"
        }
    ]
];
const X = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("x", __iconNode);
;
 //# sourceMappingURL=x.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/x.js [app-ssr] (ecmascript) <export default as X>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "X",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$x$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$x$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/x.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/monitor.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Monitor
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "rect",
        {
            width: "20",
            height: "14",
            x: "2",
            y: "3",
            rx: "2",
            key: "48i651"
        }
    ],
    [
        "line",
        {
            x1: "8",
            x2: "16",
            y1: "21",
            y2: "21",
            key: "1svkeh"
        }
    ],
    [
        "line",
        {
            x1: "12",
            x2: "12",
            y1: "17",
            y2: "21",
            key: "vw1qmm"
        }
    ]
];
const Monitor = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("monitor", __iconNode);
;
 //# sourceMappingURL=monitor.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/monitor.js [app-ssr] (ecmascript) <export default as Monitor>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Monitor",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$monitor$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$monitor$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/monitor.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/camera.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Camera
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M13.997 4a2 2 0 0 1 1.76 1.05l.486.9A2 2 0 0 0 18.003 7H20a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h1.997a2 2 0 0 0 1.759-1.048l.489-.904A2 2 0 0 1 10.004 4z",
            key: "18u6gg"
        }
    ],
    [
        "circle",
        {
            cx: "12",
            cy: "13",
            r: "3",
            key: "1vg3eu"
        }
    ]
];
const Camera = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("camera", __iconNode);
;
 //# sourceMappingURL=camera.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/camera.js [app-ssr] (ecmascript) <export default as Camera>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Camera",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$camera$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$camera$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/camera.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/bot.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Bot
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M12 8V4H8",
            key: "hb8ula"
        }
    ],
    [
        "rect",
        {
            width: "16",
            height: "12",
            x: "4",
            y: "8",
            rx: "2",
            key: "enze0r"
        }
    ],
    [
        "path",
        {
            d: "M2 14h2",
            key: "vft8re"
        }
    ],
    [
        "path",
        {
            d: "M20 14h2",
            key: "4cs60a"
        }
    ],
    [
        "path",
        {
            d: "M15 13v2",
            key: "1xurst"
        }
    ],
    [
        "path",
        {
            d: "M9 13v2",
            key: "rq6x2g"
        }
    ]
];
const Bot = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("bot", __iconNode);
;
 //# sourceMappingURL=bot.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/bot.js [app-ssr] (ecmascript) <export default as Bot>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Bot",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$bot$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$bot$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/bot.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/user.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>User
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2",
            key: "975kel"
        }
    ],
    [
        "circle",
        {
            cx: "12",
            cy: "7",
            r: "4",
            key: "17ys0d"
        }
    ]
];
const User = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("user", __iconNode);
;
 //# sourceMappingURL=user.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/user.js [app-ssr] (ecmascript) <export default as User>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "User",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$user$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$user$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/user.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/code.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Code
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "m16 18 6-6-6-6",
            key: "eg8j8"
        }
    ],
    [
        "path",
        {
            d: "m8 6-6 6 6 6",
            key: "ppft3o"
        }
    ]
];
const Code = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("code", __iconNode);
;
 //# sourceMappingURL=code.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/code.js [app-ssr] (ecmascript) <export default as Code>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Code",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$code$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/code.js [app-ssr] (ecmascript)");
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/terminal.js [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

/**
 * @license lucide-react v0.544.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */ __turbopack_context__.s([
    "__iconNode",
    ()=>__iconNode,
    "default",
    ()=>Terminal
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/createLucideIcon.js [app-ssr] (ecmascript)");
;
const __iconNode = [
    [
        "path",
        {
            d: "M12 19h8",
            key: "baeox8"
        }
    ],
    [
        "path",
        {
            d: "m4 17 6-6-6-6",
            key: "1yngyt"
        }
    ]
];
const Terminal = (0, __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$createLucideIcon$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])("terminal", __iconNode);
;
 //# sourceMappingURL=terminal.js.map
}),
"[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/terminal.js [app-ssr] (ecmascript) <export default as Terminal>", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "Terminal",
    ()=>__TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$terminal$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"]
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$Agent__master__$2f$genesis$2d$agent$2f$cortex$2d$chat$2d$ui$2f$node_modules$2f$lucide$2d$react$2f$dist$2f$esm$2f$icons$2f$terminal$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/Agent master /genesis-agent/cortex-chat-ui/node_modules/lucide-react/dist/esm/icons/terminal.js [app-ssr] (ecmascript)");
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__b23c38c1._.js.map