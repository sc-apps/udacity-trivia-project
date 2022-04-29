
################################################
Getting Started
################################################

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http:127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

###############################################
Error Handling
################################################

Errors are returned as JSON objects in the following format:

{
  "success": False,
  "error": 404,
  "message": "resource not found"
}

The API will return five error types when requests fail:
400: Bad Request
404: Resource Not Found
405: Method Not Allowed
422: Unprocessable
500: Internal Server Error

################################################
Endpoints
################################################


GET '/categories’

General:
	Returns a dictionary of categories, in which the key is the id of the category and the value is the corresponding string of the category, and success value
	Request Arguments: None
Sample: curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}


GET ‘/questions’

General:
	Returns a list of question objects, success value, total number of questions, categories, and current category
	Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1/questions
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },  
  "success": true, 
  "total_questions": 3 
} 


POST ‘/questions’
General:
	Creates a new question and returns it’s id, and success value
	Request Arguments: question, answer, category (int: id), difficulty (int: id)
Sample: curl http://127.0.0.1/questions -X POST -H “Content-Type: application/json” -d ‘{“question”:”What is the capital of Switzerland?”,”answer”:”Bern”,”category”:3,”difficulty”:1}'
{  
  "success": true, 
  “created": 4
} 


DELETE ‘/questions<int:question_id>’
General:
	Deletes an existing question and returns success value
	Request Arguments: question’s id to be provided that is intended to be deleted
Sample: curl http://127.0.0.1/questions/4
{  
  "success": true, 
} 

POST ‘/questions/search’
General:
	Returns a list of question objects that have a search term in the question attribute, total number of questions, curretn category, and success value
	Request Arguments: a search term 
Sample:curl http://127.0.0.1/questions/search -X POST -H “Content-Type: application/json” -d ‘{“searchTerm”:”bird”}'
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
          }, 
  "success": true, 
  "total_questions": 1 
} 


GET ‘/categories<int:category_id>/questions’
General:
	Returns a list of question objects that are within the provided category, total number of questions, current category, and success value
	Request Arguments: category’s id 
Sample: curl http://127.0.0.1/categories/4/questions
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 2
}


POST ‘/quizzes’
General:
	Returns a random question from a given category, and success value
	Request Arguments: category object
Sample curl http://127.0.0.1/quizzes -X POST -H “Content-Type: application/json” -d ‘{"quiz_category":{"id”:4,"type”:"history"}}'
{ 
  "question": {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  }, 
  "success": true
}
