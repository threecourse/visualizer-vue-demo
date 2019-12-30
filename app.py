import os
import tornado.web
import tornado.escape
import tornado.ioloop
from tornado.options import define
from model import Model


class IndexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html")


class GameHandler(tornado.web.RequestHandler):

    def initialize(self, model: Model):
        self.model = model

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        cmd_type = data["cmd_type"]
        cmd_data = data["cmd_data"]

        if cmd_type == "new_game":
            h_color = cmd_data
            self.new_game(h_color=h_color)

        if cmd_type == "try_move":
            y, x = int(cmd_data[0]), int(cmd_data[2])
            self.try_move(y, x)

        board_str = self.board_str()
        messages = []
        messages.append(f"turn: {self.model.turn}")
        messages.append(f"next_player: {self.model.next_player}")
        if self.model.over:
            messages.append(f"game is over: winner {self.model.winner}")

        self.write({"board": board_str, "message": "\n".join(messages)})

    def new_game(self, h_color):
        self.model.start_game(h_color=h_color)
        self.move_by_ai_while_ai_turn()

    def try_move(self, y, x):
        if self.model.over:
            print("game is already over")
            return
        if not self.model.is_legal(y, x):
            print("action is unavailable")
            return
        self.model.move(y, x)
        self.move_by_ai_while_ai_turn()

    def move_by_ai_while_ai_turn(self):
        while True:
            if self.model.is_next_human or self.model.over:
                break
            self.model.move_by_ai()

    def board_str(self) -> str:
        ret = ""
        for y in range(3):
            for x in range(3):
                ret += self.model.board[y, x]
        return ret


class Application(tornado.web.Application):

    def __init__(self, model: Model):
        handlers = [
            (r"/", IndexHandler),
            (r"/game", GameHandler, dict(model=model)),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


def start():
    model = Model()
    model.start_game(h_color="black")

    define("port", default=8888, help="run on the given port", type=int)
    app = Application(model)
    port = int(os.environ.get("PORT", 8888))
    app.listen(port)
    print("Run server on port: {}".format(port))

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    start()
