# Diabetes Prediction - Backend

Backend for diabetes prediction. You can find the frontend [here](https://github.com/mtlv99/diabetes-app).

Authors:
- Marco León Vargas
- Dwight García Esquivel

# Technologies used
- **Language**: Python 3.10
- **Web Framework**: Django
- **Data Analysis**: pandas
- **Machine Learning**: scikit-learn (sklearn)
- **Data Visualization**: seaborn, matplotlib
- **Database**: MariaDB

## Installation

Download Python version 3.10 before continuing.

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

For running a MariaDB instance, you can use XAMPP version 8.2.12. You can download it from [here](https://www.apachefriends.org/download.html). You only need to select MySQL and phpMyAdmin components during the installation process.

> Note: XAMPP uses MariaDB instead of MySQL, even if the installer says MySQL.

### 3. Create .env file

Create a file named `.env` in the root directory of the project with the following content:

```txt
DATABASE_NAME=diabetes_db
DATABASE_USER=root
DATABASE_PASSWORD=''
DATABASE_HOST=localhost
DATABASE_PORT=3306
```


### 4. Create the database

```bash
python manage.py makemigrations diabetes
python manage.py migrate
```

### 5. Run the server

```bash
python manage.py runserver
```


### Exit the virtual environment

```bash
deactivate  # On Windows use: .\venv\Scripts\deactivate
```



## Test Examples

### a. User with diabetes

```json
{
    "pregnancies": 3,
    "glucose": 180.0,
    "blood_pressure": 90.0,
    "skin_thickness": 40.0,
    "insulin": 200.0,
    "bmi": 35.2,
    "diabetes_pedigree_function": 0.9,
    "age": 55
}
```

### b. User without diabetes

```json
{
    "pregnancies": 1,
    "glucose": 95.0,
    "blood_pressure": 75.0,
    "skin_thickness": 20.0,
    "insulin": 80.0,
    "bmi": 22.5,
    "diabetes_pedigree_function": 0.3,
    "age": 30
}
```