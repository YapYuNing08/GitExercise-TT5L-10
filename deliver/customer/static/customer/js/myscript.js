$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

// original ver.
// $('.plus-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this.parentNode.children[2];
//     var quantity = parseInt(eml.innerText);
//     $.ajax({
//         type:"GET",
//         url:"/pluscart",
//         data:{
//             prod_id:id,
//             quantity:quantity
//         },
//         success:function(data){
//             // console.log("data=",data);
//             eml.innerText=data.quantity; 
//             document.getElementById("amount").innerText=data.amount; 
//             document.getElementById("totalamount").innerText=data.totalamount;
//         }
//     })
// })

// $('.minus-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this.parentNode.children[2] 
//     $.ajax({
//         type:"GET",
//         url:"/minuscart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             eml.innerText=data.quantity 
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount
//         }
//     })
// })

// $('.remove-cart').click(function(){
//     var id=$(this).attr("pid").toString();
//     var eml=this
//     $.ajax({
//         type:"GET",
//         url:"/removecart",
//         data:{
//             prod_id:id
//         },
//         success:function(data){
//             document.getElementById("amount").innerText=data.amount 
//             document.getElementById("totalamount").innerText=data.totalamount
//             eml.parentNode.parentNode.parentNode.parentNode.remove() 
//         }
//     })
// })


// testing
$(document).ready(function(){
    $('.quantity-input').change(function(){
        var id = $(this).attr("id").replace("quantity-", "");
        var quantity = $(this).val();
        $.ajax({
            type: "GET",
            url: "/updatecart",
            data: {
                prod_id: id,
                quantity: quantity
            },
            success: function(){
                location.reload(); // Reload the page to update the cart section
            }
        })
    });

    $('.plus-cart').click(function(){
        var id = $(this).attr("pid").toString();
        var eml = this.parentNode.children[2];
        var quantity = parseInt(eml.innerText);
        $.ajax({
            type: "GET",
            url: "/pluscart",
            data: {
                prod_id: id,
                quantity: quantity
            },
            success: function(data){
                eml.innerText = data.quantity; 
                document.getElementById("amount").innerText = data.amount; 
                document.getElementById("totalamount").innerText = data.totalamount;
                location.reload();

                // Update total price for the item
                var pricePerUnit = parseFloat($(".cart-item[data-product-id='" + id + "']").data('price-per-unit'));
                var totalPriceElement = $("#total-price-" + id);
                totalPriceElement.text("RM " + (pricePerUnit * data.quantity).toFixed(2));
            }
        })
    });

    $('.minus-cart').click(function(){
        var id = $(this).attr("pid").toString();
        var eml = this.parentNode.children[2];
        $.ajax({
            type: "GET",
            url: "/minuscart",
            data: {
                prod_id: id
            },
            success: function(data){
                eml.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                location.reload();

                // Update total price for the item
                var pricePerUnit = parseFloat($(".cart-item[data-product-id='" + id + "']").data('price-per-unit'));
                var totalPriceElement = $("#total-price-" + id);
                totalPriceElement.text("RM " + (pricePerUnit * data.quantity).toFixed(2));
            }
        })
    });

    $('.remove-cart').click(function(){
        var id = $(this).attr("pid").toString();
        var eml = this;
        $.ajax({
            type: "GET",
            url: "/removecart",
            data: {
                prod_id: id
            },
            success: function(data){
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                eml.parentNode.parentNode.parentNode.parentNode.remove();
            }
        })
    });
});


// update info/ad section
document.addEventListener("DOMContentLoaded", function() {
    // Show the pop-up after 1 second
    setTimeout(function() {
        document.getElementById("popup").style.display = "flex";
    }, 1000);
});

function closePopup() {
    document.getElementById("popup").style.display = "none";
}