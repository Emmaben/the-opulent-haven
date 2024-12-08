from flask import Flask, render_template, request, jsonify,  redirect, url_for
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time
from sqlalchemy.types import Date, Time
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate

app = Flask(__name__)

# Flask Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'theopulenthaven03@gmail.com'
app.config['MAIL_PASSWORD'] = 'maggoznswenvflrc' # Theopulenthaven@0874
app.config['MAIL_DEFAULT_SENDER'] = 'theopulenthaven03@gmail.com'

mail = Mail(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Reservation model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False, default=lambda: datetime.utcnow().time().replace(microsecond=0))
    guests = db.Column(db.Integer, nullable=False)
    table_number = db.Column(db.Integer, nullable=False)
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(microsecond=0))

# Define the Subscriber model
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    subscribed_at = db.Column(db.DateTime, default=lambda: datetime.utcnow().replace(microsecond=0))

# Create the database tables
with app.app_context():
    db.create_all()
    print("Database recreated successfully!")

# Reservation conflict checker
def check_conflict(date, time):
    return Reservation.query.filter_by(date=date, time=time).first()

# Test Email!
# @app.route('/send-mail')
# def send_mail():
#     try:
#         msg = Message("Test Email", recipients=["theopulenthaven03@gmail.com"])
#         msg.body = "This is a test email sent from Flask using Gmail SMTP."
#         mail.send(msg)
#         return "Email sent successfully!"
#     except Exception as e:
#         return f"Failed to send email: {e}"
#
# if __name__ == '__main__':
#     app.run(debug=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/menu')
def menu():
    menu_items = {
        "Appetizers": [
            {"name": "Truffle-Infused Soup",
                "description": "A rich and creamy soup with black truffle essence.",
                "price": "£12",
                "allergies": "Contains dairy, gluten",
                "image": "Truffle-Infused Soup.png"},

            {"name": "Gourmet Bruschetta",
                "description": "Crispy bread topped with fresh tomatoes, basil, and olive oil.",
                "price": "£10",
                "allergies": "Contains gluten",
                "image": "Gourmet Bruschetta.png"},

            {"name": "Smoked Salmon Tartare",
                "description": "Delicately smoked salmon with a tangy caper and dill dressing.",
                "price": "£15",
                "allergies": "Contains fish",
                "image": "Smoked Salmon Tartare.png"},

            {"name": "Stuffed Mushrooms",
                "description": "Portobello mushrooms stuffed with garlic, breadcrumbs, and parmesan.",
                "price": "£12",
                "allergies": "Contains dairy, gluten",
                "image": "Stuffed Mushrooms.png"}
        ],

        "Main Courses": [
            {"name": "Steak with Red Wine Reduction",
                "description": "Succulent steak paired with a bold red wine sauce.",
                "price": "£35",
                "allergies": "None (gluten-free)",
                "image": "Steak with Red Wine Reduction.png"},

            {"name": "Vegan Risotto",
                "description": "Creamy risotto with seasonal vegetables.",
                "price": "£25",
                "allergies": "None (vegan and gluten-free)",
                "image": "Vegan Risotto.png"},

            {"name": "Grilled Seabass",
                "description": "Perfectly grilled seabass served with a citrus butter sauce.",
                "price": "£30",
                "allergies": "Contains fish, dairy",
                "image": "Grilled Seabass.png"},

            {"name": "Chicken Marsala",
                "description": "Tender chicken breast simmered in a marsala wine sauce with mushrooms.",
                "price": "£28",
                "allergies": "Contains dairy",
                "image": "Chicken Marsala.png"},

            {"name": "Vegetable Wellington",
                "description": "Puff pastry filled with a medley of roasted vegetables and herbs.",
                "price": "£22",
                "allergies": "Contains gluten", "image": "Vegetable Wellington.png"},

            {"name": "Lamb Shank with Herb Couscous",
                "description": "Slow-cooked lamb shank served with herb couscous and root vegetables.",
                "price": "£38",
                "allergies": "Contains gluten",
                "image": "Lamb Shank with Herb Couscous.png"}
        ],

        "Sides": [
            {"name": "Garlic Parmesan Mashed Potatoes",
                "description": "Creamy mashed potatoes infused with roasted garlic and topped with grated parmesan cheese.",
                "price": "£8",
                "allergies": "Contains dairy",
                "image": "Garlic Parmesan Mashed Potatoes.png"},

            {"name": "Sautéed Seasonal Vegetables",
                "description": "A colorful medley of fresh, seasonal vegetables lightly sautéed in olive oil and garlic.",
                "price": "£7",
                "allergies": "None (vegan and gluten-free)",
                "image": "Sautéed Seasonal Vegetables.png"},

            {"name": "Truffle Fries",
                "description": "Crispy golden fries tossed in truffle oil and sprinkled with parmesan and fresh parsley.",
                "price": "£9",
                "allergies": "Contains dairy",
                "image": "Truffle Fries.png"},

            {"name": "Herb-Roasted Brussels Sprouts",
                "description": "Oven-roasted Brussels sprouts seasoned with fresh thyme and rosemary, drizzled with balsamic glaze.",
                "price": "£8",
                "allergies": "None (vegan and gluten-free)",
                "image": "Herb-Roasted Brussels Sprouts.png"},

            {"name": "Wild Mushroom Risotto",
                "description": "Creamy risotto with a blend of wild mushrooms, white wine, and fresh herbs.",
                "price": "£10",
                "allergies": "Contains dairy",
                "image": "Wild Mushroom Risotto.png"}
        ],

        "Desserts": [
            {"name": "Molten Chocolate Lava Cake",
                "description": "Decadent chocolate cake with a gooey center.",
                "price": "£15",
                "allergies": "Contains dairy, eggs, gluten",
                "image": "Molten Chocolate Lava Cake.png"},

            {"name": "Crème Brûlée",
                "description": "Classic vanilla custard topped with caramelized sugar.",
                "price": "£14",
                "allergies": "Contains dairy, eggs",
                "image": "Crème Brûlée.png"},

            {"name": "Berry Cheesecake",
                "description": "Creamy cheesecake topped with a mixed berry compote.",
                "price": "£13",
                "allergies": "Contains dairy, gluten",
                "image": "Berry Cheesecake.png"},

            {"name": "Seasonal Fruit Tart",
                "description": "Fresh seasonal fruits over a light custard and flaky pastry.",
                "price": "£12",
                "allergies": "Contains dairy, gluten, eggs",
                "image": "Seasonal Fruit Tart.png"},

            {"name": "Vegan Chocolate Mousse",
                "description": "Silky smooth chocolate mousse made with avocado and coconut cream.",
                "price": "£11",
                "allergies": "None (vegan and gluten-free)",
                "image": "Vegan Chocolate Mousse.png"}
        ]
    }
    return render_template('menu.html', menu_items=menu_items)

@app.route('/drinks', methods=['GET', 'POST'])
def drinks():
    drinks_data = {
        "Cocktails": [
            {"name": "Mojito",
                "description": "A refreshing blend of mint, lime, and rum.",
                "price": "£12",
                "image": "Mojito.png"},

            {"name": "Old Fashioned",
                "description": "Classic whiskey cocktail with bitters and sugar.",
                "price": "£15",
                "image": "Old Fashioned.png"},

            {"name": "Margarita",
                "description": "A zesty mix of tequila, lime juice, and triple sec.",
                "price": "£14",
                "image": "Margarita.png"},

            {"name": "Cosmopolitan",
                "description": "A chic blend of vodka, cranberry, and lime.",
                "price": "£13",
                "image": "Cosmopolitan.png"},

            {"name": "Pina Colada",
                "description": "A tropical mix of coconut, pineapple, and rum.",
                "price": "£12",
                "image": "Pina Colada.png"},

            {"name": "Whiskey Sour",
                "description": "A tangy blend of whiskey, lemon, and sugar.",
                "price": "£15",
                "image": "Whiskey Sour.png"},

            {"name": "Long Island Iced Tea",
                "description": "A potent mix of spirits with a hint of cola.",
                "price": "£18",
                "image": "Long Island Iced Tea.png"},

            {"name": "Daiquiri",
                "description": "A sweet and sour rum-based classic.",
                "price": "£13",
                "image": "Daiquiri.png"}
        ],
        "Mocktails": [
            {"name": "Virgin Mojito",
                "description": "A non-alcoholic twist on the classic mojito.",
                "price": "£8",
                "image": "Virgin Mojito.png"},

            {"name": "Cranberry Spritzer",
                "description": "Fizzy cranberry juice with a hint of lime.",
                "price": "£7",
                "image": "Cranberry Spritzer.png"},

            {"name": "Tropical Breeze",
                "description": "A blend of pineapple, mango, and orange juice.",
                "price": "£9",
                "image": "Tropical Breeze.png"},

            {"name": "Mint Lemonade",
                "description": "Fresh lemonade with a hint of mint.",
                "price": "£6",
                "image": "Mint Lemonade.png"},

            {"name": "Berry Bliss",
                "description": "Mixed berry juice with a touch of soda.",
                "price": "£8",
                "image": "Berry Bliss.png"},

            {"name": "Cucumber Cooler",
                "description": "Refreshing cucumber and lime soda.",
                "price": "£7",
                "image": "Cucumber Cooler.png"}
        ],
        "Wines": [
            {"name": "Chardonnay",
                "description": "A smooth and buttery white wine.",
                "price": "£18",
                "image": "Chardonnay.png"},

            {"name": "Pinot Noir",
                "description": "A light-bodied red wine with fruity notes.",
                "price": "£20",
                "image": "Pinot Noir.png"},

            {"name": "Rosé",
                "description": "A refreshing pink wine with floral hints.",
                "price": "£16",
                "image": "Rosé.png"},

            {"name": "Champagne",
                "description": "Sparkling wine perfect for celebrations.",
                "price": "£25",
                "image": "Champagne.png"}
        ],
        "Beers & Ciders": [
            {"name": "Craft IPA",
                "description": "A hoppy and aromatic craft beer.",
                "price": "£9",
                "image": "Craft IPA.png"},

            {"name": "Hard Apple Cider",
                "description": "Refreshing cider with a crisp apple flavor.",
                "price": "£8",
                "image": "Hard Apple Cider.png"},

            {"name": "Lager",
                "description": "A classic smooth and malty beer.",
                "price": "£7",
                "image": "Lager.png"},

            {"name": "Stout",
                "description": "Rich and creamy dark beer.",
                "price": "£10",
                "image": "Stout.png"}
        ],
        "Spirits": [
            {"name": "18-Year Single Malt Scotch",
                "description": "Aged to perfection with smoky undertones.",
                "price": "£25",
                "image": "18-Year Single Malt Scotch.png"},

            {"name": "GreyGoose Vodka",
                "description": "Ultra-smooth vodka, perfect for sipping.",
                "price": "£20",
                "image": "GreyGoose Vodka.png"},

            {"name": "Añejo Tequila",
                "description": "Aged tequila with caramel and oak notes.",
                "price": "£22",
                "image": "Añejo Tequila.png"},

            {"name": "Dark Rum",
                "description": "Rich and smooth with a hint of molasses.",
                "price": "£19",
                "image": "Dark Rum.png"},

            {"name": "Boatyard Gin",
                "description": "Classic London dry gin with herbal tones.",
                "price": "£18",
                "image": "Boatyard Gin.png"},

            {"name": "Louis 13 Cognac",
                "description": "Sophisticated brandy with deep flavors.",
                "price": "£28",
                "image": "Louis 13 Cognac.png"}
        ],
        "Hot Beverages": [
            {"name": "Espresso",
                "description": "Rich and bold single-shot espresso.",
                "price": "£5",
                "image": "Espresso.png"},

            {"name": "Earl Grey Tea",
                "description": "Fragrant black tea with hints of bergamot.",
                "price": "£4",
                "image": "Earl Grey Tea.png"},

            {"name": "Hot Chocolate",
                "description": "Creamy hot cocoa with whipped cream.",
                "price": "£6",
                "image": "Hot Chocolate.png"},

            {"name": "Cappuccino",
                "description": "Espresso topped with steamed milk foam.",
                "price": "£5",
                "image": "Cappuccino.png"},

            {"name": "Latte",
                "description": "Smooth and creamy espresso with milk.",
                "price": "£5",
                "image": "Latte.png"},

            {"name": "Green Tea",
                "description": "Light and refreshing antioxidant-rich tea.",
                "price": "£4",
                "image": "Green Tea.png"}
        ]
    }

    if request.method == 'POST':
        base_spirit = request.form.get('base-spirit', '').capitalize()
        mixer = request.form.get('mixer', '').replace('-', ' ').capitalize()
        garnish = request.form.get('garnish', '').replace('-', ' ').capitalize()

        if base_spirit and mixer and garnish:
            custom_drink = {
                "Base Spirit": base_spirit,
                "Mixer": mixer,
                "Garnish": garnish,
                "Message": "Enjoy your custom drink!"
            }
            return jsonify(custom_drink)
        else:
            return jsonify({"error": "All fields are required."}), 400
    return render_template('drinks.html', drinks_data=drinks_data)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Reservation details
        name = request.form.get('name')
        contact = request.form.get('contact')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')
        guests = request.form.get('guests')
        special_requests = request.form.get('special_requests', '')

        # Validate form fields
        if not all([name, contact, email, date, time, guests]):
            return jsonify({"message": "Please fill out all required fields.", "status": "error"}), 400

        try:
            reservation_date = datetime.strptime(date, "%Y-%m-%d").date()
            reservation_time = datetime.strptime(time, "%H:%M").time()
        except ValueError:
            return jsonify({"message": "Invalid date or time format.", "status": "error"}), 400

        # Check for reservation conflicts
        conflict = Reservation.query.filter_by(date=reservation_date, time=reservation_time).first()
        if conflict:
            return jsonify({"message": "This time slot is already booked. Please choose another time.", "status": "error"}), 400

        # Allocate a table
        table_number = allocate_table(reservation_date, reservation_time, guests)
        if not table_number:
            return jsonify({"message": "No tables available for this time slot.", "status": "error"}), 400

        # Save the reservation
        new_reservation = Reservation(
            name=name,
            contact=contact,
            email=email,
            date=reservation_date,
            time=reservation_time,
            guests=int(guests),
            table_number=table_number,
            special_requests=special_requests
        )
        db.session.add(new_reservation)
        db.session.commit()

        # Attempt to send a confirmation email
        try:
            msg = Message(
                subject="Table Reservation Confirmation - The Opulent Haven",
                recipients=[email]
            )
            msg.body = f"""
                Dear {name},

                Thank you for reserving a table at The Opulent Haven.

                Reservation Details:
                - Date: {reservation_date}
                - Time: {reservation_time}
                - Guests: {guests}
                - Table Number: {table_number}
                - Special Requests: {special_requests or "None"}

                We look forward to hosting you!

                Regards,
                The Opulent Haven Team
                """
            mail.send(msg)
            return jsonify({
                "message": f"Your table (Table #{table_number}) has been reserved successfully! A confirmation email has been sent.",
                "status": "success"
            }), 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return jsonify({
                "message": "Reservation successful, but the confirmation email couldn't be sent. Please contact us if needed.",
                "status": "error"
            }), 500

    return render_template('contact.html')

# Reservations
@app.route('/reservations')
def reservations():
    all_reservations = Reservation.query.order_by(Reservation.date, Reservation.time).all()
    return render_template('reservations.html', reservations=all_reservations)


# Reservations Table Allocation System
def allocate_table(date, time, guests):
    existing_reservations = Reservation.query.filter_by(date=date).all()
    allocated_tables = {res.table_number for res in existing_reservations}

    for table in range(1, 61):  # Total 60 tables
        if table not in allocated_tables:
            return table
    return None  # No table available

# Reservations Reminder
def send_reminder_emails():
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).isoformat()
    reservations = Reservation.query.filter_by(date=tomorrow).all()

    for reservation in reservations:
        msg = Message(
            subject="Reminder: Your Reservation at The Opulent Haven",
            recipients=[reservation.email],
        )
        msg.body = f"""
        Dear {reservation.name},

        This is a friendly reminder of your reservation at The Opulent Haven:

        Date: {reservation.date}
        Time: {reservation.time}
        Guests: {reservation.guests}

        We look forward to hosting you.

        Best regards,
        The Opulent Haven
        """
        mail.send(msg)

# Schedule the reminder emails
scheduler = BackgroundScheduler()
scheduler.add_job(send_reminder_emails, 'cron', hour=9, minute=0)
scheduler.start()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    # Check if the email is already subscribed
    existing_subscriber = Subscriber.query.filter_by(email=email).first()
    if existing_subscriber:
        return jsonify({"message": "You are already subscribed!", "status": "error"}), 200

    # Add new subscriber to the database
    new_subscriber = Subscriber(email=email)
    db.session.add(new_subscriber)
    db.session.commit()

    # Send a Thank You email
    try:
        msg = Message(
            subject="Welcome to The Opulent Haven",
            recipients=[email]
        )
        msg.body = f"""
        Dear Member,

        Thank you for subscribing to The Opulent Haven's newsletter. We look forward to keeping you updated with our latest events, offers, and news.

        Warm regards,
        The Opulent Haven Team
        """
        mail.send(msg)
        return jsonify(
            {"message": "Thank you for subscribing! A confirmation email has been sent.", "status": "success"}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({
                           "message": "Subscription successful, but we couldn't send the confirmation email. Please contact us if needed.",
                           "status": "error"}), 500

@app.route('/subscribers')
def subscribers():
    all_subscribers = Subscriber.query.order_by(Subscriber.subscribed_at.desc()).all()
    return render_template('subscribers.html', subscribers=all_subscribers)


if __name__ == '__main__':
    app.run(debug=True)
