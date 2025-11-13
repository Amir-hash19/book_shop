# 🚀 Django REST API Platform
❤️ For kelaasor platform 
## 📖 Reference
- [Platform for learning ](https://kelaasor.com/)

A scalable and modular backend built with **Django REST Framework**, featuring **JWT authentication**, **Redis caching**, **Celery background tasks**, and multiple apps including **User Account**, **Bootcamp**, **Ticket**, **Support**, and **Blog**.

![Demo](https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZGpuanNhc2g3ZDJrMXkzdGc3NjlqdWpvdTAxeWdnM2FsbmloMmNmNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5XnfRp2sTnw1qYdLUV/giphy.gif)

# 🧠 Django REST Backend System

A production-ready Django REST API project with:
- 🔐 JWT authentication  
- ⚙️ Rate limiting  
- ⚡ Redis caching  
- 🔁 Celery background tasks  
- 🧩 Modular apps: useraccount, bootcamp, ticket, support, and blog




## 🧰 Technologies Used

This project is built using modern and production-ready technologies to ensure performance, scalability, and clean architecture.

### ⚙️ Backend
- 🐍 **Python 3.11**
- 🧱 **Django 5.x**
- ⚡ **Django REST Framework (DRF)** — for building robust RESTful APIs
- 🔐 **JWT Authentication** — secure user authentication using JSON Web Tokens

### 🧩 Apps
- 👤 **UserAccount** — user management & authentication
- 🎓 **Bootcamp** — training or course management
- 🎟️ **Ticket** — ticketing & issue tracking system
- 💬 **Support** — support chat / helpdesk functionality
- 📰 **Blog** — article publishing & content management

### 🚀 Performance & Optimization
- 🧮 **Rate Limiting** — API request throttling using DRF throttles
- ⚡ **Caching with Redis** — improving performance and response time
- 🔁 **Background Tasks with Celery + Redis** — for async task processing (emails, notifications, etc.)

### 🗄️ Database & Storage
- 🐘 **PostgreSQL** — main relational database
- 🧰 **Redis** — in-memory cache and message broker

### 🧰 DevOps / Tools
- 🐳 **Docker & Docker Compose** — containerized environment setup
- 🧪 **Pytest / Django Test Framework** — testing and CI-ready setup
- 🧹 **Black / isort / flake8** — code formatting and linting
- ☁️ **Environment Variables (.env)** — secure configuration management

---

### 📦 Example Stack Overview
```text
Django + DRF  →  PostgreSQL  →  Redis  →  Celery  →  Docker


## 🚀 How to Run

You can run this Django REST Framework project either **locally** or using **Docker Compose**.

---

### 🧩 1️⃣ Run Locally (Development Mode)

#### 🔹 Prerequisites
Make sure you have installed:
- Python 3.11+
- PostgreSQL (or your configured database)
- Redis (for cache & Celery)
- pip or Poetry

#### 🔹 Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/yourproject.git
cd yourproject

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Run Redis & Celery (in separate terminals)
redis-server
celery -A yourproject worker -l info

# 7. Start the server
python manage.py runserver
