import socket
import urllib.request


class ConnectionStatus:
    def check_internet(self, timeout=4):
        try:
            request = urllib.request.Request(
                "https://www.google.com/generate_204",
                headers={"User-Agent": "Yabandeh/1.0"}
            )

            with urllib.request.urlopen(
                request, timeout=timeout
            ) as response:
                return {
                    "connected": response.status < 500,
                    "message": "اتصال اینترنت برقرار است",
                    "status_code": response.status
                }

        except Exception as error:
            return {
                "connected": False,
                "message": "اتصال اینترنت در دسترس نیست",
                "error": str(error)
            }

    def check_host(self, host, port=443, timeout=4):
        try:
            with socket.create_connection(
                (host, int(port)), timeout=timeout
            ):
                return True
        except (OSError, ValueError):
            return False
