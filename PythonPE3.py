# Impowt required Python libraries and modules
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import gutenberg

# Download Moby Dick form the Gutenberg dataset using NLTK
nltk.download("gutenberg")
moby_dick = gutenberg.raw("melville-moby_dick.txt")

# Tokenization: split text into words using NLTK's word_tokenize function
tokens = word_tokenize(moby_dick)

# Stopwords filtering: load stop words for English and filter out stop words and non-alphabetic characters in text
stop_words = set(stopwords.words("english"))
filtered_tokens = [word for word in tokens if word.lower() not in stop_words and word.isalpha()]

# Parts-of-Speech (POS) tagging: the filtered words are marked with POS
pos_tags = pos_tag(filtered_tokens)

# POS frequency: Count the number of occurrence of different part of speech
pos_counts = Counter(tag for word, tag in pos_tags)
top_pos = pos_counts.most_common(5)

# Lemmatization: using WordNetLemmatizer to restore the word after POS tagging
lemmatizer = WordNetLemmatizer()
top_lemmas = [lemmatizer.lemmatize(word) for word, _ in pos_counts.most_common(20)]

# Plotting frequency distribution: a bar chart of POS distribution was drawn using the Matplotlib library
freq_dist = FreqDist(pos_tags)
freq_dist.plot(30, cumulative=False)
plt.show()

# Print out the top five most common POS and their frequencies as well as the top 20 words
print("Top 5 Parts of Speech and their Frequencies:")
for pos, count in top_pos:
    print(f"{pos}: {count}")

print("\nTop 20 Lemmatized Tokens:")
print(top_lemmas)