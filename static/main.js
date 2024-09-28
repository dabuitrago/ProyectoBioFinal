
    function getParamos() {
        var departamento = document.getElementById("departamento").value;
        fetch('/get_paramos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'departamento=' + encodeURIComponent(departamento)
        })
        .then(response => response.json())
        .then(data => {
            var tableBody = document.getElementById("paramos-table").getElementsByTagName("tbody")[0];
            tableBody.innerHTML = ""; // Limpiar la tabla antes de agregar nuevos datos
            data.forEach(function(item) {
                var row = document.createElement("tr");
                var cell1 = document.createElement("td");
                cell1.textContent = item.nombre_paramo; // Nombre del páramo
                var cell2 = document.createElement("td");
                cell2.textContent = item.total_hectareas.toFixed(2); // Área total en hectáreas
                var cell3 = document.createElement("td");
                cell3.textContent = item.municipios; // Municipios
                row.appendChild(cell1);
                row.appendChild(cell2);
                row.appendChild(cell3);
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error(error));
    }
