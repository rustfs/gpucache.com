(function () {
  var toggle = document.querySelector("[data-nav-toggle]");
  var nav = document.querySelector("[data-nav]");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
      nav.classList.toggle("is-open", !open);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
        toggle.focus();
      }
    });
  }

  document.querySelectorAll("pre").forEach(function (pre) {
    var code = pre.querySelector("code");
    if (!code) return;
    var copyLabel = pre.getAttribute("data-copy") || "Copy";
    var copiedLabel = pre.getAttribute("data-copied") || "Copied";
    var button = document.createElement("button");
    button.type = "button";
    button.className = "copy-button";
    button.textContent = copyLabel;
    button.addEventListener("click", function () {
      var text = code.innerText.replace(/\n$/, "");
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(text).then(function () {
        button.textContent = copiedLabel;
        window.setTimeout(function () {
          button.textContent = copyLabel;
        }, 1500);
      });
    });
    pre.appendChild(button);
  });
})();
