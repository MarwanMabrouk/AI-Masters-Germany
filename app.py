from flask import Flask, render_template, request
import pandas as pd
import openpyxl

app = Flask(__name__)


def get_data():
    data = pd.read_excel("University Data LA Project(4).xlsx")
    course_name = data['Course Name'].tolist()
    degree_Name = data['Degree Name'].unique().tolist()
    uni_fachhochschule_tu = data['Uni/Fachhochschule/TU'].unique().tolist()
    # uni_name=data['Uni Name'].unique().tolist()
    ccn = len(course_name)
    cdn = len(degree_Name)
    cuft = len(uni_fachhochschule_tu)
    return course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft


@app.route("/")
def firstPage():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("firstPage.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)


@app.route("/search")
def second_page():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("second_page.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)


@app.route("/visualization")
def third_page():
    course_name, degree_Name, uni_fachhochschule_tu, ccn, cdn, cuft = get_data()
    return render_template("third_page.html", course_name=course_name, degree_Name=degree_Name,
                           uft=uni_fachhochschule_tu, ccn=ccn, cdn=cdn, cuft=cuft)

if __name__ == '__main__':
    app.debug = True
    app.run()