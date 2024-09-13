from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess



def process_audio(audio_file_path):
    model_dir = "SenseVoice"
    model = AutoModel(
        model=model_dir,
        vad_model="fsmn-vad",
        vad_kwargs={"max_single_segment_time": 30000},
        device="cuda:0",
        hub="hf",
        disable_update=True,
    )

    res = model.generate(
        input=audio_file_path,
        cache={},
        language="auto",
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    return text