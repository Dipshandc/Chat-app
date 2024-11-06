# Real-Time Chat Application

This is a **Real-Time Chat Application** built using Django and Django Channels, featuring JWT-based authentication, custom WebSocket middleware for secure communication, and several user-centric functionalities. The app allows users to register, manage profiles, and interact in real-time, with indicators for online/offline status.

## Features

- **Real-Time Messaging**: Instant message delivery using Django Channels and WebSockets.
- **JWT Authentication**: Secure user authentication and session management using JSON Web Tokens.
- **Custom Middleware for WebSocket Authentication**: Ensures that only authenticated users can initiate WebSocket connections.
- **User Registration and Profile Management**: Users can register, edit their profile information, and manage their account settings.
- **Online/Offline Status Indicators**: See who is currently online, enabling better communication and engagement.

## Project Structure

The project is organized as follows:

```plaintext
project-root/
│
├── chat_app/
│   ├── consumers.py            # WebSocket consumers handling real-time communication
│   ├── middleware.py           # Custom middleware for WebSocket JWT authentication
│   ├── models.py               # Database models for user profiles and messages
│   ├── serializers.py          # Serializers for handling data representation
│   ├── urls.py                 # URL configurations for the chat app
│   └── views.py                # REST API views for user-related operations
│
├── config/
│   ├── settings.py             # Django settings, including Channels setup
│   ├── urls.py                 # Project-wide URL routing
│   └── asgi.py                 # ASGI configuration for WebSocket support
│
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```
## Getting Started
### Prerequisites
- Python 3.x
- Django and Django Channels
- Redis (as a message broker for handling real-time data flow)
### Installation
1 Clone the Repository:
```code
git clone https://github.com/your-username/real-time-chat-app.git
cd real-time-chat-app
```
2 Install Dependencies:
```code
pip install -r requirements.txt
```
3 Configure Redis:
 Ensure Redis is installed and running on the default port (6379). Adjust settings in settings.py if necessary.

4 Apply Migrations:
```code
python manage.py migrate
```
5 Run the Server:
 Start the Django server and Redis:
 
```code
python manage.py runserver
```
### Running the Chat Application
Once the server is running, access the app at http://localhost:8000. Users can register, log in, and start real-time messaging with others.

### Usage
1 User Registration: New users can sign up and set up their profiles.
2 User Login: Authenticate using JWT tokens for secure communication.
3 Real-Time Chat: Send and receive messages instantly, with live updates.
4 Online/Offline Status: View active users in real time.

### Technology Stack
- Backend: Django, Django Channels
- Authentication: JSON Web Tokens (JWT)
- Real-Time Communication: WebSocket, Redis
- Database: SQLite (or any preferred database)
### Future Enhancements
- Media Sharing: Allow users to share images or files within the chat.
- Typing Indicators: Show when other users are typing in real-time.
- Message Reactions: Add emoji-based reactions to messages.
-Video and Audio Calls: Integrate WebRTC for real-time audio and video communication.
