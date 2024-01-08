import json
import time
import copy
import threading
import wave
import sys

import simpleaudio as sa

import io

from .enums import ConverterStatus, Voice
from .config import ConverterConfig, Settings
from .textedit import TextEditor
from .units import RestfulApiHandler, Tools


status_and_error_codes = {
    200: '成功',

    40101: 'jwt token 過期',
    40102: 'jwt token 無法解析',
    40103: 'email 存在，但密碼錯誤',
    40104: '使用者不在訂單區間中',

    40301: '沒有使用此 model 的權限',

    42201: '參數內容錯誤',
    42202: '送來的檔案非 jpg, jpeg, png, 或檔案過大',
    42203: '缺少 authorization header',
    42204: '所選擇的 synthesis 非 processing or waiting',
    42205: '所選擇的 synthesis 非 error',
    42206: '所選擇的 synthesis 非 success or error',
    42207: '超過單次合成字數',
    42208: '超過一個月可合成的字數',
    42209: '超過可保留的合成紀錄數',
    42210: '目前在隊列內或合成中的任務已達到上限',
    42211: '超過可保留的草稿紀錄數',
    42212: 'ssml 格式錯誤',

    40401: 'user id 不存在',
    40402: 'jwt token 不存在',
    40403: 'draft 不存在',
    40404: 'synthesis 不存在',
    40405: 'order num 不存在',
    40406: 'model 不存在',

    40901: 'order num 重複新增',
    40902: 'user 已經註冊，但尚未認證',
    40903: 'user 已經註冊，且認證完畢',

    50001: 'server 發生未知錯誤',

    50301: '寄 email 發生錯誤',
    50302: '資料庫發生錯誤',
}


class ConverterResult(object):
    """
    status：轉換器的狀態\n
    data：[{"id": (int)task_id, "data": (byte)auido_data}]\n
    detail：結果說明\n
    error_msg：error message
    """
    status:ConverterStatus
    task_data = [] # [{"id": (int)task_id, "data": (byte)auido_data}]
    detail:str
    error_message:str

    def __init__(self, status:ConverterStatus, data, detail, error_msg) -> None:
        self.status = status
        self.task_data = data
        self.detail = detail
        self.error_message = error_msg

    def save(self, filename = "aivoice", is_merge = False) -> None:
        """
        filename：檔案名稱，預設為'aivoice'\n
        is_merge：如果音檔數量超過一個，是否將其合併為一個檔案\n
        """
        task_list_length = len(self.task_data)
        if task_list_length > 0:
            if is_merge and (task_list_length > 1):
                audio_data = []
                for each_data in self.task_data:
                    audio_data.append(each_data['data'])
                Tools().merge_wav_file(filename, audio_data)
            else:
                count = 1
                for each_data in self.task_data:
                    file_number = "-" + str(count)
                    if task_list_length == 1:
                        file_number = ""

                    if each_data['data'] != None:
                        Tools().save_wav_file(filename + file_number, each_data['data'])
                    count += 1

class LivePlayAudioTask:
    _is_finished:bool = False
    _data = None

    def __init__(self, is_finished, data):
        self._is_finished = is_finished
        self._data = data

    def get_is_finished(self):
        return self._is_finished

    def get_data(self):
        return self._data

class VoiceConverter(object):
    config:ConverterConfig
    text:TextEditor
    _api_handler:RestfulApiHandler

    _text = []

    _task_list = [] # [{"id": "0~XX", "text": "paragraphs"}]
    _each_task_text_limit = Settings.each_task_text_limit

    _live_get_speech_event = None
    _live_play_audio_event = None
    _live_get_speech_thread = None
    _live_play_audio_thread = None
    _live_get_speech_error_flg = {}
    _live_play_audio_error_flg = {}
    _live_play_audio_queue = []
    _live_play_audio_task = []

    def __init__(self, config = ConverterConfig()):
        self.config = copy.deepcopy(config)
        self._api_handler = RestfulApiHandler(self.config)
        self.text = TextEditor(self._text, self.__update_config_value)


    def _translate_result_code(self, result_json:json) -> str:
        code = result_json['data']['error_code']
        if code in status_and_error_codes:
            if Settings.print_log:
                print(f"[ERROR] {status_and_error_codes[code]} (Error code: {code})")
            return status_and_error_codes[code]
        else:
            if Settings.print_log:
                print(f"[ERROR] Get server not define error code. (Error code: {code})\nMessage: {result_json['data']}")
            return result_json['data']


    def __create_task_list(self):
        # task_list = [{"id": "123", "text": "msg"}, {"id": "456", "text": "msgg"}, {"id": "789", "text": "msggg"}]
        self._task_list.clear()
        self._live_play_audio_task.clear()
        self._live_play_audio_queue.clear()
        self._live_get_speech_error_flg = {"error": False, "error_msg": ""}
        self._live_play_audio_error_flg = {"error": False, "error_msg": ""}

        i = 0
        for i in range(len(self._text)):
            self._task_list.append({"id": "", "text": self._text[i]._text})
            self._live_play_audio_task.append({"id": "", "status": "Ready", "data": ""})


    # ---------- Config ----------

    def __voice_value_to_name(self, voice_value):
        for vo in Voice:
            if voice_value == vo.value:
                return vo


    def __update_config_value(self, value:dict):
        # For text editor update converter config
        if self.config.get_voice() == None:
            self.config.set_voice(self.__voice_value_to_name(value['config_voice']))


    def update_config(self, config:ConverterConfig):
        """
        config：轉換器設定檔
        """
        if type(config) != ConverterConfig:
            raise TypeError("Parameter 'config(ConverterConfig)' type error.")

        self.config.set_token(config.get_token())
        self.config.set_server(config.get_server())
        self.config.set_voice(config.get_voice())


    # ---------- Task infomation ----------
    def get_task_list(self) -> list:
        result = []
        if len(self._task_list) < 1:
            print("[INFO] Task list is empty.")
            return result

        for task in self._task_list:
            result.append({"id": task['id'],"text": task['text']})
        return result


    def _init_threads(self):
        self._live_get_speech_event = threading.Event()
        self._live_play_audio_event = threading.Event()
        self._live_get_speech_thread = threading.Thread(target=self._run_live_get_speech, args=(self._live_get_speech_event,))
        self._live_play_audio_thread = threading.Thread(target=self._run_live_play_audio_task, args=(self._live_play_audio_event,))
        self._live_get_speech_thread.daemon = True
        self._live_play_audio_thread.daemon = True
        self._live_get_speech_thread.start()
        self._live_play_audio_thread.start()

    # ---------- Live get speech ----------
    def _run_live_get_speech(self, event):
        count = 0

        try:
            # print("run_live_get_speech...")
            while True:
                # print("thread run_live_get_speech running...")
                while len(self._live_play_audio_queue) > 0:
                    index = self._live_play_audio_queue[count]['index']
                    self._live_play_audio_task[index]['data'] = \
                        self.get_speech_by_id(self._live_play_audio_queue[count]['id'])
                    self._live_play_audio_task[index]['status'] = 'Success'
                    self._live_play_audio_queue.pop(0)
                if event.is_set():
                    # print("run_live_get_speech thread break")
                    break
                time.sleep(0.1)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as error:
            self._live_get_speech_error_flg["error"] = True
            self._live_get_speech_error_flg["error_msg"] = error


    # ---------- Live play audio ----------
    def _run_live_play_audio_task(self, event):
        task_number = len(self._live_play_audio_task)
        count = 0
        test_count = 0

        try:
            # print(f"count: {count}, task_number: {task_number}")
            while count < task_number:
                # print(f"thread running count: {count}...")
                # print(f"{count} thread status: {self._live_play_audio_task[count]['status']}")
                if self._live_play_audio_task[count]['status'] == 'Success':
                    # print("test1")
                    raw_data = self._live_play_audio_task[count]['data']

                    with io.BytesIO(raw_data) as stream:
                        with wave.open(stream, 'rb') as wf:
                            format_info = {
                                'num_channels': wf.getnchannels(),
                                'bytes_per_sample': wf.getsampwidth(),
                                'sample_rate': wf.getframerate()
                            }

                    wave_obj = sa.WaveObject(raw_data, format_info['num_channels'],
                                             format_info['bytes_per_sample'],
                                             format_info['sample_rate'])
                    play_obj = wave_obj.play()
                    play_obj.wait_done()

                    count += 1
                    # print(f"count: {count}")
                if event.is_set():
                    # print("run_live_play_audio_task thread break")
                    break
                time.sleep(0.1)
                test_count += 1

        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as error:
            self._live_play_audio_error_flg["error"] = True
            self._live_play_audio_error_flg["error_msg"] = error
        finally:
            self._live_get_speech_event.set()

    # ---------- Task ----------
    def run(self, interval_time = 0, is_wait_speech = False) -> ConverterResult:
        """
        interval_time：伺服器忙碌時，重試合成任務間隔時間，最小值=0 (不重試), 最大值=10\n
        is_wait_speech：是否等待語音合成完成，True=執行後會等待語音合成結束，Result與(func)get_speech相同
        """
        if type(interval_time) != int:
            raise TypeError("Parameter 'wait_time(int)' type error.")
        if (interval_time < 0) or (interval_time > 10):
            raise ValueError("Parameter 'wait_time(int)' value error.")

        if len(self._text) < 1:
            raise ValueError("Text is empty.") # TODO 改return result?

        self.__create_task_list()

        status = ConverterStatus.ConverterStartUp
        task_data = []
        detail = ""
        error_msg = ""

        task_number = len(self._task_list)
        task_count = 0
        task_status = 'None'
        result_json = {}

        current_queue = []

        is_live_play = Settings.is_live_play_audio

        if is_live_play == True:
            self._init_threads()

        status = ConverterStatus.ConverVoiceStart

        while task_count < task_number and \
            not self._live_get_speech_error_flg['error'] and \
                not self._live_play_audio_error_flg['error']:

            result_json = self._api_handler.add_ssml_task(self._task_list[task_count]['text'])
            if result_json['code'] != 422:
                detail = f"(Start Convert: {task_count + 1}/{task_number})"
                self._task_list[task_count]['id'] = result_json['data']['synthesis_id']
                current_queue.append(self._task_list[task_count]['id'])
                task_count += 1
            else:
                if result_json['data']['error_code'] != 42210:
                    status = ConverterStatus.ConverVoiceFail
                    task_status = 'Error'
                    error_msg = f"{self._translate_result_code(result_json)} (In process {task_count}/{task_number})"
                    break

                status = ConverterStatus.ConverVoiceRunning
                task_status = 'None'
                count = 0
                while task_status != 'Success' and task_status != 'Error' and len(current_queue) > 0:
                    result_json = self._api_handler.get_task_status(current_queue[count])
                    task_status = result_json['data']['status']

                    if task_status == 'Success':
                        status = ConverterStatus.ConverVoiceCompleted
                        index = next((index for (index, d) in enumerate(self._task_list) if d["id"] == current_queue[count]), None)
                        self._live_play_audio_queue.append({'id': current_queue[count], 'index': index})
                        self._live_play_audio_task[index]['status'] = 'Get_Speech'
                        self._live_play_audio_task[index]['id'] = current_queue[count]
                        current_queue.pop(count)
                    count += 1
                    if count >= len(current_queue):
                        count = 0

            if task_count == task_number:
                if result_json['code'] == 422 and result_json['data']['error_code'] != 42210:
                    status = ConverterStatus.ConverVoiceFail
                    task_status = 'Error'
                    error_msg = f"{self._translate_result_code(result_json)} (In process {task_count}/{task_number})"
                    break

                status = ConverterStatus.ConverVoiceRunning
                task_status = 'None'
                count = 0
                while task_status != 'Success' and task_status != 'Error' and len(current_queue) > 0:
                    result_json = self._api_handler.get_task_status(current_queue[count])
                    task_status = result_json['data']['status']

                    if task_status == 'Success':
                        index = next((index for (index, d) in enumerate(self._task_list) if d["id"] == current_queue[count]), None)
                        self._live_play_audio_queue.append({'id': current_queue[count], 'index': index})
                        self._live_play_audio_task[index]['status'] = 'Get_Speech'
                        self._live_play_audio_task[index]['id'] = current_queue[count]
                        current_queue.pop(count)
                        if len(current_queue) != 0:
                            task_status = 'None'

                    count += 1
                    if count >= len(current_queue):
                        count = 0

            time.sleep(interval_time)

        if self._live_get_speech_error_flg['error']:
            raise Exception(f"An unexpected error occurred: {self._live_get_speech_error_flg['error_msg']}")
        if self._live_play_audio_error_flg['error']:
            raise Exception(f"An unexpected error occurred: {self._live_play_audio_error_flg['error_msg']}")

        if task_status == "Success":
            if is_live_play:
                self._live_get_speech_thread.join()
                self._live_play_audio_thread.join()
                self._live_get_speech_event.set()
                self._live_play_audio_event.set()
            if is_wait_speech == True:
                return self.get_speech()

            return ConverterResult(status, task_data, detail, error_msg)
        else:
            if is_live_play:
                self._live_get_speech_event.set()
                self._live_play_audio_event.set()


        return ConverterResult(ConverterStatus.ConverVoiceFail, task_data, "", error_msg)


    def check_status(self) -> ConverterResult:
        """
        合成任務狀態["Success", "Waiting", "Error", "Processing"]
        """
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")

        status = ConverterStatus.ConverterStartUp
        task_data = []
        detail = ""
        error_msg = ""

        task_number = len(self._task_list)
        task_count = 1
        for task in self._task_list:
            result_json = self._api_handler.get_task_status(task['id'])

            if Settings.print_log:
                print(f"[INFO] Task({task['id'][:8]}) convert status '{result_json['data']['status'].lower()}'")

                if result_json['data']['status'] == "Success":
                    status = ConverterStatus.ConverVoiceCompleted
                elif result_json['data']['status'] == "Processing":
                    status = ConverterStatus.ConverVoiceRunning
                    detail = f"Voice Converting: Task({task_count}/{task_number})"
                elif result_json['data']['status'] == "Waiting":
                    status = ConverterStatus.ServerBusy
                else:
                    error_msg = self._translate_result_code(result_json)
                    status = ConverterStatus.ConverVoiceFail

            task_data.append({"id": task['id'], "data": None})
            task_count += 1
        return ConverterResult(status, task_data, detail, error_msg)


    def get_speech(self) -> ConverterResult:
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")

        task_data = []
        error_msg = ""
        for task in self._task_list:
            result_json = self._api_handler.get_task_audio(task['id'])
            # print(f"result_json['code']: {result_json['code']}")

            if result_json['code'] != 200:
                error_msg = self._translate_result_code(result_json)
                task_data.append({"id": task['id'], "data": None})
                return ConverterResult(ConverterStatus.GetSpeechFail, task_data, "", error_msg)

            task_data.append({"id": task['id'], "data": result_json['data']})
        return ConverterResult(ConverterStatus.GetSpeechSuccess, task_data, "", error_msg)

    def get_speech_by_id(self, id):
        if len(self._task_list) < 1:
            raise RuntimeError("Converter task list is empty, Please start convert first.")

        result_json = self._api_handler.get_task_audio(id)

        if result_json['code'] != 200:
            error = self._translate_result_code(result_json)
            raise Exception(f"An unexpected error occurred: {error}")

        return result_json['data']


    def get_models(self) -> list:
        models = []
        result_json = self._api_handler.get_models()
        for model in result_json['data']:
            models.append({
                'model_id': model['model_id'],
                'name': model['name'],
                'gender': model['gender'],
                'languages': model['languages'],
            })

        return models