# Function to count and replace "terrible"

def count_replace_terrible(content):
    # Split the content into sentence using period as the delimiter
    sentences = content.split(".")
    # Initialize a counter for "terrible"
    terrible_count = 0
    # Initialize a list to store modified sentences
    result_sentences = []

    # Iterate through each sentence
    for sentence in sentences:
        # Split the sentence into words
        words = sentence.split()
        # Iterate through each word in the sentence
        for i, word in enumerate(words):
            # Check if the word is "terrible" (case-insensitive)
            if "terrible" in word.lower():
                # Increment the "terrible" count
                terrible_count += 1
                # Check if the count is even or odd
                if terrible_count % 2 == 0:
                    # Replace even occurrences with "pathetic"
                    words[i] = word.replace("terrible", "pathetic")
                else:
                    # Replace odd occurrences with "marvellous"
                    words[i] = word.replace("terrible", "marvellous")
        # Join the modified words back into a sentence
        result_sentences.append(" ".join(words))

    # Join the modified sentences back into the content
    return ". ".join(result_sentences), terrible_count

# Open the file for reading

with open("file_to_read.txt", "r") as file:
    content = file.read()

# Perform counting and replacement

modified_content, terrible_count = count_replace_terrible(content)

# Write the modified content to "result.txt"

with open("result.txt", "w") as result_file:
    result_file.write(modified_content)

# Display the total count of "terrible"

print(f"Total occurences of 'terrible': {terrible_count}")