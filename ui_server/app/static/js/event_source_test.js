$(document).ready(function() {
    const source1 = new EventSource("http://127.0.0.1:5001/sse1");

    source1.addEventListener("new_message", function(event) {

        console.log(event);

    });

    const source2 = new EventSource("http://127.0.0.1:5001/sse2");

    source2.addEventListener("new_message", function(event) {

        console.log(event);

    });

});