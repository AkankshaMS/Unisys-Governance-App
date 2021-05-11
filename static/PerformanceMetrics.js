function syncperformance(projectname) {

    var uName = 'setup';
    var password = 'setup';

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
            
            //$("#cpu-load-needle").animate({transform: "rotate("+cpu_load_deg+"deg)"},1000)
            
            $("#cpu-load-gauge").text(Math.round(stat['systemCpuLoad']))
            
            var memory_usage = Math.round((memory_information['usedMemory']/ memory_information['maxMemory'])*100)
            console.log(memory_usage)
            
            
            var memory_usage_deg = Math.round(180 * memory_usage)
            $(".semi-donut").attr("style","--fill: #28a745 ;margin-left: 12%;padding-bottom: 2px;--percentage:"+memory_usage)
            //$(".semi-donut").css("background-color","red")

            //$(".semi-donut").css("transform", "rotate("+memory_usage_deg+"deg)")

            $("#memory-usage-gauge").text("Memory Use - "+memory_usage)
            
            
            
            // $("#card-body-container:last-child").remove()
            $('#card-body-container').html('\
                <tr>\
            <td class="five wide column">Host</td>\
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
            <td>Java Version</td>\
            <td>'+ stat['javaVersion'] + '</td>\
          </tr>\
          <tr>\
            <td>Process CpuTime </td>\
            <td>'+ stat['processCpuTimeMillis'] + '</td>\
          </tr>\
          <tr>\
            <td>System Load Average</td>\
            <td>'+ stat['systemLoadAverage'] + '</td>\
          </tr>\
          <tr>\
            <td>System Cpu Load</td>\
            <td>'+ stat['systemCpuLoad'] + '</td>\
          </tr>\
          <tr>\
            <td>Start Date</td>\
            <td>'+ stat['startDate'] + '</td>\
          </tr>\
          <tr>\
            <td>Thread Count</td>\
            <td>'+ stat['threadCount'] + '</td>\
          </tr>\
          <tr>\
            <td>Used Buffered Memory</td>\
            <td>'+ memory_information['usedBufferedMemory'] + '</td>\
          </tr>\
          <tr>\
          </tr>\
          '
            );
        }
    });
}
var period_now = 'jour'

function getChangedPeriodUrl(graph,period){
  var str = $(graph).attr("src");
  stripped = str.substring(0, str.indexOf('period='));
  // console.log(stripped)
  stripped = stripped+ 'period='+period
  return stripped
}
function syncGraphs(projectname,period){
  period_now = period
  $(".graphs").children()
  .each(function () {


    $(this).attr("src",getChangedPeriodUrl(this,period))
    $(".graph>img").attr("src",getChangedPeriodUrl($(".graph>img"),period))
});
  //str = 'http://localhost:8080/{{project.project_name}}/monitoring?graph=httpSessions&width=150&height=35&period=jour'

}

function changeGraph(projectname,graph){

  $(".graph>img").attr("src",'http://localhost:8080/'+projectname+'/monitoring?graph='+graph+'&width=750&height=500&period='+period_now)
}