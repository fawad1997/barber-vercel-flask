from flask import render_template, request, jsonify, redirect, url_for
from flask_login import UserMixin, login_user, login_required, logout_user
from app.models import db, Customer, Feedback
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from app import app, db

# app = Flask(__name__)
#
# app.config['SECRET_KEY'] = 'e5f3458721344b349ab9c7d9a242e4e9'
#
#
# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///queue.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

# Configure login manager
login_manager = LoginManager()
login_manager.init_app(app)


# Dummy user model for demonstration
class User(UserMixin):
    id = 1
    username = "admin"
    password = "password"  # You should store hashed passwords in real applications


@login_manager.user_loader
def load_user(user_id):
    if user_id == "1":
        return User()
    return None


# Route for login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "password":
            user = User()
            login_user(user)
            return redirect(url_for('admin_page'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')


# Route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Route to serve the customer-facing page
@app.route('/')
def customer_page():
    return render_template('index.html')


# API to join the waitlist
@app.route('/join_queue', methods=['POST'])
def join_queue():
    phone_number = request.form.get('phone_number')

    if phone_number:
        # Calculate position
        position = Customer.query.count() + 1
        new_customer = Customer(phone_number=phone_number, queue_position=position)
        db.session.add(new_customer)
        db.session.commit()

        return jsonify({"queue_number": position, "estimated_wait_time": position * 10})  # Simple 10 mins per customer
    return jsonify({"error": "Phone number is required"}), 400


# API to get the updated queue status
@app.route('/queue_status', methods=['GET'])
def queue_status():
    queue = Customer.query.order_by(Customer.queue_position).all()
    return jsonify([{"phone_number": c.phone_number, "queue_position": c.queue_position} for c in queue])


# Admin Page
@app.route('/admin')
@login_required
def admin_page():
    queue = Customer.query.order_by(Customer.queue_position).all()
    return render_template('admin.html', queue=queue)


# Admin API to remove a customer from the queue
@app.route('/remove_customer/<int:id>', methods=['POST'])
def remove_customer(id):
    customer = Customer.query.get(id)
    if customer:
        db.session.delete(customer)
        db.session.commit()
        # Adjust the queue positions of other customers
        customers_to_update = Customer.query.filter(Customer.queue_position > customer.queue_position).all()
        for c in customers_to_update:
            c.queue_position -= 1
        db.session.commit()
    return redirect(url_for('admin_page'))


# Admin API to update the estimated wait time (future feature)
@app.route('/update_wait_time/<int:id>', methods=['POST'])
def update_wait_time(id):
    # Placeholder for updating estimated wait time, to be implemented later
    pass


# Route to serve the feedback page
@app.route('/feedback')
def feedback_page():
    return render_template('feedback.html')


# API to submit feedback
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    phone_number = request.form.get('phone_number')
    rating = request.form.get('rating')
    comments = request.form.get('comments')

    if phone_number and rating:
        feedback = Feedback(phone_number=phone_number, rating=int(rating), comments=comments)
        db.session.add(feedback)
        db.session.commit()
        return redirect(url_for('feedback_page', success=True))
    return jsonify({"error": "Phone number and rating are required"}), 400

# Route for admin to view customer feedback
@app.route('/admin/feedback')
@login_required
def view_feedback():
    feedback_list = Feedback.query.order_by(Feedback.id.desc()).all()
    return render_template('view_feedback.html', feedback=feedback_list)


if __name__ == '__main__':
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    app.run(debug=True)