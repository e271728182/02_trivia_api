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

  cors=CORS(app, resources={"r/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
      response.headers.add("Access-Control-Allow-Headers",
      "Content-Type,Authorization,true")
      response.headers.add("Access-Control-Allow-Methods",
      "GET,PATCH,POST,DELETE,OPTIONS")
      return response

  @app.route('/categories',methods=['GET'])
  def get_categories():
      categories=Category.query.order_by(Category.type).all()
      if len(categories)==0:
          abort(404)
      return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })


  @app.route('/questions',methods=['GET'])
  def get_questions():
      questions=Question.query.all()
      if len(questions)==0:
          abort(404)
      paginatedQuestions = paginate_request(request, questions,QUESTIONS_PER_PAGE)
      #query categories
      categories = Category.query.order_by(Category.type).all()
      return (jsonify({'success':True,
      'questions':paginatedQuestions,
      'totalQuestions':len(questions),
      'categories': {category.id: category.type for category in categories},
      'current_category': None}),200)


  @app.route('/questions',methods=['POST'])
  def post_question():
      """
      get request input for a new question. Will be rejected if any of the input
      is null or None
      """
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

  @app.route('/questions/<int:question_id>',methods=['DELETE'])
  def delete_question(question_id):
      """
      deletes a question with a given question_id as input
      """
      try:
          questionToDelete=Question.query.get(int(question_id))
          questionToDelete.delete()
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
      search_term=input.get('search_term')

      search_results = (Question.query.filter(Question.question.ilike("%{}%"
      .format(search_term))).all())
      if len(search_results)==0:
          abort(404)

      return(jsonify({'success':True,
      'questions':[question.format() for question in search_results],
      'total_questions':3
      }),200)

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

  @app.route('/quizzes',methods=['POST'])
  def get_quiz_questions():
      """
      get questions based on previous category
      """
      data = request.get_json()
      previousQuestions = data.get("previous_questions")
      quizCategory = data.get("quiz_category")
      quizCategoryId = int(quizCategory["id"])
      #filter questions over the selected category and eliminate
      #questions already played in previous rounds which are stored if __name__ == '__main__':
      # previous_questions list
      questions=(Question.query.filter_by(category=quizCategoryId)
      .filter(Question.id.notin_(previousQuestions)).all())

      #select as random question among the filtered ones
      question=random.choice(questions).format()

      return(jsonify({'success':True,
      'question':question}),200)
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


  return app
