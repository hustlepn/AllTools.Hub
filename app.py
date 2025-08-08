from flask import Flask, render_template, request, send_file, send_from_directory
from werkzeug.utils import secure_filename
import yt_dlp
import os
import requests
from datetime import datetime
import shutil

app = Flask(__name__)

# Create temp directory for downloads
os.makedirs('temp_downloads', exist_ok=True)

# Main Pages
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

# Tools
@app.route('/tools/pdf_tools')
def pdf_tools():
    return render_template('tools/pdf_tools.html')

@app.route('/tools/qr')
def qr():
    return render_template('tools/qr.html')

@app.route('/tools/shortener')
def shortener():
    return render_template('tools/shortener.html')

# ---------- REPLACE the downloader route in app.py with this ----------
@app.route('/tools/downloader', methods=['GET', 'POST'])
def downloader():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            return render_template('tools/downloader.html', error="Please paste a video URL first.")

        # Create per-request temp folder (safer for concurrency)
        temp_dir = tempfile.mkdtemp(prefix="dl_")
        try:
            # Basic output template inside temp dir
            outtmpl = os.path.join(temp_dir, "%(title).50s.%(ext)s")

            # Detect if ffmpeg is available in PATH
            ffmpeg_available = shutil.which('ffmpeg') is not None

            # Base options
            ydl_opts = {
                'outtmpl': outtmpl,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # If ffmpeg found, allow merging to mp4 for best quality
                # else, try to prefer single-file mp4 if possible (no-merge fallback)
            }

            if ffmpeg_available:
                ydl_opts.update({
                    'format': 'bestvideo+bestaudio/best',
                    'merge_output_format': 'mp4',
                })
            else:
                # no ffmpeg -> avoid requesting merge to prevent failure
                # prefer mp4 if available, or best available
                ydl_opts.update({
                    'format': 'best[ext=mp4]/best',
                })

            # If there's a cookies file for Instagram, use it (optional)
            # The project will look for cookies_instagram.txt at project root
            cookies_path = os.path.join(os.getcwd(), "cookies_instagram.txt")
            if os.path.isfile(cookies_path):
                ydl_opts['cookiefile'] = cookies_path

            # Run yt-dlp and download into temp_dir
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)

            # Prepare file path to send back
            # If the extractor created multiple files, find the largest file in temp_dir
            files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]
            if not files:
                raise Exception("No file was downloaded.")

            # Choose the biggest file (likely the merged mp4)
            files.sort(key=lambda x: os.path.getsize(x), reverse=True)
            file_path = files[0]
            filename = os.path.basename(file_path)

            # Create safe download name and send the file
            safe_download_name = secure_filename(filename)
            return send_file(file_path, as_attachment=True, download_name=safe_download_name)

        except Exception as e:
            # Show a user-friendly error (but log the real one on server logs)
            app.logger.exception("Downloader error")
            msg = str(e)
            # Provide clearer hints for common problems
            if "cookiefile" in msg.lower():
                hint = " (Instagram may require login cookies — see settings)"
                msg = msg + hint
            return render_template('tools/downloader.html', error=f"Download failed: {msg}")
        finally:
            # Clean up temp dir (delete files)
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass

    # GET request -> show form
    return render_template('tools/downloader.html')
# ---------------------------------------------------------------------

@app.route('/tools/calculator')
def calculator():
    return render_template('tools/calculator.html')

# Blog
@app.route('/blog')
def blog():
    return render_template('blog.html')

# Blog Posts
@app.route('/blog/video-guide')
def video_guide():
    return render_template('blog_posts/video_guide.html')

@app.route('/blog/url-safety')
def url_safety():
    return render_template('blog_posts/url_safety.html')

@app.route('/blog/pdf-security')
def pdf_security():
    return render_template('blog_posts/pdf_security.html')

@app.route('/blog/loan-tips')
def loan_tips():
    return render_template('blog_posts/loan_tips.html')

@app.route('/blog/qr-uses')
def qr_uses():
    return render_template('blog_posts/qr_uses.html')

@app.route('/blog/pdf-merge')
def pdf_merge():
    return render_template('blog_posts/pdf_merge.html')

@app.route('/blog/video-formats')
def video_formats():
    return render_template('blog_posts/video_formats.html')

@app.route('/blog/url-tracking')
def url_tracking():
    return render_template('blog_posts/url_tracking.html')

@app.route('/blog/pdf-accessibility')
def pdf_accessibility():
    return render_template('blog_posts/pdf_accessibility.html')

@app.route('/blog/social-media-tips')
def social_media_tips():
    return render_template('blog_posts/social_media_tips.html')

# Verification Files
@app.route('/google-site-verification.html')
def google_verification():
    return send_from_directory('static', 'google-site-verification.html')

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

# Cleanup temporary files
@app.after_request
def remove_temp_files(response):
    try:
        for filename in os.listdir('temp_downloads'):
            file_path = os.path.join('temp_downloads', filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                app.logger.error(f"Error deleting {file_path}: {e}")
    except Exception as e:
        app.logger.error(f"Temp cleanup error: {e}")
    return response

if __name__ == '__main__':
    app.run(debug=True)
