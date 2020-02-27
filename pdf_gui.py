##
# @author Francesco Antoniazzi <francesco.antoniazzi1991@gmail.com>
 # @file Description
 # @desc Created on 2020-02-24 4:33:57 pm
 # @copyright APPI SASU
 #
 
from flask import Flask, render_template, request, redirect
from urllib.parse import urlparse, unquote
from os.path import join, expanduser, exists, dirname, realpath
import os
import pdf

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = set(["pdf"])
file_tuple_list = []

@app.route('/')
def launch_pdf():
    return render_template("pdf_gui_easy.html", file_list=file_tuple_list)

@app.route("/execute")
def execute():
    if len(file_tuple_list) == 1:
        return redirect("/extract")
    else:
        return redirect("/merge")

@app.route("/extract", methods=["POST", "GET"])
def extract():
    pathList = [dirname(realpath(__file__))+"\\uploads\\{}{}".format(filename,pagerange) for (filename,pagerange) in file_tuple_list]
    app.logger.debug(pathList)
    output_path = join(expanduser("~"), "Desktop", "output.pdf")
    pdf.main({"extract": pathList[0], "destination": output_path, "merge": None})
    remove_everything_from_uploads()
    return """<a href="file:///{}">Output result</a>""".format(output_path)

@app.route("/merge", methods=["POST", "GET"])
def merge():
    pathList = [dirname(realpath(__file__))+"\\uploads\\{}{}".format(filename,pagerange) for (filename,pagerange) in file_tuple_list]
    app.logger.debug(pathList)
    output_path = join(expanduser("~"), "Desktop", "output.pdf")
    pdf.main({"merge": pathList, "destination": output_path, "extract": None})
    remove_everything_from_uploads()
    return """<a href="file:///{}">Output result</a>""".format(output_path)

@app.route("/file_upload", methods=["POST"])
def file_upload():
    global file_tuple_list
    for k,v in request.files.items():
        ftl_len = len(file_tuple_list)
        file_range = request.form.get("pagerange")
        file_name = "filename_{}.pdf".format(ftl_len)
        full_path = join(app.config["UPLOAD_FOLDER"], file_name)
        v.save(full_path)
        file_tuple_list.append((file_name,file_range))
        app.logger.debug("{}: {}".format(file_tuple_list[ftl_len][0],file_tuple_list[ftl_len][1]))
    return redirect("/")

@app.route("/remove/<file_obj>", methods=["POST"])
def remove(file_obj="*"):
    global file_tuple_list
    app.logger.debug("File object = {}".format(file_obj))
    if file_obj == "*":
        remove_everything_from_uploads()
    else:
        real_path = dirname(realpath(__file__))+"\\uploads\\{}".format(file_obj)
        if exists(real_path):
            app.logger.debug("Real path: {}".format(real_path))
            os.remove(real_path)
            file_found = [item for item in file_tuple_list if item[0] == file_obj][0]
            app.logger.debug("File found: {}".format(file_found))
            file_tuple_list.remove(file_found)
            app.logger.debug("File tuple list: {}".format(file_tuple_list))
    return redirect("/")

def remove_everything_from_uploads():
    d = dirname(realpath(__file__))+"\\uploads\\"
    filesToRemove = [join(d,f) for f in os.listdir(d)]
    for f in filesToRemove:
        os.remove(f)

if __name__ == "__main__":
    app.run()