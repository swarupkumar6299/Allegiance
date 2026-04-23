import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# 1. Load the secret variables from your .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_allegience_key"  

# ==========================================
# EMAIL SETUP (NEW)
# ==========================================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')
mail = Mail(app) # Initialize Flask-Mail

# ==========================================
# DATABASE SETUP
# ==========================================
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================
# DATABASE MODEL
# ==========================================
class Consultation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=db.func.current_timestamp())

# (Keep all your visa and settlement routes exactly as they are here)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/ukwork')
def ukwork():
    return render_template('ukwork.html')

@app.route('/australia')
def australia():
    return render_template('australia.html')

@app.route('/canada')
def canada():
    return render_template('canada.html')

@app.route('/germanyjob')
def germanyjob():
    return render_template('germanyjob.html')

@app.route('/spain')
def spain():
    return render_template('spain.html')

@app.route('/portugal')
def portugal():
    return render_template('portugal.html')

@app.route('/uae')
def uae():
    return render_template('uae.html')

@app.route('/sweden')
def sweden():
    return render_template('sweden.html')

@app.route('/usa_settlement')
def usa_settlement():
    return render_template('usa_settlement.html')

@app.route('/europe_settlement')
def europe_settlement():
    return render_template('europe_settlement.html')

@app.route('/uk_settlement')
def uk_settlement():
    return render_template('uk_settlement.html')

@app.route('/canada_settlement')
def canada_settlement():
    return render_template('canada_settlement.html')

@app.route('/australia_settlement')
def australia_settlement():
    return render_template('australia_settlement.html')


@app.route('/schengen_work')
def schengen_work():
    return render_template('schengen_work.html')


@app.route('/australia_work')
def australia_work():
    return render_template('australia_work.html')

@app.route('/europe_work')
def europe_work():
    return render_template('europe_work.html')
@app.route('/family_visa')
def family_visa():
    return render_template('family_visa.html')

@app.route('/business_visa')
def business_visa():
    return render_template('business_visa.html')

@app.route('/investor_visa')
def investor_visa():
    return render_template('investor_visa.html')

@app.route('/student_visa')
def student_visa():
    return render_template('student_visa.html')

@app.route('/caribbean_settlement')
def caribbean_settlement():
    return render_template('caribbean_settlement.html')

@app.route('/tourist_visa')
def tourist_visa():
    return render_template('tourist.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route('/asia')
def asia():
    return render_template('asia.html')



# --- CONTACT FORM ROUTE ---

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Grab the data they typed into the form
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        # NEW: Prepare the email
        msg = Message(
            subject=f"Allegiance Contact Form: {subject}",
            # NEW: This changes the display name in your inbox!
            sender=(f"{name} (Website)", os.environ.get('MAIL_USERNAME')), 
            recipients=[os.environ.get('MAIL_USERNAME')],
            reply_to=email,
            body=f"""
            New message from the Contact Page:
            
            Name: {name}
            Email: {email}
            Subject: {subject}
            
            Message:
            {message}
            """
        )

        # NEW: Send the email
        try:
            mail.send(msg)
            flash("Thank you! Your message has been sent successfully.", "success")
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("Sorry, there was an issue sending your message.", "error")

        return redirect(url_for('contact'))

    # If they are just visiting the page normally, show them the HTML
    return render_template('contact.html')


    # Notice we added 'GET' here so it can display the HTML page!
# Notice we added 'GET' here so it can display the HTML page!
 
@app.route('/book-consultation', methods=['GET', 'POST'])
def book_consultation():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        destination = request.form.get('destination')
        phone = request.form.get('phone')
        
        # MISSING LINE: You must have this line so Python knows what "email" is!
        email = request.form.get('email') 
        
        message = request.form.get('message')

        msg = Message(
            subject=f"New Consultation Request: {first_name} {last_name}",
            sender=(f"{first_name} {last_name} (Consultation)", os.environ.get('MAIL_USERNAME')),
            recipients=[os.environ.get('MAIL_USERNAME')],
            reply_to=email, # Now Python knows exactly what variable to put here
            body=f"""
            New Consultation Request from Allegiance Website:
            
            Name: {first_name} {last_name}
            Email: {email}
            Phone Number: {phone}
            Desired Destination: {destination}
            
            Message:
            {message}
            """
        )


        try:
            mail.send(msg)
            flash("Thank you! Your consultation request has been sent.", "success")
            return redirect(url_for('index'))
            
        except Exception as e:
            print(f"Error sending email: {e}")
            flash("Sorry, there was an error sending your request.", "error")
            return redirect(url_for('book_consultation'))

    return render_template('book_Consultation.html')


if __name__ == "__main__":
    app.run(debug=True)