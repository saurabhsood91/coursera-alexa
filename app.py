from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from coursera import Coursera

import json

app = Flask(__name__)
ask = Ask(app, "/")

def _get_course_names(course):
    return course['name']

@ask.launch
def new_ask():
    welcome = render_template('welcome')
    empty = render_template('empty')

    return question(welcome).reprompt(empty)


@ask.intent('SearchCourseIntent')
def search_course(query):
    if not query:
        empty_query = render_template('empty')
        return question(empty_query)

    courses = Coursera.search_courses(query)

    number_of_results = len(courses['elements'])

    results = render_template('results', number_of_results=number_of_results)

    courses = map(_get_course_names, courses['elements'])

    session.attributes['results'] = courses
    session.attributes['index'] = 0

    return question(results)

@ask.intent('AMAZON.YesIntent')
def show_result():
    current_index = session.attributes['index']
    course_name = session.attributes['results'][current_index]
    session.attributes['index'] += 1

    result = render_template('course_name', course_name=course_name)
    return question(result)

@ask.intent('AMAZON.NoIntent')
def close():
    result = render_template('exit')
    return statement(result)

@ask.intent('AMAZON.HelpIntent')
def help():
    result = render_template('help')
    return question(result)

if __name__ == '__main__':
    app.run(debug=True)
