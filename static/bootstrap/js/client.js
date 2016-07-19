/*

// инициализируем socket.io
var io = io();

// обработчики эмитов сервера
io.on('disconnect', function () {
 //alert('Disconnect') // отключение
});
io.on('reconnect', function () {
 //alert('Reconnect') // переподключение
});
io.on('req_data', function (data) { // возврат после эмита send_data
  //alert(data);
  console.log(JSON.stringify(data));
});

// обработчик кнопки id="id_send"
document.getElementById('id_send').onclick=function(){
// получить все выбранные значения id_scheme
var items = document.getElementById('id_scheme');
for(i=0; i < items.options.length; i++) if (items.options[i].selected){
 // эмит клиента send_data
 io.emit('send_data', [
                      items.options[i].value,                         // схема
                      document.getElementById('id_login').value,      // логин
                      document.getElementById('id_old_pass').value,   // старый пароль
                      document.getElementById('id_new_pass_1').value, // новый пароль
                      document.getElementById('id_new_pass_2').value  // новый пароль 2
                      ]);
}                   
//io.emit('send_data', {'login'  :document.getElementById('id_login').value});
}
*/
// Attach a submit handler to the form
$( "#searchForm" ).submit(function( event ) {
 
  // Stop form from submitting normally
  event.preventDefault();
 
  // Get some values from elements on the page:
  var $form = $( this ),
    usr  = $form.find( "input[name='username']" ).val(),
    pass = $form.find( "input[name='password']" ).val(),
    url  = $form.attr( "action" );
 
  // Send the data using post
  var data = { password: pass, username: usr }
  //var posting = $.post( url, { password: pass, username: usr } );
  var posting = $.post( url, JSON.stringify(data) );
 
  // Put the results in a div
  posting.done(function( data ) {
    var content = $( data ).find( "#content" );
    $( "#result" ).empty().append( content );
  });
});

//////////
    function submitform(){
        //alert("Sending Json");
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == XMLHttpRequest.DONE) {
                alert(xhr.responseText);
            }
        }
        //xhr.open(form.method, form.action, true);
        xhr.open("POST", '/post', true);
        xhr.responseType = 'blob';
        
        xhr.onload = function(e) {
          if (this.status == 200) {
              var blob = this.response;
              //document.getElementById("myImage").src = window.URL.createObjectURL(blob);
              }
        };

        xhr.onerror = function(e) {
          alert("Error " + e.target.status + " occurred while receiving the document.");
        };
        
        xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
        var j = {
                "template": "myfile.odt",
                "outformat": "new_myfile.odt"
              }  ;
        xhr.send(JSON.stringify(j));
        }
        
/////////////////
var myJSON = {
        "template": "myfile.odt",
        "outformat": "new_myfile.odt"
      };
function requestFile(myJSON) {

    var urlrequest = "mywebappexport/excel";
    var link = $('#exportbtn');
    $.ajax({
        url: '/post',
        type: "POST",
        data: JSON.stringify(myJSON),
        cache: true,
        contentType: "application/json; charset=utf-8",
        //complete: function (data) {
        /*
        success: function (data) {
                    var ifr = ($('<iframe src='+data+'></iframe>').appendTo('body'));
                    setTimeout(function () {ifr.remove();}, 5000);
                } */
        success: function (data) {
                  //var content = $( data ).find( "#content" );
                  //$( "#ifr" ).empty().append( data ); 
                  //$("#result").html(data);
                  $("#result").contents().html(data);
                }
    })

};