# my_ai_services_sdk/my_ai_services_sdk/gemini_client.py
import os
import google.generativeai as genai

# 將模型名稱變成一個可以輕鬆修改的常數
DEFAULT_MODEL = 'gemini-2.5-flash-lite' # 你提到的 Gemini 1.5 Flash

# --- 核心的、通用的函式 ---
def generate_content(prompt, model_name=DEFAULT_MODEL):
    """
    最通用的 Gemini 內容生成函式。

    Args:
        prompt (str): 你想傳給 Gemini 的完整提示。
        model_name (str, optional): 要使用的模型名稱。預設為 'gemini-1.5-flash-latest'。

    Returns:
        str: Gemini 生成的內容，或在失敗時返回 None。
    """
    try:
        api_key = os.environ["GEMINI_API_KEY"]
    except KeyError:
        print("錯誤：請設定 GEMINI_API_KEY 環境變數")
        return None
    
    genai.configure(api_key=api_key)
    
    try:
        #print(f"正在使用模型 '{model_name}' 呼叫 Gemini API...")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(prompt)
        print("Gemini API 呼叫成功。")
        return response.text
    except Exception as e:
        print(f"Gemini API 呼叫失敗: {e}")
        return None

# --- 方便使用的快捷函式 (基於通用函式) ---
def translate_text(text, source_lang="中文", target_lang="日文"):
    """
    一個方便的翻譯快捷函式，它內部呼叫通用的 generate_content。
    """
    # 在這裡動態組合 prompt
    prompt = f"你是一個專業的即時翻譯官。請將以下的'{source_lang}'句子翻譯成流利且自然的'{target_lang}'。只需要回傳翻譯後的結果，不要有任何額外的解釋。\n\n原文：{text}\n\n翻譯："
    
    return generate_content(prompt)