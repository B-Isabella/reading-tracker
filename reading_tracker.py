import flet as ft

def main(page: ft.Page):
    page.title = "Reading Tracker"
    
ft.app(target = main, assets_dir="assets")