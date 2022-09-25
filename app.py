from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.debug = True # why does this not work???
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)


RESPONSES_KEY = "user_answers"


@app.route('/')
def home_page():
  """ This is the survey home page """
  return render_template('home.html', survey=survey)


@app.route('/start_survey', methods = ['POST'])
def start_survey():
  """ Starts the survey and returns the first question. This will also clear session responses"""
  
  # setting the value of the Key to an empty list
  session[RESPONSES_KEY] = []

  return redirect("/questions/0")


@app.route('/questions/<int:question_num>')
def show_question(question_num):
  """ Show current question """

  responses = session.get(RESPONSES_KEY)

  if responses is None:
    return redirect("/")

  if len(responses) == len(survey.questions):
    """ If length of responses is as long as the number of survey questions
        then the user has completed the survey.
    """
    return render_template('survey_complete.html')  

  elif len(responses) != question_num:
    flash(f"Invalid question id: {question_num}.")
    return redirect(f"/questions/{len(responses)}")

  else:
    cur_question = survey.questions[question_num]
    return render_template('questions.html',cur_question=cur_question, question_num = question_num+1)


@app.route('/answer', methods=['POST'])
def answer():

  # get answer from survey question
  choice = request.form['answer']

  #session is like a dictionary, get value from RESPONSES_KEY and store it in responses
  responses = session[RESPONSES_KEY] # responses is a list
  # add choice to responses list
  responses.append(choice)
  # update the values for the specified Key, here we are basically updating the old list with a newer list
  session[RESPONSES_KEY] = responses

  if len(responses) == len(survey.questions):
    return render_template('survey_complete.html')
  
  else:
    return redirect(f"/questions/{len(responses)}")
    
 