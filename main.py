from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET-запросов с маршрутизацией"""
        path = self.path.split('?')[0]

        routes = {
            '/': 'general.html',
            '/general': 'general.html',
            '/categories': 'categories.html',
            '/orders': 'orders.html',
            '/contacts': 'contacts.html'
        }

        filename = routes.get(path)

        if not filename:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            error_html = """
            <!DOCTYPE html>
            <html>
            <head><title>404 - Страница не найдена</title></head>
            <body>
                <h1>404 - Страница не найдена</h1>
                <p>Доступные страницы:</p>
                <ul>
                    <li><a href="/">Главная</a></li>
                    <li><a href="/categories">Категории</a></li>
                    <li><a href="/orders">Заказы</a></li>
                    <li><a href="/contacts">Контакты</a></li>
                </ul>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode('utf-8'))
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        try:
            current_dir = Path(__file__).parent
            html_file_path = current_dir / 'templates' / filename

            with open(html_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            self.wfile.write(html_content.encode('utf-8'))

        except FileNotFoundError:
            self.send_error(404, f"Файл {filename} не найден")
        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")

    def log_message(self, log_format, *args):
        """Переопределение метода логирования для отключения стандартного вывода"""
        pass


def run_server(port=8000):
    """Запуск HTTP-сервера"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHandler)
    print(f"Сервер запущен на http://localhost:{port}")
    print("Доступные страницы:")
    print("  http://localhost:8000/ - Главная")
    print("  http://localhost:8000/general - Главная (альтернатива)")
    print("  http://localhost:8000/categories - Категории")
    print("  http://localhost:8000/orders - Заказы")
    print("  http://localhost:8000/contacts - Контакты")
    print("\nНажмите Ctrl+C для остановки сервера")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
