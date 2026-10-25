# Movie Ticket Booking & Management System

A desktop movie ticket booking and cinema management application developed for a Class XII Computer Science project using **Python, Tkinter, and MySQL**.

## Features

- Add and view movie records
- Schedule shows and track seat availability
- Select seats through an interactive graphical grid
- Book tickets and calculate the total ticket amount
- Cancel bookings and restore seat availability
- View booking history, confirmed bookings, and revenue statistics

## Technologies

- Python 3
- Tkinter (GUI)
- MySQL 8
- MySQL Connector/Python

## Run locally

1. Install Python 3 and MySQL Server.
2. Install the Python dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Open `main.py` and change the `DB_CONFIG` password placeholder to your **local** MySQL password. **Do not commit your actual password to GitHub.**
4. Run:

   ```bash
   python main.py
   ```

The application creates its database and tables on startup when MySQL credentials are valid.

## Notes

- The ticket price is set to Rs. 200 per seat in the original project.
- This repository preserves the original Class XII project implementation.
- This application has not been independently runtime-tested in this repository package; a running local MySQL installation is required.
- Do not enter real customers' personal information when preparing public demonstrations or screenshots.

## Project context

Developed as a CBSE Class XII Computer Science project to demonstrate Python-MySQL connectivity, relational database operations, and graphical user interface programming.
