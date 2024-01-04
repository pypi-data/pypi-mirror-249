import unittest
from unittest.mock import MagicMock, patch


from ouigo.stations import DateProcessingError as ProcessingErrorStations
from ouigo import stations
import requests


class TestLoadStations(unittest.TestCase):

    @patch('ouigo.stations.requests.get')
    def test_load_stations_api_error(self, mock_get):
        print("Empieza la prueba")
        # Configurar el mock para simular una respuesta de error de la API
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # Llamar a la función bajo prueba y esperar una excepción DateProcessingError
        with self.assertRaises(ProcessingErrorStations) as context:
            stations.load_stations("es")

        # Verificar que la excepción tiene el mensaje correcto
        self.assertEqual(str(context.exception), "API call exception load_stations, API call error load_stations, 500")



