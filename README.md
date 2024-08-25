# GateWay Faucet App

A Sepolia Eth faucet app which sends 0.0001 Sepolia Eth to a supplied address

## SETUP
To setup the app on your local machine.

* Install a python interpreter(minimum of python 3.8). For windows install Ananconda Navigator. For Linux do:
```bash
sudo apt-get update
sudo apt-get install python3 pip
```

* Next is to setup a python virtual environment. For windows use the following command to create a virtual environment named venv in the base project structure:
```cmd
python -m venv venv
```
--> For linux:
```bash
python3 -m venv venv
```

* Next step is to activate the Virtual Environment. For Windows use the following commands:
```cmd
venv\Scripts\activate.bat
```
For linux:
```bash
source venv/bin/activate
```

* Next is to install the required packages. Same command applies to both windows and linux:
```bash
pip install -r requirements.txt
```

* You can setup your environment variables by manually setting(windows use set) or exporting(linux use the export command) them or you can create a .env file inside the faucet file using the .env_example.

* create migrations files and run migrations on the db. Also create cache table for your app cache settings
```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createcachetable
```

* Run the app. For windows you can
```cmd
gunicorn -c gunicorn.config.py
//or
python manage.py runserver
```
for linux:
```bash
#run the run.py file
$ gunicorn -c gunicorn.config.py
#or 
$ python manage.py runserver #development server
```

with that you app development server should be running you can access at [localhost:8000](localhost:8000)


## SETUP USING DOCKER
You can setup the app by running in a containerized setting by taking advantage of the docker containerization technology.

* Install and setup docker on your local machine
* To build the Docker image, navigate to the directory containing your Dockerfile. Works for both windows and linux and run:

```bash
docker build -t faucet_app .
```
* To run the Docker container. This will expose your Django application on port 8000 of your local machine:

```docker
docker run -p 8000:8000 faucet_app
```
### Using Docker-Compose
* You can build and run once the `docker-compose.yml` file with the following command

```bash
docker-compose up --build
```
* Tear down with:

```bash
docker-compose down
```

### Swagger/OpenApi Documentation
Swagger(now OpenAPI) was used to provide a simple documentation for the RESTAPI. After initialization visit [localhost:8000/docs](localhost:8000/docs) and interact with the documentation.You can make requests directly to the REST API from this interface.