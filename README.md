# shopcarts


[![Run Python Tests](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/workflow.yml/badge.svg)](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/workflow.yml)
[![BDD Tests](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/bdd-tests.yml/badge.svg)](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/bdd-tests.yml)
[![codecov](https://codecov.io/gh/nyu-devops-squad/shopcarts/branch/main/graph/badge.svg?token=HE22505N7V)](https://codecov.io/gh/nyu-devops-squad/shopcarts)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

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
`GET /shopcarts/` | LIST | Returns list of all of the shopcart items for all customers
`GET /shopcarts/<int:customer_id>` | READ | Returns list of all of the shopcart items for a customer
`GET /shopcarts/<int:customer_id>/products/<int:product_id>` | READ | Returns a particular item from a customer's shopcart
`POST /shopcarts/<int:customer_id>/products` | CREATE | Creates a new item entry for the shopcart
`PUT /shopcarts/<int:customer_id>/products/<int:product_id>` | UPDATE | Update a particular item quantity
`DELETE /shopcarts/<int:customer_id>` | DELETE | Delete all shopcart items for a customer
`DELETE /shopcarts/<int:customer_id>/products/<int:product_id>` | DELETE | Delete a particular item from a customer's shopcart
