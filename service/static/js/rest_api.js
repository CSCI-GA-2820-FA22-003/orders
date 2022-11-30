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
            "id": order_id,
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
            $("#list_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th">id</th>'
            header += '<th">name</th>'
            header += '<th">address</th>'
            header += '<th">date_created</th></tr>'
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
            $("#list_item_results").append('<table class="table-striped" cellpadding="10">');
            var header = '<tr>'
            header += '<th">id</th>'
            header += '<th">order_id</th>'
            header += '<th">product_id</th>'
            header += '<th">price</th>'
            header += '<th">quantity</th>'
            header += '<th">status</th></tr>'
            $("#list_item_results").append(header); 
            for (var i = 0; i < res.length; i++) {
                var item = res[i];
                var row = "<tr><td style='padding-right:2px'>" + item.id + "</td><td style='padding-right:2px'>" + item.order_id + "</td><td style='padding-right:2px'>" 
                          + item.product_id + "</td><td style='padding-right:2px'>" + item.price + "</td><td style='padding-right:2px'>" 
                          + item.quantity + "</td><td style='padding-right:2px'>" + item.status + "</td></tr>";
                $("#list_item_results").append(row);
            }
            $("#list_item_results").append('</table>');

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
            "id": item_id,
            "order_id": order_id,
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
})
