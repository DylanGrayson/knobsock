
var currentGroup = 0;

var source = $("#template").html();
var template = Handlebars.compile(source);
var context = {};
$.getJSON("/api/groups/s.json", function(data) {
		context['groups'] = data.groups;
		var html = template(context);
		$('body').append(html);
	})

change_group = function(index) {
	currentGroup = index;
}
