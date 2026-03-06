import json
import os

stack_icons = {
    "Python 3.11": "fab fa-python",
    "Django 4.2": "fab fa-python",
    "Django 5": "fab fa-python",
    "MySQL": "fas fa-database",
    "PostgreSQL 15": "fas fa-database",
    "PostgreSQL": "fas fa-database",
    "MySQL 8": "fas fa-database",
    "SQLite": "fas fa-database",
    "OpenAI API": "fas fa-robot",
    "Bitrix24 REST API": "fas fa-plug",
    "Bitrix24 API": "fas fa-plug",
    "Maxma API": "fas fa-plug",
    "Teletrack API": "fas fa-plug",
    "AGBIS API": "fas fa-plug",
    "AmoCRM API": "fas fa-plug",
    "Speech2Text API": "fas fa-microphone",
    "Redis": "fas fa-memory",
    "Nginx": "fas fa-server",
    "Docker": "fab fa-docker",
    "Docker SDK": "fab fa-docker",
    "Debian 11": "fab fa-linux",
    "Ubuntu 24": "fab fa-ubuntu",
    "REST": "fas fa-exchange-alt",
    "Websockets": "fas fa-network-wired",
    "Pyrogram 2": "fab fa-telegram",
    "Telegram API": "fab fa-telegram",
    "Blockchain": "fas fa-link",
    "Symfony": "fab fa-php",
    "PHP": "fab fa-php",
    "PHP 8.1": "fab fa-php",
    "PHP 8.2": "fab fa-php",
    "PHP 8.4.1": "fab fa-php",
    "Filament": "fab fa-laravel",
    "Laravel": "fab fa-laravel",
    "Laravel 10": "fab fa-laravel",
    "Laravel 11": "fab fa-laravel",
    "Laravel 12": "fab fa-laravel",
    "C# .NET Framework 8": "fab fa-cuttlefish",
    "RestoFrontAPI 8": "fas fa-code",
    "Unity 2021": "fa-brands fa-unity",
    "Unity 2023": "fa-brands fa-unity",
    "Java SDK": "fab fa-java",
    "Unity 6": "fa-brands fa-unity",
    "C# 8.0": "fab fa-cuttlefish",
}


def lang_file(lang: str, file: str):
    return f"content/{lang}/{file}"


def load_lang_file(lang: str, file: str):
    file_path = lang_file(lang, file)
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def load_projects(lang, skip=None):

    filters = []
    projects = load_lang_file(lang, "projects.json")

    for project in projects:
        project["id"] = project.get('title', "").lower().replace(" ", "-")
        pictures_folder = project.get("pictures", "")

        if pictures_folder:
            picture_path = f"static/pictures/{pictures_folder}"
            if os.path.exists(picture_path):
                project["images"] = [
                    f"/static/pictures/{pictures_folder}/{img}"
                    for img in sorted(os.listdir(picture_path))
                    if img.endswith('.webp')
                ]
                project["image_count"] = len(project["images"])
            else:
                project["images"] = []
        else:
            project["images"] = []

        stack = project.get("stack", [])
        if stack:
            project["stack"] = [
                {
                    "name": item,
                    "icon": stack_icons.get(item)
                } for item in stack
            ]

        project_filter = project.get('filter', None)
        if project_filter and project_filter not in filters:
            filters.append(project_filter)

    if not skip:
        skip = []
    return [p for p in projects if p['id'] not in skip], filters