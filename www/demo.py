from stirling.daemons.servers.http.middleware import App

class Demo(App):
    @App.url('^/$')
    def index(self):
        return "Welcome to here!"
    
    @App.url('^/another-page/$')
    def another_page(self):
        return "Look! Another page."

def start(app):
    app.url('')(Demo())

