# OpenLibraryApi

OpenLibraryapi is a Python library for interacting with the Open Library API. It allows you to search for books and retrieve information about them.

# Features

Search for books using the Open Library API.
Retrieve information about each book, including title, cover URL, ISBN, edition count, authors, and first publish year.

# Installation

pip install openlibraryapi

#Usage Example: 

from openlibrarypy import OpenLibraryApi

# Create an instance of OpenLibraryApi with a search term

search_term = "The Lord of the Rings"
open_library_instance = OpenLibraryApi(search_term)

# Search for books

search_results = open_library_instance.search_books()

if search_results:
    # Parse and print information about each book
    parsed_results = open_library_instance.parse_results(search_results)

    if parsed_results:
        for book in parsed_results:
            print("Book Information:")
            print(book)
            print("\n")
    else:
        print("No books found.")
else:
    print("Failed to retrieve search results.")

