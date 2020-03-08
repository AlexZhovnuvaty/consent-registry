var m = require("mithril")

module.exports = {

    view: function(vnode) {
        return m("main.layout", [
            m("nav.menu", [
                m("a", {href: "/consumer", oncreate: m.route.link}, "As Consumer|"),
                m("a", {href: "/academic", oncreate: m.route.link}, "As Academic|"),
            ]),
            m("section", vnode.children),
        ])
    }
}