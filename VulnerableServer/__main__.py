import os
import pdfkit
from uuid import uuid4
from flask import Flask, render_template, request, Response, redirect, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid4())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if 'url' not in request.form:
        return render_template('index.html', error='Invalid form submission')

    url = request.form['url']
    temp_name = os.path.join(os.path.dirname(__file__), f'temp', f'temp-{uuid4()}.pdf')

    try:
        pdfkit.from_url(url, temp_name)
    except OSError as e:
        print(f"Url: {url}\nError: {e}")
        flash('Error: Website not found')
        return redirect('/', 301)

    with open(temp_name, 'rb') as pdf:
        response = Response(pdf.read(), mimetype='application/pdf', headers={'Content-Disposition': f'attachment; filename={url}.pdf'})
    
    os.remove(temp_name)
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)