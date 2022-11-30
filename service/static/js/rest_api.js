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
})
