$(document).ready(function() {
    var wl = window.location;
    var site_base_url = wl.protocol + '//' + wl.host;
    var refresh_interval = 1500;

    // button handler for help queue
    $("#help-queue-table").on('click', '.btn-floating', function () {
        var kerb = $(this).parent().parent().data("kerberos");

        $.ajax({
            type: "POST",
            url: site_base_url + "/queue",
            data: '&kerberos=' + kerb + '&remove=true'
        }).then(function(data) {
            console.log(data);
        });

        $(this).parent().parent().remove();
    });

    // refresh the lab queue every `refresh_interval` milliseconds
    setInterval( function() {
        $.ajax({
            type: "GET",
            url: site_base_url + "/queue"
        }).then( function(data) {
            $('#help-queue-table').empty();
            if (data.message.length > 0) {
                console.log(data.message);
            }
            $.each(data.help_queue, function(i, item) {
                pulse = i == 0 ? 'pulse' : '';

                $('#help-queue-table').append(
                    $('<tr>').append(
                        $('<td>').text(item.elapsed),
                        $('<td>').text(item.name),
                        $('<td>').text(item.kerberos),
                        $('<td>').text(item.type),
                        $('<td>').append(
                            $('<a>').addClass("btn-floating btn-small waves-effect waves-light red "+pulse).append(
                                $('<i>').addClass("material-icons").text('remove')
                            )
                        )
                    ).data('kerberos', item.kerberos)
                );
            });
        });
    }, refresh_interval);

});