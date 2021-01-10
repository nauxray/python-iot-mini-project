from flask import Flask
app=Flask(__name__)

@app.route('/')
def index():
    return "Hello World"

@app.route('/page2')
def page2():
    return "second page"

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0') 