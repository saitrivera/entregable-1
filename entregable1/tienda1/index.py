from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Cambia esto a una clave secreta más segura en producción

# Simulación de base de datos de productos
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 1000, "descripcion": "Laptop de alta gama", "imagen": "laptop.jpg"},
    {"id": 2, "nombre": "Smartphone", "precio": 500, "descripcion": "Smartphone Android", "imagen": "smartphone.jpg"},
    {"id": 3, "nombre": "Audífonos", "precio": 50, "descripcion": "Audífonos con cancelación de ruido", "imagen": "audifonos.jpg"},
    {"id": 4, "nombre": "Monitor", "precio": 300, "descripcion": "Monitor 4K", "imagen": "monitor.jpg"},
]

# Simulación de base de datos de usuarios
usuarios = {
    'usuario1': 'contraseña1',
    'usuario2': 'contraseña2'
}

# Carrito de compras (vacío al inicio)
@app.before_request
def inicializar_carrito():
    if 'carrito' not in session:
        session['carrito'] = []

@app.route('/')
def principal():
    return render_template('index.html')

# Página de productos
@app.route('/productos')
def mostrar_productos():
    return render_template('productos.html', productos=productos)

# Agregar producto al carrito
@app.route('/agregar_al_carrito/<int:producto_id>')
def agregar_al_carrito(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        # Revisar si el producto ya está en el carrito
        carrito = session.get('carrito', [])
        for item in carrito:
            if item['id'] == producto_id:
                item['cantidad'] += 1
                break
        else:
            # Si no está, agregarlo con cantidad 1
            carrito.append({'id': producto['id'], 'nombre': producto['nombre'], 'precio': producto['precio'], 'cantidad': 1})
        session['carrito'] = carrito
    return redirect(url_for('ver_carrito'))

# Ver carrito de compras
@app.route('/carrito')
def ver_carrito():
    carrito = session.get('carrito', [])
    total = sum(item['precio'] * item['cantidad'] for item in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

# Página de pago
@app.route('/pago', methods=['GET', 'POST'])
def pago():
    if request.method == 'POST':
        # Aquí puedes manejar el pago real, como con una API de pagos
        session['carrito'] = []  # Limpiar el carrito después del pago
        return render_template('pago.html', mensaje="¡Pago exitoso!")
    return render_template('pago.html')

# Ruta para mostrar el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in usuarios and usuarios[username] == password:
            session['usuario'] = username
            return redirect(url_for('mostrar_productos'))
        else:
            return "Credenciales incorrectas", 403  # Puedes redirigir a una página de error personalizada
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('mostrar_productos'))

if __name__ == '__main__':
    app.run(debug=True, port=5017)
