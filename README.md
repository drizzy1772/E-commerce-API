#  E-Commerce API

Production-ready REST API for an online store with authentication, order management, and email notifications.

## Stack
- **FastAPI** 
- **PostgreSQL** 
- **Redis** 
- **SQLAlchemy 2.0** 
- **Docker Compose** 
## Key Features
- ✅ JWT authentication with Access + Refresh tokens
- ✅ Email account verification and password reset (Resend)
- ✅ Cart and order management with transactions
- ✅ State machine for order statuses
- ✅ Email notifications on order status change
- ✅ Rate limiting on critical endpoints (slowapi)
- ✅ Redis caching for GET requests
- ✅ Global error handling in RFC 7807 format
- ✅ Test coverage (pytest)
- ✅ CI/CD pipeline via GitHub Actions
- ✅ CORS configuration

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

## Structure of Project
<img width="560" height="406" alt="ecommerce-apitonka drawio" src="https://github.com/user-attachments/assets/117e3edb-57d2-4c59-9f3b-d81932e1d3d2" />



## API Docs
Swagger UI available at: `http://localhost:8000/api/docs`

## Author

This project is developed by Drizzy1772.

## License

This project is licensed under MIT License.
