odoo.define("itsm.tree_date", function(require) {
	"use strict";

	var AbstractField = require("web.AbstractField");
	var field_registry = require("web.field_registry");

	var tree_date = AbstractField.extend({
		init: function() {
			this._super.apply(this, arguments);
		},
		_render: function() {
			var text =this.value
			var time = new Date(text*1000);
			var commonTime = time.toLocaleString();
			this.$el.html(commonTime);
		}
	});

	field_registry.add("tree_date", tree_date);
	return tree_date;
});
