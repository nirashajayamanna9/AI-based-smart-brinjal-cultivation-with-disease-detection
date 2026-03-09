AI in Smart Brinjal Cultivation: Brinjal Monitoring with Disease Detection and Solutions

An intelligent web-based application designed to assist home gardeners, urban farmers, and small-scale cultivators in managing brinjal (eggplant) crops. The system leverages Deep Learning for disease detection and real-time APIs for climate-aware farming guidance.

🚀 Key Features

1. AI Disease Detection: Uses a trained YOLOv8 model to identify common brinjal diseases (e.g., Bacterial Wilt, Leaf Spot) from uploaded images.

2. Climate-Aware Guidance: Integrates with a Weather API to provide real-time cultivation advice based on local temperature and humidity.

3. Stage-Based Instructions: Offers a comprehensive A–Z guide for every growth stage of the brinjal plant.

4. Admin Dashboard: A centralized interface for agricultural experts to manage disease records, growing guidelines, and weather alerts.

5. Mobile-Responsive UI: Built with Bootstrap to ensure accessibility for farmers using smartphones in the field.

🛠️ Tech Stack

  Backend: Python (Flask)

  Database: PostgreSQL (with SQLAlchemy ORM)

  AI/ML: YOLOv8, OpenCV, NumPy

  Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

  API: OpenWeatherMap API (or similar)

📋 Prerequisites

Before running the project, ensure you have the following installed:

  Python 3.13+

  PostgreSQL

  Pip (Python package manager)

⚙️ Installation & Setup

  Clone the Repository

  Create a Virtual Environment

  Install Dependencies

  Database Configuration

Create a PostgreSQL database and update your connection string in app.py:

  Initialize Database

  Run the Application

  Access the app at http://127.0.0.1:5000/

🧪 Testing

The system includes comprehensive test cases covering:

  User Authentication: Valid/Invalid login and duplicate signup detection.

  Admin Side: Management of Growing and Weather guidelines (CRUD operations).

  AI Logic: Disease detection accuracy and file format validation.


