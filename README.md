📊 Flask Dashboard
A dynamic and interactive dashboard built using Flask, MySQL, and Bootstrap, displaying insights from a JSON dataset. The dashboard provides filtering options to analyze data efficiently.

🚀 Features
📌 Data Visualization – Displays key insights using interactive charts and tables.

🔍 Filtering Options – Filter data based on end_year, topics, sector, region, source, country, and city.

📂 Database Integration – Uses MySQL for storing and querying data.

🎨 Responsive UI – Designed with Bootstrap for a clean and user-friendly interface.

🔥 Flask Backend – Lightweight and efficient server-side handling.

🏗️ Project Structure

flask_dashboard/
│── static/          # CSS, JavaScript, images
│── templates/       # HTML templates
│── app.py           # Main Flask application
│── config.py        # Database configuration
│── models.py        # Database schema and queries
│── routes.py        # Flask routes
│── requirements.txt # Required dependencies
│── README.md        # Project documentation
🛠️ Setup & Installation
1️⃣ Clone the repository

git clone https://github.com/prachi-pandey-github/flask_dashboard.git
cd flask_dashboard
2️⃣ Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
4️⃣ Set up MySQL database
Import the JSON file into MySQL

Update config.py with your MySQL credentials

5️⃣ Run the Flask app

python app.py
The dashboard will be available at http://127.0.0.1:5000/.
