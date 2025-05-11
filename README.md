# README

- DON'T RENAME AND DELETE FOLDER OR FILES
- except in api/templates/api, api/urls.py, api/views.py

## urls.py is path page website CAN EDIT

- urls.py in api/templates/api not in mysite/urls.py

## HOW START SERVER, WEBSITE, CSS OF TAILWIND

### Please-do-step-by-step

Open command prompt and type:
    python manage.py tailwind start

Open a new command prompt and type:
    python manage.py runserver

## HOW Change or Update Database

Open a command prompt and type:
    โดย Django จะมี 2 คำสั่งในขั้นตอนนี้คือ
        Migrations: คือการอัปเดตฐานข้อมูลให้เป็นปัจจุบัน (แต่ตอนนี้ข้อมูลยังไม่ได้อัปเดตในฐานข้อมูล)
        Migrate: คือการส่งฐานข้อมูลของเราไปอัปเดตที่ฐานข้อมูลจริง ๆ

### UPDATE DataBase

    python manage.py makemigrations
    python manage.py migrate

### CREATE USER(Role Admin)

python manage.py createsuperuser

### UPDATE Requirements Libraries

pip freeze > requirements.txt
