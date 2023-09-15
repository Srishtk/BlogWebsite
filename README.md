# Blog Website with Flask and SQLAlchemy

Welcome to the Blog Website repository! This project is a simple yet powerful blog platform built using Flask and SQLAlchemy. It features user authentication, blog creation, rating, and commenting functionality.

## Features

- **User Authentication**: Secure user registration and login system powered by Flask-Login.
- **Blog Creation**: Registered users can easily create and publish their blogs on the platform.
- **Read Blogs**: Users can explore and read blogs submitted by others.
- **Rating**: Rate and provide feedback on blogs.
- **Author Controls**: Authors have the ability to edit and delete their blogs.

## Technologies Used

- Flask: A micro web framework for Python.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library.
- Bootstrap: Front-end framework for responsive and appealing design.
- SQLite: Lightweight and serverless relational database.

## Project Structure

- `routes.py`: The main Flask application.
- `models.py`: Database models defined using SQLAlchemy.
- `templates/`: HTML templates for rendering web pages.
- `static/`: Static assets (CSS file).
- `instance/`: Contains database.

## Installation and Usage

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/Srishtk/BlogWebsite.git

2. Create a virtual environment and install the required dependencies.

   ```bash
   cd BlogWebsite
   python -m venv venv
   source venv/bin/activate  (Linux/Mac) or venv\Scripts\activate (Windows)
   pip install -r requirements.txt

3. Run the Flask application.

