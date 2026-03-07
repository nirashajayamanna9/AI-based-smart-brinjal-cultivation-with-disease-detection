from pydoc import text

from flask import Flask, flash, jsonify, render_template, request, redirect, url_for, session
import os
from flask_sqlalchemy import SQLAlchemy
from config import Config
import requests
from ultralytics import YOLO
from sqlalchemy import text
import numpy as np
import cv2

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)

API_KEY ="fd2a68cc4b3d7235e04c7437e4b6c9d2"

# Load YOLO model once
MODEL_PATH = "best.pt"
model = YOLO(MODEL_PATH)

db = SQLAlchemy(app)

# ======================
# Database Model
# ======================
class User(db.Model):
    __tablename__ = "usertable"

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    cultivation_size = db.Column(db.String(50))
    climate_type = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class CultivationGuideline(db.Model):
    __tablename__ = "cultivation_guidelines"

    id = db.Column(db.Integer, primary_key=True)
    climate_type = db.Column(db.String(20), nullable=False)          # wet / dry
    cultivation_size = db.Column(db.String(20), nullable=False) # small / medium
    activity = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))  # optional

class DiseaseTreatment(db.Model):
    __tablename__ = "eggplant_disease_management"

    disease_id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(20), nullable=False)         
    treatment = db.Column(db.Text, nullable=False)
    prevention_tips = db.Column(db.Text, nullable=False)
    

class WeatherGuideline(db.Model):
    __tablename__ = "weather_guidelines"

    id = db.Column(db.Integer, primary_key=True)

    min_temp = db.Column(db.Float, nullable=False)
    max_temp = db.Column(db.Float, nullable=False)

    min_humidity = db.Column(db.Float, nullable=False)
    max_humidity = db.Column(db.Float, nullable=False)

    watering = db.Column(db.Text, nullable=False)
    fertilization = db.Column(db.Text, nullable=False)
    general_care = db.Column(db.Text, nullable=False)


# ======================
# Create Tables
# ======================
with app.app_context():
    db.create_all()

# ======================
# Public Pages
# ======================
@app.route('/')
def home():
    return render_template('open/index.html')

@app.route('/aboutus')
def about():
    return render_template('open/aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('open/contactus.html')

# ======================
# Login
# ======================
@app.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':

        email = request.form.get("email")
        password = request.form.get("password")

        # ==========================
        # ADMIN LOGIN (HARDCODED)
        # ==========================
        if email == "admin@gmail.com" and password == "admin123":
            session.clear()
            session['admin'] = True
            session['email'] = email

            return '''
                <script>
                    alert("Admin Login Successful!");
                    window.location.href = "/admin_dashboard";
                </script>
            '''

        # ==========================
        # NORMAL USER LOGIN
        # ==========================
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session.clear()
            session['user_id'] = user.user_id
            session['email'] = user.email
            session['name'] = user.name
            session['cultivation_size'] = user.cultivation_size
            session['climate_type'] = user.climate_type

            return '''
                <script>
                    alert("Login Successful! Welcome Back 🌱");
                    window.location.href = "/mainhome";
                </script>
            '''

        return '''
            <script>
                alert("Invalid Email or Password!");
                window.location.href = "/login";
            </script>
        '''

    return render_template("open/login.html")

# ======================
# Signup
# ======================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        email = request.form['email']

        # --------------------------
        # Check duplicate email
        # --------------------------
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template(
                'open/signup.html',
                error="Email already registered"
            )

        user = User(
            name=request.form['name'],
            city=request.form['city'],
            cultivation_size=request.form['cultivation_size'].lower(),
            climate_type=request.form['climate_type'].lower(),
            email=email,
            password=request.form['password']
        )


        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('open/signup.html')

# # ======================
# # After Sign In
# # ======================
# @app.route('/aftersignin')
# def aftersignin():
#     if "user_id" not in session:
#         return redirect(url_for('login'))

#     return render_template(
#         "aftersignin.html",
#         name=session['name']
#     )

@app.route('/mainhome')
def mainhome():

    # Check login
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Get user from database
    user = db.session.get(User, session["user_id"])

    if not user:
        return redirect(url_for("login"))

    # Store important values in session (for guideline & weather pages)
    session["climate_type"] = user.climate_type.lower() if user.climate_type else ""
    session["cultivation_size"] = user.cultivation_size.lower() if user.cultivation_size else ""

    return render_template(
        'main/home.html',
        name=user.name,
        climate=user.climate_type,
        size=user.cultivation_size
    )


@app.route('/weatherguideline')
def weatherguideline():
    return render_template('main/weatherguideline.html')


# ✅ THIS IS THE ROUTE CALLED FROM JAVASCRIPT
@app.route("/get_weather", methods=["POST"])
def get_weather():

    data = request.get_json()
    city = data.get("city")

    if not city:
        return jsonify({"error": "City is required"})

    # ---- OpenWeather API ----
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    weather_data = response.json()

    if response.status_code != 200:
        return jsonify({"error": "City not found"})

    temp = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind = weather_data["wind"]["speed"]
    condition = weather_data["weather"][0]["main"]

    # ---- Get Guideline From Database ----
    guideline = db.session.execute(
        text("""
            SELECT watering, fertilization, general_care
            FROM weather_guidelines
            WHERE :temp BETWEEN min_temp AND max_temp
            AND :humidity BETWEEN min_humidity AND max_humidity
            LIMIT 1
        """),
        {"temp": temp, "humidity": humidity}
    ).fetchone()

    if guideline:
        watering = guideline[0]
        fertilizer = guideline[1]
        general = guideline[2]
    else:
        watering = "Normal watering"
        fertilizer = "Regular fertilizing"
        general = "Normal care"

    return jsonify({
        "city": city.title(),
        "temp": temp,
        "humidity": humidity,
        "wind": wind,
        "condition": condition,
        "watering": watering,
        "fertilizer": fertilizer,
        "general": general
    })

def bytes_to_bgr(image_bytes: bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image")
    return img
    
@app.route('/dieaseasDetection')
def dieaseasDetection():
    return render_template('main/diseasesDetection.html')


@app.route('/predict', methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image_bytes = file.read()

    img = bytes_to_bgr(image_bytes)

    results = model.predict(source=img, verbose=False)
    r = results[0]

    probs = r.probs.data.cpu().numpy()
    top_idx = int(np.argmax(probs))
    confidence = float(probs[top_idx]) * 100
    class_name = r.names[top_idx]

    print("YOLO predicted:", class_name)
    print("Predicted index:", top_idx)

    # 🔥 Match using ID instead of name
    disease_data = DiseaseTreatment.query.filter_by(
        disease_id=top_idx
    ).first()

    if disease_data:
        treatment = disease_data.treatment
        prevention = disease_data.prevention_tips
    else:
        treatment = "No treatment found in database."
        prevention = "No prevention tips found."

    return jsonify({
        "disease": class_name,
        "confidence": round(confidence, 2),
        "treatment": treatment,
        "prevention": prevention
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/guideline")
def guideline():
    if "user_id" not in session:
        return redirect(url_for("login"))

    # Logged-in user
    user = db.session.get(User, session["user_id"])

    climate_tye = user.climate_type.lower()
    cultivation_size = user.cultivation_size.lower()

    # 🔥 MAIN QUERY
    guidelines = CultivationGuideline.query.filter(
        CultivationGuideline.climate_type == climate_tye,
        CultivationGuideline.cultivation_size == cultivation_size
    ).all()

    return render_template(
        "main/guideline.html",
        guidelines=guidelines,
        climate=climate_tye,
        size=cultivation_size
    )


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")

@app.route("/user")
def user():
    all_users = User.query.all()
    return render_template("admin/user.html", users=all_users)

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for("user"))   # name of the route function



@app.route("/database")
def database():
    all_disease = DiseaseTreatment.query.all()
    return render_template(
        "admin/admin_diseasestreatment.html",
        diseases=all_disease
    )




@app.route('/update_treatment/<int:disease_id>', methods=['GET', 'POST'])
def update_treatment(disease_id):
    disease = DiseaseTreatment.query.get_or_404(disease_id)

    if request.method == 'POST':
        disease.treatment = request.form['treatment']
        disease.prevention_tips = request.form['prevention_tips']

        db.session.commit()
        return redirect(url_for('database'))

    return render_template(
        'admin/update_diseasestreatment.html',
        disease=disease      # ✅ send as 'disease'
    )

@app.route('/model_monitoring')
def model_monitoring():
    return render_template("admin/ai_model.html")
@app.route("/logs")
def logs():
    return render_template("admin/logs.html")

@app.route("/adminguideline")
def adminguidelines():
    guidelines = CultivationGuideline.query.all()   # fetch all records
    return render_template(
        "admin/adminguideline.html",
        guidelines=guidelines
    )

@app.route('/add_guidelines', methods=['GET', 'POST'])
def add_guidelines():
    if request.method == 'POST':
        guideline = CultivationGuideline(
            climate_type=request.form['climate_type'],
            cultivation_size=request.form['cultivation_size'],
            activity=request.form['activity'],
            notes=request.form['notes'],
            image_url=request.form['image_url']
        )

        db.session.add(guideline)
        db.session.commit()

        flash("Guideline added successfully!", "success")
        return redirect(url_for('adminguidelines'))

    return render_template('admin/add_guideline.html')

@app.route("/delete_guideline/<int:id>")
def delete_guideline(id):
    guideline = CultivationGuideline.query.get_or_404(id)
    db.session.delete(guideline)
    db.session.commit()

    flash("Guideline deleted successfully!", "danger")
    return redirect(url_for("adminguidelines"))



@app.route('/edit_guideline/<int:id>', methods=['GET','POST'])
def edit_guideline(id):

    guideline = CultivationGuideline.query.get_or_404(id)

    if request.method == 'POST':
        guideline.climate_type = request.form['climate_type']
        guideline.cultivation_size = request.form['cultivation_size']
        guideline.activity = request.form['activity']
        guideline.notes = request.form['notes']
        guideline.image_url = request.form['image_url']

        db.session.commit()

        flash("Guideline updated successfully!", "info")
        return redirect(url_for('adminguidelines'))

    return render_template('admin/edit_guideline.html', guideline=guideline)



# ---------------- ADMIN PAGE ----------------
@app.route("/admin_weather_guidelines")
def admin_weather_guidelines():
    guidelines = WeatherGuideline.query.all()
    return render_template("admin/adminweatherguideline.html", guidelines=guidelines)


# ---------------- ADD NEW RULE ----------------
@app.route("/admin/add_weather_guideline")
def adminweatherguidelines():
    guidelines = WeatherGuideline.query.all()
    return render_template("adminweatherguideline.html", guidelines=guidelines)


@app.route("/add-weather-guideline", methods=["POST"])
def add_weather_guideline():
    new_rule = WeatherGuideline(
        min_temp=float(request.form['min_temp']),
        max_temp=float(request.form['max_temp']),
        min_humidity=float(request.form['min_humidity']),
        max_humidity=float(request.form['max_humidity']),
        watering=request.form['watering'],
        fertilization=request.form['fertilization'],
        general_care=request.form['general_care']
    )

    db.session.add(new_rule)
    db.session.commit()

    return redirect(url_for("admin_weather_guidelines"))


@app.route("/edit_weatherguideline/<int:id>")
def edit_weather_guideline(id):
    guideline = WeatherGuideline.query.get_or_404(id)
    return render_template("admin/edit_weatherguideline.html", guideline=guideline)

@app.route("/update_weatherguideline/<int:id>", methods=["POST"])
def update_weather_guideline(id):
    guideline = WeatherGuideline.query.get_or_404(id)

    guideline.min_temp = float(request.form['min_temp'])
    guideline.max_temp = float(request.form['max_temp'])
    guideline.min_humidity = float(request.form['min_humidity'])
    guideline.max_humidity = float(request.form['max_humidity'])
    guideline.watering = request.form['watering']
    guideline.fertilization = request.form['fertilization']
    guideline.general_care = request.form['general_care']

    db.session.commit()

    return redirect(url_for("admin_weather_guidelines"))



@app.route("/delete_weatherguideline/<int:id>")
def delete_weather_guideline(id):
    guideline = WeatherGuideline.query.get_or_404(id)
    db.session.delete(guideline)
    db.session.commit()
    return redirect(url_for("admin_weather_guidelines"))




if __name__ == "__main__":
    app.run(debug=True)
