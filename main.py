import json
from typing import Optional, Dict, Any


class Book:
    """Класс, представляющий книгу в библиотеке."""

    STATUS_YES: str = "в наличии"
    STATUS_NO: str = "выдана"

    def __init__(self, title: str, author: str, year: int) -> None:
        """Инициализация объекта Book."""
        self.title = title  # название книги
        self.author = author  # автор книги
        self.year = year  # год издания книги
        self._id: Optional[int] = None  # пока книга не в библиотеке - у нее нет id
        self._status: Optional[str] = None  # пока книга не в библиотеке - у нее нет статуса

    @property
    def title(self) -> str:  # геттер свойства title
        """Возвращает название книги."""
        return self._title

    @title.setter
    def title(self, value: str) -> None:  # сеттер свойства title
        """Устанавливает название книги."""
        if not isinstance(value, str):
            raise ValueError("Название книги должно быть в формате строки.")
        self._title = value

    @property
    def author(self) -> str:  # геттер свойства author
        """Возвращает автора книги."""
        return self._author

    @author.setter
    def author(self, value: str) -> None:  # сеттер свойства author
        """Устанавливает автора книги."""
        if not isinstance(value, str):
            raise ValueError("Имя автора должно быть в формате строки.")
        if value.isdigit():
            raise ValueError("Имя автора не может состоять из цифр.")
        self._author = value

    @property
    def year(self) -> int:  # геттер свойства year
        """Возвращает год издания книги."""
        return self._year

    @year.setter
    def year(self, value: int) -> None:  # сеттер свойства year
        """Устанавливает год издания книги."""
        if not isinstance(value, int):
            raise ValueError("Год издания книги должен быть числом")
        self._year = value

    @property
    def id(self) -> int:  # геттер свойства id
        """Возвращает идентификатор книги."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:  # сеттер свойства id
        """Устанавливает идентификатор книги."""
        if value is not None and not isinstance(value, int):
            raise ValueError("ID должно быть числом")
        self._id = value

    @property
    def status(self) -> str:  # геттер свойства status
        """Возвращает статус книги."""
        return self._status

    @status.setter
    def status(self, value: str) -> None:  # сеттер свойства status
        """Устанавливает статус книги."""
        if value is not None and value not in (Book.STATUS_YES, Book.STATUS_NO):
            raise ValueError(f"Неверный статус: статус может быть либо '{Book.STATUS_YES}', либо '{Book.STATUS_NO}'")
        self._status = value

    def to_dict(self) -> dict:
        """Преобразует объект Book в словарь."""
        return {
            'id': self._id,
            'title': self._title,
            'author': self._author,
            'year': self._year,
            'status': self._status
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """Создает объект Book из словаря."""
        book = cls(data['title'], data['author'], data['year'])
        book.id = data['id']
        book.status = data['status']
        return book

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта Book."""
        return (f"ID: {self._id}, "
                f"Title: {self._title}, "
                f"Author: {self._author}, "
                f"Year: {self._year}, "
                f"Status: {self._status}")


class Library:
    """Класс, представляющий библиотеку, которая управляет коллекцией книг."""

    def __init__(self) -> None:
        """Инициализация объекта Library."""
        self.books = []  # список книг в библиотеке
        self.next_id = 1  # следующий доступный идентификатор для новой книги

    def add_book(self, title: str, author: str, year: int) -> 'Book':
        """Добавляет новую книгу в библиотеку."""
        book = Book(title, author, year)
        book.id = self.next_id
        book.status = Book.STATUS_YES
        self.books.append(book)
        self.next_id += 1
        return book

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу из библиотеки по её идентификатору."""
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]
        return len(self.books) < initial_length

    def find_books(self, title: str = None, author: str = None, year: int = None) -> list:
        """Находит книги в библиотеке по заданным критериям."""
        result = []
        for book in self.books:
            if (title is None or book.title == title) and \
                    (author is None or book.author == author) and \
                    (year is None or book.year == year):
                result.append(book)
        return result

    def display_books(self) -> None:
        """Выводит информацию о всех книгах в библиотеке."""
        if self.books:
            for idx, book in enumerate(self.books, start=1):
                print(f"{idx}. {book}")
        else:
            print('Пока в библиотеке отсутствуют книги.')

    def change_status(self, book_id: int) -> bool:
        """Изменяет статус книги по её идентификатору."""
        for book in self.books:
            if book.id == book_id:
                if book.status == Book.STATUS_YES:
                    book.status = Book.STATUS_NO
                elif book.status == Book.STATUS_NO:
                    book.status = Book.STATUS_YES
                else:
                    raise ValueError("Неизвестный статус книги")
                return True
        return False

    def save_to_json(self, filename: str) -> None:
        """Сохраняет текущее состояние библиотеки в JSON файл."""
        data = {
            'next_id': self.next_id,
            'books': [book.to_dict() for book in self.books]
        }
        filename = f"{filename}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename: str) -> None:
        """Загружает состояние библиотеки из JSON файла."""
        filename = f"{filename}.json"
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.next_id = data['next_id']
            self.books = [Book.from_dict(book_data) for book_data in data['books']]

    def save_to_text(self, filename: str) -> None:
        """Сохраняет текущее состояние библиотеки в текстовый файл."""
        filename = f"{filename}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"{self.next_id}\n")
            for book in self.books:
                f.write(f"{book.id}|{book.title}|{book.author}|{book.year}|{book.status}\n")

    def load_from_text(self, filename: str) -> None:
        """Загружает состояние библиотеки из текстового файла."""
        filename = f"{filename}.txt"
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            self.next_id = int(lines[0].strip())
            self.books = []
            for line in lines[1:]:
                parts = line.strip().split('|')
                book = Book(parts[1], parts[2], int(parts[3]))
                book.id = int(parts[0])
                book.status = parts[4]
                self.books.append(book)


def main():
    """Основная функция для управления библиотекой через консольный интерфейс."""
    library = Library()  # Создание экземпляра библиотеки

    while True:
        print("\nСистема управления библиотекой")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Сохранить библиотеку в JSON")
        print("7. Загрузить библиотеку из JSON")
        print("8. Сохранить библиотеку в текстовый файл")
        print("9. Загрузить библиотеку из текстового файла")
        print("10. Выйти\n")

        choice = input("Выберите действие: ")

        if choice == '1':
            # Добавление новой книги
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания книги: "))
            except ValueError:
                print("Год издания книги должен быть числом.")
                continue

            try:
                result = library.add_book(title, author, year)
            except ValueError as e:
                print(e)
            else:
                print(f"Книга '{result.title}' (автор: {result.author}) {result.year} года издания "
                      f"успешно добавлена в библиотеку.")

        elif choice == '2':
            # Удаление книги по ID
            try:
                book_id = int(input("Введите ID книги для удаления: "))
            except ValueError:
                print("ID должно быть числом.")
                continue
            if library.remove_book(book_id):
                print("Книга с указанным ID удалена из библиотеки.")
            else:
                print("Книга с указанным ID отсутствует в библиотеке.")

        elif choice == '3':
            # Поиск книги по критериям
            print("Поиск книги по:")
            print("1. Названию")
            print("2. Автору")
            print("3. Году издания")

            search_choice = input("Выберите критерий поиска: ")
            if search_choice == '1':
                title = input("Введите название книги: ")
                books = library.find_books(title=title)
            elif search_choice == '2':
                author = input("Введите автора книги: ")
                books = library.find_books(author=author)
            elif search_choice == '3':
                try:
                    year = int(input("Введите год издания книги: "))
                except ValueError:
                    print("Год должен быть целым положительным числом.")
                    continue
                books = library.find_books(year=year)
            else:
                print("Неверный выбор.")
                continue

            if books:
                print(f"По указанному критерию найдено следующее количество книг: {len(books)}", f"А именно:", sep='\n')
                for idx, book in enumerate(books, start=1):
                    print(f"{idx}. {book}")
            else:
                print("Книги по указанному критерию не найдены.")

        elif choice == '4':
            # Отображение всех книг в библиотеке
            library.display_books()

        elif choice == '5':
            # Изменение статуса книги по ID
            try:
                book_id = int(input("Введите ID книги для изменения статуса: "))
            except ValueError:
                print("ID должно быть числом.")
                continue
            if library.change_status(book_id):
                print("Статус книги с указанным ID изменен.")
            else:
                print("Книга с указанным ID отсутствует в библиотеке.")

        elif choice == '6':
            # Сохранение библиотеки в JSON файл
            filename = input("Введите имя файла (без расширения) для сохранения в JSON: ")
            library.save_to_json(filename)
            print(f"Библиотека успешно сохранена в файл {filename}.json.")

        elif choice == '7':
            # Загрузка библиотеки из JSON файла
            filename = input("Введите имя файла (без расширения) для загрузки из JSON: ")
            try:
                library.load_from_json(filename)
            except FileNotFoundError:
                print('Указанный JSON-файл отсутствует')
            else:
                print(f"Библиотека успешно загружена из файла {filename}.json.")

        elif choice == '8':
            # Сохранение библиотеки в текстовый файл
            filename = input("Введите имя файла (без расширения) для сохранения в текстовый формат: ")
            library.save_to_text(filename)
            print(f"Библиотека успешно сохранена в файл {filename}.txt.")

        elif choice == '9':
            # Загрузка библиотеки из текстового файла
            filename = input("Введите имя файла (без расширения) для загрузки из текстового формата: ")
            try:
                library.load_from_text(filename)
            except FileNotFoundError:
                print('Указанный текстовый файл отсутствует')
            else:
                print(f"Библиотека успешно загружена из файла {filename}.txt.")

        elif choice == '10':
            # Выход из программы
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 10.")


# Проверка, запущен ли скрипт напрямую (а не импортирован как модуль)
if __name__ == "__main__":
    main()  # Вызов основной функции, если скрипт запущен напрямую
