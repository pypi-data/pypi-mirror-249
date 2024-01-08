import requests
import json
import wave
import io

from .config import Settings
from .config import ConverterConfig
from .enums import Voice

class RestfulApiHandler(object):
    _config:ConverterConfig

    _server_support_json_status_code = [200, 300, 400, 401, 403, 404, 409, 422, 500, 503]

    def __init__(self, config:ConverterConfig) -> None:
        self._config = config

    def _restful_sender(self, api_url:str, payload:map, token="") -> requests.models.Response:
        # print(f"server url: {self._config.get_server()}{api_url}")
        url = f"{self._config.get_server()}{api_url}"
        headers = {'content-type': 'application/json', 'Authorization': f'{self._config.get_token()}'}
        return requests.post(url, headers=headers, json=payload, timeout=10)


    def _restful_getter(self, api_url:str, params=None) -> requests.models.Response:
        # print(f"server url: {self._config.get_server()}{api_url}")
        url = f"{self._config.get_server()}{api_url}"
        headers = {'Authorization': f'{self._config.get_token()}'}
        return requests.get(url, params=params, headers=headers, timeout=10)


    def _response_handler(self, result:requests.models.Response) -> json:
        if result.status_code == 200:
            if Settings.print_log:
                print(f"Restful API: Success{result.status_code}")
        else:
            if Settings.print_log:
                print(f"Error in undefined status code: {result.status_code}")
        return {"data": result.json(), "code": result.status_code}


    def get_models(self) -> json:
        api_url = "/api/v1/models/api_token"

        try:
            result = self._restful_getter(api_url)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def add_ssml_task(self, ssml_text:str) -> json:
        if self._config.voice.value == None:
            raise RuntimeError("Converter voice is 'None'")

        api_url = "/api/v1/syntheses/api_token"
        payload = {
            "ssml": f'<speak xmlns="http://www.w3.org/2001/10/synthesis" version="{self._config.get_ssml_version()}" xml:lang="{self._config.get_ssml_lang()}">\
<voice name="{self._config.voice.value}">\
{ssml_text}\
</voice></speak>'
        }

        # ssml default length = 191
        # print(f"payload length(ssml): {len(payload['ssml'])}, content length: {len(ssml_text)}")
        if len(payload['ssml']) > 2000:
            return {"data": "超過單次合成字數", "code": 42207}

        # print(f"ssml payload: {payload.get('ssml')}")

        try:
            result = self._restful_sender(api_url, payload)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def get_task_status(self, task_id:str) -> json:
        api_url = f"/api/v1/syntheses/{task_id}/api_token"

        try:
            result = self._restful_getter(api_url)
            return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


    def get_task_audio(self, task_id:str) -> json:
        # print(f"task_id: {task_id}")
        api_url = f'/api/v1/syntheses/{task_id}/api_token'

        try:
            result = self._restful_getter(api_url, params={'synthesis_id': task_id})
            # print(f"result1 : {result.json()}")
            result = self._restful_getter(result.json()['synthesis_path'].replace(self._config.get_server(), ""))
            # result = self._restful_getter('/api/v1/s/a/d0c7bd805800460e93780292d17d20f7/8aaa461ae5da4402a5c12a0740cf10b9')

            # print(f"result2 : {result.text}")
            if result.headers['Content-Type'] == "audio/x-wav":
                return {"data": result.content, "code": 200}
            else:
                return self._response_handler(result)
        except Exception as error:
            raise Exception(f"An unexpected error occurred: {error}")


class Tools(object):

    def __init__(self) -> None:
        self._support_file_type = Settings.support_file_type


    def save_wav_file(self, file_name:str, data:bytes):
        try:
            with open(f"{file_name}.wav", 'wb') as write_index:
                write_index.write(data)
                write_index.close()
        except Exception:
            raise IOError("Save wav file fail.")


    def merge_wav_file(self, filename:str, audio_data_list:list):
        try:
            merge_data = []
            for audio_data in audio_data_list:
                reader = wave.open(io.BytesIO(audio_data), 'rb')
                merge_data.append([reader.getparams(), reader.readframes(reader.getnframes())])
                reader.close()

            writer = wave.open(f"{filename}.wav", 'wb')
            writer.setparams(merge_data[0][0])
            for data in merge_data:
                writer.writeframes(data[1])
            writer.close()
        except Exception:
            raise IOError("Merge wav file fail.")


    def open_file(self, file_path:str, encode = "utf-8") -> str:
        text = ""
        try:
            with open(file_path, 'r', encoding = encode) as f:
                text = f.read()
                f.close()
        except FileNotFoundError as error:
            raise FileNotFoundError(f"No such file or directory: {file_path}")
        except Exception:
            raise Exception(f"An unexpected error occurred: {error}")

        return text
