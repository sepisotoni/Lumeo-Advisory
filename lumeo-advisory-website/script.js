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

  // Contact form: submits directly to Formspree
  var form = document.getElementById("contact-form");
  var note = document.getElementById("form-note");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var fields = [
        form.querySelector('[name="name"]'),
        form.querySelector('[name="email"]'),
        form.querySelector('[name="business"]'),
        form.querySelector('[name="message"]')
      ];
      var valid = true;

      fields.forEach(function (field) {
        if (field.name === "business") return;
        var value = field.value.trim();
        var ok = value !== "" && (field.type !== "email" || /^\S+@\S+\.\S+$/.test(value));
        field.setAttribute("aria-invalid", ok ? "false" : "true");
        if (!ok) valid = false;
      });

      if (!valid) {
        note.className = "form-note error";
        note.textContent = "Please fill in your name, a valid email and a message.";
        return;
      }

      var submit = form.querySelector('[type="submit"]');
      var data = new FormData(form);
      data.set("_subject", "New website enquiry from " + data.get("name").trim());
      submit.disabled = true;
      note.className = "form-note";
      note.textContent = "Sending your request…";

      fetch(form.action, {
        method: "POST",
        body: data,
        headers: { "Accept": "application/json" }
      }).then(function (response) {
        if (!response.ok) {
          return response.json().then(function (result) {
            throw new Error(result.error || "Your request could not be sent. Please try again.");
          });
        }
        form.reset();
        fields.forEach(function (field) { field.removeAttribute("aria-invalid"); });
        note.className = "form-note";
        note.textContent = "Thanks, your request has been sent. We will get back to you within one working day.";
      }).catch(function (error) {
        note.className = "form-note error";
        note.textContent = error.message || "We could not send your request. Please try again or email us directly.";
      }).then(function () {
        submit.disabled = false;
      });
    });
  }
})();
