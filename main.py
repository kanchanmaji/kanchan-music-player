import os
from functools import lru_cache
from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app) # Prevents frontend blocking if accessed across local networks

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "provider": "Groq",
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "mixtral-8x7b-32768",
            "gemma2-9b-it",
            "whisper-large-v3"
        ]
    }), 200
  
# --- CACHING LOGIC ---
@lru_cache(maxsize=128)
def fetch_search_results(query):
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist", 
        "skip_download": True,
        "ignoreerrors": True, # Skips broken videos instead of crashing
        "socket_timeout": 10
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        
    if not info:
        return {"tracks": [], "source_title": "No results found"}

    tracks = []
    source_title = info.get("title") or info.get("id") or "Media Search"
    if query.startswith("ytsearch"):
        source_title = f"Search: {query.replace('ytsearch15:', '')}"

    entries = info.get("entries") if "entries" in info else [info]

    for entry in entries:
        if not entry:
            continue
        v_id = entry.get("id") or entry.get("url")
        title = entry.get("title", "Unknown Title")
        uploader = entry.get("uploader") or entry.get("channel") or "YouTube"
        thumb = entry.get("thumbnail") or f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg"

        tracks.append({
            "id": v_id,
            "title": title,
            "artist": uploader,
            "thumbnail": thumb
        })
        
    return {"tracks": tracks, "source_title": source_title}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/parse", methods=["POST"])
def parse_input():
    data = request.get_json() or {}
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Empty search query."}), 400

    if not query.startswith("http") and not query.startswith("www"):
        query = f"ytsearch15:{query}" 

    try:
        result = fetch_search_results(query)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/stream", methods=["POST"])
def get_stream():
    data = request.get_json() or {}
    video_id = data.get("video_id", "").strip()
    mode = data.get("mode", "audio")

    if not video_id:
        return jsonify({"error": "Video ID missing."}), 400

    target_url = video_id if video_id.startswith("http") else f"https://www.youtube.com/watch?v={video_id}"
    
    # Priority on m4a for audio. Browsers keep m4a alive in the background better than webm.
    format_str = "best" if mode == "video" else "bestaudio[ext=m4a]/bestaudio/best"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "format": format_str,
        "noplaylist": True,
        "socket_timeout": 10
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            stream_url = info.get("url")

            if not stream_url:
                for f in info.get("formats", []):
                    if f.get("acodec") != "none" and (mode == "video" or f.get("vcodec") == "none"):
                        stream_url = f.get("url")

            if not stream_url:
                return jsonify({"error": "Unable to resolve stream."}), 400

            return jsonify({"stream_url": stream_url}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/download", methods=["GET"])
def download_track():
    video_id = request.args.get("video_id", "").strip()
    if not video_id:
        return "Video ID missing", 400
    
    target_url = video_id if video_id.startswith("http") else f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "noplaylist": True,
        "socket_timeout": 10
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(target_url, download=False)
            stream_url = info.get("url")
            
            if stream_url:
                return redirect(stream_url)
            return "Unable to resolve download URL.", 400
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
