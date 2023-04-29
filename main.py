#!/usr/bin/env python3
import sys
import openai
import flask
import ssl

context = ssl.SSLContext()
context.load_cert_chain(
    "/etc/letsencrypt/live/generated.website/fullchain.pem",
    "/etc/letsencrypt/live/generated.website/privkey.pem"
    )

TOKEN = sys.argv[1]
MODEL = "gpt-3.5-turbo"
PROMPT = open("prompt.txt", "r").read()

app = flask.Flask(__name__)

@app.route("/")
def index() -> str:
    return """<img src="https://www.unilad.co.uk/wp-content/uploads/2018/11/Big-neck-man-2.jpg">"""

@app.route("/<path:url>")
def create_page(url) -> str:
    print(url)
    html = generate_page(url)
    return html

def generate_page(url:str) -> str:
    response = openai.ChatCompletion.create(
        api_key=TOKEN,
        model=MODEL,
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": url}
        ],
        max_tokens=1000,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    html = response.choices[0].message.content
    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context=context, debug=False, port=443)