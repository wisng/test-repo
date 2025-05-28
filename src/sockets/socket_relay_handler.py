import base64
import io
from flask_socketio import emit
import soundfile as sf
from src.dto.models import AudioChunkResponse, AudioStreamRequest, ErrorResponse
from src.services import tts_service


class SocketRelayHandler:
    def __init__(self, socketio):
        self.socketio = socketio

    def initialize_handlers(self):
        @self.socketio.on('connect')
        def handle_connect():
            print('Client connected')

        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('Client disconnected')

        @self.socketio.on('audio_stream_request')
        def handle_stream_text(data):
            try:
                print(f'Received audio stream request: {data}')
                request_data = AudioStreamRequest.model_validate(data)

                if request_data.text == "":
                    print("Empty data received")
                    response = AudioChunkResponse(
                        audio=None,
                        text=request_data.text,
                        EOT=request_data.EOT
                    ).model_dump()
                    emit('audio_response', response)
                    print('Empty data response sent successfully')
                    return

                # Process TTS request
                print(f'Processing TTS request for text: {request_data.text}')
                sample_rate, audio_wave = tts_service.tts_service.process_audio(
                    request_data.reference_path,
                    request_data.text,
                    ref_text=request_data.transcript
                )
                print("Audio stream processed successfully")

                # Convert audio to bytes
                output = io.BytesIO()
                sf.write(output, audio_wave, sample_rate, format='WAV')
                audio_bytes = output.getvalue()

                # Send response back to the requesting client
                response = AudioChunkResponse(
                    audio=base64.b64encode(audio_bytes).decode('utf-8'),
                    text=request_data.text,
                    EOT=request_data.EOT
                ).model_dump()

                emit('audio_response', response)
                print(f'Audio stream sent back to client')

            except Exception as e:
                print(f'Error in handle_stream_text: {str(e)}')
                emit('error', ErrorResponse(error=str(e)).model_dump())
