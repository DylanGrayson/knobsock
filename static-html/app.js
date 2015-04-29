
var currentGroup = 0;

var group_source = $("#group_template").html();
var group_template = Handlebars.compile(group_source);
var group_context = {};

var member_source = $("#member_template").html();
var member_template = Handlebars.compile(member_source);
var member_context = {};


$.getJSON("/api/groups/s.json", function(data) {
		group_context['groups'] = data.groups;
		var group_html = group_template(group_context);
		$('#group_list').append(group_html);

		member_context['members'] = data.groups[currentGroup].members;
		member_context['curGroup'] = data.groups[currentGroup].name;
		var member_html = member_template(member_context)
		$('#member_list').append(member_html);
	})


change_group = function(index) {
	currentGroup = index;
	member_context['curGroup'] = group_context['groups'][currentGroup].name;
	member_context['members'] = group_context['groups'][currentGroup].members;
	var member_html = member_template(member_context)
	document.getElementById('member_list').innerHTML = member_html;
}
