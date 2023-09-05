# AquaTrack - Water Consumption Tracker

AquaTrack is a simple web application built using Flask, a Python web framework, that allows users to track their daily water consumption. Users can log in, add water consumption records, remove water records, reset their daily water consumption, and view their current progress towards the recommended daily water intake.

## Features

- **Dashboard**: Users are greeted with a personalized dashboard showing their current water consumption progress and recommendations.
- **Add Water**: Users can add records of the amount of water they have consumed.
- **Remove Water**: Users can remove records of water consumption if they make a mistake.
- **Reset Water Consumption**: Users can reset their daily water consumption to zero.
- **Disconnect**: Users can log out of their accounts.

## Installation

To run AquaTrack locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AquaTrack.git
   cd AquaTrack
   ```

2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by creating a `.env` file in the root directory with the following content:

   ```dotenv
   AQUATRACK_SECRET_KEY=your_secret_key
   AQUATRACK_DB_HOST=your_database_host
   AQUATRACK_DB_PORT=your_database_port
   AQUATRACK_DB_USERNAME=your_database_username
   AQUATRACK_DB_PASSWORD=your_database_password
   AQUATRACK_DB_NAME=your_database_name
   ```

   Replace the placeholders with your actual values.

4. Initialize the database (assuming you have PostgreSQL installed):

   ```bash
   python db_init.py
   ```

5. Run the application:

   ```bash
   python app.py
   ```

The application will be accessible at `http://localhost:5000` in your web browser.

## Usage

1. **Login**: Log in using your username and password.

2. **Dashboard**: Upon successful login, you will be directed to your personalized dashboard. This page displays your current water consumption progress.

3. **Add Water**: To log your water consumption, use the "Add" button to specify the amount of water you've consumed (in milliliters) and submit the form. An alert will confirm your success.

4. **Remove Water**: If you make a mistake, you can remove water records by specifying the amount to be removed and clicking the "Remove" button. An alert will confirm your action.

5. **Reset Water Consumption**: You can reset your daily water consumption to zero by clicking the "Reset Water Consumption" button. Confirm the action when prompted.

6. **Disconnect**: To log out of your account, click the "Disconnect" button.

## Development

If you want to contribute to AquaTrack or make improvements, here are some tips:

- The application uses Flask for the backend and Jinja2 templates for the frontend. HTML templates are in the `templates` directory, and static assets (CSS) are in the `static` directory.

- You can customize the HTML templates and styles to match your preferences or branding.

- The database schema is simple, with a single `users` table to store user information. You can expand the database and add more features as needed.

## Acknowledgments

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- psycopg2: [https://www.psycopg.org/](https://www.psycopg.org/)
- python-dotenv: [https://github.com/theskumar/python-dotenv](https://github.com/theskumar/python-dotenv)
