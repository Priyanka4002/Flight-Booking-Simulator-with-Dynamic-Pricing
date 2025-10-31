✈ Airline Booking Simulator — 

🌟 Overview

This project is a full-stack airline booking simulation system built with FastAPI (Python) for the backend and a modern, interactive HTML/CSS/JavaScript frontend.
It supports dynamic pricing, seat reservation concurrency control, simulated payments, booking confirmation, and downloadable receipts.


---

🧠 Key Features

🚀 Backend (FastAPI)

Retrieve all flights and search by origin, destination, and date

Dynamic pricing based on:

Remaining seats

Time to departure

Simulated demand


Concurrency-safe seat booking using DB transactions

Multi-step booking flow:

Flight & seat selection

Passenger details

Simulated payment (success/fail)

Confirmation and PNR generation


Booking cancellation and history retrieval

Background market simulator for seat/demand updates

PDF receipt generation endpoint

MySQL database integration


💻 Frontend (HTML/CSS/JavaScript)

Clean, minimal yet vibrant user interface

Flight search and booking forms with smooth transitions

Confirmation and receipt pages with fade-in animation

Downloadable PDF booking receipts

Responsive and mobile-friendly design



---

🏗 Project Structure

📦 airline-booking-simulator
│
├── backend/
│   ├── backend.py
│   ├── db_config.py
│   ├── models.py
│   ├── pricing_engine.py
│   └── utils.py
│
├── frontend/
│   ├── index.html
│   ├── booking.html
│   ├── confirmation.html
│   ├── receipt.html
│   ├── script.js
│   └── style.css
│
└── README.md


---

⚙ Setup Instructions

🐍 Backend Setup

1. Install dependencies

pip install fastapi uvicorn sqlalchemy pymysql reportlab


2. Database Setup

Create a MySQL database named project

Import your SQL schema (e.g. Lucky.session.sql)

Update connection details inside db_config.py:

DATABASE_URL = "mysql+pymysql://root:yourpassword@localhost/project"



3. Run the FastAPI server

uvicorn backend:app --reload

Server runs at: http://127.0.0.1:8000



🖥 Frontend Setup

1. Open the frontend folder in VS Code


2. Right-click on index.html → “Open with Live Server”
(or use any static file server such as python -m http.server)


3. Make sure the backend server is running before using the frontend.




---

🔍 API Endpoints Summary

Method	Endpoint	Description

GET	/flights	Retrieve all flights
GET	/search	Search flights by origin, destination, and date
GET	/dynamic_price/{airline_code}	Fetch dynamic price
POST	/bookings/create	Create a booking
POST	/bookings/{pnr}/pay	Simulate payment
POST	/bookings/{pnr}/confirm	Confirm booking
POST	/bookings/{pnr}/cancel	Cancel booking
GET	/bookings/{pnr}	Retrieve booking details
GET	/bookings/{pnr}/receipt	Download booking receipt as PDF



---

📸 Frontend Pages

Page	Description

index.html	Search flights by origin/destination
booking.html	Passenger booking form
confirmation.html	Displays booking confirmation (PNR, seat)
receipt.html	Shows booking summary and allows PDF download



---

🧩 Tech Stack

Category	Technology

Backend Framework	FastAPI
Database	MySQL
Frontend	HTML, CSS, JavaScript
Styling	Modern minimal + travel-themed UI
Concurrency	SQLAlchemy transactions
PDF Generation	ReportLab



---

📈 Future Enhancements

User authentication (login/register)

Real-time flight availability updates

Integration with third-party airline APIs

Enhanced dashboard for admins



---

👨‍💻 Author

Developed by: Priyanka Meka
Technologies: FastAPI • MySQL • HTML • CSS • JavaScript
