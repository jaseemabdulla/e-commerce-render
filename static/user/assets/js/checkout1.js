$(document).ready(function () {
   
   $('.payWithRazorpay').click(function (e) { 
      e.preventDefault();

      var address = $("[name='address']").val();
      var token = $("[name='csrfmiddlewaretoken']").val();

      $.ajax({
         method: "GET",
         url: "/proceed_to_pay/",
         success: function (response) {
            console.log(response)

            var options = {
               "key": "rzp_test_N99cHmOCgAjJPj", // Enter the Key ID generated from the Dashboard
               "amount": response.total_price*100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
               "currency": "INR",
               "name": "LojLove", //your business name
               "description": "Thank You",
               "image": "https://example.com/your_logo",
               // "order_id": "order_9A33XWu170gUtm", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
               
               "handler": function (responseb){
                  // alert(responseb.razorpay_payment_id);
                  data = {
                    
                    'address':address,
                    'payment_method':'Razorpay',
                    'payment_id':responseb.razorpay_payment_id,
                     csrfmiddlewaretoken: token

                  }
                  
                  $.ajax({
                     method: "POST",
                     url: "/place_order/",
                     data: data,
                    
                     success: function (responsec) {
                        Swal.fire("Congratulations!", responsec.status, "success").then((value) => {
                        
                           window.location.href = '/rpay_order_summary/' + responsec.order_id;
                           
                          
                         });
                     }
                  });

              }, 
              

               "prefill": { //We recommend using the prefill parameter to auto-fill customer's contact information especially their phone number
                   "name": "Gaurav Kumar", //your customer's name
                   "email": "gaurav.kumar@example.com",
                   "contact": "9000090000" //Provide the customer's phone number for better conversion rates 
               },
               "notes": {
                   "address": "Razorpay Corporate Office"
               },
               "theme": {
                   "color": "#3399cc"
               }
           };
           var rzp1 = new Razorpay(options);
           rzp1.open(); 

         }
      });


      
      
   });


});