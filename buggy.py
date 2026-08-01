class Book:
    def __init__(self, title, author, copies):
        self.title = title
        self.author = author
        self.copies = copies

class Library:
    def __init__(self):
        self.inventory = {}

    def add_book(self, book):
        # Adds a book object to the inventory dictionary
        if book.title in self.inventory:
            self.inventory[book.title].copies += book.copies
        else:
            self.inventory[book.title] = book

    def borrow_book(self, title):
        # Checks out a book if available
        if title in self.inventory:
            book = self.inventory[title]
            if book.copies > 0:
                book.copies -= 1
                print(f"Successfully borrowed {title}!")
            else:
                print(f"Sorry, {title} is currently out of stock.")
        else:
            print(f"Error: {title} is not found in our catalog.")

    def return_book(self, title):
        # Returns a borrowed book to the system
        if title in self.inventory:
            self.inventory[title].copies += 1
            print(f"Thank you for returning {title}.")
        else:
            print("We do not accept books that do not belong to us.")

    def display_catalog(self):
        # Prints all books and their current quantities
        print("\n--- Library Catalog ---")
        for title, book in self.inventory.items():
            print(f"Title: {title} | Author: {book.author} | Copies Available: {book.copies}")

    def search_by_author(self, author_name):
        # Finds all books written by a specific author
        results = []
        for book in self.inventory.values():
            if book.author.lower() == author_name.lower():
                results.append(book.title)
        
        if len(results) > 0:
            print(f"\nBooks by {author_name}:")
            for i, title in enumerate(results, start=1):
                print(f"{i}. {title}")
        else:
            print(f"No books found by author: {author_name}")


# --- Testing the System ---

lib = Library()

# Create books
b1 = Book("The Hobbit", "J.R.R. Tolkien", 3)
b2 = Book("1984", "George Orwell", 1)
b3 = Book("Animal Farm", "George Orwell", 2)

# Load library
lib.add_book(b1)
lib.add_book(b2)
lib.add_book(b3)

# Add duplicate book to increase stock
b4 = Book("1984", "George Orwell", 2)
lib.add_book(b4)

# Test borrowing functionality
lib.borrow_book("1984")
lib.borrow_book("1984")
lib.borrow_book("1984") 
lib.borrow_book("1984") # Should fail (out of stock)

# Test returning an unknown book
lib.return_book("Moby Dick") 

# Test search feature
lib.search_by_author("George Orwell")