from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import os

pipeline_ms = pipeline(
    task=Tasks.auto_speech_recognition,
    model="damo/speech_paraformer-large-vad-punc-spk_asr_nat-zh-cn",
    model_revision="v0.0.2",
    vad_model="damo/speech_fsmn_vad_zh-cn-16k-common-pytorch",
    punc_model="damo/punc_ct-transformer_cn-en-common-vocab471067-large",
    output_dir="results",
)


def get_result_ms(audio_f):
    result_dir = os.path.dirname(audio_f)
    rec_result = pipeline_ms(
        audio_in=audio_f,
        batch_size_token=5000,
        batch_size_token_threshold_s=40,
        max_single_segment_time=6000,
    )
    # convert rec result to desired format.
    speakers = []
    for a in rec_result["sentences"]:
        speaker = {}
        speaker["start"] = a["start"] / 1000
        speaker["end"] = a["end"] / 1000
        speaker["text"] = a["text"]
        speaker["speaker"] = a["spk"]
        speaker["unit_len"] = a["end"] - a["start"]
        speakers.append(speaker)
    return speakers
