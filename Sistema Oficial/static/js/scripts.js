
function listarMotoristas() {
    fetch("listar_motoristas.py")
        .then(response => response.json())
        .then(data => {
            const tabelaMotoristas = document.getElementById("tabela_motoristas");
            tabelaMotoristas.innerHTML = "";

            data.forEach(motorista => {
                const tr = document.createElement("tr");
                const tdNome = document.createElement("td");
                const tdStatus = document.createElement("td");

                tdNome.textContent = motorista[0];
                tdStatus.textContent = motorista[1];

                tr.appendChild(tdNome);
                tr.appendChild(tdStatus);
                tabelaMotoristas.appendChild(tr);
            });
        })
        .catch(error => {
            console.error("Erro ao listar motoristas:", error);
        });
}

// Chame a função listarMotoristas quando a página for carregada
document.addEventListener("DOMContentLoaded", listarMotoristas);

function initMap() {
    // Coordenadas do centro do mapa
    const center = { lat: -23.550520, lng: -46.633308 }; // São Paulo, por exemplo

    // Crie um novo mapa e defina as opções do mapa
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: center,
    });

    // Recuperar as coordenadas dos motoristas e adicionar marcadores no mapa
    fetch("listar_coordenadas_motoristas.py")
        .then(response => response.json())
        .then(data => {
            data.forEach(motorista => {
                const coordenadas = {
                    lat: parseFloat(motorista[0]),
                    lng: parseFloat(motorista[1])
                };
                new google.maps.Marker({
                    position: coordenadas,
                    map: map,
                });
            });
        })
        .catch(error => {
            console.error("Erro ao listar coordenadas dos motoristas:", error);
        });

    // Adicione aqui qualquer outra funcionalidade relacionada ao mapa
}


// Função para atualizar o status do motorista
function atualizarStatusMotorista(usuario, status) {
    fetch("/status_motorista", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `usuario=${usuario}&status=${status}`,
    })
        .then((response) => {
            if (response.ok) {
                alert("Status atualizado com sucesso!");
            } else {
                alert("Erro ao atualizar o status!");
            }
        })
        .catch((error) => {
            console.error("Erro ao atualizar o status:", error);
        });
}

function listarMotoristas(motoristas) {
    let tabelaMotoristas = document.getElementById("tabela_motoristas");
    tabelaMotoristas.innerHTML = "";

    motoristas.forEach(motorista => {
        let statusColor;
        switch (motorista.status) {
            case "em_servico":
                statusColor = "green";
                break;
            case "fora_servico":
                statusColor = "red";
                break;
            case "em_demanda":
                statusColor = "yellow";
                break;
            case "almoco":
                statusColor = "orange";
                break;
            default:
                statusColor = "gray";
        }

        tabelaMotoristas.innerHTML += `
            <tr>
                <td>${motorista.nome} ${motorista.sobrenome}</td>
                <td>${motorista.modelo_veiculo} - ${motorista.placa}</td>
                <td><span class="status-light" style="background-color: ${statusColor};"></span>${motorista.status}</td>
            </tr>
        `;
    });
}
