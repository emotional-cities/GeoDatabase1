# eMOTIONALCities
-empotics is for the webpage
# eMOTIONALCities Project Local Hosting Guide

This guide provides instructions on how to host the project locally, both with and without Docker. Choose the appropriate section based on your preferred method.

## Hosting with Docker

### Prerequisites

- Docker installed on your machine

### Instructions

1. **Clone the repository:**
```shell
git clone <repository_url>
```
2. **Navigate to the project directory:**

```shell
cd <project_directory>
```


3. **Build the Docker image:**
   ```shell
      docker build -t emo .
   ```
   
4. **Run the Docker container:**

   ```shell
      docker run -p 8000:8000 my_django_app
   ```
   

5. **Access the Django app:**

Open a web browser and visit [http://localhost:8000](http://localhost:8000) to access the emotional cities app running inside the Docker container.

## Hosting without Docker

### Prerequisites

- Python 3.x installed on your machine
- `virtualenv` package installed (optional but recommended)

### Instructions

1. **Clone the repository:**

   ```shell
      git clone <repository_url>
   ```

   
2. **Navigate to the project directory:**

   ```shell
      cd <project_directory>
   ```
   
3. **Create and activate a virtual environment (optional):**

```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver

```

Open a web browser and visit http://localhost:8000 to access your locally hosted emotional cities app.
