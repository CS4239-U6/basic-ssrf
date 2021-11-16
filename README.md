# Basic SSRF

A basic example of a SSRF vulnerability.

## Run using Python

1. Clone the repo with `git clone https://github.com/CS4239-U6/blind-ssrf.git`.
1. Go into the folder with `cd basic-ssrf`.
1. Install the requirements with `pip3 install -r requirements.txt`.
1. Install `wkhtmltopdf` using instructions from <https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf>.
1. Run `python3 ./HiddenLocalServer/__main__.py` to run the hidden local server.
1. Run `python3 ./VulnerableServer/__main__.py` to run the web facing server.
1. Visit `http://localhost:5000` to see the website.

## Run using Docker

If you do not wish to set up the Python and `wkhtmltopdf` dependencies above, an easier way to get started is using Docker.

> Note: The Dockerfile may not work on a M1 Mac due to the architecture differences, which affects the `wkhtmltopdf` installation.

Make sure you have Docker installed locally before doing the following:

1. Build the file with `docker build -t basic-ssrf .`.
1. Run the Dockerfile with `docker run -dt -p 5000:5000 basic-ssrf`.
1. Visit `http://localhost:5000` to see the website.

## Vulnerability

1. (If running on Docker) Enter `http://localhost:5001` directly. You will see that you are unable to access the website.
1. Enter `http://localhost:5001` in `http://localhost:5000` and the server will visit the webpage and fetch what is on the webpage.

## Defenses

### Allowlisting

An allowlist of allowed websites can be put in place in order to narrow the scope of the websites that the user can visit.
This can be both in the sense of the URL schemas or even the URLs themselves.
However, with many websites, the allowlist can accumulate and before very long.

Example of code that can be added:

```python
ALLOWLIST = ('http://www.google.com',)

# ...

# Within the function that checks IP
url = request.form.get('url', '')

if url not in ALLOWLIST:
   flash('URL is not in allowlist')
   return redirect(url_for('index'))

# ...
```

### Denylisting

A denylist of websites that are not allowed. The opposite of an allowlist.
This can be both in the sense of the URL schemas or even the URLs themselves.
Note that in this case it is very easy to miss out a website and this will result in a possible SSRF attack on the website itself.

It may also be avoided when the user changes the representation.
For example, `localhost:3000` == `127.0.0.1:3000` == `127.1:3000`

Example of code that can be added:

```python
DENYLIST = ("127.0.0.1",)

# ...

# Within function that checks IP
ip = socket.gethostbyname(url)
if ip in DENYLIST:
   flash('URL is in denylist')
   return redirect(url_for('index'))

# ...
```

### Input Sanitisation

The input URLs can be filtered and check if it points to any internal service before they are are passed to the PDF downloader.
This can be both in the sense of the URL schemas or even the URLs themselves.

Input sanitisation may contain loopholes it if makes use of replacements.
For example, if we replace all `../` with `/`, `....//` -> `../`, the attacker is still able to do `../`.

Example of code that can be added:

```python
from urllib.parse import quote

# Within the function that checks IP
url = request.form.get('url', '')
sanitized_url = quote(url, safe='/:?&')

# Work with sanitized_url
# ...
```

### Enable authentication on all servers

When the vulnerable server makes a request to the hidden local server, the vulnerable server will need to authenticate.
Without the authentication details, the malicious user is unable to access any information.

This is to be implemented on all other servers including the vulnerable server.
