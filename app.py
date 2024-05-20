from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json

def crear_app():
    app = Flask(__name__)

    @app.route('/<ISBN>')
    def inicio(ISBN):
        codigo_BE = ISBN
        web = f'https://www.abebooks.com/servlet/SearchResults?ref_=search_f_cms&isbn={codigo_BE}'
        response = requests.get(web)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        results = soup.find("li", {"id": "book-1"})

        libro = {
            "ISBN": results.find('meta', itemprop="isbn")['content'],
            "Autor": results.find('meta', itemprop="author")['content'],
            "Nombre": results.find('meta', itemprop="name")['content'],
            "Publicador": results.find('meta', itemprop="publisher")['content']
        }

        json_libro = json.dumps(libro)
        return render_template('index.html', codigo_FE = codigo_BE, libro_FE =  json_libro)
    return app
if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)
