Vue.config.debug = true;
var app = new Vue({
    el: "#app",
    delimiters: ["[[", "]]"],
    data: {
        H: 3,
        W: 3,
        board: ".........",
        message: ""
    },
    created: function () {

    },
    methods: {
        getCellImage: function (ri, ci) {
            var i = ri * this.W + ci;
            var cell = this.board[i];
            switch (cell) {
                case ".":
                    return "none";
                case "o":
                    return "maru";
                case "x":
                    return "batsu";
            }
        },
        new_game: function (player) {
            var data = {
                "cmd_type": "new_game",
                "cmd_data": player,
            };
            var self = this;
            this.post(data);
        },
        try_move: function (ri, ci) {
            var data = {
                "cmd_type": "try_move",
                "cmd_data": ri + "," + ci,
            };
            this.post(data);
        },
        post: function (data) {
            var self = this;
            fetch("/game", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }).then(function (resp) {
                var data = resp.json();
                return data;
            }).then(function (data) {
                self.board = data["board"];
                self.message = data["message"];
            });
        }
    }
});
