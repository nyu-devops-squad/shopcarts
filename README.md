# shopcarts

[![codecov](https://codecov.io/gh/nyu-devops-squad/shopcarts/branch/main/graph/badge.svg?token=HE22505N7V)](https://codecov.io/gh/nyu-devops-squad/shopcarts)

To run the flask app -  
``` 
    vagrant up
    vagrant ssh  
    cd /vagrant      
    export FLASK_APP= services/__init__.py    
    flask run --host=0.0.0.0  
```  

To run testing we use -  
``` 
    vagrant up
    vagrant ssh  
    cd /vagrant      
    nosetests 
```  

#### API calls
URL | Operation | Description
-- | -- | --
`GET /shopcarts/` | LIST | Returns list of all of the shop cart items for all customers
`GET /shopcarts/<int:customer_id>` | READ | Returns list of all of the shop cart items for a customer
`POST /shopcarts/<int:customer_id>` | CREATE | Creates a new item entry for the cart
`PUT /shopcarts/<int:customer_id>/<int:product_id>` | UPDATE | Update particular item quantity
`DELETE /shopcarts/<int:customer_id>` | DELETE | Delete all shopcart items for a customer
