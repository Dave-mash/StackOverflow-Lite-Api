# StackOverflow-lite-APIs

# StackOverflow-lite application endpoints
## The following are API endpoints enabling one to:
* Create an account and log in 
* Get all questions.
* Get a question.
* Post a question.
* Post an answer to a question.
* Edit a question
* Delete a question
* Post an answer to a question
* View an answer
* Mark an answer as the preferred
### Prerequisites
* Python3
* Git
* Postman
### The following are API endpoints enabling one to:
* Create an account and log in 
* Get all questions.
* Get a question.
* Post a question.
* Delete a question.
* Post an answer to a question.
### StackOverflow-lite application endpoints
| Endpoint        | Functionality           | HTTP method  |
| ------------- |:-------------:| -----:|
| `/auth/signup`      | Register a user | POST |
| `/auth/login`      | Login a user       |   POST |
| `/questions` | Fetch all questions       |    GET |
| `/questions/<questionId>` | Fetch a specific  question        |    GET |
| `/questions/<questionId>` | Delete a question        |    DELETE |
| `/questions/<questionId>/answers` | Post an answer to a  question        |    POST |
| `/questions/<questionId>/answers/<answer Id>` | Post an answer to a  question        |    PUT |

### Authors
David Macharia @[Dave-mash](https://github.com/Dave-mash)
