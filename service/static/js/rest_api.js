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
            url: "/orders",
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
})