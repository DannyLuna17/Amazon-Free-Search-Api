# Amazon-Free-Search-Api
Este es un proyecto que usa Flask para crear un servidor que permite buscar productos en Amazon. El proyecto incluye autenticación con JSON Web Tokens (JWT).

# Uso
Para buscar productos, usa la ruta /search con los parámetros keyword, proxy (opcional) y quantity (opcional). La autenticación es necesaria para buscar productos. Para registrarte, usa la ruta /register, y para iniciar sesión, usa la ruta /login.

# Instalación
1. Clona este repositorio
2. Instala los paquetes necesarios pip install -r requirements.txt
3. Ejecuta python app.py
4. Ve a http://localhost:5000 en tu navegador web para ver la página principal.

# Créditos
Este proyecto fue creado por LunaPy17 y está bajo la licencia GPL 3.0. Para más información, ve al archivo LICENSE.

# Contribución
Las contribuciones son bienvenidas. Si quieres contribuir, sigue los siguientes pasos:

1.Haz un fork de este repositorio
2. Crea una nueva rama (git checkout -b feature)
3. Haz tus cambios y haz commit (git commit -am 'Add feature')
4. Empuja la rama (git push origin feature)
5. Abre un Pull Request
