document.querySelector('#add_to_cart').onsubmit = function() {

  // Create request object
  const request = new XMLHttpRequest();

  // Variable to get the pizza selected from the document
  let pizza_selected = document.querySelector('#pizza_name').value;

  // Initialize the request
  request.open('POST', '/add_to_cart');

  // Callback function when request completes
  request.onload() = () => {

    // Extract JSON data from the request
    const data = JSON.parse(request.responseText);

    // Give feedback to user upon success/failure
    if(data.success) {
      const p = document.createElement("p");
      p.innerHTML = "Pizza added to the cart!";

      document.querySelector('#cart').append(p);
    }
    else {
      const p = document.createElement("p");
      p.innerHTML = "No pizza selected!";
      document.querySelector('#cart').append(p);
    }
  };

  // Add data to send with the request
  const data = new FormData();
  data.append('pizza', pizza_selected);

  // Send request
  request.send(data);

  // Stop form submitting to another page
  return false;
};

// Function to add topping
document.querySelector('#add_topping').onsubmit = () => {

  // Create request object
  const request = new XMLHttpRequest();

  // Variables to determine the size and topping selected from the document
  let topping_selected = document.querySelector('#topping_selected').value;

  // Initialize the request
  request.open('POST', '/add_topping', true);

  // Set RequestHeader as csfrtoken
  request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

  // Callback function when the function completes
  request.onload() = () => {

    // Extract JSON data from the request object
    const data = JSON.parse(request.responseText);

    console.log(data);
    console.log(json);
    console.log(request);

    // Give feedback to user upon success/failure
    if(data.success) {
      const p = document.createElement("p");
      p.innerHTML = "Topping added.";

      // Append it to the #summary_before_add_to_cart div
      document.querySelector('#summary_before_add_to_cart').append(p);
    }
    else {
      const p = document.createElement("p");
      p.innerHTML = "No topping added yet.";

      // Append it to the #summary_before_add_to_cart div
      document.querySelector('#summary_before_add_to_cart').append(p);
    }
  };

  // Add data to send with the request
  const data = new FormData();
  data.append('topping_selected', topping_selected);

  request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));

  // Send the request
  request.send(data);

  // Stop submitting to another page
  return false;
};

function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 };
