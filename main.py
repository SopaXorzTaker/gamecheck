from socket import timeout
from flask import *
from server_ping.server_ping_helper import ServerPingHelper

COLORS = [
    "#000000", "#00007f", "#007f00", "#007f7f",
    "#7f0000", "#7f007f", "#7f7f00", "7f7f7f",
    "#3f3f3f", "#0000ff", "#00ff00", "#00ffff",
    "#ff0000", "#ff00ff", "#ffff00", "#ffffff"
]


def sanitize(text):
    return text.replace("<", "").replace("\"", "").replace("'", "")


def mc_color(text):
    out = ""

    expect_code = False

    color_set = False
    closing_tags = []

    for char in text:
        if char == '\u00a7':
            expect_code = True
            continue

        if not expect_code:
            out += char
        else:
            expect_code = False
            # if not code == "r":
            #    out += closing_tags[-1:]
            #    del closing_tags[len(closing_tags) - 1]
            code = char
            if code in "0123456789abcdef":
                if color_set:
                    out += "</font>"
                out += "<font color='{0}'>".format(COLORS[int(code, 16)])
                #print out
                color_set = True
                closing_tags.append("</font>")
            elif code == "l":
                out += "<b>"
                closing_tags.append("</b>")
            elif code == "m":
                out += "<s>"
                closing_tags.append("</s>")
            elif code == "n":
                out += "<u>"
                closing_tags.append("</u>")
            elif code == "o":
                out += "<i>"
                closing_tags.append("</i>")
            elif code == "r":
                for t in reversed(closing_tags):
                    out += t
                closing_tags = []
    for t in reversed(closing_tags):
        out += t

    return out


app = Flask(__name__)

# url_for("static", filename="static/")


def check(host, port, server_type):
    return ServerPingHelper.ping((host, port), server_type)


@app.route("/")
def main_page():
    return app.send_static_file("main.html")


@app.route("/check")
def chk():
    try:
        server_type = request.args.get("type")
        addr = request.args.get("address").split(":")
        host = addr[0]
        port = int(addr[1]) if len(addr) > 1 else (25565 if server_type == "minecraft" else 19132)
        ping_result = check(host, port, server_type)
        return render_template("result.html", address=":".join(addr), servtype=ping_result.server_type,
                               version=ping_result.version, description=mc_color(sanitize(ping_result.description)),
                               ping_time=ping_result.ping_time, icon_url=ping_result.icon_url)
    except timeout:
        return app.send_static_file("timeout.html")
    except Exception as exception:
        return render_template("error.html", error=repr(exception))


@app.route("/api")
def api_req():
    try:
        host = request.args.get("host")
        port = int(request.args.get("port"))
        server_type = request.args.get("type")
        ping_result = check(host, port, server_type)
        return jsonify(vars(ping_result))
    except Exception as exception:
        return jsonify({"error": str(exception)})


if __name__ == "__main__":
    app.run(debug=True)