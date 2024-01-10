from flask import Flask,render_template, request
app = Flask(__name__)

@app.route("/")
def firstPage():
    return render_template("firstPage.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
