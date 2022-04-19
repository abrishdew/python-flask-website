# Steps to Install & Run App Locally
### 1. Make sure you have Python installed
### 2. Create virtual environment
    python3 venv -m my_env
### 3. Activate virtual environment
    source my_env/bin/activate
### 4. Install required libraries
    pip3 install -r requirements.txt
### 5. Set environment variables for 
    - FLASK_DEBUG
    - DATABASE_URL
    - SECRET_KEY
    - ADMIN_USER_NAME
    - ADMIN_PASSWORD
    - ADMIN_EMAIL
    - MAIL_SERVER
    - MAIL_POR
    - MAIL_USE_SSL
    - MAIL_USE_TLS
    - MAIL_USERNAME
    - MAIL_PASSWORD
    - UPLOAD_FOLDER
    - RECAPTCHA_PUBLIC_KEY
    - RECAPTCHA_PRIVATE_KEY
 - The variables prefixed `ADMIN` are for the moderator, `MAIL` are configurations for email verification, and the last two prefixed with `RECAPTCHA` are for recaptcha purposes.
 - You can set environment variables in two ways;
 - Inside the terminal, as follows
            
        export DATABASE_URL=your_database_url
 
 - You can check if the environment variable has been set or not by using the keyword `echo`

### OR
 - Create a `.env` file
 - Set the environment variables here in similar way to the above
 - Use Python's `os` library to get variables.

 ### 6. Inside terminal, enter command `python3 run.py`