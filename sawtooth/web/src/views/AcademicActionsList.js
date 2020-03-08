var m = require("mithril")
var Client = require("../models/Client")

module.exports = {

    oninit:
        function(vnode){
            Client.loadList()
        }
    ,
    view: function(vnode) {
        return m(".user-list", [
            m("label.label", "Client public key"),
            m("input.input[type=text][placeholder=Client public key][disabled=false]", {
                value: Client.list['academic']
            }),
            m("a.user-list-item", {href: "/academic/new/", oncreate: m.route.link}, "New Academic"),
            m("a.user-list-item", {href: "/academic_list/?client_key=" + Client.list['academic'], oncreate: m.route.link}, "Academic List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/academic/consumer_list/?client_key=" + Client.list['academic'], oncreate: m.route.link}, "Consumer List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/data_list/?client_key=" + Client.list['academic'], oncreate: m.route.link}, "Data List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/academic/consent_request_list/?client_key=" + Client.list['academic'], oncreate: m.route.link}, "Consent Requests"),
        ])

    }
}