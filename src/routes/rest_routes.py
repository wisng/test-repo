from flask import Blueprint, request, jsonify
import io
import soundfile as sf
from src.dto.tts_request_dto import TTSRequest
from src.dto.models import ErrorResponse
from src.services.tts_service import tts_service
from src.validation import validate_data
import base64

api = Blueprint('api', __name__)


@api.route('/tts', methods=['POST'])
def text_to_speech():
    try:
        print("Received TTS request...")
        data = request.get_json()
        request_dto, errors = validate_data(data, TTSRequest)
        if errors:
            print("Invalid request data:", errors)
            return jsonify({}), 400
        print("Validated request data")

        # Process TTS request
        sample_rate, processed_audio = tts_service.process_audio(
            request_dto.reference_path,
            request_dto.text,
            speed=request_dto.speed,
            cross_fade=request_dto.cross_fade,
            ref_text=request_dto.transcript
        )

        output_buffer = io.BytesIO()
        sf.write(output_buffer, processed_audio, sample_rate, format='WAV')
        audio_bytes = output_buffer.getvalue()
        base64_audio_bytes = base64.b64encode(audio_bytes).decode('utf-8')
        return {"audio": base64_audio_bytes}

    except Exception as e:
        return ErrorResponse(error=str(e)).model_dump_json(), 500
