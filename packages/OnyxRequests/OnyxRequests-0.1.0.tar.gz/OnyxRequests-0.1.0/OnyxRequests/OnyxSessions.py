"""
Desarrollado por mmenamore, Perú, 2024.

Este módulo define la clase Onyx, una extensión de la clase Session de la biblioteca requests. 
La clase Onyx está diseñada para proporcionar una experiencia de solicitudes HTTP mejorada, 
permitiendo el uso de User-Agent personalizados y ofreciendo la funcionalidad de reintentos automáticos 
en caso de fallas en las solicitudes.

La clase Onyx es ideal para aplicaciones que requieren una robusta interacción con APIs y sitios web, 
gestionando eficientemente situaciones como la pérdida temporal de conexión o problemas de acceso al servidor. 
Incorpora una lógica de reintento inteligente y configurable, lo que la hace particularmente útil en 
entornos de producción donde la estabilidad y la confiabilidad de las solicitudes HTTP son críticas.

Fecha: 2024
Hora Actual: [03/01/2024]
"""

import requests
from requests.exceptions import RequestException

class Onyx(requests.Session):
    def __init__(self, *args, **kwargs):
        """
        Inicializa una sesión Onyx con la opción de especificar un User-Agent personalizado.
        Si no se proporciona un User-Agent, se utilizará uno por defecto.
        
        Args:
            *args: Argumentos variables para la clase base Session.
            **kwargs: Argumentos clave-valor. Puede incluir 'headers' con un 'User-Agent' personalizado.
        """
        user_agent = kwargs.pop('headers', {}).get('User-Agent', "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        super(Onyx, self).__init__(*args, **kwargs)
        self.headers["User-Agent"] = user_agent

    def request(self, method: str, url: str, retrys: int = 3, **kwargs) -> requests.Response:
        """
        Envía una solicitud utilizando el método HTTP especificado con la capacidad de reintentar la solicitud
        en caso de fallas.

        Args:
            method (str): Método HTTP para la solicitud (p.ej., 'GET', 'POST').
            url (str): URL a la cual se realiza la solicitud.
            retrys (int): Número de reintentos en caso de fallas de conexión.
            **kwargs: Argumentos adicionales pasados a la solicitud, como 'headers', 'proxies', etc.

        Returns:
            requests.Response: Objeto de respuesta de la solicitud.

        Raises:
            ValueError: Si se alcanza el número máximo de reintentos sin éxito.
        """
        last_exception = None
        Retry = 0
        original_proxies = kwargs.get('proxies', None)
        half_retrys = retrys // 2

        while retrys > 0:
            try:
                response = super(Onyx, self).request(method, url, **kwargs)
                return response
            except RequestException as e:
                Retry += 1
                print(f"ONYX APIs | Requests Error: Retry Number {Retry}")
                last_exception = e
                retrys -= 1

                # Si hemos alcanzado la mitad de los intentos, intentar sin proxies
                if retrys == half_retrys and original_proxies:
                    print("ONYX APIs | Removing proxies and retrying...")
                    kwargs.pop('proxies', None)

                continue

        if retrys == 0:
            raise ValueError(f"ONYX APIs : Max Retrys Exceeded. Last exception: {last_exception} | Retrys: {Retry}")
