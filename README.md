# RedInk_API

**RedInk_API** is a RESTful API built with FastAPI that provides access to controversial books that have been banned, criticised or censored at some point in history.

---

## 📚 Project Overview

This project began as a personal and academic initiative, aimed at showcasing technical skills in API development, as a commitment to freedom of information and it also serves as a portfolio element.
This application was created to support research, educational access and freedom of information by making historically challenged, controversial or censored books available in digital format. Whether you're a researcher, developer or simply curious, RedInk_API allows you to explore these texts and to integrate them in another application. Also, I will make sure to update the database and add new books from time to time.

---

## 🚀 Available Endpoints

### 🔎 Authors

- `GET /authors`  
  Retrieve a list of all authors.

- `GET /authors/by-ID/{author_ID}`  
  Retrieve author's name and surname using the author’s ID.

- `GET /authors/by-name/{author_name}`  
  Search authors by first name.

- `GET /authors/by-surname/{author_surname}`  
  Search authors by surname.

### 📖 Books

- `GET /books`  
  Retrieve a list of all books.

- `GET /books/by-ID/{book_ID}`  
  Retrieve the name and author of a specific book using its ID.

- `GET /books/by-ID/{book_ID}/content`  
  Retrieve the full content of a specific book by its ID.

- `GET /books/by-title/{book_title}`  
  Search books by title.

- `GET /books/by-author-name/{author_name}`  
  Search books by author's first name.

- `GET /books/by-author-surname/{author_surname}`  
  Search books by author's surname.

---

## 🛠️ Setup & Installation

To run the project locally, follow these steps:

1. **Create and activate a virtual environment** (optional but recommended):

   ```bash
   python3 -m venv RedInkVenv
   source RedInkVenv/bin/activate

2. **Clone the repository**:
   ```bash
   git clone https://github.com/0x003F/RedInk_API.git
   cd RedInk_API
    ````

3. **Ensure you are on the `main` branch**:

   ```bash
   git checkout main
   ```

4. **Install required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Generate the `.env` file**:

   ```bash
   python3 env_setup.py
   ```

6. **Create the SQLite database**:
   Use the provided SQL dump to set up the database:

   ```bash
   sqlite3 RedInk.db < db_dump.sql
   ```

7. **Run the application**:
   Use Uvicorn to start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```
