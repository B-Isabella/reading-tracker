import flet as ft
import sqlite3

conn = sqlite3.connect("reading_tracker.db")
 
cursor = conn.cursor()
 
createAuthorsTable = """
                     CREATE TABLE IF NOT EXISTS Authors(
                     idAuthor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                     name TEXT NOT NULL
                     );
                     """

createBooksTable = """
                    CREATE TABLE IF NOT EXISTS Books(
                    idBooks INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    idAuthor INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    pages INTEGER NOT NULL,
                    read INTEGER NOT NULL,
                    image TEXT,
                    FOREIGN KEY (idAuthor) REFERENCES Authors(idAuthor)
                    );
                    """
 
cursor.execute(createAuthorsTable)
cursor.execute(createBooksTable)
conn.close()

def main(page: ft.Page):
    page.title = "Reading Tracker"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.appbar = ft.CupertinoAppBar(
        leading=ft.Icon(ft.Icons.BOOK_OUTLINED),
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        trailing=ft.Icon(ft.Icons.BOOK_OUTLINED),
        middle=ft.Text("Reading Tracker"),
        brightness=ft.Brightness.LIGHT,
    )

    add_button = ft.ElevatedButton("Add Book", icon = ft.Icons.ADD)
    see_button = ft.ElevatedButton("See Books", icon = ft.Icons.VIEW_LIST)
    update_button = ft.ElevatedButton("Update Book", icon = ft.Icons.UPDATE)
    delete_button = ft.ElevatedButton("Delete Book", icon = ft.Icons.DELETE)

    page.add(ft.Row([add_button, see_button, update_button, delete_button], alignment=ft.MainAxisAlignment.CENTER))
    
ft.app(target = main, assets_dir="assets")