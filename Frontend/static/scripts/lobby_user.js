function actualizarDisponibles() {
    var campoSelect = document.getElementById('campo');
    var fechaInput = document.querySelector('input[name="reservation_date"]');
    var turnoSelect = document.querySelector('select[name="turno"]');
    var span = document.getElementById('disponibles');

    var mapId = campoSelect.value;
    var fecha = fechaInput.value;
    var turnoVal = turnoSelect.value;

    if (!mapId || !fecha || !turnoVal) {
        span.textContent = '';
        return;
    }

    var modSelect = document.getElementById('modalidad');
    var modOpcion = modSelect.options[modSelect.selectedIndex];
    var maxCupo = parseInt(modOpcion.getAttribute('data-max-cupo') || '4', 10);

    var slotMap = JSON.parse(document.getElementById('slot-map-data').textContent);
    var times = slotMap[turnoVal] || [];
    if (times.length < 2) {
        span.textContent = '';
        return;
    }
    var st = times[0], et = times[1];

    var reservasData = JSON.parse(document.getElementById('reservas-data').textContent);

    var count = reservasData.filter(function(r) {
        return String(r.map_id) === String(mapId)
            && r.reservation_date === fecha
            && r.start_time === st
            && r.end_time === et;
    }).length;

    var disponibles = maxCupo - count;
    if (disponibles <= 0) {
        span.textContent = 'LLENO';
        span.style.color = '#ff5252';
    } else {
        span.textContent = disponibles + ' / ' + maxCupo + ' disponibles';
        span.style.color = '#4caf50';
    }
}

function filtrarCampos() {
    var selectMod = document.getElementById('modalidad');
    var opcion = selectMod.options[selectMod.selectedIndex];
    var data = opcion.getAttribute('data-map-ids') || '';
    var ids = data.split(',').filter(Boolean);
    var campoSelect = document.getElementById('campo');
    campoSelect.selectedIndex = 0;
    campoSelect.disabled = !data;
    for (var i = 0; i < campoSelect.options.length; i++) {
        var opt = campoSelect.options[i];
        if (i === 0) continue;
        if (ids.indexOf(opt.value) === -1) {
            opt.classList.add('oculto');
        } else {
            opt.classList.remove('oculto');
        }
    }
    actualizarDisponibles();
}

document.addEventListener('DOMContentLoaded', function() {
    var modSelect = document.getElementById('modalidad');
    if (modSelect) {
        document.getElementById('campo').addEventListener('change', actualizarDisponibles);
        document.querySelector('input[name="reservation_date"]').addEventListener('change', actualizarDisponibles);
        document.querySelector('select[name="turno"]').addEventListener('change', actualizarDisponibles);
        document.getElementById('modalidad').addEventListener('change', filtrarCampos);
        filtrarCampos();
    }

    document.querySelectorAll('.kit-select').forEach(function(sel) {
        sel.addEventListener('change', function() {
            var salaId = this.id.replace('kit-', '');
            var baseEl = document.getElementById('precio-base-' + salaId);
            var kitEl = document.getElementById('precio-kit-' + salaId);
            var totalEl = document.getElementById('precio-total-' + salaId);
            if (!baseEl) return;
            var base = parseInt(baseEl.textContent.replace('$', '').replace(/\./g, '')) || 0;
            if (this.value) {
                var option = this.options[this.selectedIndex];
                var kitPrice = parseInt(option.dataset.price) || 0;
                kitEl.textContent = ' + $' + kitPrice + ' (kit)';
                kitEl.style.display = 'inline';
                totalEl.textContent = ' = $' + (base + kitPrice);
                totalEl.style.display = 'inline';
            } else {
                kitEl.style.display = 'none';
                totalEl.style.display = 'none';
            }
        });
    });

    document.querySelectorAll('.btn-unirse').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var salaId = this.dataset.salaId;
            var kit = document.getElementById('kit-' + salaId);
            if (!kit || !kit.value) {
                alert('Seleccioná un kit de equipamiento primero.');
                return;
            }
            var baseEl = document.getElementById('precio-base-' + salaId);
            var base = baseEl ? parseInt(String(baseEl.textContent).replace('$', '').replace(/\./g, '')) || 0 : 0;
            var option = kit.options[kit.selectedIndex];
            var kitPrice = option && option.dataset.price ? parseInt(option.dataset.price) || 0 : 0;
            var totalPrice = base + kitPrice;
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = '/lobby/unirse-publica';
            form.appendChild(hiddenInput('sala_id', salaId));
            form.appendChild(hiddenInput('equipment_kit_id', kit.value));
            form.appendChild(hiddenInput('total_price', totalPrice));
            document.body.appendChild(form);
            form.submit();
        });
    });
});

function hiddenInput(name, value) {
    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = name;
    input.value = value;
    return input;
}
