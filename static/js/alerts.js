// $(document).ready(function() {

//   //$("#alert").hide()

  


// });
function showMessage(msg,msg_type){

  $("#alert").text(msg)
  $("#alert").show()
  setTimeout(function(){
    $("#alert").fadeOut(500)
  },
    2000
  );
  
}