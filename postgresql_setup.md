# PostgreSQL Setup Guide

## Install PostgreSQL on Ubuntu

1. **Install PostgreSQL:**
   ```bash
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   ```

2. **Start PostgreSQL service:**
   ```bash
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

3. **Create database and user:**
   ```bash
   sudo -u postgres psql
   ```
   
   In the PostgreSQL prompt:
   ```sql
   CREATE DATABASE storedb;
   CREATE USER storeuser WITH PASSWORD 'storepass';
   GRANT ALL PRIVILEGES ON DATABASE storedb TO storeuser;
   \q
   ```

4. **Update Django settings:**
   Change the DATABASES configuration in `store/store/settings.py`:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'storedb',
           'USER': 'storeuser',
           'PASSWORD': 'storepass',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Install psycopg2:**
   ```bash
   source venv/bin/activate
   pip install psycopg2-binary
   ```

6. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## Recommendation

For development, **stick with SQLite** as it's:
- Easier to set up
- No additional dependencies
- Perfect for development and testing
- File-based (no server needed)

Only use PostgreSQL when you're ready for production deployment. 