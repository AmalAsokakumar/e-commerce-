# Zaya 

Welcome to My Commercial Website, a web platform built using Python and Django. This site is designed to provide a convenient and user-friendly interface for our customers to browse and purchase our products.

## Requirements

- Python 3.6 or higher
- Django 3.1 or higher

## Installation

To set up the project locally on your machine, follow these steps:

1. Clone the repository:

git clone https://github.com/comrider/e-commerce-.git

Copy code

2. Change into the project directory:

cd my-commercial-website

Copy code

3. Create a virtual environment and activate it:

python3 -m venv venv
source venv/bin/activate

Copy code

4. Install the dependencies:

pip install -r requirements.txt

Copy code

5. Run the database migrations:

ython manage.py makemigrations

python manage.py migrate

Copy code

6. Start the development server:

python manage.py runserver

Copy code

The website will be available at http://localhost:8000/.

## Usage

To use the site, simply navigate to the homepage and browse our products. You can add items to your cart and checkout when you are ready to make a purchase.

Guest users can also add items to there cart.

## Support

If you encounter any issues or have any questions about the site, please don't hesitate to contact ma at amalcdac521@gmail.com 

#

# Deployment of Django Application on AWS

### The steps taken to successfully deploy a Django-based application on AWS using Nginx, uWSGI, and EC2. The application is also utilizing Route53 and RDS for DNS and database management.

1. Infrastructure

- EC2: The application is hosted on an EC2 instance, which serves as the web server.
- Nginx: Nginx is used as a reverse proxy and load balancer for the application.
- uWSGI: uWSGI is used as an application server to handle the Django application.
- Route53: Route53 is used for DNS management and to map the custom domain name to the application.
- RDS: RDS is used for database management and is connected to the application via settings.py.
- SSL: SSL certification is implemented for secure communication.
- 
### Deployment Steps

- Spin up an EC2 instance on AWS and connect to it via SSH.
- Install Nginx, uWSGI and other dependencies on the EC2 instance.
- Configure Nginx as a reverse proxy and load balancer for the application.
- Configure uWSGI to handle the Django application.
- Connect the RDS instance to the application via settings.py.
- Create a Route53 hosted zone and map the custom domain name to the application.
- Obtain and implement an SSL certificate for the custom domain name.
- Test the application and ensure it is functioning as expected.
- 
### Maintenance

- To ensure the application continues to function smoothly, it is important to keep the EC2 instance, Nginx, uWSGI, and dependencies up to date. Additionally, the database should be regularly backed up and the SSL certificate should be renewed before expiration.
