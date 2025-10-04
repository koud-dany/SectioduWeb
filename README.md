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
- **Payment Integration**: Mobile Money integration for premium features

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite
- **Authentication**: Flask sessions
- **Payment**: Mobile Money APIs (MTN MoMo, Orange Money, Airtel Money)
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

5. Configure Mobile Money (optional):
   - Edit `mobile_money_config.py` with your API credentials
   - See `MOBILE_MONEY_SETUP.md` for detailed setup instructions

6. Run the application:
```bash
python run_app.py
```

Visit `http://localhost:5000` to access the application.

## Deployment on Render (Free)

### Prerequisites
- GitHub account with your code pushed to a repository
- Render account (free at render.com)

### Deployment Steps

1. **Prepare your repository** (already done):
   - `requirements.txt` includes `gunicorn`
   - `render.yaml` and `Procfile` are present
   - Code is committed to GitHub

2. **Deploy on Render**:
   - Go to [Render.com](https://render.com) and sign up/login
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: videovote-app
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`

3. **Set Environment Variables** in Render dashboard:
   ```
   SECRET_KEY=your-super-secret-key-here
   FLASK_ENV=production
   MTN_MOMO_API_USER=bcf6b5d8-5a06-4f33-af77-7b8c9e2f1a3d
   MTN_MOMO_API_KEY=test-api-key-for-development-2024
   MTN_MOMO_SUBSCRIPTION_KEY=4842e41f28e44ed5b43f629dd9785b41
   ```

4. **Deploy**: Click "Deploy" and wait for completion

### Troubleshooting Render Deployment

- **"gunicorn: command not found"**: Ensure `gunicorn==21.2.0` is in `requirements.txt`
- **Mobile Money errors**: Set environment variables for Mobile Money API keys
- **Database issues**: SQLite works on Render's free tier

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
