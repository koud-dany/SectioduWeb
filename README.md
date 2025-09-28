# SectionduWeb - Video Competition Platform

A modern Flask-based video competition platform where users can upload videos, vote on submissions, and compete for rankings.

## Features

- **User Authentication**: Secure registration and login system
- **Video Upload**: Users can upload videos with titles and descriptions
- **Rating System**: 5-star rating system for video submissions
- **Leaderboard**: Real-time rankings based on video ratings
- **User Profiles**: Comprehensive user profiles with statistics and achievements
- **Admin Panel**: Administrative interface for managing users and content
- **Responsive Design**: Modern, mobile-friendly Bootstrap UI
- **Payment Integration**: Stripe integration for premium features

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Authentication**: Flask sessions
- **Payment**: Stripe API
- **File Upload**: Video and image handling

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/sectionduweb.git
cd sectionduweb
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python setup.py
```

5. Configure Stripe (optional):
   - Copy `stripe_config.py.example` to `stripe_config.py`
   - Add your Stripe API keys

6. Run the application:
```bash
python run_app.py
```

Visit `http://localhost:5000` to access the application.

## Project Structure

```
sectionduweb/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── setup.py             # Database initialization
├── static/              # Static assets
│   ├── avatars/         # User profile pictures
│   ├── uploads/         # Video uploads
│   └── translations/    # Internationalization files
├── templates/           # HTML templates
│   ├── admin/          # Admin panel templates
│   └── *.html          # Main application templates
└── README.md           # This file
```

## Features Overview

### User Features
- User registration and authentication
- Profile management with avatar upload
- Video upload with metadata
- Rating and commenting on videos
- Personal statistics and achievements
- Responsive design for all devices

### Admin Features
- User management
- Video moderation
- Platform analytics
- System settings
- Content management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact the development team.
