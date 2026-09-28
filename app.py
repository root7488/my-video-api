from flask import Flask, jsonify, request
import yt_dlp

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "My Video API is working!"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })


@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    video_url = data.get("url", "").strip()

    if not video_url:
        return jsonify({
            "status": "error",
            "message": "Video URL is required"
        }), 400

    try:
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)

        formats = []

        for f in info.get("formats", []):
            url = f.get("url")
            if not url:
                continue

            formats.append({
                "format_id": f.get("format_id"),
                "quality": f.get("format_note") or f.get("resolution"),
                "extension": f.get("ext"),
                "width": f.get("width"),
                "height": f.get("height"),
                "video_url": url
            })

        return jsonify({
            "status": "success",
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "formats": formats
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
