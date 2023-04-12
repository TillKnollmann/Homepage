 window.addEventListener("load", () => {
    function sendData() {
      const XHR = new XMLHttpRequest();

      // Bind the FormData object and the form element
      const FD = new FormData(form);

      // determine language
      var notifications;

      if (lang === "de") {
        notifications = de;
      }
      if (lang === "en") {
        notifications = en;
      }

      let button = document.getElementById("submit-button");
      button.innerHTML = notifications[0];
      button.setAttribute("disabled", "");

      // Define what happens on successful data submission
      XHR.addEventListener("load", (event) => {
        let button = document.getElementById("submit-button");
        button.innerHTML = notifications[1];
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
      XHR.open("POST", "../submit.php");

      // The data sent is what the user provided in the form
      XHR.send(FD);
    }

    // Get the form element
    const form = document.getElementById("contact-form");

    // get the language
    const lang = document.getElementsByTagName("html")[0].getAttribute("lang");

    const en = ["Sending ...", "Sent!"];
    const de = ["Sendet ...", "Gesendet!"];

    // Add 'submit' event handler
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      sendData();
    });
  });