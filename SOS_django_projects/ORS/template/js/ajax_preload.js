<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

<script>

$(document).on("change", ".cascade", function () {

    let element = $(this);

    let url = element.data("url");
    let map = element.data("map");

    if (!url || !map) return;

    let config = JSON.parse(map);

    let requestData = {};
    requestData[config.param] = element.val();

    $.ajax({
        url: url,
        type: "GET",
        data: requestData,
        success: function (res) {

            // target dropdown update
            let targetSelector = "[name='" + config.target + "']";

            if (res[config.target + "_select"]) {
                $(targetSelector).html(res[config.target + "_select"]);
            }
        }
    });
});

</script>