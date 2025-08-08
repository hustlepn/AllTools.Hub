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

@app.route('/tools/downloader', methods=['GET', 'POST'])
def downloader():
    if request.method == 'POST':
        url = request.form['url']

        try:
            ydl_opts = {
                'quiet': True,
                'skip_download': False,
                'outtmpl': 'temp_downloads/%(title).50s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                title = info.get('title', 'video')
                ext = info.get('ext', 'mp4')

            safe_name = f"{secure_filename(title)}.{ext}"

            return send_file(
                filename,
                as_attachment=True,
                download_name=safe_name
            )

        except Exception as e:
            return render_template('tools/downloader.html', error=f"Download failed: {str(e)}")

    return render_template('tools/downloader.html')

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
