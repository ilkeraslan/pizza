document.querySelector('#add_to_cart').onsubmit = function() {

  // Create request object
  const request = new XMLHttpRequest();

  // Variable to get the pizza selected from the document
  let pizza_selected = document.querySelector('').value;

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
  data.append('pizza', pizza);

  // Send request
  request.send(data);

  // Clear form
  document.querySelector('').value = '';

  // Stop form submitting to another page
  return false;
};
