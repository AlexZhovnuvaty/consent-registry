var m = require("mithril")

var Academic = {
    list: [],
    consentRequestList: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/academic",
            headers: {
                'ClientKey': clientKey
            }
//            withCredentials: true,
        })
        .then(function(result) {
            Academic.error = ""
            Academic.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Academic.error = e.message
            Academic.list = []
        })
    },

    consent_request_list: function(clientKey) {   //i.e Investigator
        return m.request({
            method: "GET",
            url: "/api/academic/consent_request_list",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            console.log("Get Consent Request List")
            Academic.error = ""
            Academic.consentRequestList = result.data
        })
        .catch(function(e) {
            console.log(e)
            Academic.error = e.message
            Academic.informConsentRequestList = []
        })
    },

    get_data: function(hospitalPKey, investigatorPKey) {   //i.e Investigator
        return m.request({
            method: "GET",
            url: "/api/hospitals/get_shared_data/" + hospitalPKey,
            headers: {
                'ClientKey': investigatorPKey
            }
        })
        .then(function(result) {
            console.log("Get shared data")
            Hospital.error = ""
            Hospital.sharedDataList = result.data
        })
        .catch(function(e) {
            console.log(e)
            Hospital.error = e.message
            Hospital.sharedDataList = []
        })
    },
//    decline_inform_consent: function(investigatorPKey, clientKey) {
//        return m.request({
//            method: "GET",
//            url: "/api/patients/decline_inform_consent/" + investigatorPKey,
//            headers: {
//                'ClientKey': clientKey
//            }
////            data: Doctor.current,
////            useBody: true,
////            withCredentials: true,
//        })
//        .then(function(items) {
////            Data.todos.list = items
//            Patient.error = ""
//        })
//        .catch(function(e) {
//            console.log(e)
//            Patient.error = e.message
//        })
//    },

    current: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/academic",
            data: Academic.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Academic.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Academic.error = e.message
        })
    }
}

module.exports = Academic