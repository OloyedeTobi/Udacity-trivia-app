from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random


from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, requested_data):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        formatted_questions = [data.format() for data in requested_data]
        current_questions = formatted_questions[start:end]
        return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response


   
#GET CATEGORIES
    @app.route('/categories',  methods=['GET'])
    def get_categories():
        selection = Category.query.all()
        selection = [category.format() for category in selection]
        selection = [data['type'] for data in selection]
        return jsonify({'success': True,
                        'categories': selection})


   #GET QUESTIONS 
    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.all()
        questions_paginate = paginate_questions(request, questions)
        if len(questions_paginate) == 0:
            abort(404)
        categories = [category.format() for category in Category.query.all()]
        categories_list = [data['type'] for data in categories]
        current_category = categories_list
        return jsonify({'questions': questions_paginate,
                        'total_questions': len(questions),
                        'current_category': current_category,
                        'categories': categories_list})


#DELETE QUESTIONS
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter_by(id=question_id).one_or_none()
        if question is None:
            abort(404)
        try:
            question.delete()
            return jsonify({'success': True,
                            'question_id':question.id}, 
                           200)
        except:
            abort(422)

   

#POST OR SEARCH QUESTIONS
    @app.route('/questions', methods=['POST'])
    def post_search_question():
        body = request.get_json()
        if not body:
            abort(400)
        search_term = request.get_json().get('searchTerm', "")
        if search_term:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            if questions:
                formatted_questions = [question.format() for question in questions]
                return jsonify({'question': formatted_questions,
                                'total_question': len(formatted_questions),
                                'current_category': questions[0].category,
                                'success': True})
            else:
                abort(404)

        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')
        if not question or not answer or not difficulty or not category:
            abort(400)
        try:
            new_question = Question(question=question,
                                    answer=answer,
                                    category=category,
                                    difficulty=difficulty)
            new_question.insert()
            return jsonify({'success': True, 'question_id': new_question.id}, 201)
        except:
            abort(422)




#GET QUESTIONS BY CATEGORY
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        cat_id = category_id + 1
        category = Category.query.filter(Category.id == cat_id).first()

        selection = Question.query.order_by(Question.id).filter(Question.category == cat_id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': [cat.type for cat in Category.query.all()],
            'current_category': category.format()
        })

   

    

    #POST QUIZZES
    @app.route('/quizzes', methods=['POST'])
    def post_quizzes():
        body = request.get_json()
        if not body:
            abort(404)
        prev_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)
        if not prev_questions:
            if quiz_category:
                question_list = Question.query.filter(Question.category == (quiz_category['id'])).all()
            else:
                question_list = Question.query.all()
        else:
            if quiz_category:
                question_list = Question.query.filter(Question.category == str(quiz_category['id'])). \
                    filter(Question.id.notin_(prev_questions)).all()
            else:
                question_list = Question.query.filter(Question.id.notin_(prev_questions)).all()
        formatted_questions = [question.format() for question in question_list]
        total = len(formatted_questions)
        if total == 1:
            randomQues = formatted_questions[0]
        else:
            randomQues= formatted_questions[random.randint(0, len(formatted_questions))]

        return jsonify({
            'success': True,
            'question': randomQues
        })

    #ERROR HANDLERS
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Requested resource can not be found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed for requested url"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": 'Request can not be processed'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    return app


   