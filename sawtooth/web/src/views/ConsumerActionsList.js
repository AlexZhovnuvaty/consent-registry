var m = require("mithril")
var Client = require("../models/Client")

module.exports = {

    oninit: //Client.loadList
        function(vnode){
            Client.loadList()
        }
    ,
    view: function(vnode) {
        return m(".user-list", [
            m("label.label", "Client public key"),
            m("input.input[type=text][placeholder=Client public key][disabled=false]", {
                value: Client.list['consumer'] //vnode.attrs.client_pkey
            }),
            m("a.user-list-item", {href: "/consumer/new/", oncreate: m.route.link}, "New Consumer"),
            m("a.user-list-item", {href: "/consumer_list/?client_key=" + Client.list['consumer'], oncreate: m.route.link}, "Consumer List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/academic_list/?client_key=" + Client.list['consumer'], oncreate: m.route.link}, "Academic List"),
            m("a.user-list-item", "---"),
            m("a.user-list-item", {href: "/data/new/?client_key=" + Client.list['consumer'], oncreate: m.route.link}, "Add Data"),
            m("a.user-list-item", {href: "/data_list/?client_key=" + Client.list['consumer'], oncreate: m.route.link}, "Data List"),
        ])

    }
}