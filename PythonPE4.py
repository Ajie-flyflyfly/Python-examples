import mysql.connector
import re

# Function to create the database and tables
def create_database_and_table():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )
    cursor = connection.cursor()

    # Create the database (if it doesn't exist)
    cursor.execute("CREATE DATABASE IF NOT EXISTS library")
    cursor.execute("USE library")

    # Create the Books table (if it doesn't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            BookID VARCHAR(10) PRIMARY KEY,
            Title VARCHAR(255),
            Author VARCHAR(255),
            ISBN VARCHAR(255),
            Status BOOLEAN
        )""")
    
    # Create Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            UserID VARCHAR(10) PRIMARY KEY,
            Name VARCHAR(255),
            Email VARCHAR(255)
        )""")
    
    # Create Reservations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reservations (
            ReservationID VARCHAR(10) PRIMARY KEY,
            BookID VARCHAR(10),
            UserID VARCHAR(10),
            ReservationDate DATE,
            FOREIGN KEY (BookID) REFERENCES Books (BookID),
            FOREIGN KEY (UserID) REFERENCES Users (UserID)
        )""")

    connection.commit()
    connection.close()

create_database_and_table()

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123456",
    database = "library"
)

cursor = connection.cursor()

def add_book():
    book_id = input("Enter BookID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = False # Default status is False (not reserved)

    cursor.execute("""INSERT INTO Books (BookID, Title, Author, ISBN, Status)
                   VALUES (%s, %s, %s, %s, %s)""", (book_id, title, author, isbn, status))
    connection.commit
    print("Book added successfully!")

def find_book_details(book_id):
    cursor.execute("SELECT * FROM Books WHERE BookID = %s", (book_id,))
    book = cursor.fetchone()

    if book:
        book_id, title, author, isbn, status = book
        cursor.execute("SELECT UserID, ReservationDate FROM Reservations WHERE BookID = %s", (book_id,))
        reservation = cursor.fetchone()
        if reservation:
            user_id, reservation_date = reservation
            cursor.execute("SELECT Name, Email FROM Users WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                user_name, email = user
                print(f"BookID: {book_id}")
                print(f"Title: {title}")
                print(f"Author: {author}")
                print(f"ISBN: {isbn}")
                print(f"Reservation Status: {'Reserved' if status else 'Not Reserved'}")
                print(f"Reserved by: {user_name}")
                print(f"User Email: {email}")
                print(f"Reservation Date: {reservation_date}")
            else:
                print("User details not found.")
        else:
            print(f"BookID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Reservation Status: {'Reserved' if status else 'Not Reserved'}")
            print("This book is not reserved by anyone.")
    else:
        print("Book not found.")

def find_reservation_status(search_text):
    if search_text.startswith("LB"):
        cursor.execute("SELECT Status FROM Books WHERE BookID = %s", (search_text,))
        status = cursor.fetchone()
        if status:
            print(f"Reservation Status for BookID {search_text}: {'Reserved' if status[0] else 'Not Reserved'}")
        else:
            print("Book not found.")
    elif search_text.startswith("LU"):
        cursor.execute("SELECT BookID FROM Reservations WHERE UserID = %s",(search_text,))
        books = cursor.fetchall()
        if books:
            print(f"Books reserved by UserID {search_text}: ")
            for book in books:
                find_book_details(book[0])
        else:
            print("No reservations found for this user.")
    elif search_text.startswith("LR"):
        cursor.execute("SELECT BookID FROM Reservations WHERE ReservationID = %s", (search_text,))
        book = cursor.fetchone()
        if book:
            find_book_details(book[0])
        else:
            print("Reservation not found.")
    else:
        cursor.execute("SELECT BookID FROM Books WHERE Title = %s",(search_text,))
        book = cursor.fetchone()
        if book:
            find_book_details(book[0])
        else:
            print("Book not found.")

def find_all_books():
    cursor.execute("SELECT * FROM Books")
    books = cursor.fetchall()
    if books:
        print("All Books in the Database:")
        for book in books:
            book_id, title, author, isbn, status = book
            print(f"BookID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Reservation Status: {'Reserved' if status else 'Not Reserved'}")
            print()
    else:
        print("No books found in the database.")

def update_book_details(book_id):
    cursor.execute("SELECT * FROM Books WHERE BookID = %s", (book_id,))
    book = cursor.fetchone()

    if book:
        book_id, title, author, isbn, status = book
        print("Current Details:")
        print(f"BookID: {book_id}")
        print(f"Title: {title}")
        print(f"Author: {author}")
        print(f"ISBN: {isbn}")
        print(f"Reservation Status: {'Reserved' if status else 'Not Reserved'}")

        new_title = input("Enter new Title (press Enter to keep current): ")
        new_author = input("Enter new Author (press Enter to keep current): ")
        new_isbn = input("Enter new ISBN (press Enter to keep current): ")
        new_status = input("Update Reservation Status (True/False) (press Enter to keep current): ")

        if new_title:
            cursor.execute("UPDATE Books SET Title = %s WHERE BookID = %s", (new_title, book_id))
        if new_author:
            cursor.execute("UPDATE Books SET Author = %s WHERE BookID = %s", (new_author, book_id))
        if new_isbn:
            cursor.execute("UPDATE Books SET ISBN = %s WHERE BookID = %s", (new_isbn, book_id))
        
        # Check if the reservation status is updated
        if new_status in ["True", "False"]:
            new_status = True if new_status == "True" else False
            if new_status != status:
                cursor.execute("UPDATE Books SET Status = %s WHERE BookID = %s", (new_status, book_id))

                # Update the Reservation table if the reservation stataus changed
                if new_status: # If the book is now reserved
                    reservation_id = input("Enter Reservation ID (LR-XXX): ")
                    user_id = input("Enter User ID(LU-XXX) for reservation: ")
                    reservation_date = input("Enter Reservation Date (YYYY-MM-DD): ")
                    user_name = input("Enter User Name: ")
                    user_email = input("Enter User Email: ")
                    cursor.execute("INSERT INTO Users (UserID, Name, Email) VALUES (%s, %s, %s)",
                                   (user_id, user_name, user_email))
                    cursor.execute("INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (%s, %s, %s, %s)",
                                   (reservation_id, book_id, user_id, reservation_date))
                else:
                    # Delete reservation if the book is no longer reserved
                    cursor.execute("DELETE FROM Reservations WHERE BookID=%s", (book_id,))

        connection.commit()
        print("Book details updated successfully!")
    else:
        print("Book not found.")

def delete_book(book_id):
    cursor.execute("SELECT * FROM Books WHERE BookID = %s", (book_id,))
    book = cursor.fetchone()

    if book:
        # Check if the book has reservations
        cursor.execute("SELECT * FROM Reservations WHERE BookID = %s", (book_id,))
        reservations = cursor.fetchall()

        if reservations:
            # Delete reservations first
            cursor.execute("DELETE FROM Reservations WHERE BookID = %s", (book_id,))

        # Now safely delete the book
        cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
        connection.commit()
        print("Book deleted successfully!")
    else:
        print("Book not found.")


while True:
    print("\nLibrary Management System")
    print("1. Add a new book")
    print("2. Find a book's detail")
    print("3. Find a book's reservation status")
    print("4. Find all books")
    print("5. Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_book()
    elif choice == "2":
        book_id = input("Enter BookID: ")
        find_book_details(book_id)
    elif choice == "3":
        search_text = input("Enter BookID (LB-XXX), UserID (LU-XXX), ReservationID (LR-XXX), or Title: ")
        find_reservation_status(search_text)
    elif choice == "4":
        find_all_books()
    elif choice == "5":
        book_id = input("Enter BookID: ")
        update_book_details(book_id)
    elif choice == "6":
        book_id = input("Enter BookID: ")
        delete_book(book_id)
    elif choice == "7":
        print("Goodbye!")
        connection.close()
        break
    else:
        print("Invalid choice. Please try again.")