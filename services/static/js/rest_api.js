$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#customer_id").val(res.customer_id);
        $("#product_id").val(res.product_id);
        $("#product_name").val(res.product_name);
        $("#product_price").val(res.product_price);
        $("#product_quantity").val(res.quantity);
    }

    // Clear all form fields
    function clear_form_data() {
        $("#customer_id").val("");
        $("#product_id").val("");
        $("#product_name").val("");
        $("#product_price").val("");
        $("#product_quantity").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Add a Product
    // ****************************************

    $("#create-btn").click(
        function() {
            var cust_id = $("#customer_id").val();
            var prod_id = $("#product_id").val();
            var name = $("#product_name").val();
            var price = $("#product_price").val();
            var quantity = $("#product_quantity").val();

            if(!cust_id){
                flash_message("Customer ID can't be empty!")
                return
            }

            if(!prod_id){
                flash_message("Product ID can't be empty!")
                return
            }

            if(!name){
                flash_message("Product Name can't be empty!")
                return
            }

            if(!price){
                flash_message("Product Price can't be empty!")
                return
            }

            if(!quantity){
                flash_message("Product Quantity can't be empty!")
                return
            }

            var data = {
                "product_id": prod_id,
                "customer_id": cust_id,
                "product_price": price,
                "quantity": quantity,
                "product_name": name
            };

            var ajax = $.ajax({
                type: "POST",
                url: "/api/shopcarts/" + cust_id + "/products/", // string concat
                contentType: "application/json",
                data: JSON.stringify(data)
            });

            ajax.done(function(res) {
                update_form_data(res)
                flash_message("Create Customer: ["+ cust_id +"] with product ["+prod_id+ "] Success!")
            });

            ajax.fail(function(res) {
                flash_message(res.responseJSON.error)
            });
        }
    );

    // ****************************************
    // Update a Product
    // ****************************************

    $("#update-btn").click(function () {

        var cust_id = $("#customer_id").val();
        var prod_id = $("#product_id").val();
        var name = $("#product_name").val();
        var price = $("#product_price").val();
        var quantity = $("#product_quantity").val();

        var data = {
            "product_id": prod_id,
            "customer_id": cust_id,
            "product_price": price,
            "quantity": quantity,
            "product_name": name
        };

        var ajax = $.ajax({
                type: "PUT",
                url: "/api/shopcarts/" + cust_id + "/products/" + prod_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Successfully Update!")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.error)
        });

    });


    // ****************************************
    // List shopcarts
    // (type in customer_id, show all products in the particular customer's shopcart)
    // (type in nothing, show all shopcarts)
    // (type in price optionally to set price threshold)
    // ****************************************

    $("#search-btn").click(function () {
        var cust_id = $("#customer_id").val();
        var price = $("#product_price").val();
        
        var url = "";

        if (cust_id)
            url = "/api/shopcarts/" + cust_id;
        else
            url = "/api/shopcarts";

        if (price)
            url += '?price=' + price

        var ajax = $.ajax({
            type: "GET",
            url: url,
            Accept: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th style="width:22%">CustomerID</th>'
            header += '<th style="width:22%">ProductID</th>'
            header += '<th style="width:22%">ProductName</th>'
            header += '<th style="width:22%">ProductPrice</th>'
            header += '<th style="width:22%">ProductQuantity</th></tr>'

            $("#search_results").append(header);
            var firstProduct = "";
            for(var i = 0; i < res.length; i++) {
                var product = res[i];
                var row = "<tr><td>"+product.customer_id+"</td><td>"+product.product_id+"</td><td>"+product.product_name+"</td><td>"+product.product_price+"</td><td>"+product.quantity+"</td></tr>";
                $("#search_results").append(row);
                if (i == 0) {
                    firstProduct = product;
                }
            }

            $("#search_results").append('</table>');

            // copy the first result to the form
            if (firstProduct != "") {
                update_form_data(firstProduct)
            }

            flash_message("Search Success!")
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.error)
        });

    });

    
    // ****************************************
    // Read a product from a shopcart
    // ****************************************
    $("#retrieve-btn").click(function () {
        var cust_id = $("#customer_id").val();
        var prod_id = $("#product_id").val();

        if(prod_id == ''){
            var ajax = $.ajax({
                type: "GET",
                url: "/api/shopcarts/"+cust_id,
                contentType:"application/json",
                data: ''
            })
    
            ajax.done(function(res){
                //alert(res.toSource())
                $("#search_results").empty();
                $("#search_results").append('<table class="table-striped"><thead>');
                var header = '<tr>'
                header += '<th style="width:22%">Customer ID</th>'
                header += '<th style="width:22%">Product ID</th>'
                header += '<th style="width:22%">Product Name</th>'
                header += '<th style="width:22%">Product Price</th>'
                header += '<th style="width:22%">Product Quantity</th></tr>'
                $("#search_results").append(header);
                for(var i = 0; i < res.length; i++) {
                    product = res[i];
                    var row = "<tr><td>"+product.customer_id+"</td><td>"+product.product_id+"</td><td>"+product.product_name+"</td><td>"+product.product_price+"</td><td>"+product.quantity+"</td></tr>";
                    $("#search_results").append(row);
                    if(i==0){
                        firstProduct = product;
                    }
                }
    
                $("#search_results").append('</table>');

                if(firstProduct != ""){
                    update_form_data(firstProduct)
                }
    
                flash_message("Successfully Retrieve a shopcart of customer: ["+ cust_id+"]")
            });
    
            ajax.fail(function(res){
                flash_message(res.responseJSON.error)
            });
        }

        else{
            var ajax = $.ajax({
                type: "GET",
                url: "/api/shopcarts/" + cust_id + "/products/" + prod_id,
                contentType: "application/json",
                data: ''
            })
    
            ajax.done(function(res){
                //alert(res.toSource())
                update_form_data(res)
                $("#search_results").empty();
                $("#search_results").append('<table class="table-striped"><thead>');
                var header = '<tr>'
                header += '<th style="width:22%">Customer ID</th>'
                header += '<th style="width:22%">Product ID</th>'
                header += '<th style="width:22%">Product Name</th>'
                header += '<th style="width:22%">Product Price</th>'
                header += '<th style="width:22%">Product Quantity</th></tr>'
                $("#search_results").append(header);

                product = res;
                var row = "<tr><td>"+product.customer_id+"</td><td>"+product.product_id+"</td><td>"+product.product_name+"</td><td>"+product.product_price+"</td><td>"+product.quantity+"</td></tr>";
                $("#search_results").append(row);
                $("#search_results").append('</table>');

                flash_message("Successfully Retrieve a prodect of customer: ["+ cust_id+"] with product ["+prod_id+"]")
            });
    
            ajax.fail(function(res){
                clear_form_data()
                flash_message(res.responseJSON.error)
            });
        }

    });


    // ****************************************
    // Delete a Shopcart
    // (type in customer_id, delete all products in the customer's shopcart)
    // ****************************************
    $("#delete-btn").click(function () {

        var cust_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/shopcarts/" + cust_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("The shopcart has been deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });
  
    // ****************************************
    // Checkout a Customer
    // (type in customer_id, delete all products in the customer's shopcart)
    // ****************************************
    $("#checkout-btn").click(function () {
        var cust_id = $("#customer_id").val();

        var ajax = $.ajax({
            type: "PUT",
            url: "/api/shopcarts/" + cust_id + "/checkout",
            contentType: "application/json",
            data: ''
        })

        ajax.done(function(res){
            //alert(res.toSource())
            clear_form_data()

            $("#search_results").empty();
            $("#search_results").append('<table class="table-striped"><thead>');
            var header = '<tr>'
            header += '<th style="width:22%">Customer ID</th>'
            header += '<th style="width:22%">Product ID</th>'
            header += '<th style="width:22%">Product Name</th>'
            header += '<th style="width:22%">Product Price</th>'
            header += '<th style="width:22%">Product Quantity</th></tr>'
            $("#search_results").append(header);
            $("#search_results").append('</table>');

            flash_message("Checkout Successful for Customer: " + cust_id)
        });

        ajax.fail(function(res){
            clear_form_data()
            flash_message(res.responseJSON.error)
        });
    });


    // ****************************************
    // Delete a Product
    // (type in customer_id & product_id, delete the product in the corresponding shopcart)
    // ****************************************
    $("#delete-prod-btn").click(function () {

        var cust_id = $("#customer_id").val();
        var prod_id = $("#product_id").val();

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/shopcarts/" + cust_id + "/products/" + prod_id,
            contentType: "application/json",
            data: '',
        })

        ajax.done(function(res){
            clear_form_data()
            flash_message("The product has been deleted!")
        });

        ajax.fail(function(res){
            flash_message("Server error!")
        });
    });

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        clear_form_data();
        $("#search_results").empty();
        $("#search_results").append('<table class="table-striped"><thead>');
        var header = '<tr>'
        header += '<th style="width:22%">Customer ID</th>'
        header += '<th style="width:22%">Product ID</th>'
        header += '<th style="width:22%">Product Name</th>'
        header += '<th style="width:22%">Product Price</th>'
        header += '<th style="width:22%">Product Quantity</th></tr>'
        $("#search_results").append(header);
        $("#search_results").append('</table>');
        $("#flash_message").empty();
        flash_message("Form cleared")
    });

})