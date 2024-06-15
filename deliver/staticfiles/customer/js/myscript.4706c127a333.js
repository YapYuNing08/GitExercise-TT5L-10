$(document).ready(function(){
    console.log("Document is ready");

    $('.quantity-input').change(function(){
        var id = $(this).attr("id").replace("quantity-", "");
        var quantity = $(this).val();
        console.log("Quantity input changed: ", id, quantity);
        $.ajax({
            type: "GET",
            url: "/updatecart",
            data: {
                prod_id: id,
                quantity: quantity
            },
            success: function(data){
                console.log("Update cart success", data);
                updateCartUI(data);
            }
        });
    });

    // Handle the plus-cart click event
    $('.plus-cart').click(function(){
        var id = $(this).attr("cid").toString();
        var eml = this.parentNode.children[2];
        var quantity = parseInt(eml.innerText) + 1;
        
        console.log("Plus cart clicked: ", id);

        $.ajax({
            type: "GET",
            url: "/pluscart",
            data: {
                cart_item_id: id
            },
            success: function(data){
                console.log("Plus cart success", data);
                var amount = parseFloat(data.amount);
                var totalamount = parseFloat(data.totalamount);
                if (!isNaN(amount) && !isNaN(totalamount)) {
                    eml.innerText = data.quantity; 
                    document.getElementById("amount").innerText = 'RM ' + amount.toFixed(2); 
                    document.getElementById("totalamount").innerText = 'RM ' + totalamount.toFixed(2);
                    
                    // Update total price for the item
                    var pricePerUnit = parseFloat($(".cart-item[data-cart-item-id='" + id + "']").data('price-per-unit'));
                    var totalPriceElement = $("#total-price-" + id);
                    totalPriceElement.text("RM " + (pricePerUnit * data.quantity).toFixed(2));

                    // Reload the page
                    console.log("Reloading page after plus cart");
                    location.reload();
                } else {
                    console.error("Invalid data format: ", data);
                }
            }
        });
    });

    // Handle the minus-cart click event
    $('.minus-cart').click(function(){
        var id = $(this).attr("cid").toString();
        var eml = this.parentNode.children[2];
        
        console.log("Minus cart clicked: ", id);

        $.ajax({
            type: "GET",
            url: "/minuscart",
            data: {
                cart_item_id: id
            },
            success: function(data){
                console.log("Minus cart success", data);
                var amount = parseFloat(data.amount);
                var totalamount = parseFloat(data.totalamount);
                if (!isNaN(amount) && !isNaN(totalamount)) {
                    if (data.quantity > 0) {
                        eml.innerText = data.quantity;
                        document.getElementById("amount").innerText = 'RM ' + amount.toFixed(2); 
                        document.getElementById("totalamount").innerText = 'RM ' + totalamount.toFixed(2);

                        // Update total price for the item
                        var pricePerUnit = parseFloat($(".cart-item[data-cart-item-id='" + id + "']").data('price-per-unit'));
                        var totalPriceElement = $("#total-price-" + id);
                        totalPriceElement.text("RM " + (pricePerUnit * data.quantity).toFixed(2));
                    } else {
                        // If quantity is zero, remove the item from the cart
                        eml.parentNode.parentNode.parentNode.parentNode.remove();
                    }

                    // Reload the page
                    console.log("Reloading page after minus cart");
                    location.reload();
                } else {
                    console.error("Invalid data format: ", data);
                }
            }
        });
    });

    // Handle the remove-cart click event
    $('.remove-cart').click(function(){
        var id = $(this).attr("cid").toString();
        var eml = this;
        
        console.log("Remove cart clicked: ", id);

        $.ajax({
            type: "GET",
            url: "/removecart",
            data: {
                cart_item_id: id
            },
            success: function(data){
                console.log("Remove cart success", data);
                var amount = parseFloat(data.amount);
                var totalamount = parseFloat(data.totalamount);
                if (!isNaN(amount) && !isNaN(totalamount)) {
                    document.getElementById("amount").innerText = 'RM ' + amount.toFixed(2); 
                    document.getElementById("totalamount").innerText = 'RM ' + totalamount.toFixed(2);
                    eml.parentNode.parentNode.parentNode.parentNode.remove();

                    // Reload the page
                    console.log("Reloading page after remove cart");
                    location.reload();
                } else {
                    console.error("Invalid data format: ", data);
                }
            }
        });
    });
});

// Function to update the cart UI dynamically
function updateCartUI(data) {
    // Assuming data contains the updated quantities and prices
    var amount = parseFloat(data.amount);
    var totalamount = parseFloat(data.totalamount);
    if (!isNaN(amount) && !isNaN(totalamount)) {
        document.getElementById("amount").innerText = 'RM ' + amount.toFixed(2); 
        document.getElementById("totalamount").innerText = 'RM ' + totalamount.toFixed(2);

        data.items.forEach(function(item) {
            var quantityElement = document.querySelector(".quantity-input[data-cart-item-id='" + item.id + "']");
            if (quantityElement) {
                quantityElement.value = item.quantity;
            }

            var totalPriceElement = document.getElementById("total-price-" + item.id);
            if (totalPriceElement) {
                totalPriceElement.textContent = "RM " + (item.price_per_unit * item.quantity).toFixed(2);
            }
        });
    } else {
        console.error("Invalid data format: ", data);
    }
}

// Popup handling
document.addEventListener("DOMContentLoaded", function() {
    // Show the pop-up after 1 second
    setTimeout(function() {
        document.getElementById("popup").style.display = "flex";
    }, 1000);
});

function closePopup() {
    document.getElementById("popup").style.display = "none";
}