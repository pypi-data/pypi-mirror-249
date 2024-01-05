import requests

class Book:
    def __init__(self, title, cover_url, isbn, edition_count, authors, first_publish_year):
        self.title = title
        self.cover_url = cover_url
        self.isbn = isbn
        self.edition_count = edition_count
        self.authors = authors
        self.first_publish_year = first_publish_year

    def __str__(self):
        return f"Title: {self.title}\nCover URL: {self.cover_url}\nISBN: {self.isbn}\nEdition Count: {self.edition_count}\nAuthors: {', '.join(self.authors)}\nFirst Publish Year: {self.first_publish_year}"

class OpenLibraryApi:
    def __init__(self, search_term):
        self.api_endpoint = "https://openlibrary.org/search.json"
        self.search_term = search_term

    def search_books(self):
        params = {'q': self.search_term}
        response = requests.get(self.api_endpoint, params=params)

        return response

    def parse_results(self, response):
        if response.status_code == 200:
            data = response.json()
            parsed_results = []

            for work in data.get('docs', []):
                title = work.get('title', 'N/A')
                cover_url = f"https://covers.openlibrary.org/b/id/{work.get('cover_i', 'N/A')}-L.jpg"
                edition_count = work.get('edition_count', 'N/A')
                isbn_list = work.get('isbn', ['N/A'])
                isbn = isbn_list[0] if isbn_list else 'N/A'
                authors = work.get('author_name', ['N/A'])
                first_publish_year = work.get('first_publish_year', 'N/A')

                book = Book(title, cover_url, isbn, edition_count, authors, first_publish_year)
                parsed_results.append(book)

            return parsed_results

        else:
            print(f"Failed to retrieve search results. Status code: {response.status_code}")
            return None
