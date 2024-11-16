from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
import os
import re
import openai

# Configuración de OpenAI
openai.api_key = settings.OPENAI_API_KEY

class AnalyzeTextView(APIView):
    def post(self, request):
        try:
            # Obtener el texto enviado en la solicitud
            detected_text = request.data.get("text", "").strip()

            if not detected_text:
                return Response({"error": "El texto a analizar es requerido"}, status=400)

            # Llamada a OpenAI para analizar el texto
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

            # Extraer el resultado de OpenAI
            detected_department_code = response_openai.choices[0].message.content

            patron = r"\[([^\[\]]+)\]"

            department_code = str(re.search(patron, detected_department_code).group(1)).upper()

            print(f"Resultado de OpenAI: {department_code}")

            # Devolver el resultado
            return Response({"openai_depto": department_code})
        
        except Exception as e:
            print(f"Error interno: {e}")
            return Response({"error": "Error interno del servidor"}, status=500)