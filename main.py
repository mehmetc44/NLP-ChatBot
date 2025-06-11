from src.gui.home import UI
from src.tts import TextToSpeech as tts

if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()  # İsteğe bağlı ama önerilir
    ui = UI()
    ui.run()



