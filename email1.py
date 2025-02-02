# # pip install sendgrid python-dotenv
# from dotenv import load_dotenv
# load_dotenv()

# import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail

# message = Mail(
#     from_email='safebuddy2025@gmail.com',
#     to_emails='asgarfataymamode@gmail.com',
#     subject='Emergency: Your friend is in danger',
#     html_content='<strong>Your friend is at NYUAD for more than 30 min with no movement at 2 am</strong>')
# try:
#     sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
#     response = sg.send(message)
#     print(f"Email sent! Status Code: {response.status_code}")
#     print(response.body)
#     print(response.headers)
# except Exception as e:
#     print(f"Error: {e}")
import os
import time
import threading
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# Load environment variables first
load_dotenv()

def send_email():
    """Send email with detailed error handling"""
    try:
        api_key = os.getenv("SENDGRID_API_KEY")
        if not api_key or not api_key.startswith("SG."):
            raise ValueError("Invalid or missing SendGrid API key")

        message = Mail(
            from_email='safebuddy2025@gmail.com',
            to_emails='hariharanjanardhanan2@gmail.com',
            subject='Reminder Email',
            html_content='<strong>This is an automated email sent after 1 minute.</strong>'
        )
        
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        
        print(f"\nEmail sent successfully!\nStatus Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")

    except Exception as e:
        print(f"\nFailed to send email:\n{str(e)}")
        if hasattr(e, 'body') and e.body:
            print(f"Error details: {e.body}")

def main():
    """Main function with cancellation feedback"""
    print("Starting email scheduler...")
    print(f"Current directory: {os.getcwd()}")
    print(f"API Key exists: {bool(os.getenv('SENDGRID_API_KEY'))}")
    
    email_timer = threading.Timer(60.0, send_email)
    email_timer.daemon = True  # Allow program to exit while timer runs
    email_timer.start()

    print("\nPress Enter to cancel (you have 60 seconds)...")
    try:
        if input().strip() == "":
            email_timer.cancel()
            print("\nCancellation confirmed. Email will not be sent.")
        else:
            print("\nInvalid input. Email will be sent as scheduled.")
    except KeyboardInterrupt:
        email_timer.cancel()
        print("\nProcess interrupted. Email cancelled.")

if __name__ == "__main__":
    main()
    # Keep program running while timer is active
    time.sleep(70)  # Wait 10 seconds longer than timer duration
