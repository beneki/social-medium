# Social Media Project

Welcome to the Social Media Project, a Python-based application designed to facilitate social interaction through a user-friendly platform. This project demonstrates how to build a basic social media site with functionalities such as user profiles, posts, and comments.

## Current Status

This is the initial commit of the project. So far, the following features have been completed:

- **User Authentication**: Secure sign-up, login, and password management.
- **User Profiles**: Customisable profiles with bio, profile image, and location.

Work on additional features like posts, comments, and more advanced functionalities will follow in subsequent updates.

## Features

- **User Authentication**: Secure sign-up, login, and password management.
- **User Profiles**: Customisable profiles with bio, profile image, and location.
- **Posts**: (To be implemented)
- **Comments**: (To be implemented)
- **Responsive Design**: A modern, responsive user interface.

## Requirements

- Python 3.8 or higher
- Django 5.1 or higher
- Pillow (for image handling)
- Other dependencies listed in `requirements.txt`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/social-media-project.git
   cd social-media-project
   ```

2. **Create a Virtual Environment**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Migrations**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

## Configuration

Update your settings.py file with your preferred database settings, and configure any additional settings such as static files and media files.
Ensure you have a .env file or environment variables set up for sensitive data like SECRET_KEY and database credentials.

## Usage

- **Sign Up**: Create a new account with a username, email, and password.
- **Log In**: Access your account with your username and password.
- **Profile Settings**: Update your profile with a bio, profile image, and location.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Be sure to follow the project's coding standards and include tests for new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or feedback, please reach out to ekramian.hossein@gmail.com.