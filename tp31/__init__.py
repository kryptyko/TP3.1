from flask import Flask, jsonify, request
import requests
from config import Config
from datetime import datetime

def init_app():
    """Crea y configura la aplicación Flask"""
    app = Flask(__name__, static_folder = Config.STATIC_FOLDER, template_folder = Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)
    ####modificaciones
    ##recontramodificado
    #cambiar fehca a 18 de agosto de 2023 11:06:00
    #cambiar fehca a 18 de agosto de 2023 11:07:00
    # Ejercicio 1
    @app.route('/')
    def welcome():
        return "Bienvenidx!"
    
    # Ejercicio 2
    @app.route('/info')
    def mensaje():
        return f"Bienvenido a Programación 2 esta es una prueba - {app.config['APP_NAME']}"
    
    # Ejercicio 3
    @app.route('/about')
    def about():
        data = {
            "app_name": app.config['APP_NAME'],
            "description": app.config['DESCRIPTION'],
            "developers": app.config['DEVELOPERS'],
            "version": app.config['VERSION']
        
        }
        return jsonify(data)
    
    # Ejercicio 4
    @app.route('/sumar/<int:num1>/<int:num2>')
    def sumar(num1, num2):
        resultado = num1 + num2
        return f"El resultado de {num1} y {num2} es {resultado}"
    
    # Ejercicio 5
    @app.route('/age/<dob>')
    def calcular_edad(dob):
        try:
            fecha_de_nacimiento = datetime.strptime (dob, '%Y-%m-%d')
            fecha_actual = datetime.now()

            if fecha_de_nacimiento > fecha_actual:
                mensaje_de_error = {'error': 'La fecha de nacimiento es posterior a la fecha de hoy'}
                return jsonify(mensaje_de_error), 400
            
            edad = fecha_actual.year - fecha_de_nacimiento.year - ((fecha_actual.month, fecha_actual.day)
                < (fecha_de_nacimiento.month, fecha_de_nacimiento.day))
            return jsonify({'Edad': edad})
        
        except ValueError:
            mensaje_de_error = {'error': 'Formato de fecha invalido'}
            return jsonify(mensaje_de_error), 400
    
    # Ejercicio 6
    @app.route('/operate/<string:operation>/<int:num1>/<int:num2>')
    def operate(operation, num1, num2):
        if operation == 'sum':
            resultado = num1 + num2
        elif operation == 'sub':
            resultado = num1 - num2
        elif operation == 'mult':
            resultado = num1 * num2
        elif operation == 'div':
            if num2 == 0:
                return jsonify({'error': 'La división por cero no está definida'}), 400
            resultado = num1 / num2
        else:
            return jsonify({'error': 'Operacion no definida'}), 400

        return jsonify({'resultado': resultado})

    # Ejercicio 7
    @app.route('/operate2')
    def operate2():
        operation = request.args.get('operation')
        num1 = int(request.args.get('num1'))
        num2 = int(request.args.get('num2'))

        if operation == 'sum':
            resultado = num1 + num2
        elif operation == 'sub':
            resultado = num1 - num2
        elif operation == 'mult':
            resultado = num1 * num2
        elif operation == 'div':
            if num2 == 0:
                return jsonify({'error': 'La division por cero no esta definida'}), 400
            resultado = num1 / num2
        else:
            return jsonify({'error': 'Operación no válida'}), 400

        return jsonify({'result': resultado})
    # Ejercicio 8
    @app.route('/title/<string:word>')
    def formatear_titulo(word):
        palabra = word.capitalize()
        return jsonify({'Formatted_Word': palabra})

    # Ejercicio 9
    @app.route('/formatted/<string:dni>')
    def formatear_dni(dni):
        dni = dni.replace('.', '').replace('-', '')  # Eliminar puntos y guiones
        if len(dni) != 8 or not dni.isdigit():  # Verificar longitud y que sean dígitos
            return jsonify({'error': 'DNI invalido'}), 400
        if dni[0] == '0':  # Verificar si el primer dígito es cero
            return jsonify({'error': 'DNI invalido. No puede comenzar con 0'}), 400
        formatted_dni = int(dni)
        return jsonify({'dni_formateado': formatted_dni})
    #Ejercicio 10
    @app.route('/format', methods=['GET'])
    def formatear_user_data():
        firstname=request.args.get('firstname') #Obtengo los datos del usuario
        lastname=request.args.get('lastname') 
        dob=request.args.get('dob')
        dni=request.args.get('dni')
        if not firstname or not lastname or not dob or not dni: #Verifico que no falten datos
            return jsonify({'error': 'Faltan parámetros'}), 400
        formatted_firstname_endpoint=f'/title/{firstname}' #Formateo los datos
        formatted_firstname_response=requests.get(f'http://127.0.0.1:5000{formatted_firstname_endpoint}') #Envio los datos formateados
        if formatted_firstname_response.status_code != 200:
            return jsonify({'error': 'Nombre inválido'}), 400 
        formatted_lastname_endpoint=f'/title/{lastname}'
        formatted_lastname_response=requests.get(f'http://127.0.0.1:5000{formatted_lastname_endpoint}')
        if formatted_lastname_response.status_code != 200:
            return jsonify({'error': 'Apellido inválido'}), 400
        formatted_dob_endpoint=f'/age/{dob}'
        formatted_dob_response=requests.get(f'http://127.0.0.1:5000{formatted_dob_endpoint}')
        if formatted_dob_response.status_code != 200:
            return jsonify({'error': 'Fecha de nacimiento inválida'}), 400
        formatted_dni_endpoint=f'/formatted/{dni}'
        formatted_dni_response=requests.get(f'http://127.0.0.1:5000{formatted_dni_endpoint}')
        if formatted_dni_response.status_code != 200:
            return jsonify({'error': 'DNI inválido'}), 400
        firstname_data=formatted_firstname_response.json() #Obtengo los datos formateados
        lastname_data=formatted_lastname_response.json()    
        dob_data=formatted_dob_response.json()
        dni_data=formatted_dni_response.json()
        formatted_name=firstname_data['Formatted_Word']
        formatted_lastname=lastname_data['Formatted_Word']
        formatted_dob=dob_data['Edad']
        formatted_dni=dni_data['dni_formateado']

        #Creo el diccionario con los datos formateados
        formatted_data={ 
            'firstname': formatted_name,
            'lastname': formatted_lastname,
            'age': formatted_dob,
            'dni': formatted_dni
        }

        return jsonify({'datos_formateados': formatted_data}) #Devuelvo los datos formateados
    #Ejercicio 11
    morse_code_dict_a = {
    'A': '.-', 'B': '-...',
    'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',
    'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-',
    'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}

    @app.route('/encode/<path:text>')
    def encode_text(text):
        
        encoded_text = ''

        for char in text.upper():
            if char in morse_code_dict_a:
                encoded_text += morse_code_dict_a[char] + '+'
            if char=='+':
                encoded_text += '^+'
        encoded_text = encoded_text.strip('+')

        return jsonify({'encoded_text': encoded_text})
    
    #Ejercicio 12


    morse_code_dict_b = {
        '.-': 'A', '-...': 'B',
        '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H',
        '..': 'I', '.---': 'J', '-.-': 'K',
        '.-..': 'L', '--': 'M', '-.': 'N',
        '---': 'O', '.--.': 'P', '--.-': 'Q',
        '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W',
        '-..-': 'X', '-.--': 'Y', '--..': 'Z',
        '-----': '0', '.----': '1', '..---': '2',
        '...--': '3', '....-': '4', '.....': '5',
        '-....': '6', '--...': '7', '---..': '8',
        '----.': '9'
    }

    @app.route('/decode/<path:text>')
    def decode_morse(text):
        #decoded_text = text.replace('^', ' ')
        #words = decoded_text.split(' ')
        # -...+..-+.+-.+.-+...+^+-+.-+.-.+-..+.+...+^+--.+.+-.+-+.
        decoded_text = ''
        words=text.split('^')
        for word in words:
            chars = word.split('+')
            for char in chars:
                if char in morse_code_dict_b:
                    decoded_text += morse_code_dict_b[char]
            decoded_text += ' '
        decoded_text = decoded_text.strip()
        
        return jsonify({'decoded_text': decoded_text})
    #Ejercicio 13
    @app.route('/convert/binary/<string:num>')
    def convert_binary_to_decimal(num):
        decimal = 0
        potencia = len(num) - 1

        for digito in num:
            if digito == '1':
                decimal += 2 ** potencia
            potencia -= 1

        response = {'decimal': decimal}
        return jsonify(response)
    return app