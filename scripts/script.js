window.addEventListener("load", () => {

  // Theme toggle
  function getPreferredTheme() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    icon.innerHTML = theme === 'dark' ? sunSVG : moonSVG;
  }

  const btn = document.getElementById('theme-toggle');
  const icon = document.getElementById('theme-toggle-icon');
  if (!btn || !icon) return;

  const moonSVG = `<svg width="22" height="22" viewBox="0 0 384 512" fill="currentColor" aria-hidden="true">
      <path d="M 233.5 32 C 110 32 10 132.3 10 256 S 110 480 233.5 480 c 60.6 0 115.5 -24.2 155.8 -63.4 c 5 -4.9 6.3 -12.5 3.1 -18.7 s -10.1 -9.7 -17 -8.5 c -9.8 1.7 -19.8 2.6 -30.1 2.6 c -96.9 0 -175.5 -78.8 -175.5 -176 c 0 -65.8 36 -123.1 89.3 -153.3 c 6.1 -3.5 9.2 -10.5 7.7 -17.3 s -7.3 -11.9 -14.3 -12.5 c -6.3 -0.5 -12.6 -0.8 -19 -0.8 z"/>
    </svg>`;

  const sunSVG = `<svg width="22" height="22" viewBox="0 0 512 512" fill="currentColor" aria-hidden="true">
      <path d="M361.5 1.2c5 2.1 8.6 6.6 9.6 11.9L391 121l107.9 19.8c5.3 1 9.8 4.6 11.9 9.6s1.5 10.7-1.6 15.2L446.9 256l62.3 90.3c3.1 4.5 3.7 10.2 1.6 15.2s-6.6 8.6-11.9 9.6L391 391 371.1 498.9c-1 5.3-4.6 9.8-9.6 11.9s-10.7 1.5-15.2-1.6L256 446.9l-90.3 62.3c-4.5 3.1-10.2 3.7-15.2 1.6s-8.6-6.6-9.6-11.9L121 391 13.1 371.1c-5.3-1-9.8-4.6-11.9-9.6s-1.5-10.7 1.6-15.2L65.1 256 2.8 165.7c-3.1-4.5-3.7-10.2-1.6-15.2s6.6-8.6 11.9-9.6L121 121 140.9 13.1c1-5.3 4.6-9.8 9.6-11.9s10.7-1.5 15.2 1.6L256 65.1 346.3 2.8c4.5-3.1 10.2-3.7 15.2-1.6zM160 256a96 96 0 1 1 192 0 96 96 0 1 1 -192 0zm224 0a128 128 0 1 0 -256 0 128 128 0 1 0 256 0z"/>
    </svg>`;

  setTheme(getPreferredTheme());

  btn.addEventListener('click', function () {
    const current = document.documentElement.getAttribute('data-theme');
    setTheme(current === 'dark' ? 'light' : 'dark');
  });

  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    setTheme(e.matches ? 'dark' : 'light');
  });

  // Image overlay
  const profilePic = document.getElementById("profile-picture");
  const overlay = document.getElementById("image-overlay");
  const overlayBg = document.getElementById("overlay-bg");
  const overlayContent = document.getElementById("overlay-content");
  const spinner = document.getElementById("spinner");
  const largeImg = document.getElementById("large-profile-picture");

  let imageLoaded = false;

  if (profilePic) {
    profilePic.addEventListener("click", function () {
      overlay.style.display = "flex";
      if (imageLoaded) {
        spinner.style.display = "none";
        largeImg.style.display = "block";
      } else {
        spinner.style.display = "block";
        largeImg.style.display = "none";
      }
    });
  }

  if (largeImg) {
    largeImg.onload = function () {
      imageLoaded = true;
      if (overlay.style.display === "flex") {
        spinner.style.display = "none";
        largeImg.style.display = "block";
      }
    };
    largeImg.onerror = function () {
      imageLoaded = false;
      if (overlay.style.display === "flex") {
        spinner.style.display = "none";
        overlayContent.innerHTML = "<div style='color:white'>Could not load image.</div>";
      }
    };

    // Preload large image after page load with slight delay
    if (profilePic) {
      setTimeout(() => {
        const largeSrc = profilePic.getAttribute("data-large-src");
        if (largeSrc) {
          largeImg.src = largeSrc;
        }
      }, 100);
    }
  }

  if (overlayBg) {
    overlayBg.addEventListener("click", function () {
      overlay.style.display = "none";
    });
  }
  if (largeImg) {
    largeImg.addEventListener("click", function () {
      overlay.style.display = "none";
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      overlay.style.display = "none";
    }
  });

  // Form submission
  function sendData() {
    const XHR = new XMLHttpRequest();

    const FD = new FormData(form);

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

    XHR.addEventListener("load", (event) => {
      let button = document.getElementById("submit-button");
      button.innerHTML = notifications[1];
      button.setAttribute("disabled", "");
      document.getElementById("name").setAttribute("disabled", "");
      document.getElementById("email").setAttribute("disabled", "");
      document.getElementById("textarea").setAttribute("disabled", "");
    });

    XHR.addEventListener("error", (event) => {
      console.error('Request to server failed');
    });

    XHR.open("POST", "../submit.php");

    XHR.send(FD);
  }

  const form = document.getElementById("contact-form");

  const lang = document.getElementsByTagName("html")[0].getAttribute("lang");

  const en = ["Sending ...", "Sent!"];
  const de = ["Sendet ...", "Gesendet!"];

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    sendData();
  });
});