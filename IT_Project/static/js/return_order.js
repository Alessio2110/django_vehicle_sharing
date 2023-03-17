
amount = cost_for_initial_order + cost_per_minute * 130 
console.log(amount)
$(document).ready(function() {
    var datetime = new Date(datetimeString);  // Convert the datetime string to a Date object
    console.log("Datetime:", datetime)
    // Update the timer every second
    setInterval(function() {
        var now = new Date();  // Get the current date and time
        var diff = Math.floor((now - datetime) / 1000);  // Calculate the time difference in seconds
        var minutes = Math.floor(diff % 3600 / 60);  // Convert seconds to minutes
        var hours = Math.floor(diff / 3600);  // Convert seconds to hours
        var seconds = diff % 60;  // Get the remaining seconds
        var displayMinutes = minutes.toString().padStart(2, '0');
        var displaySeconds = seconds.toString().padStart(2, '0');
        var displayHours = hours.toString().padStart(2, '0');
        amount = cost_for_initial_order + cost_per_minute * minutes + cost_per_minute * 60 * hours
        var amount = (amount / 100).toLocaleString('en-US', { style: 'currency', currency: 'GBP'});
        
        $('#timer').text('⏱️ ' + displayHours + ":" +  displayMinutes + ':' + displaySeconds + '');
            //   $('#timer').text('Time elapsed < ' + time_str + '>');
        $('#price').text('💳   ' + amount)
    }, 1000);
  });



  // Default selected icon is bike



// //AJAX POST REQUEST: CREATE ORDER
// function createOrder(){
//     fetch('/create_order/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json',
//           'X-CSRFToken': getCookie('csrftoken')
//         },
//         body: JSON.stringify({
//           username: username,
//           vehicle_type: selected,
//           loc_id: loc_id
//         })
//       }).then(function(response) {
//         if (response.ok) {
//           window.location.href = '/success/'; // Redirect to the success page
//         } else {
//           // Handle errors
//         }
//       }).catch(function(error) {
//         // Handle errors
//       });
// }
document.getElementById("submit-button").addEventListener("click", function() {
    console.log("Clicked")
    if (location_address == null){
        alert("No location chosen: find a secure place nearby to leave your vehicle ")
        return;
    }
    if (confirm("Are you sure you are ready to leave the vehicle at '" + location_address + "' ?")) {
      concludeOrder()
    } else {
    }
  });

function concludeOrder(){
    console.log("Return")
    fetch('/conclude_order/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
          username: username,
          order_id: order_id,
          loc_id: loc_id
        })
      }).then(function(response) {
        if (response.ok) {
          window.location.href = success_url; // Redirect to the success page
        } 
      }).catch(function(error) {
        console.log(error)
      });
}