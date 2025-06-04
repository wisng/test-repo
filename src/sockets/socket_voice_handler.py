import base64
import io
from sockets.socket_base_handler import BaseSocketHandler
import soundfile as sf


class VoiceSocketHandler(BaseSocketHandler):
    def __init__(self, socketio, handlers=None):
        super().__init__(socketio)
        self.handlers = handlers or []

    def register_events(self):
        @self.socketio.on('tts')
        def tts(data):
            try:
                print("Received TTS request...")

                # Process TTS request
                sample_rate, processed_audio = self.process_tts_request(
                    data['audio'],
                    data['text'],
                    speed=data.get('speed', 1.0),
                    cross_fade=data.get('cross_fade', 0.15),
                    ref_text=data.get('ref_text', "")
                )

                output_buffer = io.BytesIO()
                sf.write(output_buffer, processed_audio, sample_rate, format='WAV')
                audio_bytes = output_buffer.getvalue()
                base64_audio_bytes = base64.b64encode(audio_bytes).decode('utf-8')
                angular_client = self.get_client("angular")
                if angular_client:
                    self.socketio.emit('tts', {"audio": base64_audio_bytes})
                else:
                    print("Angular client not found")

            except Exception as e:
                return
