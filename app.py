from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

# Tool routes
@app.route('/tools/downloader')
def downloader():
    return render_template('tools/downloader.html')

@app.route('/tools/shortener')
def shortener():
    return render_template('tools/shortener.html')

@app.route('/tools/qr')
def qr():
    return render_template('tools/qr.html')

@app.route('/tools/pdf_tools')
def pdf_tools():
    return render_template('tools/pdf_tools.html')

@app.route('/tools/calculator')
def calculator():
    return render_template('tools/calculator.html')

# Add these before if __name__ == '__main__':
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)
