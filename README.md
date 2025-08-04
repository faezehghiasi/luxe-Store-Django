# 💎 LUXE – Django E-commerce Website

LUXE is a stylish online jewelry store built with Django. It includes a full shopping experience from product browsing to checkout and payment integration using Zarinpal.

## 🌟 Features

- ✅ User registration with email verification
- 🔐 Secure login/logout system
- 🛒 Product browsing and shopping cart
- 💳 Checkout process with Zarinpal payment gateway
- 📦 Order confirmation and invoice
- 📧 Email notifications for verification and order confirmation
- 🎨 Responsive frontend design
- 🌍 **Multi-language support (English & Persian)**
- 🔄 **Dynamic language switching**
- 📝 **Complete UI translations**

## 🛠️ Tech Stack

- **Backend**: Django 5+
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: SQLite (development)
- **Payment Gateway**: [Zarinpal](https://www.zarinpal.com)
- **Email**: Django email backend (SMTP)
- **Internationalization**: Django i18n with custom middleware

## 🧾 Project Structure

```
store/
├── account/           # Handles user registration, login, email verification
├── core/              # Main e-commerce logic: products, cart, checkout
├── media/             # Uploaded images (e.g. product covers)
├── templates/         # HTML templates for all views
├── locale/            # Translation files (English & Persian)
└── store/             # Django project settings
```

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/faezehghiasi/luxe-Store-Django.git
cd luxe-Store-Django
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure .env (optional)

Set up your environment variables (email backend, secret key, Zarinpal config).

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 💸 Zarinpal Integration

The project is integrated with Zarinpal sandbox for payment. You can configure the merchant ID and environment in settings.

## 📬 Email Verification

Users must verify their email before logging in. Make sure you have a working email backend set in `settings.py` for this to work.

## 🌍 Internationalization (i18n)

The website supports multiple languages with dynamic language switching:

### Supported Languages
- **English** (default)
- **Persian/Farsi** (فارسی)

### Features
- **Dynamic Language Switching**: Users can switch languages using the language switcher in the header
- **Complete UI Translations**: All text content, form labels, buttons, and navigation elements are translated
- **Session-based Language Persistence**: Language preference is saved in user session
- **Custom Middleware**: Optimized language detection and activation

### Translation Files
- Location: `locale/fa/LC_MESSAGES/django.po`
- Compiled files: `locale/fa/LC_MESSAGES/django.mo`

### Adding New Translations
1. Add `{% trans "Your text" %}` tags to templates
2. Run: `python manage.py makemessages -l fa`
3. Edit the `.po` file with translations
4. Compile: `python manage.py compilemessages`

### Testing Translations
- Visit `/test/translation/` to see all translations in action
- Use the language switcher in the header to test dynamic switching

## 📷 Screenshots


## 👤 Author

- Faezeh Ghiasi – [GitHub](https://github.com/faezehghiasi)

