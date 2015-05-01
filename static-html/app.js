invite_init = function(key) {
	document.getElementById('group_key').value = key
}

changeGroup = function(index) {
    currentGroup = index;
    member_context['curGroup'] = group_context['groups'][currentGroup];
    member_context['members'] = group_context['groups'][currentGroup].members;
    var member_html = member_template(member_context);
    $('#member_list').html(member_html);
};

// fetch knob timers by key
var KnobTimers = {};
updateKnobList = function() {
    console.info("Updating Socks");
    // clear out HTML
    $('#sock-container').html('');
    if (!current_groups.length){
        $('#sock-container').append(no_knobs_source);
    }
    // add active socks 
    for (var i = 0; i < current_groups.length; i++) {
        if (current_groups[i].knob == true) {
            var sock_context = {
                'group_name': current_groups[i].name,
                'group_key': current_groups[i].key
            };
            var sock_html = active_sock_template(sock_context);
            $('#sock-container').append(sock_html);

            id = current_groups[i].key + '-time'
            console.info(current_groups[i].timeout)
            KnobTimers[current_groups[i].key] = countdown(new Date(Date.parse(current_groups[i].timeout)), function(ts) {
                  document.getElementById(id).innerHTML = "Time Remaining: " + ts.toString();
                },
                countdown.HOURS | countdown.MINUTES | countdown.SECONDS
            );

        }

    }
    // add inactive socks
    for (var i = 0; i < current_groups.length; i++) {
        if (current_groups[i].knob != true) {
            var sock_context = {
                'group_name': current_groups[i].name,
                'group_minutes': 'minutes-' + current_groups[i].key,
                'group_slider': current_groups[i].key,
                'time_remaining': 0,
                'percentage_remaining': (current_groups[i].timein / current_groups[i].timeout) * 100
            }
            var sock_html = inactive_sock_template(sock_context);
            $('#sock-container').append(sock_html);
        }
        $('#' + current_groups[i].key).noUiSlider({
            start: 15,
            connect: 'lower',
            range: {
                'min': 5,
                'max': 120
            },
            format: wNumb({
                decimals: 0
            })
        });
        $('#' + current_groups[i].key).Link('lower').to($('#minutes-' + current_groups[i].key));
    }
};

appInit = function() {
    //$.material.init();
    fetchGroups();
    //updateKnobList();
    setInterval(fetchGroups, 1000);
    setInterval(updateKnobList, 5000);
    //setTimeout(updateKnobList, 3000);
};

$(document).ready(function() {
    $('#groups-list').html("");
    appInit();
});

