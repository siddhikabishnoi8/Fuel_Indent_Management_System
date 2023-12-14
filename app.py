import pymysql
import datetime
from flask import Flask, abort, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import send_file
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, FuelIndent, Supplier, User

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'c72b1edfea6f2ca0fd9a972493f97830'

# Initialize the extension
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%40shish209e@localhost/fuel_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the Flask app
db.init_app(app)

# Routes
@app.route("/")
def home():
    indents = FuelIndent.query.all()
    return render_template("index.html", indents=indents)

@app.route("/new", methods=["GET", "POST"])
@login_required
def new_indent():
    suppliers = Supplier.query.all()
    if request.method == "POST":
        # Get form data and add to database
        nameplate = request.form.get("nameplate")
        fuel_type = request.form.get("fuel_type")
        quantity = request.form.get("quantity")
        quality = request.form.get("quality")
        supplier_id = request.form.get("supplier_id")
        price = request.form.get("price")
        date = request.form.get("date")
        indent = FuelIndent(nameplate=nameplate, fuel_type=fuel_type, quantity=quantity, quality=quality, supplier_id=supplier_id, price=price, date=date)
        db.session.add(indent)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_indent.html", suppliers=suppliers)

@app.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_indent(id):
    indent = FuelIndent.query.get_or_404(id)
    suppliers = Supplier.query.all()
    if request.method == "POST":
        # Get form data and update the database record
        indent.nameplate = request.form.get("nameplate")
        indent.fuel_type = request.form.get("fuel_type")
        indent.quantity = request.form.get("quantity")
        indent.quality = request.form.get("quality")
        indent.supplier_id = request.form.get("supplier_id")
        indent.price = request.form.get("price")
        indent.date = request.form.get("date")
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update_indent.html", indent=indent, suppliers=suppliers)

@app.route("/delete/<int:id>", methods=["POST"])
@login_required
def delete_indent(id):
    indent = FuelIndent.query.get_or_404(id)
    db.session.delete(indent)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/add_supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        name = request.form.get('name')
        proximity = request.form.get('proximity')
        reliability = request.form.get('reliability')
        pricing = request.form.get('pricing')
        new_supplier = Supplier(name=name, proximity=proximity, reliability=reliability, pricing=pricing)
        db.session.add(new_supplier)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_supplier.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists! Choose a different one."
        user = User(username=username, password=password)  # In a real-world scenario, you'd hash the password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Again, in a real-world scenario, you'd check a hashed password
            login_user(user)
            return redirect(url_for('home'))
        return "Invalid credentials. Try again."
    return render_template('login.html')

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        current_user.name = request.form.get("name")
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("edit_profile.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        # Update the user's password in the database
        current_user.password = request.form.get("new_password")
        db.session.commit()
        return redirect(url_for("profile"))
    return render_template("change_password.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/protected_page')
@login_required
def protected_page():
    return "This page is only for logged-in users!"

@app.route("/search", methods=["POST"])
@login_required
def search_indents():
    search_nameplate = request.form.get("search_nameplate")
    indents = FuelIndent.query.filter(FuelIndent.nameplate.ilike(f"%{search_nameplate}%")).all()
    return render_template("index.html", indents=indents)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/print_slip/<int:id>')
@login_required
def print_slip(id):
    indent = FuelIndent.query.get_or_404(id)
    supplier = Supplier.query.get_or_404(indent.supplier_id)

    # Create the PDF object
    pdf_path = f"static/slip_{indent.nameplate}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)

    # Creating the data for the table
    data = [
        ['Nameplate', indent.nameplate],
        ['Fuel Type', indent.fuel_type],
        ['Quantity', indent.quantity],
        ['Quality', indent.quality],
        ['Price', indent.price],
        ['Date', indent.date.strftime('%Y-%m-%d')],
        ['Supplier Name', supplier.name],
        ['Supplier Proximity', supplier.proximity],
        ['Supplier Reliability', supplier.reliability],
        ['Supplier Pricing', supplier.pricing]
    ]

    # Creating the table
    table = Table(data)
    style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])

    table.setStyle(style)

    # Building the PDF
    elements = [table]
    doc.build(elements)

    return send_file(pdf_path, as_attachment=True)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))  # redirect if not admin
    users = User.query.all()
    suppliers = Supplier.query.all()
    indents = FuelIndent.query.all()
    return render_template('admin_dashboard.html', users=users, suppliers=suppliers, indents=indents)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password and user.is_admin:
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        return "Invalid credentials or not an admin. Try again."
    return render_template('admin_login.html')

@app.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists! Choose a different one."
        user = User(username=username, password=password, is_admin=True)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin_register.html')

@app.route('/admin/users')
@login_required
def manage_users():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template('manage_users.html', users=users)

@app.route('/admin/suppliers')
@login_required
def manage_suppliers():
    if not current_user.is_admin:
        abort(403)
    suppliers = Supplier.query.all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

@app.route('/admin/indents')
@login_required
def manage_indents():
    if not current_user.is_admin:
        abort(403)
    indents = FuelIndent.query.all()
    return render_template('manage_indents.html', indents=indents)

@app.route('/update_supplier/<int:id>', methods=['GET', 'POST'])
@login_required
def update_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    if request.method == 'POST':
        supplier.name = request.form.get('name')
        supplier.proximity = request.form.get('proximity')
        supplier.reliability = request.form.get('reliability')
        supplier.pricing = request.form.get('pricing')
        db.session.commit()
        return redirect(url_for('manage_suppliers'))
    return render_template('update_supplier.html', supplier=supplier)

@app.route('/delete_supplier/<int:id>', methods=['POST'])
@login_required
def delete_supplier(id):
    supplier = Supplier.query.get_or_404(id)
    db.session.delete(supplier)
    db.session.commit()
    return redirect(url_for('manage_suppliers'))

@app.route('/delete_user/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.is_admin:
        abort(403)  # Forbidden access if not an admin
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('manage_users'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
