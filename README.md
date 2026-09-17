# Student Register — Backend (Django REST Framework)

Pairs with the Student Register dashboard. Implements the REST API in the
SOP's table 7.6, using `students` as the resource name.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations students
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

The API is now live at `http://127.0.0.1:8000/api/students/`.

## Endpoints

| Operation | Method | Endpoint                  | Notes                                   |
|-----------|--------|----------------------------|------------------------------------------|
| Create    | POST   | `/api/students/`           | body: roll_no, name, email, course, year, status |
| Read all  | GET    | `/api/students/`           | `?search=`, `?course=`, `?status=` filters |
| Read one  | GET    | `/api/students/{id}/`      |                                           |
| Update    | PUT    | `/api/students/{id}/`      | full replace                             |
| Update    | PATCH  | `/api/students/{id}/`      | partial update                           |
| Delete    | DELETE | `/api/students/{id}/`      |                                           |

## Validation

- `roll_no` is required, unique (case-insensitive), and limited to letters/numbers/hyphens.
- `name` is required and cannot be blank/whitespace-only.
- `email` must be a valid email format if provided.
- `year` is restricted to 1–4 via model choices.
- All of the above are enforced server-side in `serializers.py`, independent of
  whatever validation the frontend does — matching the SOP's requirement that
  server-side validation exists even when client-side validation is present.

## Connecting the dashboard to this API

The published dashboard currently stores data in the browser (`localStorage`)
so it works standalone with no backend running. To wire it to this API instead,
replace the `load()`/`save()`/`performDelete()`/form-submit logic with `fetch`
calls to these endpoints (as the SOP's section 7.7 describes), e.g.:

```js
fetch("http://127.0.0.1:8000/api/students/")
  .then(r => r.json())
  .then(data => { students = data.results || data; render(); });
```

Remember to keep `CORS_ALLOWED_ORIGINS` in `settings.py` in sync with wherever
the frontend is served from.

## Testing

Use Postman (or `curl`) against each endpoint with valid, missing, duplicate,
and invalid data, per SOP section 10 — e.g.:

```bash
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Content-Type: application/json" \
  -d '{"roll_no":"CS-103","name":"Jordan Lee","email":"jordan@example.edu","course":"B.Sc Computer Science","year":1,"status":"active"}'
```
