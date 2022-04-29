import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  # DONE: Use the after_request decorator to set Access-Control-Allow
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

 
  # DONE: Create an endpoint to handle GET requests for all available categories.
  @app.route('/categories')
  def get_categories():
    try:
      categories = Category.query.all()
      if len(categories)==0:
        abort(404)

      else:
        return jsonify({
          'success': True,
          'categories': {category.id: category.type for category in categories}
      })
    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + 10
      questions = Question.query.all()
      formatted_questions = [question.format() for question in questions]
      current_category = request.args.get('currentCategory', None)
      categories = Category.query.all()
      return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': {category.id: category.type for category in categories},
            'current_category': current_category
        })
    except:
      abort(422)
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter_by(id=question_id).first_or_404()
    question.delete()

    return jsonify({
          'success': True
      })


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    try:
      body = request.get_json()
    
      new_question = Question(
                question = body.get('question', None),
                answer = body.get('answer', None),
                category = body.get('category', None),
                difficulty = body.get('difficulty', None)
              )
      new_question.insert()
      
      return jsonify({
            'success': True,
            'created': new_question.id
      })
    except:
      abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  @app.route('/questions/search', methods=['POST'])
  def search_question():
    try:
      body = request.get_json()
      search = body.get('searchTerm', None)
      questions = Question.query.filter(Question.question.ilike("%" + search + "%")).all()
      formatted_questions = [question.format() for question in questions]
      current_category = request.args.get('currentCategory', None)
      
      return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(formatted_questions),
            'current_category': current_category
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_by_category(category_id):
    questions = Question.query.filter(Question.category==category_id).all()
    formatted_questions = [question.format() for question in questions]
    current_category = request.args.get('currentCategory', None)
    if len(formatted_questions)==0:
      abort(404)
    return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': len(formatted_questions),
          'current_category': current_category
        })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes', methods=['POST'])
  def start_quiz():
    try:
      body = request.get_json()
      category = body.get('quiz_category')
      category_id = category.get('id') # taking category_id from the body payload
      previous_questions = body.get('previous_questions', None)

      if category_id: 
        if previous_questions == None: 
          questions = Question.query.filter_by(category=category_id).all()
        else:
          # source where I found how to use not_in() https://stackoverflow.com/questions/26182027/how-to-use-not-in-clause-in-sqlalchemy-orm-query
          questions = Question.query.filter_by(category=category_id).filter(Question.id.not_in(previous_questions)).all()
      elif category_id == 0:  
        if previous_questions == None:
          questions = Question.query.all()
        else:
          questions = Question.query.filter(Question.id.not_in(previous_questions)).all()

      question = random.choice(questions)

      return jsonify({
        'success': True,
        'question': question.format()
            
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
          'success': False,
          'error': 400,
          'message': 'bad client request'
      }), 400


  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
          'success': False,
          'error': 404,
          'message': 'resource not found'
      }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
          'success': False,
          'error': 405,
          'message': 'method not allowed'
      }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
          'success': False,
          'error': 422,
          'message': 'unprocessable'
      }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
          'success': False,
          'error': 500,
          'message': 'internal server error'
      }), 500

  return app

  