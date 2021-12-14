# Shopcarts


[![TDD Tests](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/workflow.yml/badge.svg)](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/workflow.yml)
[![BDD Tests](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/bdd-tests.yml/badge.svg)](https://github.com/nyu-devops-squad/shopcarts/actions/workflows/bdd-tests.yml)
[![codecov](https://codecov.io/gh/nyu-devops-squad/shopcarts/branch/main/graph/badge.svg?token=HE22505N7V)](https://codecov.io/gh/nyu-devops-squad/shopcarts)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Setup

For easy setup, you need to have [Vagrant](https://www.vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/) installed. Then all you have to do is clone this repo and invoke vagrant:

```sh
git clone https://github.com/nyu-devops-squad/shopcarts.git
cd shopcarts
vagrant up
```

## Manually running the Tests

This repository has both unit tests and integration tests. You can now run `nosetests` and `behave` to run the TDD and BDD tests respectively.

### Test Driven Development (TDD)

This repo has unit tests that you can run `nose`

```sh
vagrant ssh  
cd /vagrant 
nosetests
```

`nose` is configured to automatically include the flags `--with-spec --spec-color` so that red-green-refactor is meaningful. If you are in a command shell that supports colors, passing tests will be green while failing tests will be red.

### Behavior Driven Development (BDD)

These tests require the service to be **running**. Unlike the TDD unit tests that test the code locally, these BDD integration tests are using **Selenium** to manipulate a web page on a running server.

You may run the BDD tests using `behave`

#### Run BDD tests in 2 terminals
```sh
# terminal 1
vagrant ssh
cd /vagrant
honcho start

# terminal 2
vagrant ssh
cd /vagrant
behave
```

#### Run BDD tests in 1 terminal
```sh
vagrant ssh
cd /vagrant
honcho start &
behave
```

Note that the `honcho start` runs the server in the background. To stop the server, you must bring it to the foreground and then press `Ctrl+C`

Stop the server with

```sh
fg
<Ctrl+C>
```


## What's featured in the project?

    * services/routes.py -- the main Service using Python Flask-RESTX for Swagger
    * services/models.py -- a Shopcart model that uses Cloudant for persistence
    * tests/test_routes.py -- test cases using unittest for the microservice
    * tests/test_models.py -- test cases using unittest for the Shopcart model
    * ./features/shopcarts.feature -- Behave feature file
    * ./features/steps/web_steps.py -- Behave step definitions

## API calls
URL | Operation | Description
-- | -- | --
`GET /shopcarts/` | LIST | Return a list of all the shopcart items for all customers
`GET /shopcarts/<int:customer_id>` | READ | Return a list of all the shopcart items for a customer
`GET /shopcarts/<int:customer_id>/products/<int:product_id>` | READ | Return a particular item from a customer's shopcart
`POST /shopcarts/<int:customer_id>/products` | CREATE | Create a new item entry for the shopcart
`PUT /shopcarts/<int:customer_id>/products/<int:product_id>` | UPDATE | Update a particular item's quantity
`DELETE /shopcarts/<int:customer_id>` | DELETE | Delete all shopcart items for a customer
`DELETE /shopcarts/<int:customer_id>/products/<int:product_id>` | DELETE | Delete a particular item from a customer's shopcart
`GET /shopcarts/<int:customer_id>/checkout` | GET | Checkout for a customer and clear the shopcart for the customer
`GET /shopcarts?price=<int:product_price>` | GET | Return a list of all product items in a customer's shopcart with price above a threshold
`GET /shopcarts/<int:customer_id>?price=<int:product_price>` | GET | Return a list of all product items with price above a threshold

## Vagrant shutdown

If you are using Vagrant and VirtualBox, when you are done, you should exit the virtual machine and shut down the vm with:

```bash
 $ exit
 $ vagrant halt
```

If the VM is no longer needed you can remove it with:

```bash
  $ vagrant destroy
```