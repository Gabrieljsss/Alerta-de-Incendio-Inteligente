
$(document).ready(function(){
    var myChart = null
    $.ajax({
        type : 'POST',
        url : "/getLeituras",
        contentType: 'application/json',
        success: function(response) {
            console.log(response.length)
            if(response.length == 0){
                response = [[0,0,0]];
            }
            var ids = [];
            var temps = [];
            var gas = [];

            for (var i = 0; i < response.length; i++) {
                console.log("loop index" + i);
                ids.push(response[i][0]);
                temps.push(response[i][1]);
                gas.push(response[i][2]);
                if (parseInt(response[i][2]) > 100 || parseInt(response[i][1]) > 55){
                    console.log("ALERT");
                    $("html").css("background-color", "rgba(218, 58, 18, 0.479)");
                }
            }
            ids = ids.reverse();
            temps = temps.reverse();
            gas = gas.reverse();
            console.log(response);

            var ctx = document.getElementById("myChart");
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ids,
                    datasets: [{
                        label: 'Temperatura',
                        data: temps,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.0)',
                            'rgba(54, 162, 235, 0.0)',
                            'rgba(255, 206, 86, 0.0)',
                            'rgba(75, 192, 192, 0.0)',
                            'rgba(153, 102, 255, 0.0)',
                            'rgba(255, 159, 64, 0.0)'
                        ],
                        borderColor: [
                            'rgba(255,99,132,1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    },
                    {
                        label: 'gas',
                        data: gas,
                        backgroundColor: [
                            'rgba(132, 132, 132, 0.0)',
                        ],
                        borderColor: [
                            'rgba(132,132,132,1)',
                        ],
                        borderWidth: 1
                    }]
                },
                 options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    },
                    responsive: false,
                    title: {
                      display: true,
                      text: 'Leituras de gás e temperatura em função do tempo'
                    }
                }

            });
            (function updater() {
                console.log("request");
                $.ajax({
                    type : 'POST',
                    url : "/getUltimaLeitura",
                    contentType: 'application/json',
                    success: function(resposta) {
                        if(resposta == null){
                            resposta = [0,0,0];
                        }
                        id = resposta[0];
                        temp = resposta[1];
                        gas = resposta[2];
                        console.log(gas, temp);
                        if (parseInt(gas) > 100 || parseInt(temp) > 55){
                            console.log("ALERT");
                            $("html").css("background-color", "rgba(218, 58, 18, 0.479)");
                            $("body").css("background-color", "rgba(218, 58, 18, 0.479)");
                        }
                        myChart.data.labels.push(id);
                        myChart.data.datasets[0].data.push(temp);
                        myChart.data.datasets[1].data.push(gas);
                        myChart.update();
                        setTimeout(updater, 3000);  
                    },
                    error: function () {
                        console.log("error");
                    }
                });
            })();
        },
        error: function () {
            console.log("error");
        }
    });
    console.log("teste");

    
    $("#control").click(function(){
        console.log(myChart.data);
        myChart.data.labels.push(11);
        myChart.data.datasets[0].data.push(100);
        myChart.data.datasets[1].data.push(90);
        myChart.update();

    })








});