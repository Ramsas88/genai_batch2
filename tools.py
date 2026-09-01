from langchain.tools import tool

# send email, activate course, password reset, search flights, hotel booking, etc

@tool(description="use this tool to send email after completing the interview")
def send_email(hr_email: str, subject: str, email_body: str):
    print("interview result email sent")
    print(hr_email + "\n" + subject + "\n" + email_body)
    return "email sent"

@tool(description="use this tool to activate course after collecting screenshot and email")
def activate_course():
    print("course activated")
    return "course activated"

@tool
def password_reset():
    """
    use this tool to send password reset link to user email
    """
    return "password reset link sent successfully"

@tool
def search_flights():
    """
    use this tool to search flights from makemytrip
    """
    return "search flights"

@tool
def hotel_booking():
    """
    use this tool to book hotel from oyo for budgets under 3000
    """
    return "hotel booking confirmed"



