import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_request(request, selection,QUESTIONS_PER_PAGE):
    """

    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    allItems = [selectedItem.format() for selectedItem in selection]
    selected_items = allItems[start:end]
    return selected_items


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @XTODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  cors=CORS(app, resources={"r/*": {"origins": "*"}})
  '''

  @XTODO: Use the after_request decorator to set Access-Control-Allow
  '''


  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
      response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
      return response


  '''
  @TODO:
  XCreate an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories',methods=['GET'])
  def get_categories():
      categories=Category.query.order_by(Category.type).all()
      if len(categories)==0:
          abort(404)
      return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })
  '''
  @TODO:
  XCreate an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  @app.route('/questions',methods=['GET'])
  def get_questions():
      questions=Question.query.all()
      if len(questions)==0:
          abort(404)
      paginatedQuestions = paginate_request(request, questions,QUESTIONS_PER_PAGE)

      return (jsonify({'success':True,
      'questions':paginatedQuestions,
      'totalQuestions':len(questions)}),200)


  @app.route('/questions',methods=['POST'])
  def post_question():

      input= request.get_json()
      question = input.get("question")
      answer = input.get("answer")
      category = input.get("category")
      difficulty = input.get("difficulty")

      if not(question and answer and category and difficulty):
          abort(400)
      try:
          question = Question(
          question=question,
          answer=answer,
          category=category,
          difficulty=difficulty
            )
          question.insert()
      except BaseException:
          abort(400)

      return (jsonify({"success": True, "question": question.format()}), 200)
  '''
  @TODO:
  XCreate an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question():
      try:
          questionToDelete:Question.query.get_or_404(question_id)
      except:
          abort(404)
      return(
          jsonify({'success':True,
          'message':'Question deleted'}),200)


  @app.route('/questions/search',methods=['POST'])
  def search_question():
      """
      search question based on partial string match.
      """
      input=request.get_json()
      search_term=input.get('search_term',None)
      if search_term:
          search_results = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
      else:
          abort(404)
      return(jsonify({'success':True}))

  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def questions_per_categories(category_id):
      """
      returns all questions paginated for a given category
      """
      catQuestions = Question.query.filter_by(category=category_id).all()
      if len(catQuestions)==0:
          abort(404)

      paginatedCatQuestions=paginate_request(request,catQuestions,QUESTIONS_PER_PAGE)
      return(jsonify({'success':True,
          'questions':paginatedCatQuestions,
          'total_questions':len(catQuestions),
          'current_category':category_id}),200)

  @app.route('/quizzes')
  def test():
      pass

  @app.errorhandler(404)
  def not_found(error):
      return (jsonify({'success':False,
      'error':404,
      'message':'has not found any item from query'}),404)

  @app.errorhandler(400)
  def bad_request(error):
      return (jsonify({'success':False,
      'error':400,
      'message':'bad request'}),400)

  @app.errorhandler(405)
  def method_illegal(error):
      return (jsonify({'success':False,
      'error':400,
      'message':'this method is not allowed'}),405)

  @app.errorhandler(500)
  def server_error(error):
      return (jsonify({'success':False,
      'error':500,
      'message':'there was an error on the server side'}),500)

  '''
 @TODO:
 XCreate a GET endpoint to get questions based on category.

 TEST: In the "List" tab / main screen, clicking on one of the
 categories in the left column will cause only questions of that
 category to be shown.
    @TODO:
    XCreate an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.

    @TODO:
    XCreate a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.

  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''

  return app
