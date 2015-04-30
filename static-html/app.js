
var currentGroup = 0;

var group_source = $("#group_template").html();
var group_template = Handlebars.compile(group_source);
var group_context = {};

var member_source = $("#member_template").html();
var member_template = Handlebars.compile(member_source);
var member_context = {};

var active_sock_source = $('#active-sock-template').html();
var active_sock_template = Handlebars.compile(active_sock_source);
var active_sock_context = {};

fetchGroups = function() {
    $.getJSON("/api/groups/s.json", function(data) {
        group_context['groups'] = data.groups;
        member_context['members'] = data.groups[currentGroup].members;
        member_context['curGroup'] = data.groups[currentGroup].name;
    });
    var group_html = group_template(group_context);
    $('#group_list').html(group_html);

    var member_html = member_template(member_context);
    $('#member_list').html(member_html);
    console.info("Fetched Groups!");
}

change_group = function(index) {
    currentGroup = index;
    member_context['curGroup'] = group_context['groups'][currentGroup].name;
    member_context['members'] = group_context['groups'][currentGroup].members;
    var member_html = member_template(member_context)
    document.getElementById('member_list').innerHTML = member_html;
}

main_loop = function(){
    //$.material.init();
    $("#minutes-slider").noUiSlider({
        start: 15,
        connect: "lower",
        range: {
            'min': 5,
            'max': 120
        },
        format: wNumb({
            decimals: 0
        })
    });
    $("#minutes-slider").Link('lower').to($('#minutes-value'));


    fetchGroups();
    setInterval(fetchGroups, 5000);
};

main_loop();
