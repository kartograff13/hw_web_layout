from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Tuple, Type


class SimpleHandler(BaseHTTPRequestHandler):

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Инициализатор с явными аннотациями типов"""
        super().__init__(*args, **kwargs)

    def do_GET(self) -> None:
        """Обработчик GET-запросов"""
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        try:
            current_dir: Path = Path(__file__).parent
            html_file_path: Path = current_dir / "templates" / "contacts.html"

            with open(html_file_path, "r", encoding="utf-8") as file:
                html_content: str = file.read()

            self.wfile.write(html_content.encode("utf-8"))

        except FileNotFoundError:
            self.send_error(404, "Файл contacts.html не найден")
        except Exception as e:
            self.send_error(500, f"Ошибка сервера: {str(e)}")

    def log_message(self, format_str: str, *args: Any) -> None:
        """Переопределяем метод логирования для отключения стандартного вывода"""
        pass


def run_server(port: int = 8000) -> None:
    """Запускает HTTP сервер на указанном порту"""
    server_address: Tuple[str, int] = ("", port)

    handler_class: Type[BaseHTTPRequestHandler] = SimpleHandler
    httpd: HTTPServer = HTTPServer(server_address, handler_class)

    print(f"Сервер запущен на http://localhost:{port}")
    print("Нажмите Ctrl+C для остановки сервера")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
