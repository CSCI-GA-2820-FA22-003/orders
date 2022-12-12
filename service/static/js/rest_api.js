$(function () {

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    function update_form_data(message) {
        $("#flash_message").append(message);
    }

    // Create an Order
    $("#create-btn").click(function () {

        var order_id = $("#order_id").val();
        var name = $("#order_name").val();
        var address = $("#order_addr").val(); 

        var data = {
            "id": order_id,
            "name": name,
            "address": address, 
        };
        console.log(data);

        var ajax = $.ajax({
            type: "POST",
            url: "/api/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // Update an Order
    $("#update-btn").click(function () {

        var order_id = $("#update_order_id").val();
        var name = $("#update_order_name").val();
        var address = $("#update_order_addr").val(); 

        var data = {
            "name": name,
            "address": address, 
        };
        console.log(data);

        var ajax = $.ajax({
            type: "PUT",
            url: "/api/orders/" + order_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // List all Orders
    $("#listall-btn").click(function () {

        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders",
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#list_results").empty();
            $("#list_results").append('<table class="table-striped">');

            var header = '<tr>'
            header += '<th>Order ID</th>'
            header += '<th>Order Name</th>'
            header += '<th>Address</th>'
            header += '<th>Date_created</th></tr>'
            $("#list_results").append(header); 
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                var row = "<tr><td>" + order.id + "</td><td>" + order.name + "</td><td>" + order.address + "</td><td>" + order.date_created + "</td></tr>";
                $("#list_results").append(row);
            }
            $("#list_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // List Order Details
    $("#list-order-details-btn").click(function () {

        var order_id = $("#order_details_id").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders/" + order_id,
            data: ''
        })

        ajax.done(function (res) {
            //alert(res.toSource())
            $("#list_order_details_results").empty();
            $("#list_order_details_results").append('<table class="table-striped">');

            var header = '<tr>'
            header += '<th>Order ID</th>'
            header += '<th>Order Name</th>'
            header += '<th>Address</th>'
            header += '<th>Date_created</th></tr>'
            $("#list_order_details_results").append(header); 
            var order = res;
            var row = "<tr><td>" + order.id + "</td><td>" + order.name + "</td><td>" + order.address + "</td><td>" + order.date_created + "</td></tr>";
            $("#list_order_details_results").append(row);
            $("#list_order_details_results").append('</table>');

            $("#list_order_item_results").empty();
            $("#list_order_item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th>Item ID</th>'
            header += '<th>Order_id</th>'
            header += '<th>Product_id</th>'
            header += '<th>Price</th>'
            header += '<th>Quantity</th>'
            header += '<th>Status</th></tr>'
            $("#list_order_item_results").append(header); 
                for (var j = 0; j < order.items.length; j++){
                    var item = order.items[j];
                    var row = "<tr><td>" + item.id + "</td><td>" + item.order_id + "</td><td>" 
                    + item.product_id + "</td><td>" + item.price + "</td><td>" 
                    + item.quantity + "</td><td>" + item.status + "</td></tr>";
                    $("#list_order_item_results").append(row);
                }
            $("#list_order_item_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // Delete an Order
    $("#delete-btn").click(function () {

        var order_id = $("#delete_order_id").val();

        var data = {
            "id": order_id
        };

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/orders/" + order_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // Create an item
    $("#create-item-btn").click(function () {

        var item_id = $("#item_id").val();
        var order_id = $("#item_order_id").val();
        var product_id = $("#item_product_id").val();
        var price = $("#item_price").val(); 
        var quantity = $("#item_quantity").val(); 
        var status = $("#item_status").val(); 

        var data = {
            "id": item_id,
            "order_id": order_id,
            "product_id": product_id, 
            "price": price,
            "quantity": quantity,
            "status": status
        };
        console.log(data)

        var ajax = $.ajax({
            type: "POST",
            url: "/api/orders/" + order_id + "/items",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // List all Items of an Order
    $("#listall-item-btn").click(function () {

        var order_id = $("#order_id_items").val();

        var ajax = $.ajax({
            type: "GET",
            url: "/api/orders/" + order_id + "/items",
            data: ''
        })

        ajax.done(function (res) {
            $("#list_item_results").empty();
            $("#list_item_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th>Item ID</th>'
            header += '<th>Order_id</th>'
            header += '<th>Product_id</th>'
            header += '<th>Price</th>'
            header += '<th>Quantity</th>'
            header += '<th>Status</th></tr>'
            $("#list_item_results").append(header); 
            for (var i = 0; i < res.length; i++) {
                var item = res[i];
                var row = "<tr><td>" + item.id + "</td><td>" + item.order_id + "</td><td>" 
                          + item.product_id + "</td><td>" + item.price + "</td><td>" 
                          + item.quantity + "</td><td>" + item.status + "</td></tr>";
                $("#list_item_results").append(row);
            }
            $("#list_item_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // List all Items within the specified price range
    $("#listall-item-pricerange-btn").click(function () {

        //var order_id = $("#order_id_items").val();
        var min_price = $("#min_price").val();
        var max_price = $("#max_price").val();

        var ajax = $.ajax({
            type: "POST",
            url: "/api/orders_prices",
            contentType: "application/json",
            data : JSON.stringify({ min_price : min_price, max_price : max_price }),
        })

        ajax.done(function (res) {
            $("#list_item_price_results").empty();
            $("#list_item_price_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th>Item ID</th>'
            header += '<th>Order_id</th>'
            header += '<th>Product_id</th>'
            header += '<th>Price</th>'
            header += '<th>Quantity</th>'
            header += '<th>Status</th></tr>'
            $("#list_item_price_results").append(header); 
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                for (var j = 0; j < order.items.length; j++)
                {
                    var item = order.items[j];
                    console.log(item);
                    var row = "<tr><td>" + item.id + "</td><td>" + item.order_id + "</td><td>" 
                          + item.product_id + "</td><td>" + item.price + "</td><td>" 
                          + item.quantity + "</td><td>" + item.status + "</td></tr>";
                    $("#list_item_price_results").append(row);
                }
            }
            $("#list_item_price_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // List all orders placed on the specified date
    $("#listall-date-btn").click(function () {

        //var order_id = $("#order_id_items").val();
        var date = $("#order_date").val().toISOString();

        var ajax = $.ajax({
            type: "POST",
            url: "/api/orders_date" + date,
            data : '',
        })

        ajax.done(function (res) {
            $("#list_item_bydate_results").empty();
            $("#list_item_bydate_results").append('<table class="table-striped">');
            var header = '<tr>'
            header += '<th>Item ID</th>'
            header += '<th>Order_id</th>'
            header += '<th>Product_id</th>'
            header += '<th>Price</th>'
            header += '<th>Quantity</th>'
            header += '<th>Status</th></tr>'
            $("#list_item_bydate_results").append(header); 
            for (var i = 0; i < res.length; i++) {
                var order = res[i];
                for (var j = 0; j < order.items.length; j++)
                {
                    var item = order.items[j];
                    console.log(item);
                    var row = "<tr><td>" + item.id + "</td><td>" + item.order_id + "</td><td>" 
                          + item.product_id + "</td><td>" + item.price + "</td><td>" 
                          + item.quantity + "</td><td>" + item.status + "</td></tr>";
                    $("#list_item_bydate_results").append(row);
                }                 
            }
            $("#list_item_bydate_results").append('</table>');

            flash_message("Success")
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // Update an Item
    $("#update-item-btn").click(function () {

        var item_id = $("#update_item_id").val();
        var order_id = $("#order_id_update").val();
        var product_id = $("#update_product_id").val(); 
        var price = $("#update_item_price").val(); 
        var quantity = $("#update_item_quantity").val(); 
        var status = $("#update_item_status").val(); 

        var data = {
            "product_id": product_id, 
            "price": price,
            "quantity": quantity,
            "status": status
        };

        var ajax = $.ajax({
            type: "PUT",
            url: "/api/orders/" + order_id + "/items/" + item_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });

    // Delete an Item
    $("#delete-item-btn").click(function () {

        var order_id = $("#order_id_delete").val();
        var item_id = $("#item_id_delete").val();

        var data = {
            "order_id": order_id,
            "id": item_id
        };

        var ajax = $.ajax({
            type: "DELETE",
            url: "/api/orders/" + order_id + "/items/" + item_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function (res) {
            flash_message("Success ")
            update_form_data(JSON.stringify(res))
        });

        ajax.fail(function (res) {
            flash_message(res.responseJSON.message)
        });
    });
})
