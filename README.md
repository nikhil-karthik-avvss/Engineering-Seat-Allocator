# Engineering Seat Allocator

An application to manage and allocate engineering seats using **Django** with both local (PostgreSQL) and hosted (MySQL) database support.  

---

## Tech Stack
- **Backend**: Python, Django  
- **Frontend**: HTML, CSS, JavaScript  
- **Database**:  
  - PostgreSQL (Local)  
  - MySQL (Hosted via Django ORM)  

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/nikhil-karthik-avvss/Engineering-Seat-Allocator.git
cd Engineering-Seat-Allocator
````

### 2. Set up a virtual environment

```bash
python3 -m venv esa_env
```

Activate the environment:

* **Linux / MacOS**:

  ```bash
  source esa_env/bin/activate
  ```
* **Windows**:

  ```bash
  .\esa_env\Scripts\activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Database Setup

Run the following commands to set up the database:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

---

## Run the Server

Start the development server:

```bash
python3 manage.py runserver
```

By default, Django runs on **`http://localhost:8000/`**
You can access the project at:

* Local: [http://localhost:8000/index](http://localhost:8000/index)
* Hosted: [https://nikh10.pythonanywhere.com/index](https://nikh10.pythonanywhere.com/index)

---

## Notes

* Default Django port is **8000** (you can change it by specifying another port, e.g., `python3 manage.py runserver 8080`).
* Both PostgreSQL (local) and MySQL (hosted) versions use **Django ORM** for database operations.

---

## Deployment

The project is hosted on **PythonAnywhere**:
[https://nikh10.pythonanywhere.com/index](https://nikh10.pythonanywhere.com/index)

---
