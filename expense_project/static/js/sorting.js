function clearFilters() {
  document.getElementById("date_from").value = "";
  document.getElementById("date_to").value = "";
}
amount_up = document.getElementById("amount_up");
amount_down = document.getElementById("amount_down");
date_up = document.getElementById("date_up");
date_down = document.getElementById("date_down");
amount_up_form = document.getElementById("amount_up_form");
amount_down_form = document.getElementById("amount_down_form");
date_up_form = document.getElementById("date_up_form");
date_down_form = document.getElementById("date_down_form");
amount_up.addEventListener("click", (e) => amount_up_form.submit());
amount_down.addEventListener("click", (e) => amount_down_form.submit());
date_up.addEventListener("click", (e) => date_up_form.submit());
date_down.addEventListener("click", (e) => date_down_form.submit());
