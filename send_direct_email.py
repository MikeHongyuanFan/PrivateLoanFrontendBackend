import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "fanhongyuan897@gmail.com"
password = "oytebasqthbbjvdd"
receiver_email = "fanhongyuan897@gmail.com"

# Create message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Test Email - Email Config Updated"

# Email content
body = """
Hello,

This is a test email to confirm that the email configuration has been updated successfully.

Best regards,
Your Application
"""
message.attach(MIMEText(body, "plain"))

try:
    # Create server connection
    server = smtplib.SMTP(smtp_server, port)
    server.starttls()  # Secure the connection
    
    # Login
    server.login(sender_email, password)
    
    # Send email
    text = message.as_string()
    server.sendmail(sender_email, receiver_email, text)
    print("Email sent successfully!")
    
    # Close connection
    server.quit()
except Exception as e:
    print(f"Error sending email: {e}")
