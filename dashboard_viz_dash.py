from flask import Flask

app = Flask(__name__)


@app.route('/')
def viz_func():
    return "Visualization here"


if __name__ == '__main__':
    print()
