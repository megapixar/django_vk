/**
 * Created by Antatoly on 17.01.2015.
 */
 var cancelButton = document.getElementById('cancel'),
    servers = null;

ajax = function(type, url, params, callback) {
    var xhr,
        host = 'http://192.168.1.15:8000/rtc/';
    xhr = new XMLHttpRequest();
    xhr.open(type, host + url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            return callback(xhr.responseText);
        }
    };
    var form_data = new FormData();
    for (var key in params ) {
        form_data.append(key, params[key]);
    }

    return xhr.send(form_data);
};

// Speed up calls to hasOwnProperty
var hasOwnProperty = Object.prototype.hasOwnProperty;

function isEmpty(obj) {

    // null and undefined are "empty"
    if (obj == null) return true;
    if (obj == '{}') return true;
    // Assume if it has a length property with a non-zero value
    // that that property is correct.
    if (obj.length > 0)    return false;
    if (obj.length === 0)  return true;

    // Otherwise, does it have any properties of its own?
    // Note that this doesn't handle
    // toString and valueOf enumeration bugs in IE < 9
    for (var key in obj) {
        if (hasOwnProperty.call(obj, key)) return false;
    }

    return true;
}

function gotStream(stream) {
    console.log("Received local stream");
    var video = document.querySelector("video");
    video.src = URL.createObjectURL(stream);
    var pc = new webkitRTCPeerConnection(servers, {});
    pc.addStream(stream);
    pc.onaddstream = function (e) {
        console.log('Remote video was added to Offer!');
    };
    var gotCandidates = setInterval(function () {
        ajax('POST', 'candidate/',  {
            candidate: '',
            type: 'offer'
        }, function (data) {
            if (!isEmpty(data)) {
                pc.addIceCandidate(new RTCIceCandidate(JSON.parse(data)), function (pc) {
                    console.log('Offer addIceCandidate from answer');
                }, function (pc, error) {
                    console.log(error);
                });
            }
        });
    }, 500);
    cancelButton.onclick = function (){
        clearInterval(gotCandidates);
    };
    var num = 0;
    pc.onicecandidate = function (event) {
        if (event.candidate) {
            ajax('POST', 'candidate/',  {
                candidate: JSON.stringify(event.candidate),
                type: 'offer',
                num : num++
            }, function () {});
        } else {
            console.log("End of candidates.")
        }
    };

    pc.oniceconnectionstatechange = function (e) {
        console.log('Offer ICE state: ' + pc.iceConnectionState);
    };

    pc.createOffer(function (offer) {
        pc.setLocalDescription(offer, function () {
            // Send offer to remote end.
            console.log("setLocalDescription, sending to remote");
            ajax('POST', 'offer/',  {
                offer: JSON.stringify(offer)
            }, function () {
                console.log("Offer sent!");
                var timeout = setInterval(function(){
                    ajax('GET', 'get_answer/',  {},
                        function (answer) {
                        if (!isEmpty(answer)) {
                            pc.setRemoteDescription(new RTCSessionDescription(JSON.parse(answer)), function () {
                                console.log("Offer set Remote Description!");
                            }, error);
                            clearInterval(timeout);
                        }
                    });
                }, 1000);
            });
        });
    }, error);
    localstream = stream;
    stream.onended = function() { console.log("Ended"); };
}


function getUserMediaError() {
    console.log("getUserMedia() failed.");
}
function onAccessApproved(id) {
    if (!id) {
        console.log("Access rejected.");
        return;
    }
    navigator.webkitGetUserMedia({
        audio:false,
        video: { mandatory: { chromeMediaSource: "desktop",
            chromeMediaSourceId: id } }
    }, gotStream, getUserMediaError);
}

var pending_request_id = null;

document.getElementById('capture').addEventListener('click', function(e) {
    pending_request_id = chrome.desktopCapture.chooseDesktopMedia(
        ["screen", "window"], onAccessApproved);
});

function error(e) {
    if (typeof e == typeof {}) {
        alert("Oh no! " + JSON.stringify(e));
    } else {
        alert("Oh no! " + e);
    }
    endCall();
}