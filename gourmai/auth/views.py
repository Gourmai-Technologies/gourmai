import os
from werkzeug.urls import urlencode

# Flask #
from flask import render_template, redirect, request, url_for, g, Response, session, current_app, jsonify

from flask_login import current_user, login_user, logout_user

# Gourmai #
from gourmai import db, login_manager
from gourmai.auth import blueprint 
from gourmai.auth.forms import LoginForm, CreateAccountForm
from gourmai.auth.models import Users
from gourmai.auth.util import verify_pass, generate_verification_link, generate_verification_token

# Flask mailman #
from flask_mailman import Mail, EmailMessage

@blueprint.route('/')
def route_default():
    return redirect(url_for('auth_bp.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    nologin = False
    
    # Initialize the login form
    login_form = LoginForm()

    # Check if the form is submitted and valid
    if login_form.validate_on_submit():
        
        username = login_form.username.data.lower()
        password = login_form.password.data
        
        # Try to find the user by username
        user = Users.query.filter_by(username=username).first()

        # Check if user exists and the password is correct
        if user is None or not verify_pass(password, user.password):
            # If login details are incorrect, reload the login page with a message
            return render_template(
                'auth/login.html',
                error_message='Wrong user or password',
                form=login_form,
                message=nologin
            )
        else:
            if user.email_verified:
                print(login_form.remember_me.data)

                # Log in the user and remember their login state if 'remember me' is checked
                login_user(user, remember=login_form.remember_me.data) 
                
                # Redirect to the next page if it's safe; otherwise, redirect to the home page
                next_page = request.args.get('next')
                if not next_page or urlencode(next_page).netloc != '':
                    next_page = url_for('home_bp.index')
                return redirect(next_page)

            else:
                return render_template(
                    'auth/login.html',
                    error_message='Please verify your email.',
                    form=login_form,
                    message=nologin
                    )


@blueprint.route('/register', methods=['GET', 'POST'])
def register():

    # Check if the current user is already authenticated (logged in)
    if current_user.is_authenticated:
    
        # Redirect the user to the home page if already logged in
        return redirect(url_for('home_bp.index'))

    # Initialize the account creation form # 
    create_account_form = CreateAccountForm()

    # Validate form data on form submission # 
    if create_account_form.validate_on_submit():

        username = create_account_form.username.data.lower()
        input_email = create_account_form.email.data.lower()

        # Check if username and email already exists in the database
        check_user = Users.query.filter_by(username=username).first()
        email = Users.query.filter_by(email=input_email).first()
        
        if check_user:
            return render_template(
                'auth/register.html', 
                error_message='Username already registered',form=create_account_form
                )

        if email:
            return render_template(
                'auth/register.html',
                error_message='Email already registered',
                form=create_account_form
                )

        # Flask_Mail suspended me for some reason. # Ill leave this feature out for now .# 
        # Generate verification token
        # verification_token = generate_verification_token()
        # verification_link = generate_verification_link(verification_token)
        
        # message = EmailMessage(
        #     f"Email Verifacation",
        #     f"Please click the link below to verify your email address.\n\n"
        #     f"{verification_link}\n\n",
        #     "gourmai_feedback@fastmail.com",
        #     [f"{input_email}"]

        # )
        # message.send()

        # If user and email are unique:
        # Create a new user object #
        user = Users(
            username=username, 
            email=input_email, 
            password=create_account_form.password.data,

            )

        # Add the new user object to the database #
        db.session.add(user)

        # Commit the changes to the database #
        db.session.commit()
        logout_user()

        login_form = LoginForm()

        # Display a success message and clear the form #
        return render_template(
            'auth/login.html',
            success_message='Account Created',
            form=login_form
            )
    
    # else form fails #
    else:
        return render_template('auth/register.html', form=create_account_form)


@blueprint.route('/<verification_token>')
def verify_email(verification_token):

    # Initialize the login form
    login_form = LoginForm()

    # Find the user with the given verification token
    user = Users.query.filter_by(verification_token=verification_token).first()
    
    
    if user:
        # Mark the user's email as verified
        user.email_verified = True

        # Remove the verification token
        user.verification_token = None

        # Commit the changes to the database
        db.session.commit()

        # Display a success message and clear the form #
        return render_template(
            'auth/login.html',
            success_message='Email Verified',
            form=login_form
            )

    else:
        print(f"failed to find verification token in user! {user}")
        return render_template(
            'auth/login.html',
            success_message='Email Failed Verifiction',
            form=login_form
            )


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))


@blueprint.before_app_request
def pre_operations(): 

    #ALL STATIC REQUESTS BYPASS!!!
    if request.endpoint == 'static':
        return

    #REDIRECT http -> https
    if 'DYNO' in os.environ:
        current_app.logger.critical("DYNO ENV !!!!")
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
            
    g.policyCode = -1 #SET DEFAULT INDEPENDENTLY TO WRAPPER
    policyCode = session.get("cookie-policy")
    #possible values Null -> no info, 0 -> Strict, 1 -> Minimal, 
    #                                 2 -> Analisys, 3 -> All
    if policyCode !=None:
        g.policyCode = policyCode


@blueprint.route('/ajcookiepolicy/',methods=('GET', 'POST'))
def ajcookiepolicy():
    #DECIDE COOKIE PREFERENCE STRATEGY
    if request.method == 'POST':
        data = request.json
        btn_name = data['btnselected']
        checkbox_analysis = data['checkboxAnalysis']
        checkbox_necessary = data['checkboxNecessary']
        if btn_name == 'btnAgreeAll':
            session['cookie-policy'] = 3
        elif btn_name == 'btnAgreeEssential':
            session['cookie-policy'] = 1
        elif btn_name == 'btnSaveCookieSettings':
            session['cookie-policy'] = 0 #default
            if checkbox_necessary and not checkbox_analysis:
                session['cookie-policy'] = 1
            elif checkbox_analysis and not checkbox_necessary:
                #never happends if main checkbox disabled!
                session['cookie-policy'] = 2
            elif checkbox_necessary and checkbox_analysis:
                session['cookie-policy'] = 3

    return Response(status=204)


# Errors #
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('errorpages/error403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errorpages/error403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errorpages/error404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errorpages/error500.html'), 500




##########################################################################################
# API #
##########################################################################################


@blueprint.route('/api/get_user_data', methods=['GET', 'POST'])
def get_user_data():

    user_id = request.args.get('user_id')
    # Query DB #
    user = Users.query.filter_by(id=user_id).first()
    
    if user:
        # Send JSON to client #
        return jsonify(
            {
                'username': user.username, 
                'email': user.email, 
                'recipes_generated_counter': user.recipes_generated_counter, 'saved_recipes_counter': user.saved_recipes_counter, 
                'shared_recipes_counter': user.shared_recipes_counter,

                'dietary_restrictions' : user.dietary_restrictions,
                'allergens' : user.allergens,
            })
    else:
        # Handle error #
        return jsonify({'error': 'User not found'}), 404


@blueprint.route('/api/login', methods=['POST'])
def api_login():
    # Parse JSON data from the request
    data = request.json

    # Extract username and password from the JSON data
    username = data.get('username').lower()
    print(username)
    password = data.get('password')
    print(password)

    # Try to find the user by username
    user = Users.query.filter_by(username=username).first()

    # Check if user exists and the password is correct
    if user is None or not verify_pass(password, user.password):
        # If login details are incorrect, return a JSON response with an error message
        return jsonify({'error': 'Wrong email or password'}), 401

    # Check if the user's email is verified
    if not user.email_verified:
        return jsonify({'error': 'Please verify your email'}), 401

    # Return a JSON response with a success message
    user_id = user.id
    return jsonify({'message': 'Login successful', 'user_id': user_id})


@blueprint.route('/api/register', methods=['POST'])
def api_register():
    # Parse JSON data from the request
    data = request.json

    # Check if username, email, and password are provided
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    # Extract username, email, and password from the JSON data
    username = data['username'].lower()
    email = data['email'].lower()
    password = data['password']

    print("details", username , email, password)

    # Check if username and email already exist in the database
    existing_user = Users.query.filter_by(username=username).first()
    existing_email = Users.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    if existing_email:
        return jsonify({'error': 'Email already registered'}), 409

    # # Generate verification token
    # verification_token = generate_verification_token()
    # verification_link = generate_verification_link(verification_token)

    # message = EmailMessage(
    #     f"Email Verification",
    #     f"Please click the link below to verify your email address.\n\n"
    #     f"{verification_link}\n\n",
    #     "gourmai_feedback@fastmail.com",
    #     [f"{email}"]
    # )
    # message.send()

    # Create a new user object
    user = Users(
        username=username,
        email=email,
        password=password,

    )

    # Add the new user object to the database
    db.session.add(user)

    try:
        # Commit the changes to the database
        db.session.commit()
    except Exception as e:
        # Rollback the transaction if an error occurs
        db.session.rollback()
        return jsonify({'error': 'Failed to register user'}), 500
    user_id = user.id
    return jsonify({'message': 'Registration successful.', 'user_id': user_id}), 201


@blueprint.route('/api/increment-recipes-generated-counter/<user_id>', methods=['PUT'])
def api_increment_counter(user_id):

    user = Users.query.filter_by(id=user_id).first()

    if user: 
        user.increment_recipes_generated_counter(user_id)

    return jsonify({'message': 'Counter updated successfully'}), 200