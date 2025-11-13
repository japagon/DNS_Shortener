DNS URL Shortener with Flask and IONOS
Description
This project allows shortening URLs using DNS TXT records in IONOS.
Each time a URL is entered, the system generates a unique hash, creates a TXT record in the configured domain, and allows access through:
http://localhost:5000/<hash>

When accessing that address, the server queries the TXT record and automatically redirects to the original URL.

Prerequisites


IONOS account with a registered domain (for example: jxvx.es).


An IONOS API Key with DNS permissions.


Python 3 installed on the system.



Installation
Clone the repository:
git clone https://github.com/your_user/your_repository.git
cd your_repository

Create and activate a virtual environment:
python3 -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows

Install the required dependencies:
pip install flask requests python-dotenv dnspython


.env File Configuration
Create a file named .env in the project root directory with the following content:
IONOS_API_KEY=your_ionos_api_key
ZONE_ID=f7cf9131-b572-11f0-a514-0a58644418eb
DOMAIN=jxvx.es

Important:
Do not share your API Key on GitHub or in public documents.

Running the Application
Run the following command:
python app.py

You will see a message like this:
* Running on http://127.0.0.1:5000

Then, open your browser and go to:
http://localhost:5000

Usage


Enter a full URL (for example: https://www.wikipedia.org)


Click "Generate hash"


You will see:


The generated hash (e.g., ab2a63)


The command to verify it using dig


The direct redirection link





Automatic Redirection
After creating a hash, you can access directly with:
http://localhost:5000/<hash>

The system will query the DNS (hash.jxvx.es) and redirect to the original URL.

DNS Verification
You can check the created TXT record using:
dig +short TXT <hash>.jxvx.es


Project Structure
DNS_Shortener/
│
├── app.py
├── .env
├── .gitignore
├── README.md
└── templates/
    └── index.html


Technologies Used

Python 3

Flask

Requests

dnspython

IONOS DNS API



Author
Project developed by Javier Padial González
for the module Network Services (SRI) – 2nd year ASIR
