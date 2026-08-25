# Aswan Installment Management System

A production Django application built for a real client — managing 
client installments, financial settlements, and treasury operations.

> ⚠️ Source code is private (client confidentiality). 
> Available for review upon request during interviews.

---

## 🛠 Tech Stack

- **Framework:** Django & Django REST Framework
- **Auth:** JWT (SimpleJWT) with token refresh
- **Database:** PostgreSQL
- **Architecture:** Hybrid — Template Views + REST API (v1)

---

## 📦 Modules

### 🏠 Home
- Executive dashboard with real-time financial overview

### 👥 Clients
- Full client lifecycle management
- Purchase tracking with unique slug-based identification
- Installment payment recording and editing
- Settlement calculation and processing
- Client search API

### 📋 Orders
- Order creation, confirmation, rejection, and modification
- Notes system per order
- Full REST API for mobile integration

### 💰 Treasury
- Multi-method transaction tracking (Cash, Vodafone Cash, InstaPay)
- Real-time balance aggregation per payment method
- Financial reporting: net profits, salaries, commissions
- Complex Django ORM aggregations using Coalesce & Q filters

---

## 🔗 API Endpoints (v1)

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/login/ | Obtain JWT token |
| POST | /api/token/refresh/ | Refresh JWT token |

### Clients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /clients/api/v1/all_clients/ | List all clients |
| GET/POST | /clients/api/v1/purchase_details/slug/ | Purchase details |
| POST | /clients/api/v1/installment/pay/slug/ | Record payment |
| PUT/DELETE | /clients/api/v1/installment/ud/pk/ | Update/delete installment |
| GET | /clients/api/v1/sattlement/data/slug/ | Settlement data |
| POST | /clients/api/v1/sattlement/slug/ | Process settlement |
| GET | /clients/api/v1/search/ | Search clients |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /orders/api/v1/all/ | List all orders |
| POST/PUT | /orders/api/v1/add_update/slug/ | Add or update order |
| POST | /orders/api/v1/confirm_order/slug/ | Confirm order |
| POST | /orders/api/v1/reject_order/slug/ | Reject order |
| DELETE | /orders/api/v1/delete_order/slug/ | Delete order |

### Treasury
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /treasury/api/v1/operation/ | Add transaction |
| GET | /treasury/api/v1/all/ | All transactions + balances |
| GET | /treasury/api/v1/report/ | Financial report |

---

## 💡 Technical Highlights

- Slug-based client and order identification
- Django Signals for automated workflows
- Complex financial aggregations with zero null errors
- Hybrid architecture supporting both web UI and mobile API
- Secure JWT authentication with role-based access

---

## 👤 Developer

**Abdallah Mohamed (Migo)** — Backend Developer & Security Researcher

[GitHub](https://github.com/Migoo0-ee)
