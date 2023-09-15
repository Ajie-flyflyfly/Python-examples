if __name__ == "__main__":
    with open("stephen_king_adaptations.txt", "r") as file:
        stephen_king_adaptations_list = [line.strip().split(",") for line in file.readlines()]


    for item in stephen_king_adaptations_list:
        del item[0]
        movie_name, movie_year, imdb_rating = item
        print(movie_name, movie_year, imdb_rating)

