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

            var data = {
                "product_id": prod_id,
                "customer_id": cust_id,
                "product_price": price,
                "quantity": quantity,
                "product_name": name
            };

            var ajax = $.ajax({
                type: "POST",
                url: "/shopcarts/" + cust_id + "/products/", // string concat
                contentType: "application/json",
                data: JSON.stringify(data)
            });

            ajax.done(function(res) {
                update_form_data(res)
                flash_message("Success")
            });

            ajax.fail(function(res) {
                flash_message(res.responseJSON.message)
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
                url: "/shopcarts/" + cust_id + "/products/" + prod_id,
                contentType: "application/json",
                data: JSON.stringify(data)
            })

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });

    });


    // ****************************************
    // Retrieve a Shopcart
    // (type in customer_id, show all products in the customer's shopcart)
    // ****************************************

 

    
    // ****************************************
    // Read a product from a shopcart
    // ****************************************
    $("#retrieve-btn").click(function () {
        var cust_id = $("#customer_id").val();
        var prod_id = $("#product_id").val();

        if(prod_id == ''){
            var ajax = $.ajax({
                type: "GET",
                url: "/shopcarts/"+cust_id,
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
    
                flash_message("Success")
            });
    
            ajax.fail(function(res){
                flash_message(res.responseJSON.message)
            });
        }

        else{
            var ajax = $.ajax({
                type: "GET",
                url: "/shopcarts/" + cust_id + "/products/" + prod_id,
                contentType: "application/json",
                data: ''
            })
    
            ajax.done(function(res){
                //alert(res.toSource())
                update_form_data(res)
                flash_message("Success")
            });
    
            ajax.fail(function(res){
                clear_form_data()
                flash_message(res.responseJSON.message)
            });
        }

    });


    // ****************************************
    // Delete a Shopcart
    // (type in customer_id, delete all products in the customer's shopcart)
    // ****************************************

    // ****************************************
    // Delete a Product
    // (type in customer_id & product_id, delete the product in the corresponding shopcart)
    // ****************************************

    // ****************************************
    // Clear the form
    // ****************************************

    $("#clear-btn").click(function () {
        $("#customer_id").val("");
        $("#product_id").val("");
        clear_form_data()
        $("#flash_message").empty();
    });

    // ****************************************
    // Search for a Product
    // ****************************************


})
