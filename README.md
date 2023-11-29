# Sample Boiler Plate for FAST API and Celery


## create virtual env
```
# MAC/LINUX users
python3 -m venv venv
# activate enviroment
source venv/bin/activate

# install requirements
pip3 install "fastapi[all]" beautifulsoup4 pandas celery redis beanie python-dotenv selenium motor

# deactivate enviroment
deactivate
```

## runung the web app
```
uvicorn src.app:app --host 0.0.0.0 --port 8000
```
## Visit Docker Runing app
```
# build app
docker-compose up --build

# for docker run app visit
http://0.0.0.0:8001/ 
# visit the flower dashboard at 
http://0.0.0.0:5556/
```

## solving docker issues on
```
```