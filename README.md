DNS URL Shortener with Flask and IONOS
Overview

This project is a simple web application that allows you to shorten URLs using DNS TXT records in your IONOS domain.
When you submit a URL, the system generates a unique hash, creates a TXT record in your domain (for example jxvx.es), and lets you access it through:

http://localhost:5000/<hash>


When that address is visited, the app looks up the TXT record in DNS and automatically redirects to the original URL.

Requirements

Before running the project, make sure you have:

An IONOS account with a registered domain (for example: jxvx.es).

An API Key from IONOS with DNS access permissions.

Python 3 installed on your system.

Installation
1. Clone the repository
git clone https://github.com/your_user/your_repository.git
cd your_repository

2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate    # On Linux or Mac
venv\Scripts\activate       # On Windows

3. Install the required packages
pip install flask requests python-dotenv dnspython

Environment configuration

Create a file named .env in the root of the project with the following information:

IONOS_API_KEY=your_ionos_api_key
ZONE_ID=f7cf9131-b572-11f0-a514-0a58644418eb
DOMAIN=jxvx.es


Note:
Keep your API key private. Do not upload it to GitHub or share it publicly.

Running the application

Start the Flask development server with:

python app.py


You should see a message similar to:

* Running on http://127.0.0.1:5000


Then open your browser and go to:
http://localhost:5000

How to use it

Enter a full URL (for example: https://www.wikipedia.org).

Click on "Generate hash".

The page will display:

The generated hash (e.g., ab2a63)

A command to check it using dig

A direct link for redirection

Automatic redirection

Once a hash is created, you can open it directly in your browser:

http://localhost:5000/<hash>


The app will look up the DNS record (<hash>.jxvx.es) and redirect you to the original website automatically.

Verifying the DNS record

To verify that the TXT record has been created successfully, use this command:

dig +short TXT <hash>.jxvx.es


It should return the original URL.

Project structure
DNS_Shortener/
│
├── app.py
├── .env
├── .gitignore
├── README.md
└── templates/
    └── index.html

Technologies used

Python 3

Flask (for the web interface)

Requests (for API communication)

dnspython (for DNS queries)

IONOS DNS API

Author

Project developed by Javier Padial González
for the subject Network Services (SRI) – 2nd year ASIR
