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
        try:
            response = requests.get(web)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")

            results = soup.find("li", {"id": "book-1"})

            libro = {
                "ISBN": results.find('meta', itemprop="isbn")['content'],
                "Autor": results.find('meta', itemprop="author")['content'],
                "Nombre": results.find('meta', itemprop="name")['content'],
                "Publicador": results.find('meta', itemprop="publisher")['content'],
                "Fecha": results.find('meta', itemprop="datePublished")['content']
            }

            return json.dumps(libro), 200
        except:
            libro = {
                "ISBN": "Libro No encontrado, Revise el ISBN"
            }
            return json.dumps(libro), 404
    @app.errorhandler(404)
    def page_not_found(e):
        libro={
            "ISBN":"Libro No encontrado, Revise el ISBN"
        }
        return json.dumps(libro), 404
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True)
