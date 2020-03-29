# musicrs-youtubeAPI 

## Requirements 
- python3 
  - download from [https://www.python.org/](https://www.python.org/)
- create a virtualenv 
  - `$ pip3 install virtualenv` (installation)
  - `$ virtualenv venv -p python3.6` 

- activate virtualenv venv
  - `$ source venv/bin/activate`

- install all required packages 
  - **Flask** `$ pip3 install flask`
  - **dotenv** `$ pip3 install python-dotenv`  
  OR install all requirements
  - `$ pip3 install -r requirements.txt`

- Create necessary files 
  - create `app.py`
  - create `wsgi.py` 
    - run app.py: `$ python3 wsgi.py`
    - your app is running at 
      - Local: [http://localhost:5000](http://localhost:5000)

# Hosting in Heroku 
- Follow the steps: 
  - [Flask Deployment in Heroku](https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/)
  - [devcenter.heroku.com - Python](https://devcenter.heroku.com/articles/getting-started-with-python)
