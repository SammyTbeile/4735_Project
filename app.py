import os
from flask import Flask, request, render_template, send_file, Response, url_for, redirect
from werkzeug import secure_filename

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
# print(tmpl_dir)
static_dir=tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__,  static_folder=static_dir)


@app.route("/")
def index():
    print("in index")
    return render_template("index.html")

@app.route("/uploader", methods = ["GET", "POST"])
def upload_file():
    if (request.method == "POST"):
        f = request.files["file"]
        f.save(secure_filename(f.filename))
        return redirect(url_for(".uploaded", filename=secure_filename(f.filename)))

@app.route("/uploaded", methods=["GET"])
def uploaded():
    print(request.args["filename"])
    return render_template("uploaded.html",filename=request.args["filename"])

@app.route("/process", methods=["GET"])
def process():
    os.system("python3 ../ocr.py -i " + request.args["filename"] + " -t 1 -l 2")
    os.system("python3 ../TextCompute.py")
    os.system("rm page*")
    os.system("rm book/page*")
    os.system("rm *.mp3")
    os.system("rm *.txt")
    return send_file("/home/sammy/ColumbiaSenior/Visual Interfaces/project/4735_Project/flaskapp/FinalMovieFile.mp4", attachment_filename="FinalMovieFile.mp4", as_attachment=True)


app.run(host="127.0.0.1", port=5000, debug=True)
