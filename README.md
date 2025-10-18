# Photo App (social)

Simple Django photo-sharing project (development). Contains users, posts, Tailwind static assets and AJAX interactions.

## Prerequisites
- Python 3.8+ (use the version installed for the project)
- Node.js + npm (for Tailwind build)
- Git

## Quick start (Windows / PowerShell)
1. Clone repo
   - git clone <repo-url>

2. Create and activate venv
   - python -m venv venv
   - .\venv\Scripts\Activate

3. Install Python dependencies
   - pip install -r requirements.txt
   (If there is no requirements.txt, install Django, Pillow, etc. manually.)

4. Migrate database
   - python manage.py migrate

5. Create superuser (or change password)
   - python manage.py createsuperuser
   - OR: python manage.py changepassword <username>

6. Build Tailwind CSS (example)
   - npx tailwindcss -i ./users/static/users/tw.css -o ./users/static/users/tw-built.css --watch
   - Link the built CSS (`tw-built.css`) in templates (or adjust static files as needed)

7. Collect static (optional for deployment)
   - python manage.py collectstatic

8. Run development server
   - python manage.py runserver
   - Visit http://127.0.0.1:8000/

## Notes
- The password change page requires authentication. Ensure `LOGIN_URL = 'login'` is set in settings.
- Logout should be POST to remain secure — use a form with a submit button styled as a link.
- AJAX endpoints (e.g., likes) must accept POST and validate CSRF token. Example hit: `/posts/like`.
- Uploaded media files are stored in `media/` (add to .gitignore). Configure MEDIA_ROOT and MEDIA_URL in settings.

## Troubleshooting
- If Tailwind classes appear as directives in browser, ensure you run the Tailwind build and include the built CSS file.
- If `collectstatic` errors about STATIC_ROOT, set `STATIC_ROOT = BASE_DIR / 'staticfiles'` (or similar) in settings.
- To reset a user's password when you cannot remember it, use `python manage.py changepassword <username>` or set it in the shell:
  ```py
  from django.contrib.auth import get_user_model
  User = get_user_model()
  u = User.objects.get(username='youruser')
  u.set_password('NewPass123')
  u.save()
  ```

## Project structure (important paths)
- Project root: d:\Programming\Django\Projects\social
- Django settings: socialproject/socialproject/settings.py
- Users app templates: users/templates/users/
- Posts app templates: posts/templates/posts/
- Static source for Tailwind: users/static/users/tw.css
- Built Tailwind output (recommended): users/static/users/tw-built.css

Feel free to ask for a requirements.txt or a startup script for Tailwind/Dev server.