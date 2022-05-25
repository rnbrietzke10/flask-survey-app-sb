from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension

from surveys import *
app = Flask(__name__)

app.config['SECRET_KEY'] = 'astros_are_awesome'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions
    return render_template('home.html', title = title, instruction = instruction )

@app.route('/questions/<question_id>')
def question_page(question_id):
    quest_id = int(question_id)
    curr_question = list(satisfaction_survey.questions)[quest_id].question
    answer_choices = list(satisfaction_survey.questions)[quest_id].choices

    return render_template('question.html', curr_question = curr_question, quest_id = quest_id, answer_choices = answer_choices)

@app.route('/answer', methods=["POST"])
def answer_route():
    list_split_key = list(request.form.keys())[0].split('-')
    responses.append(list_split_key[0])
    quest_id = int(list_split_key[1]) + 1
    if quest_id == 5:
        return redirect('/thank_you')
    return redirect(f'/questions/{int(quest_id)}')


@app.route('/thank_you')
def thank_you_page():
    return render_template('thank_you.html')