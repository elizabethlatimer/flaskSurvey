from flask import Flask, request, render_template, redirect, flash, session
from surveys import surveys

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "ohno"

debug = DebugToolbarExtension(app)


@app.route("/")
def show_survey_list():
    return render_template("index.html", surveys=surveys.keys())


@app.route("/start-survey", methods=["POST"])
def show_start():
    session["survey_name"] = request.form["survey_name"]
    survey = surveys[session["survey_name"]]
    title = survey.title
    instructions = survey.instructions

    return render_template("start-survey.html", survey_name=title, 
                           instructions=instructions)


@app.route("/set_session", methods=["POST"])
def set_session():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<number>")
def show_question(number):
    if int(number) == len(session["responses"]):
        survey = surveys[session["survey_name"]]
        question_number = int(number)
        question_instance = survey.questions[question_number] if len(survey.questions) > question_number else None

        if question_instance:
            question = survey.questions[question_number].question
            choices = survey.questions[question_number].choices
            allow_text = survey.questions[question_number].allow_text
            next_number = question_number + 1

            return render_template("questions.html", question=question, choices=choices, next_number=next_number, allow_text=allow_text)
        else:
            return redirect("/thank-you")
    else:
        flash("You must visit questions in order you dummy!")
        return redirect(f"/questions/{len(session['responses'])}") 


@app.route("/answers", methods=["POST"])
def save_answer():
    comments = f" Comments: {request.form['comments']}" if request.form.get("comments") else "" #####
    answer = request.form["answer"] + comments
    next_number = request.form["next_number"]

    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    return redirect(f"/questions/{next_number}")


@app.route("/thank-you")
def show_thank_you():
    print(session["responses"])
    survey = surveys[session["survey_name"]]
    question_list = []

    for question in survey.questions:
        question_list.append(question.question)
    length = len(question_list)
    print(question_list)
    
    return render_template("thank-you.html", responses=session["responses"], questions=question_list, length=length)
