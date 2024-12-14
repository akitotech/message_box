from flask import Flask, render_template

app = Flask(__name__)


@app.route('/route_name')
def method_name():
    pass
