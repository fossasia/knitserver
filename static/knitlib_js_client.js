/**
 * Created by tian on 8/14/15.
 */
var ws = new WebSocket("ws://" + location.host + "/v1/knitting_socket");
ws.onmessage = function(evt){
        var received_msg = evt.data;
        console.log(received_msg);
};

ws.onopen = function(){
    ws.send("hello");
};

knitpat_dict_demo_string = JSON.stringify({
  "colors": 2,
  "file_url": "embedded",
  // TODO: add generated image data
  "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP4z8CwCgAEqwGqN0e5wwAAAABJRU5ErkJggg=="
});

var create_knitjob = function (plugin_id, port, success_function) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/create_job/",
    data: {
      "plugin_id": plugin_id,
      "port": port
    },
    success: success_function
  });
};

var init_knitjob = function (job_id, success_function) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/init_job/" + job_id,
    data: {
      /* No data should be needed for job init. */
    },
    success: success_function
  });
};

var config_knitjob = function (job_id, success_function, knitpat_dict_string) {
  
  //var fd = new FormData();
  // fd.append("knitpat_dict", JSON.stringify({"colors": 2, "file_url":"embedded" }));
  // fd.append("file", new Blob());
  
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/configure_job/" + job_id,
    data: {"knitpat_dict": knitpat_dict_string},
    success: success_function
  });
};

var knit_knitjob = function (job_id, success_function) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/knit_job/" + job_id,
    data: {
      /* No data should be needed */
    },
    success: success_function
  });
};


var get_status = function (job_id, success_function) {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "//"+location.host + "/v1/get_job_status/" + job_id,
    data: {
      /* No data should be needed for job init. */
    },
    success: success_function
  });
};

// create_knitjob();
// init_knitjob(knitjob_id)
// config_knitjob(knitjob_id)
// knit_knitjob(knitjob_id)