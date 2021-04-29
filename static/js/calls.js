// $(document).ready(function() {

    function  updatePowerStatus(check,project){
        console.log($(check).prop("checked"))
        console.log(project)
        var dat = {
            project:project,
            switch_status:$(check).prop("checked")
            }
        // setTimeout(function(){
        //     $(check).prop("checked",)
        //     console.log("Happend")
        // },2000)
        //console.log($(e>'input[type=checkbox]:checked').length)
        $.ajax({
            type: 'POST',
            data:dat,
            url: "/updatepowerstatus",
            dataType: 'json',
            success: function (data) {
                console.log(data)
            }
        });
        

    }
    
    // function syncperformance(project){
    //         var dat = {
    //         project:project,
            
    //         }
        // setTimeout(function(){
        //     $(check).prop("checked",)
        //     console.log("Happend")
        // },2000)
        //console.log($(e>'input[type=checkbox]:checked').length)
    //     $.ajax({
    //         type: 'GET',
    //         data:dat,
    //         url: "http://localhost:8080/ecommerce/api/performance",
    //         headers:{
    //             "user":'setup',
    //             "password":'setup'
    //         },
    //         contentType: 'application/json; charset=utf-8',
    //         success: function (data) {
    //             console.log(data)
    //         }
    //     });
        

    // }  
// });

