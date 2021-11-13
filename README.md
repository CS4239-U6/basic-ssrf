# Basic SSRF
A Basic example of an SSRF vulnerability


# Quick start
1. Clone the repo with `git clone {url}`
2. Go into the folder with `cd basic-ssrf`
3. Install the requirements with `pip3 install -r requirements.txt`
4. Run `python ./HiddenLocalServer/__main__.py` to run the hidden local server.
5. Run `python ./VulnerableServer/__main__.py` to run the web facing server.
6. Visit `http://localhost:5000` to see the website


# Setup with Docker
1. Build the file with `docker build -t basic-ssrf .`
2. Run the dockerfile with `docker run  -dt -p 5000:5000 basic-ssrf`
3. Visit `localhost:5000` to see the website



# Vulnerability
1. Enter `http://localhost:5001` directly
   1. Unable to access the website
2. Enter `http://localhost:5001` in `http://localhost:5000` and the server will visit the webpage and fetch what is on the webpage


# Defenses

## White listing

A whitelist of allowed websites can be put in place in order to narrow the scope of the websites that the user can visit.
This can be both in the sense of the URL schemas or even the urls themselves.
With many websites, the whitelist can accumulate and before very long.

Code addition:
```python
WHITE_LIST = ('http://www.google.com',)
...

# Within the function that checks IP
url = request.form.get('url', '')

if url not in WHITE_LIST:
   flash('Url is not in whitelist')
   return redirect(url_for('index'))
...
```


## Black listing

A blacklist of websites that are not allowed. The opposite of a whitelist.
This can be both in the sense of the URL schemas or even the urls themselves.
Note that in this case it is very easy to miss out a website and this will result in possible SSRF on the website itself.

It can also be avoided when the user changes the representation. EG: `localhost:3000` == `127.0.0.1:3000` == `127.1:3000`

```python
BLACK_LIST = ("127.0.0.1",)
...

# Within function that checks IP
ip = socket.gethostbyname(url)
if (ip in BLACK_LIST):
   flash('Url is blacklisted')
   return redirect(url_for('index'))
...
```


## Input sanitization

The input URLs can be filtered and check if it points to any internal service before they are are passed to the pdf downloader.
This can be both in the sense of the URL schemas or even the urls themselves.

Input sanitization may contain loopholes it if makes use of replacements. IE: replace all `../` with `/`, `....//` -> `../`, the attacker is still able to do `../`.

```python
from urllib.parse import quote

# Within the function that checks IP
url = request.form.get('url', '')
sanitized_url = quote(url, safe='/:?&')

# Work with sanitized_url
...
```


## Enable authentication on all servers.

When the vulnerable server makes a request to the hidden local server, the vulnerable server will need to authenticate. Without the authentication details, the malicious user is unable to access any information.

This is to be implemented on all other servers including the vulnerable server.

