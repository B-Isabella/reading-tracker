# https://flet.dev/docs/controls/cupertinoappbar/

import flet as ft
import sqlite3

def main(page: ft.Page):
    page.title = "Reading Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.height = 700
    page.window.width = 825

    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        trailing=ft.Icon(ft.Icons.BOOK_OUTLINED),
        middle=ft.Text("Reading Tracker"),
        brightness=ft.Brightness.LIGHT,
    )

    def empty_fields():
        name_field.value = ""
        pages_field.value = ""
        read_pages_field.value = ""
        author_field.value = ""
        book_id.value = ""
        page.update()

    def refresh_table():
        new_table = load_table()
        table_row.controls[0] = new_table
        page.update()

    def add_book(e):
        book_id.visible = False
        page.update()

    def update_book(e):
        book_id.visible = True
        page.update()

    def delete_book(e):
        book_id.visible = True

        conn = sqlite3.connect("reading_tracker.db")
        cursor = conn.cursor()

        book_id_value = book_id.value
        delete = "DELETE FROM Books WHERE idBooks = ?"
        parametros = (book_id_value,)
        cursor.execute(delete, parametros)
        conn.commit()
        conn.close()

        empty_fields()
        refresh_table()

    def submit(e):
        conn = sqlite3.connect("reading_tracker.db")
        cursor = conn.cursor()

        name = name_field.value
        pages = pages_field.value
        read_pages = read_pages_field.value
        author = author_field.value

        add_author = "INSERT OR IGNORE INTO Authors (name) VALUES (?);"
        parameters = (author,)
        cursor.execute(add_author, parameters)

        if book_id.value:
            book_id_value = book_id.value
            update = """
                     UPDATE Books
                     SET title = ?, pages = ?, read = ?, idAuthor = (SELECT idAuthor FROM Authors WHERE name = ?)
                     WHERE idBooks = ?;
                     """
            parametros = (name, pages, read_pages, author, book_id_value)
            cursor.execute(update, parametros)
        else:
            insert = """
                     INSERT INTO Books (title, pages, read, idAuthor)
                     VALUES (?, ?, ?, (SELECT idAuthor FROM Authors WHERE name = ?));
                     """
            parametros = (name, pages, read_pages, author)
            cursor.execute(insert, parametros)

        conn.commit()
        conn.close()

        empty_fields()
        refresh_table()

    def load_table():
        conn = sqlite3.connect("reading_tracker.db")
        cursor = conn.cursor()
        query = "SELECT Books.idBooks AS 'ID', Books.title AS 'Title', Books.pages AS 'Pages', Books.read AS 'Read Pages', Authors.name AS 'Author' " \
                "FROM Books JOIN Authors ON Books.idAuthor = Authors.idAuthor;"
        cursor.execute(query)
        columns = cursor.description
        results = cursor.fetchall()

        book_columns = [ft.DataColumn(ft.Text(column[0])) for column in columns]
        book_table = ft.DataTable(columns=book_columns)
        for idBooks, title, pages, read, author in results:
            book_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(idBooks)),
                    ft.DataCell(ft.Text(title)),
                    ft.DataCell(ft.Text(pages)),
                    ft.DataCell(ft.Text(read)),
                    ft.DataCell(ft.Text(author))
                ])
            )

        conn.close()
        return book_table

    name_field = ft.TextField(label="Book title")
    pages_field = ft.TextField(label="Number of pages")
    read_pages_field = ft.TextField(label="Pages read")
    author_field = ft.TextField(label="Author name")
    book_id = ft.TextField(label="ID: ", visible=False, width=90)

    add_button = ft.ElevatedButton("Add Book", icon=ft.Icons.ADD, on_click=add_book)
    update_button = ft.ElevatedButton("Update Book", icon=ft.Icons.UPDATE, on_click=update_book)
    delete_button = ft.ElevatedButton("Delete Book", icon=ft.Icons.DELETE, on_click=delete_book)
    submit_button = ft.ElevatedButton("Submit", icon=ft.Icons.CHECK, on_click=submit)

    table = load_table()
    table_row = ft.Row([table], alignment=ft.MainAxisAlignment.CENTER)

    page.add(ft.Row([add_button, update_button, delete_button],
                    alignment=ft.MainAxisAlignment.CENTER),
             ft.Row([name_field, author_field, book_id],
                    alignment=ft.MainAxisAlignment.START),
             ft.Row([pages_field, read_pages_field, submit_button], alignment=ft.MainAxisAlignment.START),
             table_row)

ft.app(target=main, assets_dir="assets")