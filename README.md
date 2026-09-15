#  E-Commerce API

Production-ready REST API for an online store with authentication, order management, and email notifications.

## Stack
- **FastAPI** 
- **PostgreSQL** 
- **Redis** 
- **SQLAlchemy 2.0** 
- **Docker Compose** 
## Key Features
## ✨ Features

### Security & Authentication
- **JWT-based Auth:** Secure session management using robust Access and Refresh tokens.
- **Account Verification:** Email confirmations and password resets powered by **Resend**.
- **Rate Limiting:** Brute-force and spam prevention on critical endpoints (login/register) using **SlowAPI**.
- **CORS Configured:** Strict Cross-Origin Resource Sharing policies applied.

### Core Business Logic
- **Cart & Order Management:** Reliable transaction-based processing for e-commerce flows.
- **Order State Machine:** Deterministic and strict control over order status transitions.
- **Event Notifications:** Automated email dispatch on order status changes.

### Performance & API Standards
- **Redis Caching:** Fast response times for heavy/frequent `GET` requests.
- **RFC 7807 Standard:** Global error handling returning structured problem details.

### QA & DevOps
- **Test Coverage:** Comprehensive testing suite built with **pytest**.
- **CI/CD Pipeline:** Automated testing and deployment workflows via **GitHub Actions**.
 
- **Security**: JWT-based authentication, password hashing (bcrypt), and rate-limiting via SlowAPI.
  * `POST /auth/login` (5 req/min) — Brute-force protection.
  * `POST /auth/register` (3 req/min) — Spam account prevention.
  * `POST /auth/forgot-password` (3 req/min) — Email spam prevention.

## API Scheme
<img width="1411" height="1066" alt="ecommerce-eee" src="https://github.com/user-attachments/assets/31e522ad-d154-4110-a732-8e1df6435c28" />


## API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | /products | Product list with filters and pagination |
| POST | /cart/items | Add item to cart |
| POST | /orders | Create order |
| PATCH | /orders/{id}/status | Update order status |
| POST | /auth/register | Register |
| POST | /auth/login | Login → JWT token |
| POST | /auth/refresh | Refresh access token |
| POST | /auth/verify | Email verification |
| POST | /auth/forgot-password | Request password reset |
| POST | /auth/reset-password | Reset password |

## Quick Start
```bash
git clone https://github.com/username/ecommerce-api
cd ecommerce-api
cp .env.example .env
docker compose up -d
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

## Structure of Project:
<img width="1536" height="1024" alt="ecommerce-apitonkaaa1111 drawio png" src="https://github.com/user-attachments/assets/4028e892-bfd6-4e59-b471-e44bf242e80f" />






## API Docs
***Swagger UI available at: `http://localhost:8000/api/docs`***


<img width="1365" height="790" alt="Screenshot 2026-07-01 at 01-00-36 E-commerce API - Swagger UI" src="https://github.com/user-attachments/assets/e2204d90-46ae-47fc-9f32-d885917b51bc" />


## Link for API:
## https://e-commerce-api-uo9k.onrender.com/api/docs

## Author

This project is developed by Drizzy1772.

## License

This project is licensed under MIT License.
