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

  const moonSVG = `<svg width="22" height="22" viewBox="0 0 32 32" fill="currentColor" aria-hidden="true">
      <path xmlns="http://www.w3.org/2000/svg" d="M16.8135 3.1798c.4143-.8885.8958-1.7166 1.4165-2.5039C12.7978.5843 7.5578 3.6212 5.1134 8.8633c-3.3132 7.1051-.2386 15.5523 6.8665 18.8654 5.4977 2.5636 11.786 1.2907 15.8913-2.7003-1.845.044-3.6833-.3101-5.4103-1.1154-6.9474-3.2396-9.4762-12.522-5.6473-20.7332Z"/>
    </svg>`;

  const sunSVG = `<svg width="22" height="22" viewBox="0 0 512 512" fill="currentColor" aria-hidden="true">
      <g xmlns="http://www.w3.org/2000/svg">
        <path class="st0" d="M256,118.125c-76.156,0-137.875,61.719-137.875,137.875S179.844,393.875,256,393.875   S393.875,332.156,393.875,256S332.156,118.125,256,118.125z"/>
        <rect x="235.906" class="st0" width="40.156" height="77.297"/>
        <rect x="235.906" y="434.703" class="st0" width="40.156" height="77.297"/>
        <rect x="63.657" y="82.229" transform="matrix(0.7071 0.7071 -0.7071 0.7071 102.3047 -42.376)" class="st0" width="77.296" height="40.15"/>
        <polygon class="st0" points="368.156,396.547 422.828,451.219 451.219,422.813 396.563,368.156  "/>
        <rect y="235.906" class="st0" width="77.281" height="40.156"/>
        <polygon class="st0" points="434.688,235.922 434.688,276.078 512,276.063 512,235.906  "/>
        <polygon class="st0" points="60.781,422.813 89.156,451.219 143.813,396.547 115.438,368.156  "/>
        <polygon class="st0" points="451.219,89.156 422.813,60.781 368.156,115.438 396.563,143.844  "/>
      </g>
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

  // Lazy load project images after page load
  setTimeout(() => {
    const projectImages = document.querySelectorAll('.project-image[data-src]');
    projectImages.forEach(img => {
      const src = img.getAttribute('data-src');
      img.onload = function() {
        img.style.opacity = '1';
      };
      img.src = src;
      img.removeAttribute('data-src');
    });
  }, 100);
});