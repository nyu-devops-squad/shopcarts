"""
Shopcart Steps
Steps file for Shopcart.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect

@given('the following shopcarts')
def step_impl(context):
    """ Delete all Shopcarts and load new ones """
    headers = {'accept': 'application/json'}
    # list all of the shopcarts and delete them one by one
    context.resp = requests.get(context.base_url + '/api/shopcarts', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for shopcart in context.resp.json():
        context.resp = requests.delete(context.base_url + '/api/shopcarts/' + str(shopcart["customer_id"]), headers={'Content-Type': 'application/json'})
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new shopcarts
    
    for row in context.table:
        data = {
            "customer_id": row['Customer ID'],
            "product_id": row['Product ID'],
            "product_name": row['Product Name'],
            "product_price": row['Product Price'],
            "quantity": row['Product Quantity']
            }
        create_url = context.base_url + '/api/shopcarts/' + row['Customer ID'] + '/products/'
        payload = json.dumps(data)
        # headers = {'Content-Type': 'application/json'}
        context.resp = requests.post(create_url, data=payload, headers={'Content-Type': 'application/json'})
        expect(context.resp.status_code).to_equal(201)