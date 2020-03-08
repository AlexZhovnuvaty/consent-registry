var m = require("mithril")

var Data = {
    list: [],
    consentRequestList: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/data",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            Data.error = ""
            Data.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Data.error = e.message
            Data.list = []
        })
    },

    loadConsentRequestList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/data/consent_request_list",
            headers: {
                'ClientKey': clientKey
            }
        })
        .then(function(result) {
            Data.error = ""
            Data.consentRequestList = result.data
        })
        .catch(function(e) {
            console.log(e)
            Data.error = e.message
            Data.consentRequestList = []
        })
    },

//    screening_data: function(investigatorPKey, inclExclCriteria) {   //i.e Investigator
//        return m.request({
//            method: "GET",
//            url: "/api/ehrs/pre_screening_data?" + inclExclCriteria,
//            headers: {
//                'ClientKey': investigatorPKey
//            }
//        })
//        .then(function(result) {
//            console.log("Get Pre-screening data")
//            EHR.error = ""
//            EHR.sharedDataList = result.data
//        })
//        .catch(function(e) {
//            console.log(e)
//            EHR.error = e.message
//            EHR.sharedDataList = []
//        })
//    },

    current: {},

    add: function(clientKey) {
        return m.request({
            method: "POST",
            url: "/api/data",
            data: Data.current,
            headers: {
                'ClientKey': clientKey
            },
            useBody: true,
        })
        .then(function(items) {
            Data.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Data.error = e.message
        })
    }
}

module.exports = Data