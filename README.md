📝 FastAPI Blog Application (MongoDB) 🚀

A clean and lightweight Blog Application built with FastAPI, Jinja2, and MongoDB (PyMongo).
This project demonstrates backend development using FastAPI along with template rendering and database integration.

🌟 Features

✍️ Create, 📖 Read, and ❌ Delete blog posts

🔢 Automatic numbering of posts

📄 Form handling using FastAPI

🎨 Dynamic rendering with Jinja2 Templates

🔗 Clean URL routing & path parameters

💾 MongoDB database using PyMongo

⚡ Fast development using uvicorn --reload

| Layer        | Technology        |
| ------------ | ----------------- |
| **Backend**  | FastAPI (Python)  |
| **Frontend** | Jinja2, HTML, CSS |
| **Database** | MongoDB           |
| **Driver**   | PyMongo           |
| **Server**   | Uvicorn           |


📁 Project Structure

📦 Blog_App
 ┣ 📂 templates
 ┃ ┣ index.html
 ┃ ┣ create.html
 ┣ 📂 static
 ┃ ┗ styles.css (optional)
 ┣ 📄 main.py
 ┣ 📄 requirements.txt
 ┣ 📄 README.md


⚙️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/santhosh-13/Blog_App.git
cd Blog_App

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Start MongoDB

Make sure MongoDB is running locally or use MongoDB Atlas.

4️⃣ Run the application
uvicorn main:app --reload

5️⃣ Open in browser
http://127.0.0.1:8000/

🧩 Main Functionalities
📌 Home Page

Displays list of all blog posts

Each post has:

Title

Content

Auto-incremented post number

Delete button

📌 Create Blog Page

Form to add a new blog post

Saves data to MongoDB

📌 Delete Post

Deletes specific post by ID

Redirects to home page
