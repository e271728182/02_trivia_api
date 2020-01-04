# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.




## API ENDPOINTS

POST '/questions'
- Post a new question to the database
- Request Arguments--> question:string, answer:string, difficulty:int, category:string
- Returns: A JSON with the following structure
{'success':True,
'question': question.format()} where .format() transforms a SQLAlchemy object
into a python dictionary (equivalent to the __dict__ method)

POST '/questions/search'
- Search a question based on partial string match
- Request Arguments-->search_term:String
- Returns:A JSON with the following structure <br/>
{'success':true,  
'questions':search_results,  
total_question:len(search_results) 
} 
where search_results is the results of the query based on the partial string match input from the request

POST '/quizzes'
- For a given category, select a question that has not yet been asked for a quiz session
- Request Arguments--> arr:previous_questions str:category_id
- Returns:A JSON with the following structure <br/>
{
  'success':True,  
  'question':question 
}
where question is the first item of the query filtered over the id's of the previous questions AND the category_id

GET '/questions' 
- Get all questions in the database in a paginated format of 10 questions per page 
- Returns: A JSON with the following structure<br/>
{'success':true,    
'questions':questions,    
'total_questions':len(questions)  
} .  
Where questions is a list of questions objects in dictionary format


GET '/categories/<int:category_id>/questions'
- Get all questions for a given category in a paginated format of 10 questions per page 
- Request Arguments--> int:category_id 
- Returns: A JSON with the following structure<br/>
{'questions':paginatedCatQuestions,     
'total_questions': len(paginatedCatQuestions)   
'current_category':category_id} 

where paginatedCatQuestions is the paginated output of the SQLAlchemy Query where the Question table is filtered over the category_id

DELETE'/questions/<int:question_id>'   
- Delete a question with a given question_id   
- Request Arguments--> question_id:int   
- Returns: A JSON with the following structure <br/> 

{'success':True,    
'message': 'question deleted'  
}


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
