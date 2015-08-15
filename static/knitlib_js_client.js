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

var create_knitjob = function () {
  knitjob_id = ""
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/create_job/",
    data: {
      "plugin_id": "dummy",
      "port": "/dev/null"
    },
    success: function(data){
      console.log("Created knitting job:")
      console.log(data);
      knitjob_id = data["job_id"];
    }
  });
  return knitjob_id;
};

var init_knitjob = function (job_id) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/init_job/" + job_id,
    data: {
      /* No data should be needed for job init. */
    },
    success: function(data){
      console.log("Inited knitting job:")
      console.log(data);
    }
  });
};

var config_knitjob = function (job_id) {
  
  //var fd = new FormData();
  // fd.append("knitpat_dict", JSON.stringify({"colors": 2, "file_url":"embedded" }));
  // fd.append("file", new Blob());
  
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/configure_job/" + job_id,
    data: { "knitpat_dict":
    JSON.stringify({
      "colors": 2, 
      "file_url":"embedded", 
      // TODO: add generated image data
      "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP4z8CwCgAEqwGqN0e5wwAAAABJRU5ErkJggg=="
     })},
    success: function(data){
      console.log("Configured knitting job:")
      console.log(data);
    }
  });
};

var knit_knitjob = function (job_id) {
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "//"+location.host + "/v1/knit_job/" + job_id,
    data: {
      /* No data should be needed */
    },
    success: function(data){
      console.log("Knitting knitting job:")
      console.log(data);
    }
  });
};


var get_status = function (job_id) {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "//"+location.host + "/v1/get_job_status/" + job_id,
    data: {
      /* No data should be needed for job init. */
    },
    success: function(data){
      console.log("Status of Job job:")
      console.log(data);
    }
  });
};

// create_knitjob();
// init_knitjob(knitjob_id)
// config_knitjob(knitjob_id)
// knit_knitjob(knitjob_id)