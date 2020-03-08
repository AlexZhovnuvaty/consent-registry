var m = require("mithril")
var Academic = require("../models/Academic")

module.exports = {
    oninit:
        function(vnode){
            Academic.loadList(vnode.attrs.client_key)
        },
    view: function() {
        return m(".user-list", Academic.list.map(function(academic) {
            return m("a.user-list-item",
                "PUBLIC KEY: " + academic.public_key +
                "; NAME: " + academic.name)
        }),
        m("label.error", Academic.error))
    }
}