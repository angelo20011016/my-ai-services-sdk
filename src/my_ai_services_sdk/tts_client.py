# my_ai_services_sdk/my_ai_services_sdk/tts_client.py
import os
import azure.cognitiveservices.speech as speechsdk

def speak_text(text, voice_name='zh-TW-HsiaoChenNeural'):
    """將指定的文字透過預設喇叭播放出來"""
    try:
        AZURE_API_KEY = os.environ["AZURE_API_KEY"]
        AZURE_REGION = os.environ["AZURE_REGION"]
    except KeyError:
        print("錯誤：請設定 AZURE_API_KEY 和 AZURE_REGION 環境變數")
        return

    speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    
    # 選擇語音，你可以在 Azure 文件中找到更多選擇
    speech_config.speech_synthesis_voice_name=voice_name
    
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    print(f"正在合成語音: '{text[:20]}...'")
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("語音合成完成")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print(f"語音合成被取消: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print(f"錯誤詳情: {cancellation_details.error_details}")