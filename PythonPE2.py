import mysql.connector

# Function to create the database and table
def create_database_and_table():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456"
    )
    cursor = connection.cursor()

    # Create the database (if it doesn't exist)
    cursor.execute("CREATE DATABASE IF NOT EXISTS stephen_king_adaptations_db")
    cursor.execute("USE stephen_king_adaptations_db")

    # Create the table (if it doesn't exist)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
            movieID INT AUTO_INCREMENT PRIMARY KEY,
            movieName VARCHAR(255),
            movieYear INT,
            imdbRating DECIMAL(3, 1)
        )
    """)

    connection.commit()
    connection.close()

# Function to check if data already exists in the table
def data_exists(connection, movie_name, movie_year, imdb_rating):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM stephen_king_adaptations_table
        WHERE movieName = %s AND movieYear = %s AND imdbRating = %s
    """, (movie_name, movie_year, imdb_rating))
    count = cursor.fetchone()[0]
    return count > 0

# Function to insert data into the table from a list
def insert_data_from_list(data_list):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stephen_king_adaptations_db"
    )
    cursor = connection.cursor()

    for item in data_list:
        sql = """
            INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
            VALUES (%s, %s, %s)
        """
        del item[0]
        movie_name, movie_year, imdb_rating = item
        #cursor.execute(sql, item)

        if not data_exists(connection, movie_name, movie_year, imdb_rating):
            cursor.execute("""
                INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating)
                VALUES (%s, %s, %s)
            """, (movie_name, movie_year, imdb_rating))

    connection.commit()
    connection.close()

# Function to search for movies
def search_movies():
    while True:
        print("\nOptions:")
        print("1. Search by Movie Name")
        print("2. Search by Movie Year")
        print("3. Search by IMDb Rating")
        print("4. STOP")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            movie_name = input("Enter the movie name: ")
            search_by_name(movie_name)
        elif choice == '2':
            movie_year = input("Enter the movie year: ")
            search_by_year(movie_year)
        elif choice == '3':
            rating = input("Enter IMDb rating: ")
            search_by_rating(float(rating))
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to search by movie name
def search_by_name(movie_name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stephen_king_adaptations_db"
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM stephen_king_adaptations_table WHERE movieName LIKE %s
    """, (movie_name,))

    movies = cursor.fetchall()
    
    if movies:
        for movie in movies:
            print("Movie Name:", movie[1])
            print("Movie Year:", movie[2])
            print("IMDb Rating:", movie[3])
    else:
        print("No such movie exists in our database.")

    connection.close()

# Function to search by movie year
def search_by_year(movie_year):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stephen_king_adaptations_db"
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM stephen_king_adaptations_table WHERE movieYear = %s
    """, (int(movie_year),))

    movies = cursor.fetchall()

    if movies:
        for movie in movies:
            print("Movie Name:", movie[1])
            print("Movie Year:", movie[2])
            print("IMDb Rating:", movie[3])
    else:
        print("No movies were found for that year in our database.")

    connection.close()

# Function to search by IMDb rating
def search_by_rating(rating):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="stephen_king_adaptations_db"
    )
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= %s
    """, (rating,))

    movies = cursor.fetchall()

    if movies:
        for movie in movies:
            print("Movie Name:", movie[1])
            print("Movie Year:", movie[2])
            print("IMDb Rating:", movie[3])
    else:
        print("No movies at or above that rating were found in the database.")

    connection.close()

if __name__ == "__main__":
    with open("stephen_king_adaptations.txt", "r") as file:
        stephen_king_adaptations_list = [line.strip().split(",") for line in file.readlines()]

    create_database_and_table()
    insert_data_from_list(stephen_king_adaptations_list)

    search_movies()