var m = require("mithril")
var Data = require("../models/Data")

module.exports = {
    oninit:
        function(vnode){
            Data.loadList(vnode.attrs.client_key)
        },
    view: function(vnode) {
        return m(".user-list", Data.list.map(function(data) {
            return m("a.user-list-item",
//                "NAME: " + data.name +
                "ID: " + data.id +
//                "; CLIENT PKEY: " + data.client_pkey +
                "; Field 1: " + data.field1 +
                "; Field 2: " + data.field2 +
                "; Field 3: " + data.field3 +
                "; TIMESTAMP: " + data.event_time +
                ";"
//                ,
//                m("div"),
//                m("button", {
//                    onclick: function() {
//                        EHR.current.claim_id = claim.id
//                        EHR.current.client_pkey = claim.client_pkey
////                        Claim.current.provided_service = "pills, lab tests"
//                        EHR.current.contract_id = claim.contract_id
//                        EHR.update(vnode.attrs.client_key)
//                    }
//                }, 'Update claim'),
//                m("div"),
//                m("button", {
//                    onclick: function() {
//                        Claim.current.claim_id = claim.id
//                        Claim.current.client_pkey = claim.client_pkey
////                        Claim.current.provided_service = "pills, lab tests"
//                        Claim.current.contract_id = claim.contract_id
//                        Claim.close(vnode.attrs.client_key)
//                    }
//                }, 'Close claim')
            )
        }),
//        m("label.label", "Provided Service"),
//        m("input.input[placeholder=Provided Service]", {
//            oninput: m.withAttr("value", function(value) {Claim.current.provided_service = value}),
//            value: Claim.current.provided_service
//        }),
        m("label.error", Data.error))
    }
}