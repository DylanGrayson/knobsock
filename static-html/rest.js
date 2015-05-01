
var currentGroup = 0;

var current_groups = [];

var group_source = $('#group-template').html();
var group_template = Handlebars.compile(group_source);
var group_context = {};

var member_source = $('#member_template').html();
var member_template = Handlebars.compile(member_source);
var member_context = {};

var active_sock_source = $('#sock-template').html();
var active_sock_template = Handlebars.compile(active_sock_source);
var active_sock_context = {};

var inactive_sock_source = $('#inactive-sock-template').html();
//var inactive_sock_template = Handlebars.compile(inactive_sock_source);
var inactive_sock_context = {};

var no_knobs_source = $('#no-knobs-template').html();


fetchGroups = function() {
    $.getJSON('/api/groups/s.json', function(data) {
        current_groups = data.groups;
        group_context['groups'] = data.groups;
        var group_html = group_template(group_context);

        $('#group-list').html(group_html);
        if (current_groups.length > 0) {
            member_context['members'] = data.groups[currentGroup].members;
            member_context['curGroup'] = data.groups[currentGroup];

            var member_html = member_template(member_context);
            $('#member_list').html(member_html);
        }
        else {
            console.log("No members");
            member_context['curGroup'] = null;
            var member_html = member_template(member_context);
            $('#member_list').html(member_html);
        }

        console.info('Fetched Groups!');
    });
};

fetchUser = function() {
    $.getJSON('/api/user/me.json', function(data) {
        user_context = data;
        var html = user_template(user_context);
        $('#user-greeting').append(html);
    })
}

set_sock = function(group_key) {
    $.getJSON('/api/user/me.json', function(data) {
        data['group_key'] = group_key
        jQuery.post('/api/setsock', data, function() {
            fetchGroups();
        })
    })
};

updateKnob = function(group_key, diff_minutes, message) {
    date = new Date();
    new_date = new Date(date.getTime() + diff_minutes * 60000);
    console.log(new_date.getTime());
    data = {
        'group': group_key,
        'delta_minutes': diff_minutes,
        'message': message
    }
    console.info(new_date.toString());
    $.post('/api/knobs/update', data); 
};

createGroup = function(){
    name = $("#thegroup").val();
    data = {
        'group_name': name
    }
    $.post('/api/groups/create', data, function(){
        $('#group-modal').modal('hide');
        $("#thegroup").val('');
        fetchGroups();
    }); 
};