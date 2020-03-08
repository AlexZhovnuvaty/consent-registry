var m = require("mithril")

var Consumer = {
    list: [],
    consentRequestList: [],
    error: "",
    loadList: function(clientKey) {
        return m.request({
            method: "GET",
            url: "/api/consumer",
            headers: {
                'ClientKey': clientKey
            }
//            url: "https://rem-rest-api.herokuapp.com/api/users",
//               url: "http://localhost:8008/state?address=3d804901bbfeb7",
//            withCredentials: true,
//            withCredentials: true,
//            credentials: 'include',
        })
        .then(function(result) {
            console.log("Get Consumer list")
            Consumer.error = ""
            Consumer.list = result.data
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
            Consumer.list = []
        })
    },

    current: {},

    register: function() {
        return m.request({
            method: "POST",
            url: "/api/consumer",
            data: Consumer.current,
            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Consumer.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
        })
    },

    request_consent: function(consumerPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/academic/request_consent/" + consumerPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Consumer.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
        })
    },

    approve_request: function(academicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/consumer/approve_request/" + academicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Consumer.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
        })
    },

    revoke_request: function(academicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/consumer/revoke_request/" + academicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Consumer.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
        })
    },

    decline_request: function(academicPKey, clientKey) {
        return m.request({
            method: "GET",
            url: "/api/consumer/decline_request/" + academicPKey,
            headers: {
                'ClientKey': clientKey
            }
//            data: Doctor.current,
//            useBody: true,
//            withCredentials: true,
        })
        .then(function(items) {
//            Data.todos.list = items
            Consumer.error = ""
        })
        .catch(function(e) {
            console.log(e)
            Consumer.error = e.message
        })
    }

}

module.exports = Consumer