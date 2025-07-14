function clasificarSurvived(){
    let sexo = document.getElementById("sexo").value;
    let edad = parseFloat(document.getElementById("edad").value);
    let tarifa = parseFloat(document.getElementById("tarifa").value);
    let ticket = document.getElementById("ticket").value;
    let res = document.getElementById("resultado");
    let str = `{sexo: ${sexo}, edad: ${edad}, tarifa: ${tarifa}, ticket: ${ticket}}`;
    console.log(str);

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sex: `${sexo}`,
            age: `${edad}`,
            fare: `${tarifa}`,
            ticket: `${ticket}`
        }),
    })
    .then(response => response.json())
    .then(data =>{
        if(data.error){
            res.innerHTML = `Error: ${data.error}`;
        }else{
            sob = (data.Survived === 1) ? "Sobrevivió": "No Sobrevivió";
            res.innerHTML = `La predicción de Survived es: ${data.Survived}, ${sob}`
        }
    })
    .catch(error =>{
        res.innerHTML = `Error en la solicitud`;
        console.log("Error", error);
    });

    console.log("Ha finalizado la petición");
}

function principal(){
    const btnEnviar = document.getElementById("enviar");
    btnEnviar.addEventListener("click", clasificarSurvived);
}

document.addEventListener("DOMContentLoaded", principal);