# Josh Zachary Tan - Personal Website

A modern, responsive personal website built with FastAPI, featuring user authentication, a comments system, and contact form functionality. This website showcases Josh's background in financial services and passion for DevOps and technology.

## 🌟 Features

- **Responsive Design**: Built with Tailwind CSS for optimal viewing on all devices
- **User Authentication**: Complete registration, login, and logout functionality
- **Comments System**: Authenticated users can post and view comments
- **Contact Form**: Visitors can send messages through a contact form
- **About Page**: Professional background and technical skills showcase
- **LinkedIn Integration**: Direct link to professional profile
- **Database Integration**: MySQL database for user data and content storage

## 🚀 Live Website

The website includes the following main sections:
- **Home**: Welcome page with profile picture and introduction
- **About Me**: Professional background and technical skills
- **Contact**: Message form for inquiries
- **Comments**: Interactive comment system for registered users
- **LinkedIn**: Direct link to [Josh's LinkedIn profile](https://www.linkedin.com/in/joshzacharytan/)

## 🛠 Technology Stack

- **Backend**: FastAPI (Python web framework)
- **Frontend**: HTML5, Tailwind CSS, Jinja2 templates
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Passlib with bcrypt password hashing
- **Session Management**: Starlette session middleware
- **Environment Management**: python-dotenv for configuration

## 📋 Prerequisites

- Python 3.7+
- MySQL database server
- pip (Python package manager)

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone &lt;repository-url&gt;
cd about-me
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with your MySQL database credentials:

```env
MYSQL_USER=your_mysql_username
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DB=your_database_name
```

### 4. Database Setup

The application will automatically create the necessary tables on first run. Make sure your MySQL database exists and is accessible with the provided credentials.

### 5. Static Files

Ensure you have a `static/` directory with the profile image:
- `static/Joshua.jpg` - Profile picture for the home page

### 6. Run the Application

```bash
uvicorn app:app --reload
```

The website will be available at `http://localhost:8000`

## 🗂 Project Structure

```
about-me/
├── app.py                 # Main FastAPI application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── static/               # Static files (images, CSS, JS)
│   └── Joshua.jpg        # Profile picture
└── templates/            # HTML templates
    ├── index.html        # Home page
    ├── about.html        # About me page
    ├── contact.html      # Contact form
    ├── comments.html     # Comments system
    ├── login.html        # User login
    ├── register.html     # User registration
    ├── login-error.html  # Login error page
    └── thank-you.html    # Contact form success
```

## 🔧 Configuration

### Database Models

The application uses three main database models:

- **User**: Stores user authentication information
- **Comment**: Stores user comments with timestamps and author references
- **ContactFormEntry**: Stores contact form submissions

### Security Features

- Password hashing using bcrypt
- Session-based authentication
- Protected routes for authenticated users only
- SQL injection protection via SQLAlchemy ORM

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `MYSQL_USER` | MySQL database username | Yes |
| `MYSQL_PASSWORD` | MySQL database password | Yes |
| `MYSQL_HOST` | MySQL server host | Yes |
| `MYSQL_DB` | MySQL database name | Yes |

## 🎨 Customization

### Styling
- The website uses Tailwind CSS for styling
- Inter font family is used throughout the site
- Color scheme centers around blue tones with gray accents

### Branding
- Site logo: "JZT" (Josh Zachary Tan initials)
- Consistent navigation across all pages
- Professional color scheme and typography

## 🔗 API Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| GET | `/` | Home page | No |
| GET | `/about` | About page | No |
| GET/POST | `/contact` | Contact form | No |
| GET | `/thank-you` | Contact success page | No |
| GET/POST | `/register` | User registration | No |
| GET/POST | `/login` | User login | No |
| GET | `/logout` | User logout | Yes |
| GET/POST | `/comments` | Comments system | Partial* |

*Comments can be viewed by anyone, but posting requires authentication.

## 🚧 Development Notes

### Session Management
- Sessions use a secret key defined in the application
- In production, ensure you change the secret key to a secure random string

### Database Initialization
- Tables are created automatically on application startup
- No manual database migration required

### Error Handling
- Custom login error page for failed authentication attempts
- Form validation for required fields
- Graceful error handling for database operations

## 📝 About Josh Zachary Tan

Josh is a technology enthusiast with 16 years of experience in financial services, actively managing a production-grade home lab and passionate about DevOps, cloud technologies, and automation. He combines analytical rigor from his financial background with hands-on technical skills in Linux, Python, and cloud platforms.

### Technical Skills
- **Programming**: Python, Linux, SQL
- **Databases**: MySQL, PostgreSQL
- **Cloud Platforms**: Microsoft Azure, AWS
- **Infrastructure**: Proxmox, Kubernetes, Docker Swarm
- **Services**: Nextcloud, Vaultwarden, Pi-hole, n8n

## 📄 License

This project is for personal use and portfolio demonstration.

## 🤝 Contact

For inquiries or collaboration opportunities, please use the contact form on the website or connect via [LinkedIn](https://www.linkedin.com/in/joshzacharytan/).