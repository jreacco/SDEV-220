from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    publisher = db.Column(db.String(80), nullable=False)

@app.route('/')
def index():
    return "Hello, welcome to the Book API!"

@app.route('/book', methods=['POST'])
def add_book():
    book_data = request.get_json()
    new_book = Book(
        book_name=book_data['book_name'],
        author=book_data['author'],
        publisher=book_data['publisher']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"})

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append({
            'id': book.id,
            'book_name': book.book_name,
            'author': book.author,
            'publisher': book.publisher
        })
    return jsonify(books_list)

@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    book_data = request.get_json()
    book.book_name = book_data['book_name']
    book.author = book_data['author']
    book.publisher = book_data['publisher']
    db.session.commit()
    return jsonify({"message": "Book updated successfully!"})

@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
