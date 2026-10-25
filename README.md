# Movie Ticket Booking & Management System 🎬

**Basically, a mini cinema booking counter, built with Python, Tkinter, and MySQL.**

Ever tried booking the same seat twice? Yeah, that would be a problem.

This is a desktop application I developed for my **CBSE Class XII Computer Science project**. It lets you add movies, schedule shows, pick seats on an interactive grid, book or cancel tickets, and check booking and revenue reports. The interface runs on **Tkinter**, while **MySQL** keeps track of the data behind the scenes.

No real payments or cinema integrations here. It's a working educational project built to explore how a GUI and a relational database work together.

## How I built it# Movie Ticket Booking & Management System 🎬

**Basically, a mini cinema booking counter, built with Python, Tkinter, and MySQL.**

Ever tried booking the same seat twice? Yeah, that would be a problem.

This is a desktop application I developed for my **CBSE Class XII Computer Science project**. It lets you add movies, schedule shows, pick seats on an interactive grid, book or cancel tickets, and check booking and revenue reports. The interface runs on **Tkinter**, while **MySQL** keeps track of the data behind the scenes.

No real payments or cinema integrations here. It's a working educational project built to explore how a GUI and a relational database work together.

## How I built it

I used **Python** for the application logic, **Tkinter** for the graphical interface, and **MySQL Connector/Python** to connect everything to a MySQL database.

The program creates four related tables when it starts:

- **Movies:** Titles, genres, durations, and languages.
- **Shows:** Dates, times, screens, and seat availability.
- **Customers:** Names and contact numbers entered during booking.
- **Bookings:** Reserved seats, ticket totals, timestamps, and booking status.

The database uses primary and foreign keys, and the app runs SQL queries to add records, retrieve information, update seat availability, and produce reports.

**Tech stack:** Python 3 · Tkinter · MySQL 8 · MySQL Connector/Python

## What can you actually do?

- **Manage movies:** Add titles and view the movie catalog.
- **Schedule shows:** Assign a movie, date, time, screen, and seat count.
- **Pick your seats:** Choose from a visual seat grid. Available seats are green, selected seats are yellow, and already-booked seats are red and disabled.
- **Book tickets:** Enter customer details, select seats, and receive a booking ID.
- **Cancel a booking:** Enter the booking ID to cancel it and restore the available seat count.
- **Check the numbers:** View booking records, confirmed booking totals, and total revenue.

Tickets are priced at a fixed **₹200 per seat** in this version. It's a simulated booking workflow, not a payment gateway.

## Application screenshots

### Show management
Add a screening and see its details appear in the shows table.

![Show management](ui_pics/show-management.png.png)

### Interactive seat selection
Choose seats from a visual grid. Green seats are available, while yellow seats are selected for booking.

![Interactive seat selection](ui_pics/seat-selection.png.png)

### Updated seat availability
After a booking, reserved seats appear in red and can no longer be selected.

![Updated seat availability](ui_pics/seat-availability.png.png)

### Booking reports and revenue
Review booking history, cancellation status, confirmed bookings, and total revenue.

![Booking reports and revenue](ui_pics/reports-dashboard.png.png)

## The seat-selection part

This was one of my favorite parts to build.

Rather than making users type a seat number and hope for the best, the program generates an interactive grid based on the show's seat count. It checks the database for seats already reserved for that show and marks them unavailable.

Once you confirm a booking, the app saves the selected seats and updates the show's available-seat total. Cancelling a booking restores that count.

## Running it locally

You'll need **Python 3**, **MySQL Server**, and a Python installation with **Tkinter** available.

Clone the repository:

```bash
git clone https://github.com/aztrax7/movie-ticket-booking-system.git
cd movie-ticket-booking-system
```

Install the dependency:

```bash
pip install -r requirements.txt
```

In `main.py`, locate `DB_CONFIG` and replace the placeholder password with your **local** MySQL password. **Do not commit or push your real password to GitHub.** MySQL must be running, and the configured account must have permission to create a database and tables.

Then start the app:

```bash
python main.py
```

On startup, the app creates the `movie_booking_db` database and its tables if they don't already exist.

## How to use it

1. Open the **Movies** tab and add a movie.
2. Head to **Shows**, enter the movie ID, and create a screening.
3. In **Book Ticket**, enter the show ID and customer details, then load the seat grid.
4. Select your seats and click **Confirm & Pay** to create a simulated booking.
5. Use **Cancel Booking** if you want to cancel by booking ID.
6. Open **Reports** to see booking history and summary statistics.

## Project structure

```text
movie-ticket-booking-system/
├── ui_pics/           # Screenshots of the application
├── main.py            # GUI, booking logic, and MySQL operations
├── requirements.txt   # Python dependency
├── .gitignore         # Files Git should ignore
├── LICENSE            # MIT license
└── README.md          # You're reading it
```

## Why I made this

For my Class XII Computer Science project, I wanted to build something that felt like an actual application instead of another program that only prints results in a terminal.

A cinema booking system gave me a chance to connect a lot of things we'd studied: Python functions and classes, event-driven programming, SQL tables and relationships, and database updates that change what users see on screen.

It's a school project, and it keeps things intentionally simple. But getting the interface and database to work together made the concepts much more tangible.

**Pick a movie, grab a seat, and enjoy the (simulated) show.**


I used **Python** for the application logic, **Tkinter** for the graphical interface, and **MySQL Connector/Python** to connect everything to a MySQL database.

The program creates four related tables when it starts:

- **Movies:** Titles, genres, durations, and languages.
- **Shows:** Dates, times, screens, and seat availability.
- **Customers:** Names and contact numbers entered during booking.
- **Bookings:** Reserved seats, ticket totals, timestamps, and booking status.

The database uses primary and foreign keys, and the app runs SQL queries to add records, retrieve information, update seat availability, and produce reports.

**Tech stack:** Python 3 · Tkinter · MySQL 8 · MySQL Connector/Python

## What can you actually do?

- **Manage movies:** Add titles and view the movie catalog.
- **Schedule shows:** Assign a movie, date, time, screen, and seat count.
- **Pick your seats:** Choose from a visual seat grid. Available seats are green, selected seats are yellow, and already-booked seats are red and disabled.
- **Book tickets:** Enter customer details, select seats, and receive a booking ID.
- **Cancel a booking:** Enter the booking ID to cancel it and restore the available seat count.
- **Check the numbers:** View booking records, confirmed booking totals, and total revenue.

Tickets are priced at a fixed **₹200 per seat** in this version. It's a simulated booking workflow, not a payment gateway.

## The seat-selection part

This was one of my favorite parts to build.

Rather than making users type a seat number and hope for the best, the program generates an interactive grid based on the show's seat count. It checks the database for seats already reserved for that show and marks them unavailable.

Once you confirm a booking, the app saves the selected seats and updates the show's available-seat total. Cancelling a booking restores that count.

## Running it locally

You'll need **Python 3**, **MySQL Server**, and a Python installation with **Tkinter** available.

Clone the repository:

```bash
git clone https://github.com/aztrax7/movie-ticket-booking-system.git
cd movie-ticket-booking-system
```

Install the dependency:

```bash
pip install -r requirements.txt
```

In `main.py`, locate `DB_CONFIG` and replace the placeholder password with your **local** MySQL password. **Do not commit or push your real password to GitHub.** MySQL must be running, and the configured account must have permission to create a database and tables.

Then start the app:

```bash
python main.py
```

On startup, the app creates the `movie_booking_db` database and its tables if they don't already exist.

## How to use it

1. Open the **Movies** tab and add a movie.
2. Head to **Shows**, enter the movie ID, and create a screening.
3. In **Book Ticket**, enter the show ID and customer details, then load the seat grid.
4. Select your seats and click **Confirm & Pay** to create a simulated booking.
5. Use **Cancel Booking** if you want to cancel by booking ID.
6. Open **Reports** to see booking history and summary statistics.

## Project structure

```text
movie-ticket-booking-system/
├── main.py           # GUI, booking logic, and MySQL operations
├── requirements.txt  # Python dependency
├── .gitignore        # Files Git should ignore
└── README.md         # You're reading it
```

## Why I made this

For my Class XII Computer Science project, I wanted to build something that felt like an actual application instead of another program that only prints results in a terminal.

A cinema booking system gave me a chance to connect a lot of things we'd studied: Python functions and classes, event-driven programming, SQL tables and relationships, and database updates that change what users see on screen.

It's a school project, and it keeps things intentionally simple. But getting the interface and database to work together made the concepts much more tangible.

**Pick a movie, grab a seat, and enjoy the (simulated) show.**
