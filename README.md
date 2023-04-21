# Virtual-Mentor

## Table of Contents
- [About](#about)
- [Setting up the environment](#setting-up-the-environment)
- [Running the application](#running-the-application)
- [application routes](#application-routes)
- [API Documentation](#api-documentation)
- [To-Do](#to-do)
- [Contributors](#contributors)
- [License](#license)

## About
MentorGPT is a web application that uses a chatbot to answer questions about the Python, Data Science, Machine Learning. The chatbot is connected to OpenAI's GPT-3 API. The application is built using Python, Flask and Vue.

## Setting up the environment
You should have the following installed on your machine:
- python 3.10
- flask 2.2.3
- flask-cors 3.0.10

## Running the application
- Clone the repository
```bash
git clone https://github.com/Mahhheshh/MenotGPT.git
```
- Create a virtual environment
```bash
pip install pipenv 
pipenv shell
```
- Install the dependencies
```bash
pipenv install
```
- Run the application
```bash
python main.py
```
- Open the application in your browser
```bash
http://localhost:5000/
```

## application routes
- GET /
```bash
http://localhost:5000/
```
- POST /ask
```bash
http://localhost:5000/ask
```

## API Documentation
- POST /ask, request body
```json
{
    "question": "What is difference between lists and tuPle"
}
```
- POST /ask, response body
```
    Returns a stream of data using Server-Sent Events.
```

## setting up the environment(frontend)
- Install the dependencies
```bash
cd frontend
npm install
```
- Run the application
```bash
npm run dev -- --open 
```
## To-Do
- [ ] beautify the UI

## Contributors
Contributions are welcome. Please open an issue or submit a pull request.

## License
[MIT](License)

### made with ❤️ by [Mahesh](https://github.com/Mahhheshh)