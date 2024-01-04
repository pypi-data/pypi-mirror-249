
from pyannote.audio import Pipeline
import time
import os


def get_annote_result(audio_f):
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1",
        use_auth_token="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",
    )
    # pipeline.to(torch.device("cuda"))
    folder = audio_f

    hparams = pipeline.parameters(instantiated=True)
    print(hparams)
    hparams["clustering"]["threshold"] -= 0.14
    hparams["segmentation"]["min_duration_off"] += 0.22
    pipeline.instantiate(hparams)
    print(hparams)

    t0 = time.time()
    name = os.path.basename(folder).split(".")[0]
    diarization = pipeline(folder, min_speakers=2, max_speakers=4)

    # diarization = pipeline(audio_f, num_speakers=2)
    t1 = time.time()
    print(f"time cost: {t1 - t0}")
    #  print the result
    speakers = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
        speaker_dict = {}
        speaker_dict["start"] = turn.start
        speaker_dict["end"] = turn.end
        speaker_dict["speaker"] = speaker
        speaker_dict["unit_len"] = turn.end - turn.start
        speakers.append(speaker_dict)
    # a list, contains very speaker info
    return speakers