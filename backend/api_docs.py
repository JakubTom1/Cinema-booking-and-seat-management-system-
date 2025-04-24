"""
API Documentation for Cinema Booking System

Endpoints:
----------

GET /movies/{date}
    Get all movie showings for a specific date
    Parameters:
        - date: str (YYYY-MM-DD format)
    Returns:
        - List[ShowingResponse]

GET /seats/{showing_id}
    Get all seats for a specific showing
    Parameters:
        - showing_id: int
    Returns:
        - List[SeatResponse]

POST /reservations/
    Create a new reservation
    Body:
        - TransactionCreate schema
    Returns:
        - TransactionResponse

POST /register
    Register a new user
    Body:
        - UserCreate schema
    Returns:
        - UserResponse

POST /token
    Login and get access token
    Form data:
        - username: str
        - password: str
    Returns:
        - Token

GET /users/me/
    Get current user information
    Headers:
        - Authorization: Bearer token
    Returns:
        - UserResponse
"""

API_TAGS = [
    {"name": "movies", "description": "Operations with movie showings"},
    {"name": "seats", "description": "Operations with seats"},
    {"name": "reservations", "description": "Operations with reservations"},
    {"name": "users", "description": "User operations"},
    {"name": "auth", "description": "Authentication operations"},
]
