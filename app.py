# Importing libraries
from bs4 import BeautifulSoup
import json
from requests import get
from time import sleep
from flask import Flask, request
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
import jwt

# Initializing Flask application
app = Flask(__name__)

# Configuring JWT
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
app.config['JWT_SECRET_KEY'] = 'secreto'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config["JWT_COOKIE_SECURE"] = False

jwt = JWTManager(app)

USUARIOS = {}

# Setting user identity loader
@jwt.user_identity_loader
def user_identity_lookup(usuario): return usuario

# Register route to create new users
@app.route('/register')
def registro():
    usuario = request.args.get('user', None)
    contraseña = request.args.get('password', None)

    # Checking for missing fields
    if usuario is None or contraseña is None: return {'error': 'Debes proporcionar un nombre de usuario y una Password'}, 400
    # Checking for existing user
    if usuario in USUARIOS: return {'error': 'El usuario ya existe'}, 400

    # Checking for existing user
    USUARIOS[usuario] = {'contraseña': contraseña}
    return {'mensaje': 'Usuario registrado correctamente'}, 201

# Login route to authenticate users
@app.route('/login')
def login():
    usuario = request.args.get('user', None)
    contraseña = request.args.get('password', None)

    # Checking for missing fields
    if usuario is None or contraseña is None:
        return {'error': 'Debes proporcionar un nombre de usuario y una Password'}, 400
    # Authenticating user
    if usuario not in USUARIOS or USUARIOS[usuario]['contraseña'] != contraseña:
        return {'error': 'Usuario o Password incorrectos'}, 401
    
    # Creating access token for user
    access_token = create_access_token(identity=user_identity_lookup(usuario))
    return {'access_token': access_token}

# Search route to search for products in Amazon
@app.route('/search')
@jwt_required(locations=["query_string"])
def busqueda():
    # Getting user identity
    usuario = get_jwt_identity()

    # Getting search parameters
    keyword = request.args.get("keyword", None)
    proxy = request.args.get("proxy", None)
    cantidad = request.args.get("quantity", None)

    # Searching for products
    return search(keyword, proxy, cantidad)

# Main route to show the homepage
@app.route('/')
def principal(): return "Hello World!<br>My GitHub >>> https://github.com/LunaPy17", 200

# Function to find substring between two strings
def find_between( data, first, last ):
    try:
        start = data.index( first ) + len( first )
        end = data.index( last, start )
        return data[start:end]
    except ValueError:
        return ''

# Function to search for products in Amazon
def search(keyword, proxy, cantidad):
    # Checking if quantity parameter is valid
    if cantidad != None:
        if int(cantidad) >= 10: cantidad = 10
    else: cantidad = 3

    # Checking if proxy parameter is valid
    if proxy != None:
        proxies = {
            'http': 'http://'+proxy,
            'https': 'http://'+proxy
        }
    else: proxies = None

    # Setting request headers
    headers = {
        "authority": "www.amazon.com",
        "method": "GET",
        "path": f"/s?k={keyword}",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "accept-language": "es;q=0.7",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "sec-gpc": "1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    # Send a GET request to the Amazon website and get the HTML content of the page
    html = get(f"https://www.amazon.com.mx/s?k={keyword}", headers=headers, proxies=proxies)

    # Send a GET request to the Amazon website and get the HTML content of the page
    while ("de nuestra parte. " in html.text and " intenta" in html.text) or \
            ("Para comentar el " in html.text and " a los" in html.text and "acceso automatizado" in html.text):
        print("Captcha detected. Sleeping for 1 second...")
        sleep(1)
        html = get(f"https://www.amazon.com.mx/s?k={keyword}", headers=headers, proxies=proxies)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html.content, "html.parser")

    # Get the list of products
    productos = soup.find_all("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"})
    listaEstrellas = soup.find_all("div", {"class": "a-row a-size-small"})
    listaPrecios = soup.find_all("div", {"class": "a-row a-size-base a-color-base"})
    listaNombres = soup.find_all("div", {"class": "a-section a-spacing-none a-spacing-top-small s-title-instructions-style"})

    productosNombres = []
    productosEstrellas = []
    productosLinks = []
    productosPrecios = []

    # Iterate over the list of products to get the information needed
    for estrellas in listaEstrellas[:int(cantidad)]:
        est = estrellas.find('span')['aria-label']
        productosEstrellas.append(est)

    for prices in listaPrecios[:int(cantidad)]:
        prec = prices.find('span', class_ = "a-offscreen")
        productosPrecios.append(prec.text)

    for nombres in listaNombres[:int(cantidad)]:
        nomb = nombres.find('span', class_ = "a-size-base-plus a-color-base a-text-normal")
        productosNombres.append(nomb.text)

    for producto in productos[:int(cantidad)]:
        url = producto.find('a')['href']
        productosLinks.append("https://www.amazon.com.mx"+url)

    return {
        'keywords': keyword,
        'products': [{
            'name': productosNombres[i],
            'link': productosLinks[i],
            'price': productosPrecios[i],
            'rating': productosEstrellas[i]
        } for i in range(len(productosNombres))]
    }

if __name__ == '__main__':
    app.run(host="0.0.0.0")
