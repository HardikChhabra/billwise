# 📦 BillWise API

BillWise is a RESTful API for billing, inventory management, and analytics. It supports authentication for stores and customers, inventory management, billing, and viewing sales data.

---

## 🚀 Features

- Store and customer registration & login (JWT-based authentication)
- Product inventory management (CRUD)
- Bill creation and retrieval
- Sales data per customer or bill
- Authenticated access to store data

---

## 🔑 Authentication

All protected endpoints require a **JWT token** in the `Authorization` header: "Bearer <your token>"

---

## 📋 API Endpoints

| Category     | Method | Endpoint                   | Body Params                                                                | Auth Required | Response                     | Status |
| ------------ | ------ | -------------------------- | -------------------------------------------------------------------------- | ------------- | ---------------------------- | ------ |
| **Auth**     | POST   | `/auth/stores/register/`   | `{email, name, password, location}`                                        | ❌            | `{token, store_id, name}`    | 201    |
|              | POST   | `/auth/stores/login/`      | `{email, password}`                                                        | ❌            | `{token, store_id, name}`    | 200    |
|              | POST   | `/auth/customer/register/` | `{email(optional), name, password, address, phone}`                        | ❌            | `{token, customer_id, name}` | 201    |
|              | POST   | `/auth/customer/login/`    | `{password, phone}`                                                        | ❌            | `{token, customer_id, name}` | 200    |
| **Products** | POST   | `/stores/products/`        | `{name, cost, profit_percent, stock, category, units_sold, selling_price}` | ✅            | `{}`                         | 201    |
|              | GET    | `/stores/products/`        | N/A                                                                        | ✅            | List of product objects      | 201    |
|              | PUT    | `/stores/products/<id>/`   | `{fields_to_update}`                                                       | ✅            | Updated product object       | 200    |
|              | DELETE | `/stores/products/<id>/`   | N/A                                                                        | ✅            | N/A                          | 200    |
| **Billing**  | POST   | `/stores/bills/create/`    | `{customer_id(optional), items: [{product_id, quantity}]}`                 | ✅            | Created bill                 | 201    |
|              | GET    | `/stores/bills/`           | N/A                                                                        | ✅            | List of bills                | 201    |
|              | GET    | `/stores/bills/<id>/`      | N/A                                                                        | ✅            | Bill object                  | 201    |

---

## 🧪 Sample Auth Header

Authorization: Bearer eyJhbGciOiJIUzI1...
