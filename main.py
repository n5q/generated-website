#!/usr/bin/env python3
import sys
import openai
import flask

TOKEN = sys.argv[1]
MODEL = "gpt-3.5-turbo"
PROMPT = open("prompt.txt", "r").read()

app = flask.Flask(__name__)

@app.route("/")
def index() -> None:
    return "<h1>e</h1>"

@app.route("/<url>")
def create_page(url) -> str:
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
    app.run(host="0.0.0.0", port=8080)