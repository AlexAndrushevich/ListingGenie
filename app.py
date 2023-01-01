from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
import requests
from wtforms.validators import DataRequired, InputRequired, Email,Length, email_validator
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import stripe

# Main App Defintion

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///listrdb.sqlite3'
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MJgGlBehDTnUvK0oVKvrnSkXEwhKqzC0pxC9LH6nMs39jyIAnslJYSZhakbtgJrmzvD4joMntF0CgAXrsLAnMt500zILRnGRz'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MJgGlBehDTnUvK0x5egmgKHDmV6BJ11qdfoTGTnMVeKL6AdlS76kIVVNA0OSKRjiNOV3sF95CMxGH7rc9Oga7Gk00mIe7Qp5T'

stripe.api_key =app.config['STRIPE_SECRET_KEY']
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

YOUR_DOMAIN = 'http://localhost:4242'



#Database Class Definition

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    token_balance = db.Column(db.Integer)
    listings = db.relationship('ListingDescriptions', backref='user')

class ListingDescriptions(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text(), unique=True, nullable=False)
    address =db.Column(db.String(50))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# WTFORMS Class Definition

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5,max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])
    remember = BooleanField('Remember Me')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=5,max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email!'), Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8,max=80)])


class ListrForm(FlaskForm):
    numberOfRooms = StringField("Number of Rooms")
    numberOfFloors = StringField("Number of Floors")
    numberOfBedrooms = StringField("Number of Bedrooms")
    numberOfSquareFeetOnPlot = StringField("Number of Square Feet on Plot")
    numberOfBuiltSquareFeet = StringField("Number of Built Square Feet")
    houseCondition = StringField("House Condition")
    readinessToSell = StringField("Readiness to Sell")
    listingAddress = StringField("Listing Address", validators=[InputRequired()])
    listingPrice = StringField("Listing Price")
    listingPropertyHighlights = StringField("Listing Property Highlights")
    listingRentLicenseAvailable = StringField("Is the rent license available?")
    listingIdealUse = StringField("What's the ideal use?")
    listingOpenHouseDates = StringField("Select dates for open house")
    listingAgentContactEmail = StringField("Agent Contact Email")
    listingKeyWordsList = StringField("Priority Keywords")
    listingToneOfVoice = StringField("Tone of voice: fomal, coloquial...")

    submit = SubmitField("Submit") 

### ROUTES!!!
### ROUTES!!! 
### ROUTES!!!

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    numberOfRooms= None
    numberOfFloors= None
    numberOfBedrooms= None
    numberOfSquareFeetOnPlot= None
    numberOfBuiltSquareFeet= None
    houseCondition= None
    readinessToSell= None
    listingAddress= None
    listingPrice= None
    listingPropertyHighlights= None
    listingRentLicenseAvailable= None
    listingIdealUse= None
    listingOpenHouseDates= None
    listingAgentContactEmail= None
    listingKeyWordsList= None
    listingToneOfVoice= None

    form = ListrForm()
    # CHECK TOKEN BALANCE
    # WARNING! == 0 is TEST BEHAVIOUR, CHANGE BEFORE PRODUCTION
    # WARNING! 
    # WARNING! 
    if current_user.token_balance == 0:
#Validate form
    
        if form.validate_on_submit():
            numberOfRooms= form.numberOfRooms.data + "rooms"
            form.numberOfRooms.data = ''
            numberOfFloors= form.numberOfFloors.data+ "floors"
            form.numberOfFloors.data = ''
            numberOfBedrooms= form.numberOfBedrooms.data+ "bedrooms"
            form.numberOfBedrooms.data = ''
            numberOfSquareFeetOnPlot= form.numberOfSquareFeetOnPlot.data+ "square feet plot."
            form.numberOfSquareFeetOnPlot.data=''
            numberOfBuiltSquareFeet= form.numberOfBuiltSquareFeet.data+ "built square feet."
            form.numberOfBuiltSquareFeet.data=''
            houseCondition= form.houseCondition.data+ "house conditio.,"
            form.houseCondition.data=''
            readinessToSell= form.readinessToSell.data+ "to sell."
            form.readinessToSell.data=''
            listingAddress= form.listingAddress.data+ "listing address."
            form.listingAddress.data=''
            listingPrice= form.listingPrice.data+ "price."
            form.listingPrice.data=''
            listingPropertyHighlights= form.listingPropertyHighlights.data
            form.listingPropertyHighlights.data=''
            listingRentLicenseAvailable= form.listingRentLicenseAvailable.data
            form.listingRentLicenseAvailable.data=''
            listingIdealUse= form.listingIdealUse.data+ "is the ideal use,"
            form.listingIdealUse.data=''
            listingOpenHouseDates= form.listingOpenHouseDates.data
            form.listingOpenHouseDates.data=''
            listingAgentContactEmail= form.listingAgentContactEmail.data
            form.listingAgentContactEmail.data=''
            listingKeyWordsList= form.listingKeyWordsList.data
            form.listingKeyWordsList.data=''
            listingToneOfVoice= form.listingToneOfVoice.data+ "tone of the text"
            form.listingToneOfVoice.data=''
            megaprompt = "Generate a selling real-estate listing based on the following characterstics:"+numberOfRooms+numberOfBuiltSquareFeet+numberOfFloors+numberOfBedrooms+numberOfSquareFeetOnPlot+numberOfBuiltSquareFeet+houseCondition+readinessToSell+listingAddress+listingPropertyHighlights+listingRentLicenseAvailable+listingIdealUse+listingOpenHouseDates+listingAgentContactEmail+listingKeyWordsList+listingToneOfVoice
        # Send the API request to ChatGPT
            chatgpt_url = 'https://api.openai.com/v1/completions'
            api_key = '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'
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
            data = {'prompt': megaprompt, 'model': 'text-davinci-003', 'temperature':1,'max_tokens':1000}
            response = requests.post(chatgpt_url, headers=headers, json=data)
            response_text = response.json()['choices'][0]['text']
            new_listing = ListingDescriptions(content=response_text,owner_id = current_user.id, address=listingAddress)
            db.session.add(new_listing)
            db.session.commit()
        # Render the response page with the ChatGPT response
            return render_template('response.html', response=response_text)
    else:
        flash('Insufficient tokens, please add more')
    return render_template('dashboard.html', form=form, token_balance = current_user.token_balance)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user,remember=form.remember.data)
                return redirect(url_for('dashboard'))

        flash('Wrong user or password!')
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method ='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, token_balance = 0)
        db.session.add(new_user)
        db.session.commit()
        flash('New User Created')
        return redirect(url_for('dashboard'))
    return render_template('signup.html', form=form)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', name=current_user.username, token_balance = current_user.token_balance )

@app.route('/listings')
@login_required
def listings():
    listings = ListingDescriptions.query.filter(ListingDescriptions.owner_id==current_user.id).all()
    return render_template('listings.html', name=current_user.username, token_balance = current_user.token_balance, listings=listings)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/training', methods=['GET', 'POST'])
def training():
    return render_template('tutorial.html')

@app.route('/tutorial', methods=['GET', 'POST'])
def tutorial():
    return render_template('tutorial.html')
@app.route('/pricing', methods=['GET'])
def pricing():
    return render_template('pricing.html')
@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    # Provide the exact Price ID of the product
                    'price': 'price_1MKK4lBehDTnUvK0NOsluJFX',
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('purchaseConfirmation', _external = True),
            cancel_url=url_for('home', _external = True),
            automatic_tax={'enabled': True},
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303 )

@app.route('/purchaseconfirmation')
@login_required
def purchaseConfirmation():

    return render_template('purchaseconfirmation.html')


@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    return render_template('checkout.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=4242, debug=True)
    

