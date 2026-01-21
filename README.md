# Photo App (work-in-progress)

Small Django social app where people register, drop photos, like, and comment. It is still rough around the edges but already usable for local tinkering.

## What lives here
- Users with profile photos stored under MEDIA_ROOT, created automatically when a user is made. See [socialproject/users/models.py](socialproject/users/models.py).
- Posts with images, captions, unique slugs, likes, and comments. See [socialproject/posts/models.py](socialproject/posts/models.py).
- Tailwind-based styling with a simple npm build script in [socialproject/package.json](socialproject/package.json).

## Quick start (Windows / PowerShell)
1) Clone and jump in
   - `git clone <repo-url>`
   - `cd social`

2) Virtualenv
   - `python -m venv venv`
   - `.\venv\Scripts\Activate`

3) Install deps
   - Python: `pip install -r requirements.txt`
   - JS: `npm install` (Tailwind 2.2.x)

4) Local settings to keep secrets out of git (optional but recommended)
   - copy `.env.example` to `.env` and set your own values. At minimum:
     ```env
     SECRET_KEY=change-me
     DEBUG=True
     ```
   - switch settings to read from env before production; current default key is baked into [socialproject/socialproject/settings.py](socialproject/socialproject/settings.py#L15).

5) DB and admin
   - `python manage.py migrate`
   - `python manage.py createsuperuser`

6) Build CSS (one-off)
   - `npm run build` (writes to users/static/users/styles.css)

7) Run the dev server
   - `python manage.py runserver`
   - hit http://127.0.0.1:8000/

## Dev habits and gotchas
- Media uploads land in `media/`; keep it out of git (already ignored). Delete old test uploads occasionally.
- `staticfiles/` is collectstatic output. It is ignored but already in the tree; you can prune and rebuild if it gets noisy.
- Slugs are auto-generated on save; duplicate titles will get a suffix.
- Likes are unique per user/post; trying to like twice should raise an integrity error rather than double-count.
- Profile objects are created via signals; if you import users without signals, call `Profile.objects.get_or_create(user=...)` to backfill.

## Things to improve soon
- Move SECRET_KEY and DEBUG to environment variables and add a sample settings override.
- Add a `make dev` or simple PowerShell script for repeatable setup.
- Replace the baked Tailwind build with a watch script (`npm run dev`) for live CSS reloads.
- Write tests around likes/comments and auth flows; the test modules are mostly empty.
- Trim the tracked `staticfiles/` and rely on collectstatic output only.

## Rough project map
- Settings: [socialproject/socialproject/settings.py](socialproject/socialproject/settings.py)
- URLConf: [socialproject/socialproject/urls.py](socialproject/socialproject/urls.py)
- Users app: [socialproject/users](socialproject/users)
- Posts app: [socialproject/posts](socialproject/posts)
- Tailwind input: [socialproject/users/static/users/tw.css](socialproject/users/static/users/tw.css)
- Built CSS target: `users/static/users/styles.css` (gitignored output is `tw-built.css`)