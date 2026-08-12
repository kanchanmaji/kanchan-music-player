# 🎧 Kanchan Player

> A modern, lightweight media player powered by Python, Flask, and yt-dlp.

**Kanchan Player** is a self-hostable web-based media application built with Flask and yt-dlp. It provides a clean API-driven architecture for searching media, retrieving metadata, resolving audio/video streams, and integrating those streams into a custom frontend.

**Built by Kanchan Maji.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔎 Media Search | Search YouTube content directly from the application |
| 🎵 Audio Streaming | Resolve available audio streams |
| 🎬 Video Streaming | Resolve available video streams |
| 🖼️ Thumbnails | Automatically retrieve video thumbnails |
| ⚡ Search Cache | Cache repeated searches using Python's `lru_cache` |
| 🌐 REST API | Simple JSON-based API endpoints |
| 📱 Responsive UI | Designed for desktop and mobile frontends |
| 🚀 Production Ready | Compatible with Gunicorn |
| 🧩 Self-Hosted | Run on your own server or local machine |

---

## 🛠️ Technology Stack

- **Python** — Backend
- **Flask** — Web framework and REST API
- **yt-dlp** — Media metadata and stream extraction
- **Gunicorn** — Production WSGI server
- **HTML / CSS / JavaScript** — Frontend

---

## 📁 Project Structure

```text
Kanchan-Player/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
    └── index.html
```

---

## ⚙️ Requirements

- Python **3.9+**
- `pip`
- Internet connection
- Flask
- yt-dlp
- Gunicorn *(production only)*

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/kanchanmaji/kanchan-music-player.git
cd Kanchan-Player
```

### 2. Create a virtual environment

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
Flask
yt-dlp
gunicorn
```

---

## ▶️ Run Locally

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

For another device on the same network:

```text
http://YOUR_LOCAL_IP:5000
```

---

# 🔌 API Documentation

## 🔎 Search Media

### Endpoint

```http
POST /api/parse
Content-Type: application/json
```

### Request

```json
{
  "query": "lofi music"
}
```

### Example Response

```json
{
  "source_title": "Search: lofi music",
  "tracks": [
    {
      "id": "VIDEO_ID",
      "title": "Example Track",
      "artist": "Example Channel",
      "thumbnail": "https://i.ytimg.com/vi/VIDEO_ID/hqdefault.jpg"
    }
  ]
}
```

---

## 🎵 Resolve Audio Stream

### Endpoint

```http
POST /api/stream
Content-Type: application/json
```

### Request

```json
{
  "video_id": "VIDEO_ID",
  "mode": "audio"
}
```

### Response

```json
{
  "stream_url": "https://..."
}
```

---

## 🎬 Resolve Video Stream

### Request

```json
{
  "video_id": "VIDEO_ID",
  "mode": "video"
}
```

### Response

```json
{
  "stream_url": "https://..."
}
```

---

## ⬇️ Audio Redirect

### Endpoint

```http
GET /api/download?video_id=VIDEO_ID
```

The endpoint resolves the available audio stream and redirects the request to the resulting media URL.

---

# 🧠 Architecture

```text
                    ┌──────────────────┐
                    │    User / UI        │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Flask Server      │
                    └────────┬─────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │             │
             ▼               ▼            ▼
        /api/parse      /api/stream     /api/download
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                    ┌──────────────────┐
                    │      yt-dlp      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Media Platform   │
                    └──────────────────┘
```

---

# ⚡ Caching

Search results use Python's built-in `lru_cache`:

```python
@lru_cache(maxsize=128)
def fetch_search_results(query):
    ...
```

This reduces repeated extraction requests for identical searches.

The cache is **process-local**. With multiple Gunicorn workers, each worker has its own cache.

For larger deployments, Redis or another shared cache can be used.

---

# 🚀 Production Deployment

Do **not** use Flask's development server for production.

Use Gunicorn:

```bash
gunicorn app:app
```

Example:

```bash
gunicorn --workers 2 --threads 4 --timeout 120 app:app
```

Adjust the configuration according to the resources of your server.

---

# 🔐 Security

Before exposing Kanchan Player publicly, consider implementing:

- Rate limiting
- Request validation
- API authentication
- CORS restrictions
- Proper error handling
- Server-side logging
- Request timeouts
- Abuse protection
- Resource limits

For production, avoid returning raw internal exceptions to clients.

Instead of:

```python
except Exception as e:
    return jsonify({"error": str(e)}), 500
```

prefer:

```python
except Exception:
    app.logger.exception("Media extraction failed")
    return jsonify({
        "error": "Unable to process the request."
    }), 500
```

---

# 📦 `.gitignore`

Recommended:

```gitignore
__pycache__/
*.py[cod]
*.pyo

venv/
.venv/
env/

.env
.env.*

*.log
*.local

cookies.txt
cookies.json

.DS_Store
Thumbs.db
```

---

# 🔄 Updating yt-dlp

Media platforms can change their extraction systems. Keep yt-dlp updated:

```bash
python -m pip install -U yt-dlp
```

---

# ⚠️ Limitations

Kanchan Player relies on yt-dlp and external media platforms.

Therefore:

- Extraction can break when platforms change their systems.
- Stream URLs may be temporary.
- Some media may not be available in every format.
- Availability can vary by region or platform.
- Concurrent extraction can consume significant server resources.

---

# ⚖️ Legal & Responsible Use

Kanchan Player is intended as a technical project demonstrating Flask API development, media metadata extraction, and stream integration.

Users are responsible for complying with applicable laws, copyright requirements, platform terms of service, and content licensing requirements.

Do not use the software to circumvent access controls or obtain content without the necessary rights or permissions.

---

# 🗺️ Roadmap

- [ ] Modern music-player interface
- [ ] Playlist support
- [ ] Queue management
- [ ] Search history
- [ ] Favorites
- [ ] Recently played tracks
- [ ] Audio quality selection
- [ ] Video quality selection
- [ ] Progressive Web App support
- [ ] Dark / light themes
- [ ] Keyboard shortcuts
- [ ] Redis caching
- [ ] API authentication
- [ ] Rate limiting
- [ ] Docker deployment
- [ ] Automated CI/CD

---

# 👨‍💻 Author

## Kanchan Maji

**Kanchan Player** is designed and developed by **Kanchan Maji**.

```text
╔════════════════════════════════╗
║                                      ║
║          K A N C H A N               ║
║                                      ║
║          Kanchan Player              ║
║                                      ║
╚════════════════════════════════╝
```


<div align="center">

### 🎧 Kanchan Player

**Built with Python • Flask • yt-dlp**

**Made by Kanchan Maji**

</div>
