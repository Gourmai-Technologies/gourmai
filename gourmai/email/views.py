from gourmai.email import blueprint

# Flask mailman #
from flask_mailman import Mail, EmailMessage
from flask import render_template, redirect, request, url_for, g, Response, session, current_app, send_from_directory, flash, app, jsonify

from gourmai.email.forms import messageForm, ContactUsForm


@blueprint.route('/contact_us', methods=['POST'])
def contact_us():
    
    if request.method == 'POST':
        # Parse the form data
        form_data = request.form
        name = form_data.get('name')
        email = form_data.get('email')
        subject = form_data.get('subject')
        message_body = form_data.get('message')  

        # Create the form instance with the request data
        contact_form = ContactUsForm(request.form)

        if contact_form.validate_on_submit():

            message = EmailMessage(
                f"Contact Us Submission: {subject}",
                f"Name:\n{name}\n\nEmail:\n{email}\n\nMessage:\n{message_body}",

                # Sender #
                "feedback@gourmai.co.uk",

                # Recipients #
                ["cody@gourmai.co.uk", "adrian@gourmai.co.uk"]
            )

            try:
                message.send()
                print(f"Email sent to: gourmai.feedback@gmail.com")
                response = {'message':'Mail has been sent. Your feedback is much appreciated.'}
                return jsonify(response)

            except Exception as e:        
                print("Email not sent")  
                #response = {'message':'Mail has failed to send.'}
                return jsonify(response)
        
        # If form validation fails, return form errors
        print(contact_form.errors)
        return jsonify({'message': contact_form.errors})


@blueprint.route('/send-message', methods=['POST'])
def send_message():
    
    if request.method == 'POST':
        # Parse the form data
        form_data = request.form
        message_content = form_data.get('message')

        print(message_content)

        # Create the form instance with the request data
        message_form = messageForm(request.form)

        if message_form.validate_on_submit():
            print('form valid')
            message = EmailMessage(
                f"Message from user:",
                f"{message_content}"
                
                # Sender #
                "feedback@gourmai.co.uk",

                # Recipients #
                ["gourmai.feedback@gmail.com"]
            )

            try:
                message.send()
                print(f"Email sent to: gourmai.feedback@gmail.com")
                response = {'message':'Mail has been sent. Your feedback is much appreciated.'}
                return jsonify(response)

            except Exception as e:        
                print("Email not sent")  
                #response = {'message':'Mail has failed to send.'}
                return jsonify(response)
        
        # If form validation fails, return form errors
        print(message_form.errors)
        return jsonify({'message': message_form.errors})


@blueprint.route('/api/send-message/<message>', methods=['POST'])
def api_send_message(message):
    
    # Build message object #
    message = EmailMessage(

        # Message Content #
        f"Message from user: {message}",

        # Sender #
        "safe.water3367@fastmail.com",

        # Recipients #
        ["cody@gourmai.co.uk"]
    )

    # Attempt sending #
    try:
        message.send()
    # Handle error #
    except Exception as e:
        print(f"error sending email: {e}")
        response = {'success': False, 'message': 'Mail has failed to send.'}
        return jsonify(response), 500
    response = {'success': True, 'message': 'Mail has been sent. Your feedback is much appreciated.'}
    return jsonify(response), 200


