from mcp.server.fastmcp import FastMCP

mcp_server = FastMCP("GenAI-MCP")


@mcp_server.tool(description="use this tool to send email to hr once the interview is completed", name="send_email")
def send_email_tool(hr_email: str, subject: str, email_body: str):
    print("inside mCP server send_email tool ")
    return f"email sent to {hr_email}"

@mcp_server.tool(name="activate_course", description="use this tool to activate course after collcting course details, user details and payment id from the user")
def activate_course(course_name: str, user_email: str, payment_id: str):
    print("inside mcp server activate_course tool")
    return f"course activated"


@mcp_server.tool(name="use this tool to search flights from makemytrip", description="")
def search_flights(from_city: str, to_city: str, date: str, time: str):
    print("inside mcp server search_flights tool")
    return f"10 flights found from {from_city} to {to_city}"

app = mcp_server.streamable_http_app()

