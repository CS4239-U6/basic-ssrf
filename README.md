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