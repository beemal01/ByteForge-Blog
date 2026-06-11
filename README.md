# ByteForge Blog

A professional backend engineering blog platform built with Django REST Framework, featuring JWT authentication, rich text editing, and a modern tech-focused UI.

## What This Project Does

ByteForge is a full-stack blog application where developers can:

- **Write and publish** technical articles with rich text formatting
- **Share code snippets** and backend insights
- **Manage posts** with full CRUD operations
- **Authenticate securely** via email/password with OTP verification

---

## Tech Stack

### Backend (Python/Django)

| Technology | Purpose |
| --- | --- |
| **Django 6.0** | Web framework |
| **Django REST Framework** | API endpoints for blog posts |
| **SimpleJWT** | Token-based authentication |
| **SQLite** | Database (configurable) |

### Frontend

| Technology | Purpose |
| --- | --- |
| **Bootstrap 5** | Responsive CSS framework |
| **Quill.js** | Rich text editor for blog content |
| **Vanilla JavaScript** | Client-side interactions |

---

## Project Structure

```text
SecureBlog/
├── authAccount/          # User authentication app
│   ├── models.py       # Custom user model with email auth
│   ├── views.py        # Auth API endpoints (signup, login, OTP)
│   ├── serializers.py  # Request validation & JWT token generation
│   └── urls.py         # Auth routes (/api/signupview, /api/loginview, etc.)
│
├── tweetBlog/            # Blog content app
│   ├── models.py       # Blog post model (content)
│   ├── views.py        # Blog API endpoints (CRUD)
│   ├── serializers.py  # Blog serializer
│   └── urls.py         # Blog routes (/api/blogview, /createpost/, etc.)
│
├── systemBlog/           # Project configuration
│   ├── settings.py     # Django settings, JWT config
│   └── urls.py         # Main URL router
│
├── templates/            # HTML templates
│   ├── base.html       # Base layout (nav, footer)
│   ├── index.html      # Homepage with post list
│   ├── inner_post.html # Single post view
│   ├── createPost.html # New post form
│   ├── update_post.html# Edit post form
│   ├── signin.html     # Login page
│   ├── signup.html     # Registration page
│   └── otp.html        # OTP verification page
│
├── static/
│   ├── style.css       # Professional dark navy + cyan + indigo theme
│   └── script.js       # Frontend logic (auth, CRUD operations)
│
└── media/              # Uploaded images storage
```

---

## Backend Architecture

### Authentication Flow

1. **Registration** → User submits email/name/password
2. **OTP Generation** → Random 6-digit code stored in user model
3. **Email Verification** → OTP sent via SMTP (configure in settings)
4. **JWT Tokens** → Access token (1 day) + Refresh token (7 days)

### API Endpoints

| Endpoint | Method | Auth | Description |
| --- | --- | --- | --- |
| `/api/signupview/` | POST | No | Create user, send OTP |
| `/api/otpview/` | POST | No | Verify OTP, activate account |
| `/api/loginview/` | POST | No | Get JWT tokens |
| `/api/logoutview/` | POST | Yes | Blacklist refresh token |
| `/api/blogview/` | GET/POST | Optional | List all posts / Create post |
| `/api/blogdetails/<slug>/` | GET/PUT/DELETE | Yes | Retrieve, update, delete post |
| `/api/token/refresh/` | POST | No | Refresh expired access token |

### Blog Model

```python
class content(models.Model):
    author        # Foreign key to MyUser
    title         # CharField(250)
    slug          # Auto-generated from title
    blog_body     # TextField with rich HTML content
    featured_image# ImageField
    created_at    # Auto datetime
    updated_at    # Auto datetime
```

---

## Frontend Breakdown

### Templates & Routes

| Route | Template | Purpose |
| --- | --- | --- |
| `/` | dashboard.html | All blog posts list |
| `/createpost/` | createPost.html | Form to write new post |
| `/<slug>/` | inner_post.html | Single post view |
| `/update_post/<slug>/` | update_post.html | Edit existing post |
| `/signin/` | signin.html | Login form |
| `/signup/` | signup.html | Registration form |
| `/otp/` | otp.html | OTP verification |

### JavaScript Functions (script.js)

- `signupFunc()` - Register user via API
- `optUser()` - Verify OTP and activate account
- `logUser()` - Login with email/password
- `logoutUser()` - Clear tokens, redirect to home
- `submitPost()` - Create post with image upload
- `updatePost(slug)` - Update existing post
- `deletePost(slug)` - Delete post with confirmation modal

---

## Setup & Installation

### 1. Clone & Install

```bash
git clone <repo-url>
cd SecureBlog
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Email (settings.py)

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use Gmail App Password
```

### 3. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000` to see the blog.

---

## Image Display Fix

Images in posts now display at full width using:

```html
<img src="{{ post.featured_image.url }}" style="width:100%; height:auto; max-height:400px; object-fit:cover;">
```

This ensures featured images fill the container width while maintaining aspect ratio.

---

## Environment Variables (.env)

For production, move sensitive data to environment variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-app-password
DATABASE_URL=your-database-url
```

---

## License

- MIT License - Build something awesome with this code!
MIT License - Build something awesome with this code!

