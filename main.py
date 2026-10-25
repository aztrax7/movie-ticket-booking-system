import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ==========================================
# 1. DATABASE CONFIGURATION & CONNECTIVITY
# ==========================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password'  # Change this to your local MySQL password
}

def get_connection():
    """Establishes and returns a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        messagebox.showerror("Database Error", f"Failed to connect to MySQL:\n{e}")
        return None

def initialize_database():
    """Creates the database and necessary tables if they do not exist."""
    conn = get_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS movie_booking_db")
        cursor.execute("USE movie_booking_db")
        
        # Movies table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies (
                movie_id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                genre VARCHAR(50),
                duration INT,
                language VARCHAR(30)
            )
        """)
        
        # Shows table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shows (
                show_id INT AUTO_INCREMENT PRIMARY KEY,
                movie_id INT,
                show_date DATE,
                show_time VARCHAR(20),
                screen_no INT,
                total_seats INT DEFAULT 15,
                available_seats INT DEFAULT 15,
                FOREIGN KEY (movie_id) REFERENCES movies(movie_id) ON DELETE CASCADE
            )
        """)
        
        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(15) NOT NULL
            )
        """)
        
        # Bookings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                show_id INT,
                booking_datetime DATETIME,
                seats VARCHAR(100),
                ticket_count INT,
                total_amount DECIMAL(8,2),
                status VARCHAR(20) DEFAULT 'CONFIRMED',
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (show_id) REFERENCES shows(show_id)
            )
        """)
        conn.commit()
        conn.close()

# Initialize DB on startup
initialize_database()


# ==========================================
# 2. MAIN APPLICATION INTERFACE
# ==========================================
class MovieBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System - Class XII Project")
        self.root.geometry("900x650")

        # Top Navigation Notebook (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Tab Frames
        self.tab_movies = ttk.Frame(self.notebook)
        self.tab_shows = ttk.Frame(self.notebook)
        self.tab_booking = ttk.Frame(self.notebook)
        self.tab_cancel = ttk.Frame(self.notebook)
        self.tab_reports = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_movies, text="Movies")
        self.notebook.add(self.tab_shows, text="Shows")
        self.notebook.add(self.tab_booking, text="Book Ticket")
        self.notebook.add(self.tab_cancel, text="Cancel Booking")
        self.notebook.add(self.tab_reports, text="Reports")

        # Setup Individual Interfaces
        self.setup_movies_tab()
        self.setup_shows_tab()
        self.setup_booking_tab()
        self.setup_cancel_tab()
        self.setup_reports_tab()

    # ------------------------------------------
    # MODULE 1: MOVIE MANAGEMENT
    # ------------------------------------------
    def setup_movies_tab(self):
        # Form
        frame_form = ttk.LabelFrame(self.tab_movies, text=" Add New Movie ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Title:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_title = ttk.Entry(frame_form)
        self.ent_title.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Genre:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_genre = ttk.Entry(frame_form)
        self.ent_genre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Duration (min):").grid(row=1, column=0, padx=5, pady=5)
        self.ent_duration = ttk.Entry(frame_form)
        self.ent_duration.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Language:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_lang = ttk.Entry(frame_form)
        self.ent_lang.grid(row=1, column=3, padx=5, pady=5)

        btn_add = ttk.Button(frame_form, text="Add Movie", command=self.add_movie)
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        # Table
        self.tree_movies = ttk.Treeview(self.tab_movies, columns=("ID", "Title", "Genre", "Duration", "Language"), show="headings")
        for col in ("ID", "Title", "Genre", "Duration", "Language"):
            self.tree_movies.heading(col, text=col)
            self.tree_movies.column(col, width=100)
        self.tree_movies.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_movies()

    def add_movie(self):
        title = self.ent_title.get()
        genre = self.ent_genre.get()
        duration = self.ent_duration.get()
        lang = self.ent_lang.get()

        if not title or not duration.isdigit():
            messagebox.showwarning("Input Error", "Please provide valid Title and numeric Duration.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")
        cursor.execute("INSERT INTO movies (title, genre, duration, language) VALUES (%s, %s, %s, %s)",
                       (title, genre, int(duration), lang))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Movie added successfully!")
        self.load_movies()

    def load_movies(self):
        for item in self.tree_movies.get_children():
            self.tree_movies.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")
        cursor.execute("SELECT * FROM movies")
        for row in cursor.fetchall():
            self.tree_movies.insert("", "end", values=row)
        conn.close()

    # ------------------------------------------
    # MODULE 2: SHOW MANAGEMENT
    # ------------------------------------------
    def setup_shows_tab(self):
        frame_form = ttk.LabelFrame(self.tab_shows, text=" Add New Show ")
        frame_form.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_form, text="Movie ID:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_show_movie_id = ttk.Entry(frame_form)
        self.ent_show_movie_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.ent_show_date = ttk.Entry(frame_form)
        self.ent_show_date.insert(0, str(datetime.date.today()))
        self.ent_show_date.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Time (e.g. 18:00):").grid(row=1, column=0, padx=5, pady=5)
        self.ent_show_time = ttk.Entry(frame_form)
        self.ent_show_time.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Screen No:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_show_screen = ttk.Entry(frame_form)
        self.ent_show_screen.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Total Seats:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_show_seats = ttk.Entry(frame_form)
        self.ent_show_seats.insert(0, "15")  # Default is set to 15
        self.ent_show_seats.grid(row=2, column=1, padx=5, pady=5)

        btn_add_show = ttk.Button(frame_form, text="Add Show", command=self.add_show)
        btn_add_show.grid(row=2, column=2, columnspan=2, pady=10)

        self.tree_shows = ttk.Treeview(self.tab_shows, columns=("Show ID", "Movie Title", "Date", "Time", "Screen", "Total Seats", "Available Seats"), show="headings")
        for col in ("Show ID", "Movie Title", "Date", "Time", "Screen", "Total Seats", "Available Seats"):
            self.tree_shows.heading(col, text=col)
            self.tree_shows.column(col, width=100)
        self.tree_shows.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_shows()

    def add_show(self):
        m_id = self.ent_show_movie_id.get()
        s_date = self.ent_show_date.get()
        s_time = self.ent_show_time.get()
        screen = self.ent_show_screen.get()
        seats = self.ent_show_seats.get()

        if not (m_id.isdigit() and screen.isdigit() and seats.isdigit()):
            messagebox.showwarning("Input Error", "Movie ID, Screen, and Total Seats must be numbers.")
            return

        total_seats = int(seats)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")
        cursor.execute("""
            INSERT INTO shows (movie_id, show_date, show_time, screen_no, total_seats, available_seats) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (int(m_id), s_date, s_time, int(screen), total_seats, total_seats))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Show added successfully!")
        self.load_shows()

    def load_shows(self):
        for item in self.tree_shows.get_children():
            self.tree_shows.delete(item)
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")
        query = """
            SELECT s.show_id, m.title, s.show_date, s.show_time, s.screen_no, s.total_seats, s.available_seats
            FROM shows s JOIN movies m ON s.movie_id = m.movie_id
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            self.tree_shows.insert("", "end", values=row)
        conn.close()

    # ------------------------------------------
    # MODULE 3: TICKET BOOKING & SEAT SELECTION
    # ------------------------------------------
    def setup_booking_tab(self):
        frame_input = ttk.LabelFrame(self.tab_booking, text=" Step 1: Select Show & Customer Details ")
        frame_input.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_input, text="Show ID:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_book_show_id = ttk.Entry(frame_input)
        self.ent_book_show_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Customer Name:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_cust_name = ttk.Entry(frame_input)
        self.ent_cust_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_cust_phone = ttk.Entry(frame_input)
        self.ent_cust_phone.grid(row=1, column=1, padx=5, pady=5)

        btn_load_seats = ttk.Button(frame_input, text="Load Available Seats", command=self.load_seat_grid)
        btn_load_seats.grid(row=1, column=2, columnspan=2, pady=5)

        # Seat Grid Frame
        self.frame_seats = ttk.LabelFrame(self.tab_booking, text=" Step 2: Select Seats ")
        self.frame_seats.pack(fill="both", expand=True, padx=10, pady=5)

        self.selected_seats = []
        self.seat_buttons = {}

    def load_seat_grid(self):
        show_id = self.ent_book_show_id.get()
        if not show_id.isdigit():
            messagebox.showwarning("Input Error", "Please enter a valid numeric Show ID.")
            return

        # Clear existing buttons
        for widget in self.frame_seats.winfo_children():
            widget.destroy()

        self.selected_seats.clear()
        self.seat_buttons.clear()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")

        # Get total seats allocated for this specific show
        cursor.execute("SELECT total_seats FROM shows WHERE show_id = %s", (int(show_id),))
        show_row = cursor.fetchone()

        if not show_row:
            messagebox.showerror("Error", "Show ID not found.")
            conn.close()
            return

        total_seats = show_row[0]

        # Fetch booked seats for this show
        cursor.execute("SELECT seats FROM bookings WHERE show_id = %s AND status = 'CONFIRMED'", (int(show_id),))
        booked_rows = cursor.fetchall()
        conn.close()

        booked_seats = []
        for row in booked_rows:
            booked_seats.extend(row[0].split(","))

        # Dynamic Grid Layout Generation
        import string
        rows = list(string.ascii_uppercase)  # A, B, C, D...
        seats_per_row = 5
        
        for i in range(total_seats):
            r_idx = i // seats_per_row
            c_idx = (i % seats_per_row) + 1
            row_label = rows[r_idx]
            seat_code = f"{row_label}{c_idx}"

            btn = tk.Button(self.frame_seats, text=seat_code, width=8, height=2)
            
            if seat_code in booked_seats:
                btn.config(bg="red", state="disabled")
            else:
                btn.config(bg="lightgreen", command=lambda s=seat_code, b=btn: self.toggle_seat(s, b))
            
            btn.grid(row=r_idx, column=c_idx, padx=5, pady=5)
            self.seat_buttons[seat_code] = btn

        last_row = (total_seats // seats_per_row) + 1
        btn_confirm = ttk.Button(self.frame_seats, text="Confirm & Pay (Rs. 200/seat)", command=self.confirm_booking)
        btn_confirm.grid(row=last_row, column=1, columnspan=5, pady=10)

    def toggle_seat(self, seat_code, button):
        if seat_code in self.selected_seats:
            self.selected_seats.remove(seat_code)
            button.config(bg="lightgreen")
        else:
            self.selected_seats.append(seat_code)
            button.config(bg="yellow")

    def confirm_booking(self):
        show_id = self.ent_book_show_id.get()
        name = self.ent_cust_name.get()
        phone = self.ent_cust_phone.get()

        if not name or not phone or not self.selected_seats:
            messagebox.showwarning("Input Error", "Please fill customer details and select at least one seat.")
            return

        ticket_count = len(self.selected_seats)
        total_amount = ticket_count * 200.00  # Flat rate Rs. 200
        seats_str = ",".join(self.selected_seats)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")

        # Insert customer
        cursor.execute("INSERT INTO customers (name, phone) VALUES (%s, %s)", (name, phone))
        cust_id = cursor.lastrowid

        # Insert booking (with booking_datetime)
        cursor.execute("""
            INSERT INTO bookings (customer_id, show_id, booking_datetime, seats, ticket_count, total_amount, status)
            VALUES (%s, %s, NOW(), %s, %s, %s, 'CONFIRMED')
        """, (cust_id, int(show_id), seats_str, ticket_count, total_amount))
        booking_id = cursor.lastrowid

        # Update available seats count in show table
        cursor.execute("UPDATE shows SET available_seats = available_seats - %s WHERE show_id = %s", (ticket_count, int(show_id)))

        conn.commit()
        conn.close()

        messagebox.showinfo("Booking Successful", f"Booking ID: {booking_id}\nTotal Amount: Rs. {total_amount}\nSeats: {seats_str}")
        self.load_seat_grid()
        self.load_shows()

    # ------------------------------------------
    # MODULE 4: CANCELLATION
    # ------------------------------------------
    def setup_cancel_tab(self):
        frame_cancel = ttk.LabelFrame(self.tab_cancel, text=" Cancel Booking ")
        frame_cancel.pack(padx=20, pady=20, fill="x")

        ttk.Label(frame_cancel, text="Enter Booking ID:").grid(row=0, column=0, padx=10, pady=10)
        self.ent_cancel_id = ttk.Entry(frame_cancel)
        self.ent_cancel_id.grid(row=0, column=1, padx=10, pady=10)

        btn_cancel = ttk.Button(frame_cancel, text="Cancel Ticket", command=self.cancel_ticket)
        btn_cancel.grid(row=0, column=2, padx=10, pady=10)

    def cancel_ticket(self):
        b_id = self.ent_cancel_id.get()
        if not b_id.isdigit():
            messagebox.showwarning("Input Error", "Enter a valid numeric Booking ID.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")

        # Fetch booking details
        cursor.execute("SELECT show_id, ticket_count, status FROM bookings WHERE booking_id = %s", (int(b_id),))
        row = cursor.fetchone()

        if not row:
            messagebox.showerror("Error", "Booking ID not found.")
            conn.close()
            return

        show_id, t_count, status = row
        if status == "CANCELLED":
            messagebox.showwarning("Already Cancelled", "This booking is already cancelled.")
            conn.close()
            return

        # Update status to CANCELLED
        cursor.execute("UPDATE bookings SET status = 'CANCELLED' WHERE booking_id = %s", (int(b_id),))

        # Re-increment seat count in show table
        cursor.execute("UPDATE shows SET available_seats = available_seats + %s WHERE show_id = %s", (t_count, show_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Booking ID {b_id} cancelled successfully.")
        self.load_shows()

    # ------------------------------------------
    # MODULE 5: REPORTS & SUMMARY STATISTICS
    # ------------------------------------------
    def setup_reports_tab(self):
        btn_refresh = ttk.Button(self.tab_reports, text="Refresh Report Data", command=self.load_reports)
        btn_refresh.pack(anchor="nw", padx=10, pady=5)

        self.lbl_stats = ttk.Label(self.tab_reports, text="", font=("Arial", 11, "bold"))
        self.lbl_stats.pack(anchor="nw", padx=10, pady=5)

        self.tree_reports = ttk.Treeview(self.tab_reports, columns=("Booking ID", "Customer", "Movie", "Seats", "Amount", "Status"), show="headings")
        for col in ("Booking ID", "Customer", "Movie", "Seats", "Amount", "Status"):
            self.tree_reports.heading(col, text=col)
            self.tree_reports.column(col, width=110)
        self.tree_reports.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_reports()

    def load_reports(self):
        for item in self.tree_reports.get_children():
            self.tree_reports.delete(item)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("USE movie_booking_db")

        # Calculate Total Revenue from CONFIRMED bookings using SQL SUM
        cursor.execute("SELECT SUM(total_amount) FROM bookings WHERE status = 'CONFIRMED'")
        total_rev = cursor.fetchone()[0] or 0.0

        # Count total confirmed bookings
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'CONFIRMED'")
        total_bookings = cursor.fetchone()[0] or 0

        self.lbl_stats.config(text=f"Total Confirmed Bookings: {total_bookings}  |  Total Revenue: Rs. {total_rev:.2f}")

        # Fetch detailed booking history using SQL JOIN
        query = """
            SELECT b.booking_id, c.name, m.title, b.seats, b.total_amount, b.status
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN shows s ON b.show_id = s.show_id
            JOIN movies m ON s.movie_id = m.movie_id
            ORDER BY b.booking_id DESC
        """
        cursor.execute(query)
        for row in cursor.fetchall():
            self.tree_reports.insert("", "end", values=row)

        conn.close()


# ==========================================
# 3. APPLICATION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingApp(root)
    root.mainloop()