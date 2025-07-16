import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import time

# --- 1. 전역 설정 및 모델 로드 ---
# Whisper 모델 로드 (small 또는 base 모델 권장, 처음 실행 시 다운로드될 수 있음)
# 더 큰 모델은 더 정확하지만, 더 많은 메모리와 시간이 필요합니다.
print("Whisper 모델 로딩 중... (처음 실행 시 시간이 걸릴 수 있습니다.)")
try:
    # 'base' 모델을 사용하거나 필요에 따라 'small'로 변경
    whisper_model = whisper.load_model("base") 
    print("Whisper 모델 로드 완료.")
except Exception as e:
    print(f"Whisper 모델 로드 실패: {e}")
    print("pip install openai-whisper 명령어를 다시 확인하고 인터넷 연결을 확인해주세요.")
    exit()

# pyttsx3 엔진 초기화 (음성 합성)
engine = pyttsx3.init()
# 음성 속도 설정 (조절 가능)
engine.setProperty('rate', 150) 
# 볼륨 설정 (조절 가능)
engine.setProperty('volume', 1.0) 

# --- 2. 핵심 함수 정의 ---

def record_audio(duration=5, samplerate=16000):
    """
    사용자 음성을 지정된 시간(초) 동안 녹음합니다.
    Args:
        duration (int): 녹음할 시간 (초).
        samplerate (int): 샘플링 레이트 (Hz). Whisper 모델에 권장되는 값.
    Returns:
        numpy.ndarray: 녹음된 오디오 데이터.
    """
    print(f"\n🎙️ 말하기 시작하세요! ({duration}초 녹음)")
    try:
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
        sd.wait()  # 녹음이 완료될 때까지 기다립니다.
        print("✅ 녹음 완료.")
        return audio_data
    except Exception as e:
        print(f"오디오 녹음 중 오류 발생: {e}")
        return None

def speech_to_text(audio_data):
    """
    녹음된 오디오 데이터를 Whisper 모델을 사용하여 텍스트로 변환합니다.
    Args:
        audio_data (numpy.ndarray): 녹음된 오디오 데이터.
    Returns:
        str: 변환된 텍스트.
    """
    if audio_data is None:
        return ""
    
    # Whisper 모델은 특정 오디오 포맷을 선호합니다.
    # float32 타입을 사용하여 처리합니다.
    audio = audio_data.flatten()
    
    print("✨ 음성을 텍스트로 변환 중...")
    try:
        # Whisper는 NumPy 배열을 직접 처리할 수 있습니다.
        result = whisper_model.transcribe(audio, fp16=False) # fp16=False는 GPU가 없는 경우 안정적입니다.
        transcribed_text = result["text"]
        print(f"📝 인식된 텍스트: \"{transcribed_text}\"")
        return transcribed_text
    except Exception as e:
        print(f"음성 텍스트 변환 중 오류 발생: {e}")
        return "음성 인식에 실패했습니다."

def text_to_speech(text):
    """
    텍스트를 음성으로 변환하여 재생합니다.
    Args:
        text (str): 음성으로 변환할 텍스트.
    """
    if not text.strip():
        print("💬 재생할 텍스트가 없습니다.")
        return
        
    print(f"🔊 텍스트를 음성으로 재생 중: \"{text}\"")
    try:
        engine.say(text)
        engine.runAndWait()
        print("🎶 재생 완료.")
    except Exception as e:
        print(f"음성 재생 중 오류 발생: {e}")

# --- 3. 앱 메인 루프 (초간단 UI 시뮬레이션) ---

def run_easy_korean_chat():
    """
    '쉬운 한글+음성 채팅' 앱의 메인 루프를 실행합니다.
    """
    print("--- 📱 쉬운 한글+음성 채팅 앱 시작 ---")
    print("1. '말하기 시작' (음성 입력) 버튼")
    print("2. '메시지 재생' (받은 메시지 음성 듣기) 버튼")
    print("3. '종료' 버튼")
    print("-------------------------------------")

    received_message = "" # 받은 메시지를 저장할 변수 (시뮬레이션)

    while True:
        print("\n--- 앱 메뉴 ---")
        print("[1] 말하기 시작 (음성 입력)")
        print("[2] 메시지 재생 (현재 받은 메시지: \"{}\")".format(received_message if received_message else "없음"))
        print("[3] 종료")
        
        choice = input("👉 원하시는 기능을 선택하세요 (1, 2, 3): ").strip()

        if choice == '1':
            print("\n--- 말하기 시작 ---")
            audio = record_audio(duration=5) # 5초 동안 녹음
            if audio is not None:
                transcribed_text = speech_to_text(audio)
                if transcribed_text:
                    print(f"\n🗣️ 방금 보낼 메시지: \"{transcribed_text}\"")
                    # 여기서 실제로는 메시지를 상대방에게 전송하는 로직이 들어갑니다.
                    # 여기서는 사용자에게 보낼 메시지임을 알리고, '상대방이 이 메시지를 받았다고 가정'합니다.
                    # 다음 시나리오를 위해 받은 메시지로 가정합니다.
                    received_message = f"상대방이 보낸 메시지: \"{transcribed_text}\"" 
                    print("➡️ 메시지를 성공적으로 보냈습니다. (가상)")

        elif choice == '2':
            print("\n--- 메시지 재생 ---")
            if received_message:
                text_to_speech(received_message)
            else:
                print("⚠️ 아직 받은 메시지가 없습니다.")

        elif choice == '3':
            print("\n👋 앱을 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 1, 2, 3 중 하나를 입력해주세요.")

# --- 앱 실행 ---
if __name__ == "__main__":
    run_easy_korean_chat()