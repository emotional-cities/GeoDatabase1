# eMOTIONALCities

# eMOTIONALCities Project Local Hosting Guide

This guide provides instructions on how to host the project locally, both without Docker (option A) and with Docker (option B). Choose the appropriate section based on your preferred method.

## A. Hosting without Docker 

### Prerequisites
- Installing Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
- Installing Python 3.x on your machine: https://www.python.org/downloads/
  
  on windows OS:
    1. Run the installer from Windows Explorer
    2. Check the Add Python 3.8 to Path check box
    3. Click Customize installation
    4. All Optional Features should already be checked; click Next
    5. Check Install for all users, then click Install
         
### Instructions

1. **Clone the repository:**
On windows OS run Git Bash
On Mac OS & Linux you can use the shell

   ```shell
      git clone https://github.com/emotional-cities/GeoDatabase1
   ```

   
2. **Navigate to the project directory: (you can locate the directory where GitHub is installed)**

   ```shell
      cd <project_directory>
   ```
   example: cd Users/name/OneDrive/Documents/GitHub/GeoDatabase1/empotics
3. **Install requirements:**

```shell
pip install -r req.txt


```
4. **Run the serve:**

```shell
python manage.py runserver

```
## B. Hosting with Docker

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


Open a web browser and visit http://localhost:8000 to access your locally hosted emotional cities app.
