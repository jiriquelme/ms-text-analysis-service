from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import openai
import os

# Configuración de las API
openai.api_key = settings.OPENAI_API_KEY
IMAGE_PROCESSING_SERVICE_URL = "http://34.46.252.163/api/process-image/"  # Cambia esto si tu microservicio está en otra URL

ERROR_MESSAGE = "Error al procesar el texto."

def get_text_from_image_service(image_file) -> str:
    """
    Envía una imagen al microservicio de procesamiento de imágenes y devuelve el texto detectado.

    :param image_file: Archivo de imagen a enviar.
    :return: Texto detectado en la imagen o None si ocurre un error.
    """
    try:
        # Enviar la imagen al microservicio
        files = {'image': image_file}
        response = requests.post(IMAGE_PROCESSING_SERVICE_URL, files=files)
        
        # Verificar si la respuesta fue exitosa
        if response.status_code == 200:
            detected_text = response.json().get("text").replace('\n', ' ')
            print(f"Texto detectado por el microservicio: {detected_text}")
            return detected_text
        else:
            print(f"Error del microservicio de procesamiento de imágenes: {response.status_code} - {response.json()}")
            return None
    except Exception as e:
        print(f"Error al conectarse con el microservicio de procesamiento de imágenes: {e}")
        return None

def analyze_text_with_openai(detected_text: str) -> str:
    """
    Envía el texto detectado a OpenAI para analizar y extraer el código de departamento.

    :param detected_text: Texto detectado en la imagen.
    :return: Código de departamento o un mensaje de error si ocurre un problema.
    """
    try:
        # Enviar el texto detectado a OpenAI para análisis
        response_openai = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f'Identifica el departamento del siguiente texto. El código del departamento está formado por letras y números. Devuelve únicamente el identificador, sin agregar ninguna otra información muestra SIEMPRE en el siguiente formato. Es importante que siempre los simbolos "[]" estén presentes. Formato: Departamento [identificador]. Texto: {detected_text}'
                }
            ],
            max_tokens=100,
            timeout=10  # Agregando un timeout para evitar bloqueos largos
        )

        department_code = response_openai.choices[0].message.content
        print(f"Resultado de OpenAI: {department_code}")
        return department_code
    except Exception as e:
        print(f"Error al procesar texto con OpenAI: {e}")
        return ERROR_MESSAGE

@csrf_exempt
def text_analysis(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Obtén el archivo de imagen de la solicitud
        image_file = request.FILES['image']

        detected_text = get_text_from_image_service(image_file)

        result = analyze_text_with_openai(detected_text)
        
        # Devuelve el resultado en formato JSON
        return JsonResponse({'result': result, 'texto_detectado':detected_text})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ========================================================================
#                               Render de Prueba
# ========================================================================

def test_process_image(request):
    if request.method == 'POST' and 'image' in request.FILES:
        # Obtén el archivo de imagen de la solicitud
        image_file = request.FILES['image']

        detected_text = get_text_from_image_service(image_file)

        result = analyze_text_with_openai(detected_text)
        
        # Devuelve el resultado en formato JSON
        return JsonResponse({'result': result, 'texto_detectado':detected_text})
    else:
        return render(request, 'test_process_image.html')

