from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'alien baby'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
responses_list = 'responses'

app.route('/')
def survey_home():
    '''Landing page for the survey'''
    return render_template('start.html', survey=survey)

app.route('/start', methods=['POST'])
def start_survey():
    '''clear any responses in the list and redirect to the questions'''
    session[responses_list] = []

    return redirect('/questions/0')

app.route('/questions/<int:qid>')
def questions(qid):
    '''Form of questions'''
    responses = session.get(responses_list)

    #question page was accessed too early,redirect back to the start
    if (responses is None):
        return redirect('/')
    
    #all questions answered, redirect to the finished page
    if (len(responses) == len(survey.questions)):
        return redirect('/finished')
    
    #questions come out of order, send them back to the right question
    if (len(responses) != qid):
        flash(f'Invalid question ID detected: {qid}')
        return redirect(f'/questions/{len(responses)}')


    question = survey.questions[qid]
    return render_template('questions.html',question=question,question_num=qid) 

@app.route('/answer', methods=['POST'])
def answer():
    '''Save response and display next question'''
    #grab choice from form
    ans = request.form['answer']

    #add this response to the list in this session
    responses = session[responses_list]
    responses.append(ans)
    session[responses_list] = responses

    if (len(responses) == len(survey.questions)):
        #all questions answered, redirect to the finished page
        return redirect('/finished')
    else:
        return redirect(f"/questions/{len(responses)}")
    
@app.route('/finished')
def finsihed():
    '''Survey complete and show completion page'''
    return render_template('finsihed.html')