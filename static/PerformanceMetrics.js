function syncperformance(projectname) {
    // var dat = {
    // project:project,

    // };
    var uName = 'setup';
    var password = 'setup';
    // setTimeout(function(){
    //     $(check).prop("checked",)
    //     console.log("Happend")
    // },2000)
    //console.log($(e>'input[type=checkbox]:checked').length)

    $.ajax({

        type: 'GET',
        // data:dat,
        url: "http://localhost:8080/" + projectname + "/monitoring?period=jour&format=json",
        //             headers: {
        //     "Authorization": "Basic " + btoa(uName + ":" + password)
        //   },
        contentType: 'application/json',
        success: function (data) {
            console.log(data)
            //console.log(data['list'][13])
            //console.log(data[0])

            var stat = data['list'][13]
            var memory_information = stat['memoryInformations']
            console.log(stat)

            var cpu_load_deg = Math.round(180 * (parseInt(stat['systemCpuLoad']))/100)
            $("#cpu-load-needle").css("transform", "rotate("+cpu_load_deg+"deg)")
            $("#cpu-load-gauge").text(Math.round(stat['systemCpuLoad']))
            
            var memory_usage = Math.round((memory_information['usedMemory']/ memory_information['maxMemory'])*100)
            console.log(memory_usage)
            
            
            var memory_usage_deg = Math.round(180 * memory_usage)
            $(".semi-donut").attr("style","--fill: #28a745 ;margin-left: 12%;padding-bottom: 2px;--percentage:"+memory_usage)
            //$(".semi-donut").css("background-color","red")

            //$(".semi-donut").css("transform", "rotate("+memory_usage_deg+"deg)")

            $("#memory-usage-gauge").text("Memory Use - "+memory_usage)
            
            
            
            // $("#card-body-container:last-child").remove()
            $('#card-body-container').append('\
                <tr>\
            <td class="two wide column">Host</td>\
            <td>'+ stat['host'] + '</td>\
          </tr>\
          <tr>\
            <td>Operating System</td>\
            <td>'+ stat['os'] + '</td>\
          </tr>\
          <tr>\
            <td>Available Processors</td>\
            <td>'+ stat['availableProcessors'] + '</td>\
          </tr>\
            <tr>\
            <td>javaVersion</td>\
            <td>'+ stat['javaVersion'] + '</td>\
          </tr>\
          <tr>\
            <td>processCpuTimeMillis</td>\
            <td>'+ stat['processCpuTimeMillis'] + '</td>\
          </tr>\
          <tr>\
            <td>systemLoadAverage</td>\
            <td>'+ stat['systemLoadAverage'] + '</td>\
          </tr>\
          <tr>\
            <td>systemCpuLoad</td>\
            <td>'+ stat['systemCpuLoad'] + '</td>\
          </tr>\
          <tr>\
            <td>startDate</td>\
            <td>'+ stat['startDate'] + '</td>\
          </tr>\
          <tr>\
            <td>threadCount</td>\
            <td>'+ stat['threadCount'] + '</td>\
          </tr>\
          '
            );
        }
    });


}
