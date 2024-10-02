## Portfolio Website
**This is a simple portfolio website built with Flask. 
It allows users to showcase their portfolio items and also provides an admin interface for managing portfolio data.
The site was originally conceived as a web portfolio for a data analyst.**

### Features
- **Portfolio Display:** Display portfolio items with titles, subtitles, descriptions, and images.
- **Admin Interface:** Secure login for administrators to add, edit, and delete portfolio items.
- **Contact Form:** Contact form for users to send messages directly to the site owner via Telegram.
- **Database Integration:** Utilizes SQLite database to store portfolio and admins data.

### Prerequisites
- Python 3.x installed on your system.
- Flask and other required dependencies installed (see requirements.txt).
-
### Getting Started

1. Clone the repository to your local machine:  
`git clone https://github.com/<username>/portfolio-website.git`

2. Install dependencies using pip:   
`pip install -r requirements.txt`

3. Set environment variables:

```
FLASK_S_KEY: Flask secret key.  
TG_TOKEN: Telegram bot token.  
TG_ID: Telegram chat ID.
```

4. Run the Flask application:
```
python app.py  
Access the website at http://localhost:5000.
```

### Usage  
- Visit the homepage to view the portfolio items.  
- Admins can log in to add, edit, or delete portfolio items.
 -Users can use the contact form to send messages directly to the site owner via Telegram.

### Contributing
Contributions are welcome! Please fork the repository, make changes, and submit a pull request.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

###  Acknowledgments
Flask
Flask-Bootstrap
Flask-CKEditor
Flask-Login
Flask-SQLAlchemy
