var m = require("mithril")

var AcademicList = require("./views/AcademicList")
var AcademicForm = require("./views/AcademicForm")
var ConsumerList = require("./views/ConsumerList")
var ConsumerForm = require("./views/ConsumerForm")
//var InvestigatorList = require("./views/InvestigatorList")
//var InvestigatorForm = require("./views/InvestigatorForm")
//var TrialDataList = require("./views/TrialDataList")
var DataList = require("./views/DataList")
var DataForm = require("./views/DataForm")
//var PreScreeningCheckForm = require("./views/PreScreeningCheck")
var ConsumerConsentRequestList = require("./views/ConsumerConsentRequestList")
var AcademicConsentRequestList = require("./views/AcademicConsentRequestList")
var ConsumerActionsList = require("./views/ConsumerActionsList")
var AcademicActionsList = require("./views/AcademicActionsList")
//var InvestigatorActionsList = require("./views/InvestigatorActionsList")
var Layout = require("./views/Layout")
//var Login = require("./views/Login")

m.route(document.body, "/consumer", {

    "/academic_list": {
        render: function(vnode) {
            return m(Layout, m(AcademicList, vnode.attrs))
        }
    },
    "/academic/new/": {
        render: function() {
            return m(Layout, m(AcademicForm))
        }
    },
    "/consumer_list/": {
        render: function(vnode) {
            return m(Layout, m(ConsumerList, vnode.attrs))
        }
    },
    "/consumer/new/": {
        render: function() {
            return m(Layout, m(ConsumerForm))
        }
    },
    "/data_list": {
        render: function(vnode) {
            return m(Layout, m(DataList, vnode.attrs))
        }
    },
    "/consumer/consent_request_list": {
        render: function(vnode) {
            return m(Layout, m(ConsumerConsentRequestList, vnode.attrs))
        }
    },
    "/academic/consent_request_list": {
        render: function(vnode) {
            return m(Layout, m(AcademicConsentRequestList, vnode.attrs))
        }
    },
    "/data/new/": {
        render: function(vnode) {
            return m(Layout, m(DataForm, vnode.attrs))
        }
    },
    "/consumer": {
//        onmatch: function(args, requestedPath, route) {
//            if (!localStorage.getItem("auth-token")) m.route.set("/login")
//            else return m(Layout, m(HospitalActionsList))
//        },
        render: function() {
            return m(Layout, m(ConsumerActionsList))
        }
    },
    "/academic": {
        render: function() {
            return m(Layout, m(AcademicActionsList))
        }
    },
//    "/login": {
//        render: function() {
//            return m(Login)
//        }
//    },
})