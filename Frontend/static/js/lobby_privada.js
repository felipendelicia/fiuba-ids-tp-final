var now = new Date();
var currentMonth = now.getMonth() + 1;
var currentYear = now.getFullYear();
var selectedDate = null;

var monthNames = ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
                  'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];

function fmtLocal(d) {
    var y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var day = String(d.getDate()).padStart(2, '0');
    return y + '-' + m + '-' + day;
}

function buildCalendar(month, year) {
    var firstDay = new Date(year, month - 1, 1);
    var start = new Date(firstDay);
    start.setDate(start.getDate() - start.getDay() + (start.getDay() === 0 ? -6 : 1));
    var today = new Date();
    var todayStr = fmtLocal(today);

    document.getElementById('calendarTitle').textContent = monthNames[month - 1] + ' ' + year;

    var html = '';
    for (var i = 0; i < 35; i++) {
        var d = new Date(start);
        d.setDate(start.getDate() + i);
        var num = d.getDate();
        var dateStr = fmtLocal(d);
        var isCurrent = d.getMonth() === month - 1 && d.getFullYear() === year;
        var isToday = dateStr === todayStr;
        var isSelected = dateStr === selectedDate;

        var cls = '';
        if (!isCurrent) cls += ' day-other';
        if (isToday) cls += ' day-today';
        if (isSelected) cls += ' day-selected';

        html += '<div class="' + cls.trim() + '" data-date="' + dateStr + '">' + num + '</div>';
    }
    document.getElementById('calendarDays').innerHTML = html;

    document.querySelectorAll('#calendarDays div[data-date]').forEach(function(el) {
        el.addEventListener('click', function(e) {
            var date = this.getAttribute('data-date');
            selectedDate = date;
            document.getElementById('inputFecha').value = date;
            document.querySelectorAll('#calendarDays .day-selected, #calendarDays .day-today').forEach(function(x) {
                x.classList.remove('day-selected', 'day-today');
            });
            this.classList.add('day-selected');
            if (date === todayStr) this.classList.add('day-today');
            cargarTurnos(date);
        });
    });
}

function seleccionarTurno(el, slotId) {
    document.querySelectorAll('#turnosGrid .turno-slot.seleccionado').forEach(function(x) {
        x.classList.remove('seleccionado');
    });
    el.classList.add('seleccionado');
    document.getElementById('inputTurno').value = slotId;
}

function cargarTurnos(fecha) {
    var loading = document.getElementById('calendarLoading');
    var container = document.getElementById('turnosContainer');
    var grid = document.getElementById('turnosGrid');

    loading.classList.remove('d-none');
    container.classList.add('d-none');
    document.getElementById('inputTurno').value = '';

    fetch('/api/turnos-disponibles?date=' + fecha)
        .then(function(r) { return r.json(); })
        .then(function(data) {
            var html = '';
            data.turnos.forEach(function(slot) {
                var cls = slot.disponible ? 'turno-slot disponible' : 'turno-slot ocupado';
                html += '<div class="' + cls + '" data-slot="' + slot.id + '">' + slot.label + '</div>';
            });
            grid.innerHTML = html;
            grid.querySelectorAll('.turno-slot.disponible').forEach(function(el) {
                el.addEventListener('click', function(e) {
                    seleccionarTurno(this, this.getAttribute('data-slot'));
                });
            });
            container.classList.remove('d-none');
            loading.classList.add('d-none');
        })
        .catch(function() {
            loading.classList.add('d-none');
        });
}

var preciosModalidad = {'1': 5000, '2': 4500, '3': 4000, '4': 5500};
var preciosCampo = {'1': 3000, '2': 3500, '3': 4000, '4': 4500};
//var preciosPack = {'basico': 2000};

function filtrarCampos() {
    var selectMod = document.getElementById('modalidad');
    var opcion = selectMod.options[selectMod.selectedIndex];
    var data = opcion.getAttribute('data-map-ids') || '';
    var ids = data.split(',').filter(Boolean);
    var campoSelect = document.getElementById('campo');
    for (var i = 0; i < campoSelect.options.length; i++) {
        var opt = campoSelect.options[i];
        if (ids.indexOf(opt.value) === -1) {
            opt.classList.add('oculto');
        } else {
            opt.classList.remove('oculto');
        }
    }
}

function calcularTotal() {
    var mod = document.getElementById('modalidad').value;
    var campo = document.getElementById('campo').value;
    //var pack = document.getElementById('pack').value;
    var packSelect = document.getElementById('pack');
    var packSelectedOption = packSelect.options[packSelect.selectedIndex];

    var precioPack = 0;
    if (packSelectedOption && packSelectedOption.hasAttribute('precio')){
	    precioPack = parseFloat(packSelectedOption.getAttribute('precio')) || 0;
    }


    var total = (preciosModalidad[mod] || 0) + (preciosCampo[campo] || 0) + (precioPack || 0);
    document.getElementById('precioTotal').textContent = '$' + total.toLocaleString('es-AR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
    document.getElementById('inputPrecio').value = total;
}

document.addEventListener('DOMContentLoaded', function() {
    buildCalendar(currentMonth, currentYear);

    document.getElementById('prevMonth').addEventListener('click', function() {
        currentMonth--;
        if (currentMonth < 1) { currentMonth = 12; currentYear--; }
        buildCalendar(currentMonth, currentYear);
        document.getElementById('turnosContainer').classList.add('d-none');
        selectedDate = null;
    });

    document.getElementById('nextMonth').addEventListener('click', function() {
        currentMonth++;
        if (currentMonth > 12) { currentMonth = 1; currentYear++; }
        buildCalendar(currentMonth, currentYear);
        document.getElementById('turnosContainer').classList.add('d-none');
        selectedDate = null;
    });

    document.getElementById('reservaForm').addEventListener('submit', function(e) {
        if (!document.getElementById('inputFecha').value || !document.getElementById('inputTurno').value) {
            e.preventDefault();
            alert('Seleccioná una fecha y un turno antes de confirmar.');
        }
    });

    var todayEl = document.querySelector('#calendarDays .day-today');
    if (todayEl) {
        selectedDate = todayEl.getAttribute('data-date');
        document.getElementById('inputFecha').value = selectedDate;
        todayEl.classList.add('day-selected');
        cargarTurnos(selectedDate);
    }

    document.getElementById('modalidad').addEventListener('change', filtrarCampos);
    document.getElementById('campo').addEventListener('change', calcularTotal);
    document.getElementById('pack').addEventListener('change', calcularTotal);

    filtrarCampos();
});
