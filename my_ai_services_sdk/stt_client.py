# my_ai_services_sdk/my_ai_services_sdk/stt_client.py
import os
import azure.cognitiveservices.speech as speechsdk

def recognize_from_mic():
    """從麥克風進行即時語音辨識，直到無聲或按下 Enter"""
    try:
        AZURE_API_KEY = os.environ["AZURE_API_KEY"]
        AZURE_REGION = os.environ["AZURE_REGION"]
    except KeyError:
        print("錯誤：請設定 AZURE_API_KEY 和 AZURE_REGION 環境變數")
        return None

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
    speech_config.speech_recognition_language="zh-TW"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("請開始說話...")
    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"辨識結果: {result.text}")
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("無法辨識語音")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"辨識被取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"錯誤詳情: {cancellation_details.error_details}")
        return None