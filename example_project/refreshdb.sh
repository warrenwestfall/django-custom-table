#!/bin/bash
rm db.sqlite3
rm -rf example_app/migrations/*
python3 manage.py makemigrations example_app
python3 manage.py migrate
python3 manage.py create_admin_user 
python3 manage.py create_test_data
