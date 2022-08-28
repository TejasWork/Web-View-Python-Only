import web_app

app = web_app.application(port=5000)

data = web_app.database()
data['name'] = 'Tejas'
data.save()

window = web_app.window(port=5000)
window.set_width(int(app.screen_width/2))
window.set_height(int(app.screen_height/2))

window.set_title("Window")

@app.server.route('/')
def main():
    return web_app.render_template('main.html', data=data)

window.set_route('/')
window.show()
app.start()
web_app.force_quit()