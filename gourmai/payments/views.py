import os 
import json


# Flask #
from flask_login import current_user
from flask import request, render_template, g, app, session, jsonify,redirect, url_for

# Gourmai #
from gourmai.payments import blueprint
from gourmai.auth.models import Users
from gourmai.auth.forms import LoginForm
from gourmai.payments.utils import generate_payment_token

# Stripe #
import stripe

# Init #
stripe.api_key = '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'

endpoint_secret = "pk_live_51OtCyxP27ZWoiqFWhM2JrRFXiGRvsaJ1XBogzj04sgpyoNCkPVh2atemJDYl3BRCDfzgqElWMghla1rq25RilbIh00gvMRiCnD"

@blueprint.route('/payments', methods=['GET'])
def payments():
    return render_template('payments/payment.html')


@blueprint.route('/pricing', methods=['GET'])
def pricing():
    return render_template('payments/pricing.html')


@blueprint.route('/create-checkout-session', methods=['GET'])
def create_checkout_session():
    
    checkout_session = stripe.checkout.Session.create(
        success_url=url_for('payments_bp.add_tokens', _external=True),
        cancel_url=url_for('payments_bp.pricing', _external=True),
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1OtdBQP27ZWoiqFWvxH8jg11',
            'quantity': 1,
        }],
        mode='payment',
    )
    
    # Store the checkout session ID in the session for retrieval later #
    session['checkout_session_id'] = checkout_session.id
    session['client_reference_id'] = checkout_session.client_reference_id

    return redirect(checkout_session.url)

@blueprint.route('/create-donation-checkout-session', methods=['GET'])
def create_donation_checkout_session():
    
    checkout_session = stripe.checkout.Session.create(
        success_url=url_for('home_bp.index', _external=True),
        cancel_url=url_for('home_bp.index', _external=True),
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1Ovm3oP27ZWoiqFWcEqj0XAG',
            'quantity': 1,
        }],
        mode='payment',
    )


    return redirect(checkout_session.url)


@blueprint.route('/add-tokens', methods=['GET'])
def add_tokens():

    if current_user.is_authenticated:
        # Get the Checkout Session ID from the session #
        checkout_session_id = session.get('checkout_session_id')

        if checkout_session_id:
            # Verify the payment status with Stripe using the Checkout Session ID #
            checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)  
        else:
            # Handle failed or unauthorized payment (e.g., redirect to error page)
            return render_template(
                'payments/pricing.html'
            )

        # Check if the Checkout Session is completed and successful #
        if checkout_session.payment_status == 'paid':

            # Empty the session ID #
            session['checkout_session_id'] = ''

            # Add 100 tokens to user account #
            Users.add_tokens(current_user.id, 100)
            return render_template(
                'home/index.html',
                message="Tokens have been added to your account."

            )

        else:   # Handle failed or unauthorized payment (e.g., redirect to error page)
            return render_template(
                'payments/pricing.html'
            )
      
    else: # User not logged in #  
        # Initialize the login form
        login_form = LoginForm()
        return render_template(
            'auth/login.html',
            form=login_form,
            )