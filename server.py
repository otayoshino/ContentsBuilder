"""
ContentsBuilder 開発用プレビューサーバー。
ローカルネットワーク上の他PCからも閲覧できるよう、0.0.0.0 でListenする。
"""

import http.server
import socketserver
import socket
import os

# ===========================
# 設定定数
# ===========================
PORT = 8080
HOST = "0.0.0.0"
# サーバーのルートディレクトリ（このファイルが置かれているフォルダ）
SERVE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_local_ip() -> str:
    """
    ローカルネットワークのIPアドレスを取得する。
    取得できない場合は 'localhost' を返す。
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "localhost"


class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    CORS ヘッダーを付与するHTTPリクエストハンドラー。
    開発環境でのクロスオリジンアクセスを許可する。
    """

    def end_headers(self):
        """レスポンスヘッダーにCORS許可ヘッダーを追加して送信する。"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, format, *args):
        """アクセスログをコンソールに出力する。"""
        print(f"[アクセス] {self.address_string()} - {format % args}")


def start_server():
    """
    プレビューサーバーを起動する。
    指定ディレクトリをルートとして静的ファイルを配信する。
    """
    os.chdir(SERVE_DIR)

    local_ip = get_local_ip()

    with socketserver.TCPServer((HOST, PORT), CORSRequestHandler) as httpd:
        httpd.allow_reuse_address = True
        print("=" * 50)
        print("  ContentsBuilder プレビューサーバー 起動中")
        print("=" * 50)
        print(f"  ローカル:      http://localhost:{PORT}/mock/")
        print(f"  ネットワーク:  http://{local_ip}:{PORT}/mock/")
        print("=" * 50)
        print("  停止するには Ctrl+C を押してください")
        print("=" * 50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nサーバーを停止しました。")


if __name__ == "__main__":
    start_server()
