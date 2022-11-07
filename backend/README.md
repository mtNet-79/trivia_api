# Backend - Trivia API

## Setting up the Backend


### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


# FrontEnd - Trivia API

## Setting up the frontend
### Install Node and NPM in the frontend directory
 - Visit the [NodeJS](https://nodejs.org/en/download/) docs to download Node and NPM to use the frontend
### Install project dependencies
From the /frontend folder run following bash commands:
```
npm install

npm start

```

### API / route endpoints Documentation 

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a two keys, `categories`, that contains an object of `id: category_string` key: value pairs. and `success` key and corresponding bool value 

```
json
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
```

`GET '/questions'`

- Fetches a dictionary containing four items: all questions as an array of question objects, all categories as a dictionary of key:value pairs where keys are ids and values are name string, current_cateogry key with a name string value, and total number of questions key with integer value
- Request Arguments: None
- Returns: An object with a five keys:value pairs, 1. `categories`:{"id":"Name"} , 2. `current_category`:"name", 3.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 4.`success`:bool, 5.`total_questions`:int - with pagination of 10 per page

``` 
json
{  
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "all",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    },
    {
      "answer": "Apollo 13",
      "category_id": 5,
      "difficulty": 4,
      "id": 3,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    
  ],
  "success": true,
  "total_questions': 4
}
```
`GET '/categories/<int:cat_id>/questions'`
- Fetches a dictionary containing 3 items: questions for a particular category by id as array of question objects, current category name string, and total number of quesitons as integer value
- Request Arguments: none (url id parameter given in route)
- Returns: An object with four key:value pairs - 1. `current_category`:"name", 2.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 3.`success`:bool, 4.`total_questions`:int


```
json
{
  "current_category": "History",
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    },
    {
      "answer": "George Washington Carver",
      "category_id": 4,
      "difficulty": 3,
      "id": 8,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Muhammad Ali",
      "category_id": 4,
      "difficulty": 1,
      "id": 30,
      "question": "What boxer's original name is Cassius Clay?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

`POST '/questions'`
- Fetches a dictionary containing 2 items: questions that match a search term as an array of question objects, and total number of questions returned as integer value
- Request Arguments: "searchTerm" : string
e.g.
```curl -d {"searchTerm": "Whose"} -X POST http://localhost2:5000/questions```
- Returns: An object with three key:value pairs - 1.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 2.`success`:bool, 3.`total_questions`:int


```
json
{
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    }
  ],
  "success": true,
  "totalQuestions": 1
}
```



`POST '/questions/<int:qid>'`
- DELETES a question from the questions database using an id passed via url parameter 
- Request Arguments: None
e.g.
``` curl -X DELETE http://localhost:5000/questions/3 ```
- Returns: The data from questions database after deletion as an object with four key:value pairs - 1. `deleted`: int (id of deleted record), 2.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 3.`success`:bool, 4.`total_questions`:int


```
json
{
  "deleted": 3,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    
  ],
  "success": true,
  "total_questions": 3
}
```

`POST '/add'`
- POSTs a new question to the questions database - allows user to post new questions
- Request Arguments: a json object containing a new question string, a new answer string,a category id as integer, and a difficulty rating as integer
e.g. 
```curl -d '{"question": "Who done it?", "answer": "Mr. Nobody", "category": 4, "difficulty": 3}' -H "Content-Type: application/json" -X POST http://localhost:5000/add```
- Returns: The data from questions database after creation of new question as an object with four key:value pairs - 1. `created`: int (id of created record), 2.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 3.`success`:bool, 4.`total_questions`:int - with pagination of 10 per page


```
json
{
   "created": 31,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    ...
   
  ],
  "success": true,
  "total_questions": 13
}
```
`POST '/quizzes'`
- fecthes a new random question based on other previously asked questions and choosen category - allows user to play trivia game
- Request Arguments: a json object containing a "previous_questions" key with corresponding list value containing question ids of quesitons already asked, and a "quiz_category" dictionary with a key 'type' with corresponding category  name string and key "id" with category id integer 
e.g. 
```curl -d '{"previous_questions": [4,3], "quiz_category": {"type":"All", "id":0}}' -H "Content-Type: application/json" -X POST http://localhost:5000/quizzes```

- Returns: The data from questions database after creation of new question as an object with four key:value pairs - 1. `created`: int (id of created record), 2.`questions`:[{"answer": string, "category_id": int, "difficulty": int, "question":string},{},...], 3.`success`:bool, 4.`total_questions`:int - with pagination of 10 per page


```
json
{
   "created": 31,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category_id": 4,
      "difficulty": 2,
      "id": 2,
      "question": "Whose autobiography is entitled 'I KnowWhy the Caged Bird Sings'?"
    },
    {
      "answer": "Tom Cruise",
      "category_id": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category_id": 5,
      "difficulty": 3,
      "id": 5,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    ...
   
  ],
  "success": true,
  "total_questions": 13
}
```


## Testing


To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
