from flask import Flask
from flask import redirect, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
