var m = require("mithril")
var Academic = require("../models/Academic")

module.exports = {
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Academic.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Name]", {
                oninput: m.withAttr("value", function(value) {Academic.current.name = value}),
                value: Academic.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Academic.error)
        ])
    }
}