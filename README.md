# Booking Project

## Description
This project is a housing rental booking platform designed to manage property listings, user reservations, and real-time availability. Inspired by industry standards like Booking.com, it provides a centralized system for owners to list accommodations and for clients to secure stays through an interactive interface.

## Distinctiveness and Complexity
* Dynamic UI Integration: This project enhances standard Django templates by incorporating JavaScript (and potentially React) for specific interactive features. A key example is the property filtering system, which updates results dynamically without a full page refresh, providing a smoother and more responsive user experience.
* Booking & Availability Logic: The system manages complex scheduling to prevent double-bookings and track reservation statuses, requiring more advanced backend logic and database constraints than typical course projects.
* Production-Ready Implementation: Focused on building a real-world tool using Bootstrap, ensuring the platform is responsive and professionally styled for deployment.

## File Structure
* bookings/: Main application directory containing business logic and property models.
    * models.py: Defines the data structure for users, properties, and booking records.
    * urls.py: Maps API endpoints and application routes.
    * views.py: Handles the logic for processing requests and returning data.
* config/: Central Django project configuration files.
* templates/bookings/:
    * index.html: The main dashboard containing the property search/filter form and the dynamic display area for filtered results.
* requirements.txt: List of Python dependencies required to run the project.
* manage.py: Django’s command-line utility for administrative tasks.

## Installation
1. Clone the repository to your local machine.
2. Create a virtual environment:
   python -m venv venv
3. Activate the virtual environment:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate
4. Install dependencies:
   pip install -r requirements.txt
5. Run database migrations:
   python manage.py makemigrations
   python manage.py migrate
6. Start the development server:
   python manage.py runserver