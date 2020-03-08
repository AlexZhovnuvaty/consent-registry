var m = require("mithril")
var Consumer = require("../models/Consumer")

module.exports = {
    view: function() {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Consumer.register()
                }
            }, [
            m("label.label", "Name"),
            m("input.input[type=text][placeholder=Consumer name]", {
                oninput: m.withAttr("value", function(value) {Consumer.current.name = value}),
                value: Consumer.current.name
            }),
            m("button.button[type=submit]", "Register"),
            m("label.error", Consumer.error)
        ])
    }
}