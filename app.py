import re
from flask import Flask, render_template, request, redirect, flash
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
    quest_id = len(responses)

    if len(satisfaction_survey.questions) == len(responses):
        return redirect('/thank_you')
    else:
        return render_template('home.html', title = title, instruction = instruction,  quest_id = quest_id)

@app.route('/questions/<question_id>')
def question_page(question_id):
    question_list = satisfaction_survey.questions
    quest_id = len(responses)
    if len(responses) == len(question_list):
        return redirect('/thank_you')
    if quest_id != int(question_id):
        flash("You are trying to access an invalid question.", 'error')
    curr_question = question_list[quest_id].question
    answer_choices = question_list[quest_id].choices
    return render_template('question.html', curr_question = curr_question, quest_id = quest_id, answer_choices = answer_choices)


@app.route('/answer', methods=["POST"])
def answer_route():
    if len(responses) == len(list(satisfaction_survey.questions)):
        return redirect('/thank_you')
    if(bool(list(request.form))):
        list_split_key = list(request.form.keys())[0].split('-')
        quest_id = int(list_split_key[1])
    elif not bool(list(request.form)) or len(responses) != quest_id:
        flash("Please select an answer.", 'error')
        return redirect(f'/questions/{len(responses)}')

    list_split_key = list(request.form.keys())[0].split('-')
    responses.append(list_split_key[0])
    quest_id = len(responses)
    return redirect(f'/questions/{quest_id}')


@app.route('/thank_you')
def thank_you_page():
    return render_template('thank_you.html')