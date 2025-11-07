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

| Category      | Method | Endpoint                         | Body Params                                                                | Auth Required | Response                     | Status |
| ------------- | ------ | -------------------------------- | -------------------------------------------------------------------------- | ------------- | ---------------------------- | ------ |
| **Auth**      | POST   | `/auth/stores/register/`         | `{email, name, password, location}`                                        | ❌            | `{token, store_id, name}`    | 201    |
|               | POST   | `/auth/stores/login/`            | `{email, password}`                                                        | ❌            | `{token, store_id, name}`    | 200    |
|               | POST   | `/auth/customer/register/`       | `{email(optional), name, password, address, phone}`                        | ❌            | `{token, customer_id, name}` | 201    |
|               | POST   | `/auth/customer/login/`          | `{password, phone}`                                                        | ❌            | `{token, customer_id, name}` | 200    |
| **Products**  | POST   | `/stores/products/`              | `{name, cost, profit_percent, stock, category, units_sold, selling_price}` | ✅            | `{}`                         | 201    |
|               | GET    | `/stores/products/`              | N/A                                                                        | ✅            | List of product objects      | 201    |
|               | PUT    | `/stores/products/<id>/`         | `{fields_to_update}`                                                       | ✅            | Updated product object       | 200    |
|               | DELETE | `/stores/products/<id>/`         | N/A                                                                        | ✅            | N/A                          | 200    |
| **Billing**   | POST   | `/stores/bills/create/`          | `{customer_id(optional), items: [{product_id, quantity}]}`                 | ✅            | Created bill                 | 201    |
|               | GET    | `/stores/bills/`                 | N/A                                                                        | ✅            | List of bills                | 201    |
|               | GET    | `/stores/bills/<id>/`            | N/A                                                                        | ✅            | Bill object                  | 201    |
| **Analytics** | GET    | `/stores/analytics/products`     | `?category=<category_name>`                                                | ✅            | Store-wide Analytics data    | 200    |
|               | GET    | `/stores/analytics/category`     | N/A                                                                        | ✅            | Category wise Analytics data | 200    |
|               | GET    | `/stores/analytics/top-products` | `?metric=profit`                                                           | ✅            | Top products by metric       | 200    |

---

## 🧠 Store Analytics Endpoints

### **1️⃣ GET `/stores/analytics/products/`**

Fetches comprehensive analytics for all products belonging to the authenticated store.  
You can optionally filter by a specific product category using a query parameter.

#### **Query Parameters**

| Parameter  | Type     | Required | Description                                      |
| ---------- | -------- | -------- | ------------------------------------------------ |
| `category` | `string` | ❌       | Filter results by a specific category (optional) |

#### **Response Example**

```json
{
  "most_selling_product": {
    "id": 1,
    "name": "Green Tea Pack",
    "category": "Beverages",
    "units_sold": 350,
    "total_profit": 4200.50,
    "total_revenue": 10500.00
  },
  "least_selling_product": {
    "id": 5,
    "name": "Almond Cookies",
    "category": "Snacks",
    "units_sold": 5,
    "total_profit": 35.00,
    "total_revenue": 200.00
  },
  "categories_summary": {
    "Beverages": {
      "total_revenue": 21500.00,
      "total_profit": 6200.50,
      "units_sold": 500,
      "product_count": 3
    },
    "Snacks": {
      "total_revenue": 3200.00,
      "total_profit": 450.00,
      "units_sold": 55,
      "product_count": 2
    }
  },
  "category_analytics": {
    "category": "Beverages",
    "total_products": 3,
    "total_units_sold": 500,
    "total_revenue": 21500.00,
    "total_profit": 6200.50,
    "average_profit_per_product": 2066.83,
    "top_profitable_products": [
      { "id": 1, "name": "Green Tea Pack", "total_profit": 4200.50 },
      { "id": 2, "name": "Coffee Powder", "total_profit": 2000.00 }
    ]
  }
}

## 🧪 Sample Auth Header

Authorization: Bearer eyJhbGciOiJIUzI1...
```
