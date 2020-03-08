var m = require("mithril")
var Data = require("../models/Data")

module.exports = {
//    oninit: function(vnode) {User.load(vnode.attrs.id)},
    view: function(vnode) {
        return m("form", {
                onsubmit: function(e) {
                    e.preventDefault()
                    Data.add(vnode.attrs.client_key)
                }
            }, [
//            m("label.label", "Patient pkey"),
//            m("input.input[type=text][placeholder=Patient pkey]", {
//                oninput: m.withAttr("value", function(value) {EHR.current.patient_pkey = value}),
//                value: EHR.current.patient_pkey
//            }),
            m("label.label", "ID"),
            m("input.input[placeholder=ID]", {
                oninput: m.withAttr("value", function(value) {Data.current.id = value}),
                value: Data.current.id
            }),
            m("label.label", "Field 1"),
            m("input.input[placeholder=Field 1]", {
                oninput: m.withAttr("value", function(value) {Data.current.field1 = value}),
                value: Data.current.field1
            }),
            m("label.label", "Field 2"),
            m("input.input[placeholder=Field 2]", {
                oninput: m.withAttr("value", function(value) {Data.current.field2 = value}),
                value: Data.current.field2
            }),
            m("label.label", "Field 3"),
            m("input.input[placeholder=Field 3]", {
                oninput: m.withAttr("value", function(value) {Data.current.field3 = value}),
                value: Data.current.field3
            }),
            m("button.button[type=submit]", "Add"),
            m("label.error", Data.error)
        ])
    }
}