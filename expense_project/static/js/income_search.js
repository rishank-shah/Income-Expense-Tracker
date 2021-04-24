const searchField = document.querySelector("#searchField");
const paginationContainer = document.querySelector(".pagination-container");
const income_count = document.getElementById("income_count");
let income_count_initial = income_count.innerHTML;
const tbody = document.querySelector("#table-body-data");
let income_list = tbody.innerHTML;
const no_results = document.getElementById("no-results");

searchField.addEventListener("keyup", (e) => {
  const delay = setTimeout(() => {
    searchFunction(e);
  }, 500);
  return () => clearTimeout(delay);
});

const searchFunction = (e) => {
  const searchValue = e.target.value;
  no_results.style.display = "none";
  if (searchValue.trim().length > 0) {
    paginationContainer.style.display = "none";
    tbody.innerHTML = "";
    fetch("/income/search", {
      body: JSON.stringify({ search_query: searchValue }),
      method: "POST",
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        income_count.innerHTML = data.length;
        if (data.length === 0) {
          no_results.style.display = "block";
        } else {
          no_results.style.display = "none";
          tbody.innerHTML = "";
          data.forEach((item) => {
            tbody.innerHTML += `
                <tr>
                <td>${item.amount}</td>
                <td>${
                  item.source__source.length > 20
                    ? item.source__source.substring(0, 19) + "..."
                    : item.source__source
                }</td>
                <td>${
                  item.description.length > 30
                    ? item.description.substring(0, 29) + "..."
                    : item.description
                }</td>
                <td>${item.date}</td>
                <td><a href="/income/edit-income/${
                  item.id
                }" class="btn btn-warning btn-sm">Edit</a></td>
                </tr>`;
          });
        }
      });
  } else {
    paginationContainer.style.display = "block";
    tbody.innerHTML = income_list;
    income_count.innerHTML = income_count_initial;
  }
};

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
