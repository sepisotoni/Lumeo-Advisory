(function () {
  // Change this to your real address
  var CONTACT_EMAIL = "admin@lumeo-advisory.co.za";

  var emailLink = document.getElementById("email-link");
  if (emailLink) {
    emailLink.href = "mailto:" + CONTACT_EMAIL;
    emailLink.textContent = CONTACT_EMAIL;
  }

  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Hero ledger: rows match one by one, then the status flips to Reconciled
  var rows = document.querySelectorAll("#ledger-rows li");
  var status = document.getElementById("ledger-status");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (rows.length && status) {
    if (reduce) {
      rows.forEach(function (r) { r.classList.add("is-matched"); });
    } else {
      status.textContent = "In progress";
      status.classList.add("is-pending");
      rows.forEach(function (r, i) {
        setTimeout(function () { r.classList.add("is-matched"); }, 700 + i * 420);
      });
      setTimeout(function () {
        status.textContent = "Reconciled";
        status.classList.remove("is-pending");
      }, 700 + rows.length * 420 + 200);
    }
  }

  // Blog search: filters the article list as you type
  var search = document.getElementById("post-search");
  var list = document.getElementById("post-list");
  if (search && list) {
    var items = Array.prototype.slice.call(list.querySelectorAll(".post"));
    var none = document.getElementById("no-results");
    search.addEventListener("input", function () {
      var q = search.value.trim().toLowerCase();
      var shown = 0;
      items.forEach(function (el) {
        var hit = !q || el.textContent.toLowerCase().indexOf(q) !== -1;
        el.hidden = !hit;
        if (hit) shown++;
      });
      if (none) none.hidden = shown !== 0;
    });
  }

  // Contact form: opens the visitor's email app with the details filled in
  var form = document.getElementById("contact-form");
  var note = document.getElementById("form-note");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = form.name.value.trim();
      var email = form.email.value.trim();
      var business = form.business.value.trim();
      var message = form.message.value.trim();
      var valid = true;

      [form.name, form.email, form.message].forEach(function (field) {
        var ok = field.value.trim() !== "" && (field.type !== "email" || /^\S+@\S+\.\S+$/.test(field.value.trim()));
        field.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) valid = false;
      });

      if (!valid) {
        note.className = "form-note error";
        note.textContent = "Please fill in your name, a valid email and a short message.";
        return;
      }

      var subject = "Call request from " + name + (business ? " (" + business + ")" : "");
      var body = "Name: " + name + "\nEmail: " + email + "\nBusiness: " + (business || "-") + "\n\n" + message;
      note.className = "form-note";
      note.textContent = "Opening your email app. Press send there to finish.";
      window.location.href = "mailto:" + CONTACT_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    });
  }
})();
