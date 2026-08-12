🎧 Kanchan Player

«A modern, lightweight media player powered by Python, Flask, and yt-dlp.»

Kanchan Player is a self-hostable web-based media application built with Flask and yt-dlp. It provides a clean API-driven architecture for searching media, retrieving metadata, resolving audio/video streams, and integrating those streams into a custom frontend.

Built by Kanchan Maji.

---

✨ Features

Feature| Description
🔎 Media Search| Search YouTube content directly from the application
🎵 Audio Streaming| Resolve high-quality audio streams
🎬 Video Streaming| Resolve available video streams
🖼️ Thumbnails| Automatically retrieve video thumbnails
⚡ Search Cache| Cache repeated searches using Python's "lru_cache"
🌐 REST API| Simple JSON-based API endpoints
📱 Responsive UI| Designed to work with desktop and mobile frontends
🚀 Production Ready| Compatible with Gunicorn
🧩 Self-Hosted| Run it on your own server or local machine

---

🛠️ Technology Stack

Python
   │
   ├── Flask
   │     └── REST API
   │
   └── yt-dlp
         └── Media extraction

Core Technologies

- Python — Application backend
- Flask — Web framework and REST API
- yt-dlp — Media metadata and stream extraction
- Gunicorn — Production WSGI server
- HTML / CSS / JavaScript — Frontend

---

📁 Project Structure

Kanchan-Player/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    │
    ├── css/
    │   └── style.css
    │
    ├── js/
    │   └── app.js
    │
    └── images/
        └── ...

---

⚙️ Requirements

Make sure you have:

- Python 3.9+
- "pip"
- Internet connection
- Flask
- yt-dlp
- Gunicorn (production only)

---

🚀 Installation

1. Clone the repository

git clone YOUR_REPOSITORY_URL
cd Kanchan-Player

2. Create a virtual environment

Linux / macOS

python3 -m venv venv
source venv/bin/activate

Windows

python -m venv venv
venv\Scripts\activate

3. Install dependencies

pip install -r requirements.txt

Example:

Flask
yt-dlp
gunicorn

---

▶️ Run Locally

Start the application:

python app.py

The server will run on:

http://127.0.0.1:5000

For access from another device on the same network:

http://YOUR_LOCAL_IP:5000

Example:

http://192.168.1.10:5000

---

🔌 API Documentation

🔎 Search Media

Endpoint

POST /api/parse

Request

{
  "query": "lofi music"
}

Example Response

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

---

🎵 Resolve Audio Stream

Endpoint

POST /api/stream

Request

{
  "video_id": "VIDEO_ID",
  "mode": "audio"
}

Response

{
  "stream_url": "https://..."
}

---

🎬 Resolve Video Stream

Request

{
  "video_id": "VIDEO_ID",
  "mode": "video"
}

Response

{
  "stream_url": "https://..."
}

---

⬇️ Audio Redirect

Endpoint

GET /api/download?video_id=VIDEO_ID

The server resolves the available audio stream and redirects the request to the resulting media URL.

---

🧠 Architecture

                    ┌──────────────────┐
                    │    User / UI     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Flask Server   │
                    └────────┬─────────┘
                             │
             ┌───────────────┼───────────────┐
             │               │               │
             ▼               ▼               ▼
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

---

⚡ Caching

Search results use Python's built-in "lru_cache":

@lru_cache(maxsize=128)
def fetch_search_results(query):
    ...

This prevents repeated extraction requests for recently searched queries.

Important

The cache is process-local.

If you run:

gunicorn --workers 4 app:app

each worker maintains its own cache.

For a larger deployment, Redis or another shared caching layer would be more appropriate.

---

🚀 Production Deployment

Do not use Flask's development server for production.

Use Gunicorn:

gunicorn app:app

A basic production configuration:

gunicorn \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  app:app

The correct worker configuration depends on the available CPU and memory of your server.

---

🔐 Security

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

Avoid exposing raw exceptions

Development code may contain:

except Exception as e:
    return jsonify({"error": str(e)}), 500

For production, use:

except Exception:
    app.logger.exception("Media extraction failed")
    return jsonify({
        "error": "Unable to process the request."
    }), 500

This prevents internal implementation details from being unnecessarily exposed to users.

---

📦 ".gitignore"

Do not commit local environments, secrets, caches, or temporary files.

Recommended:

# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environments
venv/
.venv/
env/

# Environment variables
.env
.env.*

# Logs
*.log

# Local configuration
*.local

# yt-dlp / cookies
cookies.txt
cookies.json

# OS files
.DS_Store
Thumbs.db

---

🔄 Updating yt-dlp

Media platforms can change their extraction systems.

Update yt-dlp regularly:

pip install -U yt-dlp

Or:

python -m pip install -U yt-dlp

---

⚠️ Limitations

Kanchan Player relies on "yt-dlp" and external media platforms.

Therefore:

- Extraction can break when platforms change their systems.
- Stream URLs may be temporary.
- Some media may not be available in every format.
- Availability can vary by region or platform.
- Multiple concurrent extraction requests can consume significant server resources.

---

⚖️ Legal & Responsible Use

Kanchan Player is intended as a technical project demonstrating Flask API development, media metadata extraction, and stream integration.

Users are responsible for complying with:

- Applicable laws
- Copyright requirements
- Platform terms of service
- Content licensing requirements
- Permissions associated with the media being accessed

Do not use the software to circumvent access controls or obtain content without the necessary rights or permissions.

---

🗺️ Roadmap

Future versions may include:

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

👨‍💻 Author

Kanchan Maji

Kanchan Player is designed and developed by Kanchan Maji.

╔══════════════════════════════════════╗
║                                      ║
║          K A N C H A N               ║
║                                      ║
║          Kanchan Player              ║
║                                      ║
╚══════════════════════════════════════╝

---

📄 License

Choose a license before distributing the project publicly.

For example:

MIT License

If using MIT, include the standard MIT License text in a separate "LICENSE" file.

---

<div align="center">🎧 Kanchan Player

Built with Python • Flask • yt-dlp

Made by Kanchan Maji

</div>
