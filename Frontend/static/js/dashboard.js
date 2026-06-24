function actualizar_pie() {
  var pieChart = document.getElementById("pie-chart");
  if (!pieChart) return;
  var ocupadas = parseInt(pieChart.getAttribute("data-ocupadas")) || 0;
  var total = parseInt(pieChart.getAttribute("data-total")) || 32;
  var porcentaje = total > 0 ? Math.round((ocupadas / total) * 100) : 0;
  var pieDate = document.getElementById("pieDate");
  pieDate.innerText = porcentaje + "%";
  pieChart.style.background = "conic-gradient(#00f2fe 0% " + porcentaje + "%, rgba(0,0,0,0.3) " + porcentaje + "% 100%)";
}

function cargarFecha(fecha, clickedEl) {
  var loading = document.getElementById("calendarLoading");
  loading.style.display = "block";

  document.querySelectorAll(".calendar-days .day-today, .calendar-days .day-selected").forEach(function(el) {
    el.classList.remove("day-today", "day-selected");
  });

  fetch("/api/dashboard/data?date=" + fecha)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      document.querySelectorAll(".kpi-value")[0].innerText = "$" + data.ingresos.dia;
      document.querySelectorAll(".kpi-value")[1].innerText = "$" + data.ingresos.semana;
      document.querySelectorAll(".kpi-value")[2].innerText = "$" + data.ingresos.mes;
      document.querySelectorAll(".kpi-value")[3].innerText = "$" + data.ingresos["a\u00f1o"];

      var barras = document.querySelectorAll(".chart-bar");
      var slots = ["cs","so","nd","od","tc","qs","do","dv"];
      var labels = ["5-7","7-9","9-11","11-13","13-15","15-17","17-19","19-21"];
      for (var i = 0; i < barras.length; i++) {
        var val = data.frecuencia[slots[i]] || 0;
        barras[i].style.height = (val * 2 + 2) + "rem";
        barras[i].innerHTML = "<span>" + labels[i] + "<br>(" + val + ")</span>";
      }

      var container = document.getElementById("reservationsBody");
      var html = "";
      data.reservas.forEach(function(r) {
        var st = r.start_time && r.start_time !== "-" ? r.start_time.substring(0, 8) : "-";
        var et = r.end_time && r.end_time !== "-" ? r.end_time.substring(0, 8) : "-";
        html += '<div class="reservations-row">';
        html += '<div>' + r.id_reserva + '</div>';
        html += '<div class="name_user_r">' + r.user_name + '</div>';
        html += '<div>' + r.dni_usuario + '</div>';
        html += '<div>' + r.user_name + '</div>';
        html += '<div>$' + r.price + '</div>';
        html += '<div>' + st + " - " + et + '</div>';
        html += '<div>' + (r.map_name || "-") + '</div>';
        html += '<div>' + (r.is_public ? "Publica" : "Privada") + '</div>';
        html += '</div>';
      });
      if (data.reservas.length === 0) {
        html += '<div class="reservations-row"><div class="dim" style="flex:1;text-align:center">Sin reservas para esta fecha</div></div>';
      }
      container.innerHTML = html;

      var pieChart = document.getElementById("pie-chart");
      pieChart.setAttribute("data-ocupadas", data.total_ocupadas);
      pieChart.setAttribute("data-total", data.total_capacidad);
      actualizar_pie();

      if (clickedEl) {
        clickedEl.classList.add("day-selected");
      }

      loading.style.display = "none";
    })
    .catch(function() {
      loading.style.display = "none";
    });
}

document.addEventListener("DOMContentLoaded", function() {
  actualizar_pie();

  var days = document.querySelectorAll(".calendar-days div");
  days.forEach(function(el) {
    el.addEventListener("click", function(e) {
      var fecha = this.getAttribute("data-date");
      if (fecha) {
        cargarFecha(fecha, this);
      }
    });
  });
});
