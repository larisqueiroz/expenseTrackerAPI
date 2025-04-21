# ExpenseTrackerAPI

## Description
A Django Rest Framework API for expense tracking.

## Built with
* Python
* Django Rest Framework
* Docker
* SimpleJWT
* PostgreSQL

## Features
* Authentication
* CRUD Users
* CRUD Expenses

## Getting Started
1. Clone this repository.

2. Run:
```
docker-compose up --build
```
3. Create user:

http://localhost:8000/api/v1/users POST (body: email and password)

4. Sign in:

http://localhost:8000/api/v1/login POST (body: email and password)

## Contact me

https://www.linkedin.com/in/larissalimaqueiroz/

## Screenshots
GET Expenses

![get_expenses.png](%2Fassets%2Fget_expenses.png)

GET Expenses with filter
![get_expenses_filter.png](%2Fassets%2Fget_expenses_filter.png)

POST expense
![post_expense.png](%2Fassets%2Fpost_expense.png)



