$(document).ready(function() {

    var socket = io.connect('http://127.0.0.1:5000');

    var sock = io()

    sock.on('audit', function(data) {
        console.log(data)
        $("#audit_body").append(`
        <tr><td>`+data['userName']+`</td>
        <td>`+data['auditDocumentName']+`</td>
        <td>`+data['auditModuleName']+`</td>
        <td>`+data['operation']+`</td>
        <td>`+data['timestamp']+`</td>
    </tr> `);

    });
  
});
