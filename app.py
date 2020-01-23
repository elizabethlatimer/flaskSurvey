from flask import Flask, request, render_template, redirect
from surveys import satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "ohno"

debug = DebugToolbarExtension(app)

responses = []


@app.route("/")
def show_home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("index.html", survey_name=title, instructions=instructions)


@app.route("/questions/<number>")
def show_question(number):
    if int(number) == len(responses):
        question_number = int(number)
        question_instance = satisfaction_survey.questions[question_number] if len(satisfaction_survey.questions) > question_number else None
        if question_instance:
            question = satisfaction_survey.questions[question_number].question
            choices = satisfaction_survey.questions[question_number].choices
            next_number = question_number + 1

            return render_template("questions.html", question=question, choices=choices, next_number=next_number)
        else:
            return redirect("/thank-you")
    else:
        return redirect(f"/questions/{len(responses)}") 


@app.route("/answers", methods=["POST"])
def save_answer():
    answer = request.form["answer"]
    next_number = request.form["next_number"]

    responses.append(answer)

    return redirect(f"/questions/{next_number}")


@app.route("/thank-you")
def show_thank_you():
    return render_template("thank-you.html")
