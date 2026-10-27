# Rory's Library — Complete Django Project with Chapter 4

This package is based on the supplied Carbid(1).zip. The existing project, SQLite database, media files, models, book catalogue, and Chapters 1–3 work have been retained. The original Windows `myenv` was deliberately excluded: virtual environments are machine-specific and would add thousands of unnecessary files.

## Chapter 4 additions
- Register users with Django's UserCreationForm and required email.
- Login, logout (secure POST), profile, password change, password reset.
- Automatically assign newly registered users to the **Member** group.
- Create **Member** and **Librarian** groups with Django permissions using `setup_roles`.
- Only librarians (or other users with relevant permissions) can add, edit, delete or toggle book availability.
- Hide restricted action links from other users.
- Automated role and registration tests.

## Windows Git Bash setup
1. Unzip this package, open `Carbid/django-textbook` in Git Bash.
2. Activate your existing `myenv` if you already have one in the original project: `source myenv/Scripts/activate`. Otherwise create one using your installed Python: `python -m venv myenv` then `source myenv/Scripts/activate`.
3. Install Django and Pillow: `python -m pip install 'Django>=5.2,<7' Pillow`.
4. Run `python manage.py migrate`.
5. Run `python manage.py setup_roles`.
6. Run `python manage.py test library`.
7. Run `python manage.py runserver`.
8. Open http://127.0.0.1:8000/ to view the catalogue.

## Important routes
- `/` catalogue homepage
- `/register/` new member registration
- `/accounts/login/` login
- `/accounts/logout/` POST-only logout (use the navbar button)
- `/profile/` logged-in user's profile
- `/accounts/password_change/` change password
- `/accounts/password_reset/` password reset (emails print in development console)
- `/books/add/` add book (Librarian)
- `/admin/` admin panel

## Assigning the Librarian role
Log into `/admin/` with a superuser, open Users, select a user, and add them to the **Librarian** group. If you have no admin account, run `python manage.py createsuperuser`. Users signing up through `/register/` become Members.

## Understanding Chapter 4
**Authentication** verifies identity: users register, log in, log out, and change or reset their passwords. Django handles hashed passwords and sessions.

**Authorization** determines what a logged-in user may do. The Member group has `view_book` permission; Librarians get book create/change/delete plus author, publisher and category management permissions.

**View protection** is enforced on the server. Anonymous visitors are sent to the login page; authenticated Members without book-editing permissions receive HTTP 403 when trying to modify books. Merely hiding buttons is not security, so the views also check permissions.

**Templates** use `{% csrf_token %}` for POST forms, and `{% if perms.library.change_book %}` etc. for conditional action links.

**Password reset** uses Django's development console email backend. It prints a reset link in the terminal instead of sending a real email. Set up a production email service before deploying.

**Production note:** The supplied project's DEBUG=True and development secret-key fallback are not suitable for deployment. Configure HTTPS, ALLOWED_HOSTS, secure secret keys, and email service before publishing online.

## Files updated
`my_first_project/settings.py`, `my_first_project/urls.py`, `library/forms.py`, `library/views.py`, `library/urls.py`, `library/tests.py`, `library/templates/library/base.html`, `library/templates/library/home.html`, `library/templates/library/book_detail.html`.

## Files added
`library/templates/library/register.html`, `library/templates/library/profile.html`, `templates/registration/*`, `library/management/commands/setup_roles.py`.

The supplied Chapter 4 reference documents are included at the package root for study.
