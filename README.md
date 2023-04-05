Amazon-Free-Search-Api
=======
[![CodeFactor](https://www.codefactor.io/repository/github/lunapy17/amazon-free-search-api/badge)](https://www.codefactor.io/repository/github/lunapy17/amazon-free-search-api)

Este es un proyecto que usa Flask para crear un servidor que permite buscar productos en Amazon. El proyecto incluye autenticación con JSON Web Tokens (JWT).

# Uso
Para buscar productos, usa la ruta /search con los parámetros keyword, proxy (opcional) y quantity (opcional). La autenticación es necesaria para buscar productos. Para registrarte, usa la ruta /register, y para iniciar sesión, usa la ruta /login.

# Ejemplo

```python
from requests import get
rq = get("http://127.0.0.1:5000/search?keyword=CellPhone&jwt=[JWT-TOKEN]&quantity=1&proxy=8.8.8.8")
print(rq.text)
```
# Salida

```json
{"keywords":"CellPhone","products":[{"link":"https://www.amazon.com.mx/SAMSUNG-Electronics-Smartphone-Brightest-Processor/dp/B09MW17JQY/ref=sr_1_1?keywords=cell+phone&qid=1680734487&sr=8-1&ufe=app_do%3Aamzn1.fos.66c34496-0d28-4d73-a0a1-97a8d87ec0b2","name":"SAMSUNG Electronics Galaxy S22 Ultra Smartphone, Factory Unlocked Android Cell Phone, 512GB, 8K Camera & Video, Brightest Display, S Pen, Long Battery Life, Fast 4nm Processor, US Version, Burgundy","price":"$20,842.82","rating":"4.6 de 5 estrellas"}]}
```


# Instalación
1. Clona este repositorio
2. Instala los paquetes necesarios pip install -r requirements.txt
3. Ejecuta python app.py
4. Ve a http://localhost:5000 en tu navegador web para ver la página principal.

# Créditos
Este proyecto fue creado por LunaPy17 y es libre de uso.

# Contribución
Las contribuciones son bienvenidas. Si quieres contribuir, sigue los siguientes pasos:

1.Haz un fork de este repositorio
2. Crea una nueva rama (git checkout -b feature)
3. Haz tus cambios y haz commit (git commit -am 'Add feature')
4. Empuja la rama (git push origin feature)
5. Abre un Pull Request
