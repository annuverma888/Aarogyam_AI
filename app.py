from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os
from chatbot import get_bot_response
from report_ocr import extract_text as report_extract_text
from ocr import extract_text as medicine_extract_text
from report_ai import analyze_report
from werkzeug.utils import secure_filename
from flask import render_template, request

from medicine_ai import analyze_medicine


from utils import *

app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load model
model = joblib.load("model/disease_model.pkl")
encoder = joblib.load("model/label_encoder.pkl")
bmi_model = joblib.load("model/bmi_model.pkl")

gender_encoder = joblib.load("model/gender_encoder.pkl")

bmi_encoder = joblib.load("model/bmi_label_encoder.pkl")

# Load symptom names
train = pd.read_csv("dataset/Training.csv")

if "Unnamed: 133" in train.columns:
    train.drop(columns=["Unnamed: 133"], inplace=True)

symptoms = train.drop("prognosis", axis=1).columns.tolist()

text = report_extract_text(filepath)
ocr_text = medicine_extract_text(filepath)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/disease")
def disease():
    return render_template("disease.html", symptoms=symptoms)

@app.route("/dashboard")
def dashboard():

    reports = len(os.listdir("reports")) if os.path.exists("reports") else 0

    return render_template(
        "dashboard.html",
        diseases=41,
        symptoms=132,
        medicines=len(medicine_df),
        reports=reports
    )
    
    
@app.route("/bmi", methods=["GET","POST"])
def bmi():

    if request.method == "POST":

        height = float(request.form["height"])

        weight = float(request.form["weight"])

        age = int(request.form["age"])

        gender = request.form["gender"]

        gender = gender_encoder.transform([gender])[0]

        prediction = bmi_model.predict([[
            height,
            weight,
            age,
            gender
        ]])

        category = bmi_encoder.inverse_transform(prediction)[0]

        return render_template(
            "bmi.html",
            category=category,
            height=height,
            weight=weight,
            age=age
        )

    return render_template("bmi.html")


@app.route("/report_analyzer", methods=["GET", "POST"])
def report_analyzer():

    if request.method == "POST":

        report = request.files["report"]

        if report.filename == "":
            return render_template(
                "report_analyzer.html",
                result="Please upload a report."
            )

        filename = secure_filename(report.filename)

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        report.save(filepath)

        # OCR
        extracted_text = extract_text(filepath)

        # AI Analysis
        ai_result = analyze_report(extracted_text)

        return render_template(
            "report_analyzer.html",
            result=ai_result
        )

    return render_template("report_analyzer.html")



@app.route("/chat", methods=["POST"])
def chat():

    message = request.form["message"]

    reply = get_bot_response(message)

    return {"reply": reply}

@app.route("/medicine")
def medicine():

    return render_template("medicine.html")

print(medicine_df.columns.tolist())

@app.route("/medicine_search", methods=["POST"])
def medicine_search():
    medicine_name = request.form.get("medicine")

    medicine = search_medicine(medicine_name)

    if medicine is None:
        return render_template("medicine.html", error="Medicine Not Found")

    return render_template("medicine.html", medicine=medicine)


@app.route("/predict", methods=["POST"])
def predict():

    selected_symptoms = request.form.getlist("symptoms")

    input_data = np.zeros(len(symptoms))

    for symptom in selected_symptoms:

        if symptom in symptoms:

            input_data[symptoms.index(symptom)] = 1

    prediction = model.predict([input_data])

    disease = encoder.inverse_transform(prediction)[0]

    return render_template(
        "result.html",
        disease=disease,
        description=get_description(disease),
        precautions=get_precautions(disease),
        medicines=get_medicines(disease),
        diet=get_diet(disease),
        workout=get_workout(disease)
    )
    
@app.route("/hospital")
def hospital():
    return render_template("hospital.html")


@app.route("/chatbot")
def chatbot():

    return render_template("chatbot.html")
@app.route("/emergency")
def emergency():
    return render_template("emergency.html")

@app.route("/pharmacy")
def pharmacy():
    return render_template("pharmacy.html")




@app.route("/medicine_scanner", methods=["GET", "POST"])
def medicine_scanner():

    if request.method == "POST":

        image = request.files["medicine_image"]

        filename = secure_filename(image.filename)

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        image.save(filepath)

        ocr_text = extract_text(filepath)

        report = analyze_medicine(ocr_text)

        return render_template(
            "medicine_scanner.html",
            result=report
        )

    return render_template("medicine_scanner.html")


@app.route("/download")
def download():

    disease=request.args.get("disease")

    description=get_description(disease)

    medicines=get_medicines(disease)

    precautions=get_precautions(disease)

    diet=get_diet(disease)

    workout=get_workout(disease)

    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename=f"reports/{disease}_Report.pdf"

    doc=SimpleDocTemplate(filename)

    styles=getSampleStyleSheet()

    story=[]

    story.append(Paragraph("<b>AI Disease Recommendation Report</b>",styles["Title"]))

    story.append(Spacer(1,20))

    story.append(Paragraph(f"<b>Date:</b> {datetime.now()}",styles["Normal"]))

    story.append(Spacer(1,15))

    story.append(Paragraph(f"<b>Disease:</b> {disease}",styles["Heading2"]))

    story.append(Spacer(1,10))

    story.append(Paragraph("<b>Description</b>",styles["Heading3"]))

    story.append(Paragraph(description,styles["Normal"]))

    story.append(Spacer(1,15))

    story.append(Paragraph("<b>Medicines</b>",styles["Heading3"]))

    for med in medicines:
        story.append(Paragraph("• "+med,styles["Normal"]))

    story.append(Spacer(1,15))

    story.append(Paragraph("<b>Precautions</b>",styles["Heading3"]))

    for p in precautions:
        story.append(Paragraph("• "+p,styles["Normal"]))

    story.append(Spacer(1,15))

    story.append(Paragraph("<b>Diet Plan</b>",styles["Heading3"]))

    for key,value in diet.items():

        story.append(Paragraph(f"<b>{key}</b> : {value}",styles["Normal"]))

    story.append(Spacer(1,15))

    story.append(Paragraph("<b>Workout Plan</b>",styles["Heading3"]))

    for key,value in workout.items():

        story.append(Paragraph(f"<b>{key}</b> : {value}",styles["Normal"]))

    story.append(Spacer(1,20))

    story.append(Paragraph(
        "<font color='red'><b>Disclaimer:</b> This report is generated by an AI-based Disease Recommendation System and should not replace professional medical advice.</font>",
        styles["Italic"]
    ))

    doc.build(story)

    return send_file(filename,as_attachment=True)
   


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
