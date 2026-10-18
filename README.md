# DevTrack

## Problem

Job seekers often track applications across spreadsheets, browser tabs, and email threads. That makes it easy to lose track of application status, forget follow-ups, or miss useful patterns in a job search.

## Users

Job seekers, students, interns, and anyone managing multiple job applications who wants one private place to organize applications and track progress.

## Solution

DevTrack is a web-based job application tracker built with Flask. Users can create an account, record job applications, update their status as they move through the hiring process, and use a dashboard to see their overall progress. Each user's application data is private and isolated from other users.

## Features

- User registration, login, and logout
- Secure password hashing
- Add, edit, and delete job applications
- Track application status:
  - Wishlist
  - Applied
  - Interviewing
  - Offer
  - Rejected
- Store company, role, application date, salary range, job URL, notes, and next follow-up date
- Search applications by company
- Filter applications by status
- Sort applications by date or company
- Paginate application lists
- Dashboard with:
  - Total applications
  - Applied count
  - Interview and offer counts
  - Interview and offer rates
  - Status board
  - Upcoming follow-ups
- User-scoped records so users cannot access one another's applications
- CSRF protection for forms
- Automated tests for authentication, application management, access control, and dashboard statistics

## Technology

- **Python** — core programming language
- **Flask** — web application framework
- **Flask-SQLAlchemy** — database integration and ORM
- **Flask-Login** — session-based user authentication
- **Flask-WTF** — form handling and CSRF protection
- **SQLite** — default local development database
- **PostgreSQL** — supported through the `DATABASE_URL` environment variable
- **pytest** — automated testing
- **Gunicorn** — production WSGI server

## Data Model

DevTrack uses two primary database models:

- **User** — email address, password hash, and account creation date
- **Application** — owner, company, role, status, application date, salary range, job URL, notes, follow-up date, and creation date

Each application belongs to one user, and all application queries are scoped to the logged-in user.

## Setup

### Clone the repository

```bash
git clone https://github.com/gilla5/devtrack.git
cd devtrack
```

### Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

The app works locally with SQLite and development defaults. For a safer local setup, create a `.env` file:

```dotenv
SECRET_KEY=replace-with-a-long-random-value
DATABASE_URL=sqlite:///instance/devtrack.db
```

For PostgreSQL, replace `DATABASE_URL` with your PostgreSQL connection string:

```dotenv
DATABASE_URL=postgresql://username:password@localhost:5432/devtrack
```

### Run the application

```bash
flask --app run.py run --debug
```

Open <http://127.0.0.1:5000> in your browser.

The database tables are created automatically when the application starts.

### Run the tests

```bash
pytest
```

## Project Structure

```text
devtrack/
├── app/
│   ├── applications/    # Application CRUD, search, filtering, and pagination
│   ├── auth/            # Registration, login, and logout
│   ├── dashboard/       # User dashboard and application statistics
│   ├── static/          # CSS assets
│   ├── templates/       # Jinja templates
│   ├── forms.py         # WTForms definitions
│   ├── models.py        # User and Application models
│   └── extensions.py    # Flask extensions
├── tests/               # Automated tests
├── config.py            # Application configuration
├── requirements.txt     # Python dependencies
└── run.py               # Application entry point
```

## Roadmap

Potential future improvements include:

- Application reminders and email notifications
- Resume and cover letter tracking
- Interview notes and preparation checklists
- Additional dashboard charts and exportable reports
- Flask-Migrate database migrations
- Production deployment configuration

## License

This project is being developed as an individual project. Add a license here if the repository will be distributed publicly.
