# ManService Django Site: Equipment and Spare Parts E-Commerce Platform

## Overview
This project is a **full-fledged e-commerce website** developed using the **Django framework**. The website simulates a company that sells equipment and spare parts, providing a complete user experience for browsing products, adding items to a cart, and submitting orders. Designed solely for **educational purposes**, the site demonstrates the integration of Django with a MySQL database and showcases functionalities such as order management, user interaction, and responsive design for mobile and tablet devices.

All product data, including images and descriptions, are sourced from open sources and generated randomly by AI for demonstration purposes. The site is not intended for commercial use.

Below is a video demonstration showcasing the functionality and design of the website:

[**Video Demonstration**](https://github.com/samedimanche/manServiceDjangosite/assets/152053503/18fc3bc7-a7ca-4234-bddf-d588e8a6802e)

---

## Features

### 1. **User-Friendly Interface**
   - Browse products and spare parts with detailed descriptions and images.
   - Responsive design optimized for **phones and tablets**.

### 2. **Shopping Cart**
   - Users can add products to their cart and specify order details.
   - Dynamic cart updates and order summary.

### 3. **Order Management**
   - Submit orders with user data (e.g., name, contact information).
   - Order details are sent to both the **store manager** and the **buyer** via email.
   - The manager contacts the buyer to confirm and finalize the order.

### 4. **Admin Panel**
   - Built-in Django admin panel for managing products, orders, and user data.

### 5. **Database Integration**
   - Uses **MySQL** (via XAMPP Control Panel) for storing product data, user information, and orders.

---

## Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: MySQL
- **Hosting**: Local server (for educational purposes)
- **Responsive Design**: Bootstrap framework

---

## Prerequisites
- **Python 3.x**
- **Django**
- **MySQL** (via XAMPP Control Panel)
- **XAMPP** (for MySQL database management)

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samedimanche/manServiceDjangosite.git
   cd manServiceDjangosite
   ```

2. **Set Up the Database**:
   - Install and configure **XAMPP**.
   - Start the MySQL server using XAMPP Control Panel.
   - Create a new MySQL database and update the `settings.py` file with the database credentials.

3. **Configure Django Settings**:
   - Update `ALLOWED_HOSTS` in `settings.py`:
     ```python
     ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-ip-address']
     ```
   - Insert the necessary database credentials in `settings.py`.

4. **Run Migrations**:
   - Apply Django migrations to set up the database schema:
     ```bash
     python manage.py migrate
     ```

5. **Run the Application**:
   - Start the Django development server:
     ```bash
     python manage.py runserver 0.0.0.0:8000
     ```
   - Access the website by navigating to `http://localhost:8000` in your browser.

---

## Usage
1. **Browse Products**:
   - Explore the catalog of equipment and spare parts.
2. **Add to Cart**:
   - Select products and add them to the shopping cart.
3. **Submit Order**:
   - Provide your details and submit the order.
4. **Order Confirmation**:
   - The manager will contact you to finalize the order details.

---

## Acknowledgments
- **Django** for providing a robust framework for web development.
- **MySQL** and **XAMPP** for database management.
- Open-source community for continuous support and inspiration.

---

For more details, visit the [GitHub repository](https://github.com/samedimanche/manServiceDjangosite).
