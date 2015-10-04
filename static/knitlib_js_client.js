/**
 * Created by tian on 8/14/15.
 */


var create_socket = function () {
    var ws = new WebSocket("ws://" + location.host + "/v1/knitting_socket");
    ws.onmessage = function (evt) {
        var received_msg = evt.data;
        console.log(received_msg);
    };

    ws.onopen = function () {
        ws.send("hello");
    };
    return ws;
};


knitpat_dict_demo_string = JSON.stringify({
    "colors": 2,
    "file_url": "embedded",
    // TODO: add generated image data
    "image_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP4z8CwCgAEqwGqN0e5wwAAAABJRU5ErkJggg=="
});

/**
 * Creates a Knitting Job on the Knitlib server.
 * @param plugin_id
 * @param port
 * @param success_function
 */
var create_knitjob = function (plugin_id, port, success_function) {
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "//" + location.host + "/v1/create_job/",
        data: {
            "plugin_id": plugin_id,
            "port": port
        },
        success: success_function
    });
};

/**
 * Initializes a knitting job.
 * @param job_id
 * @param success_function
 */
var init_knitjob = function (job_id, success_function) {
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "//" + location.host + "/v1/init_job/" + job_id,
        data: {
            /* No data should be needed for job init. */
        },
        success: success_function
    });
};

/**
 * Configure a knitjob.
 * @param job_id A string with the job's ID.
 * @param success_function A callback function on call success.
 * @param knitpat_dict_string A String version of a Knitpat config file. Must have image_data base64 embedded.
 */
var config_knitjob = function (job_id, knitpat_dict_string, success_function) {
    //var fd = new FormData();
    // fd.append("knitpat_dict", JSON.stringify({"colors": 2, "file_url":"embedded" }));
    // fd.append("file", new Blob());

    $.ajax({
        type: "POST",
        dataType: "json",
        url: "//" + location.host + "/v1/configure_job/" + job_id,
        data: {"knitpat_dict": knitpat_dict_string},
        success: success_function
    });
};

/**
 * Calls the knit method on the specified knit_job.
 * @param job_id
 * @param success_function
 */
var knit_knitjob = function (job_id, success_function) {
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "//" + location.host + "/v1/knit_job/" + job_id,
        data: {
            /* No data should be needed */
        },
        success: success_function
    });
};


/**
 * Returns the status of the job machine id.
 * @param job_id
 * @param success_function
 */
var get_status = function (job_id, success_function) {
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "//" + location.host + "/v1/get_job_status/" + job_id,
        data: {
            /* No data should be needed for job init. */
        },
        success: success_function
    });
};

// create_knitjob();
// create_knitjob("dummy", "/dev/null", console.log)
// init_knitjob(knitjob_id)
// config_knitjob(knitjob_id)
// config_knitjob("5485de4d-c319-4e13-9072-1cc0109ed74e", '{"colors": 2, "file_url": "embedded", "image_data": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAKAAAAAUCAYAAAAKlDZOAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH3QwJFSIRDWMAkwAAAVhJREFUaN7tWtEOwyAIFLP//2X2sJmYlikU1NrdJYYuVbhcEW0npZQ4AcAiZOZP/sHCrrDfa2ZY2BWWuE5FAJi9BEMCHYio+RsISsAi7NFGP8go/6P5tmLNiHF3fbz+TwnIzImITtZaIX71kfx7MJLv7HG76RPBN7dIazJbuzRJ/npktbNqBN9yr7Qj1xKzNO/SvZs+UXxVLyH1AKm7934rZi2edWwEn2NfqYpYfeyuTyRfcwLWQaWH0+pjIXws857lzsJXm4RR43bTJ5ovMTNb9jXeGaP135rho/murIA76BPJ1/QZ5heZ+uu2RO7KRlrac3l9aPn2KthpFnd8PE2fSL4v72t4hBA93yN8avi2kky79D1Znwi+eRTxu+Mq39njdtPHiixlZ90iyUTGmMF3RsXZWZ+IGPgr7gZL0z8DhxGApcj1BhsWdoXFuTTYdecBE47kAwvxBqnHFSBM3N80AAAAAElFTkSuQmCC" }')
// knit_knitjob(knitjob_id)