from flask import Flask

app = Flask(__name__)
name = "Joni Vilokki"


@app.route("/")
def hello():
    return name


if __name__ == "__main__":
    app.run()