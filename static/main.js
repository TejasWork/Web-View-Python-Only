function Request(url, json, success_function = function(data){}, error_function = function(){}){
    $.ajax({
      type: "POST",
      url: url,
      data: JSON.stringify(json),
      success: success_function,
      error: error_function
    });
  }

function console_log(string){
    Request('/console-log', {'string': 'js: '+string})
}