 window.addEventListener("load", () => {
    function sendData() {
      const XHR = new XMLHttpRequest();

      // Bind the FormData object and the form element
      const FD = new FormData(form);

      // Define what happens on successful data submission
      XHR.addEventListener("load", (event) => {
        let button = document.getElementById("submit-button");
        button.innerHTML = "Message sent!";
        button.setAttribute("disabled", "");
        document.getElementById("name").setAttribute("disabled", "");
        document.getElementById("email").setAttribute("disabled", "");
        document.getElementById("textarea").setAttribute("disabled", "");
      });

      // Define what happens in case of error
      XHR.addEventListener("error", (event) => {
        console.error('Request to server failed');
      });

      // Set up our request
      XHR.open("POST", "submit.php");

      // The data sent is what the user provided in the form
      XHR.send(FD);
    }

    // Get the form element
    const form = document.getElementById("contact-form");

    // Add 'submit' event handler
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      let button = document.getElementById("submit-button");
        button.innerHTML = "Sending...";
        button.setAttribute("disabled", "");

      sendData();
    });
  });