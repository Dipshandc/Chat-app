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
