# Imports
import re
from flask import Flask, request, render_template, flash
from werkzeug.utils import redirect
app = Flask(__name__)
app.secret_key = "my_secret_key"
from surveys import surveys

# Global variables
responses = []
SURVEY_TITLE = surveys["satisfaction"].title
SURVEY_INSTRUCTIONS = surveys["satisfaction"].instructions
SURVEY_QUESTIONS = surveys["satisfaction"].questions

@app.route("/")
def home_route():
    """Survey start page"""
    return render_template("home.html", survey_title=SURVEY_TITLE, survey_instructions=SURVEY_INSTRUCTIONS)

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save answer and redirect"""

    if (len(responses) == len(SURVEY_QUESTIONS)):
        # They've answered all the questions! Thank them.
        return redirect("/thank-you")

    else:
        # get the response answer
        answer = request.form['answer']
        responses.append(answer)
        return redirect(f"/question/{len(responses) + 1}")

@app.route("/question/<num>")
def question_route(num):
    """Page for survey questions"""

    if int(num) - 1 != len(responses):
        flash("You must answer the questions in order", "error")
        return redirect(f"/question/{len(responses) + 1}")
    elif (len(responses) == len(SURVEY_QUESTIONS)):
        # They've answered all the questions! Thank them.
        return redirect("/thank-you")

    else:
        return render_template(
        # Template
        "question.html",
        # Current Question
        current_question=SURVEY_QUESTIONS[int(num) - 1].question,
        # Question number
        number=int(num),
        # Current choices for answering the question
        current_choices=SURVEY_QUESTIONS[int(num) - 1].choices
        )

@app.route("/thank-you")
def thank_you_route():
    """Thank you page after survey has been completed"""
    print(responses)
    return render_template("thank-you.html")

