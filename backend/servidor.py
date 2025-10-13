from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Configuración del servidor
HOST = 'localhost'
PORT = 8080

class ContactoHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Servimos el formulario HTML
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Formulario de contacto simple
            self.wfile.write(b"""
            <html>
                <head>
                    <title>Formulario de Contacto</title>
                </head>
                <body>
                    <h1>Formulario de Contacto</h1>
                    <form method="POST" action="/contacto">
                        Nombre: <input type="text" name="nombre"><br><br>
                        Email: <input type="email" name="email"><br><br>
                        Mensaje: <textarea name="mensaje"></textarea><br><br>
                        <input type="submit" value="Enviar">
                    </form>
                </body>
            </html>
            """)
        else:
            self.send_error(404, "Página no encontrada")

    def do_POST(self):
        # Solo manejamos la ruta /contacto
        if self.path == '/contacto':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode('utf-8'))

            nombre = data.get('nombre', [''])[0]
            email = data.get('email', [''])[0]
            mensaje = data.get('mensaje', [''])[0]

            # Guardamos los datos en un archivo (puedes cambiarlo según tu necesidad)
            with open('contactos.txt', 'a') as f:
                f.write(f"Nombre: {nombre}, Email: {email}, Mensaje: {mensaje}\n")

            # Respondemos al usuario
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"""
            <html>
                <head><title>Gracias</title></head>
                <body>
                    <h1>¡Gracias por tu mensaje, {nombre}!</h1>
                    <p>Hemos recibido tu mensaje y te contactaremos a {email}.</p>
                    <a href="/">Volver al formulario</a>
                </body>
            </html>
            """.encode('utf-8'))
        else:
            self.send_error(404, "Página no encontrada")

# Iniciar el servidor
server = HTTPServer((HOST, PORT), ContactoHandler)
print(f"Servidor corriendo en http://{HOST}:{PORT}")
server.serve_forever()
