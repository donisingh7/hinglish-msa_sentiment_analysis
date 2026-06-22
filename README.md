# HinglishMSA

**The first multimodal sentiment analysis dataset and framework for Hindi-English (Hinglish) code-mixed speech.**

M.Tech Dissertation — Piyush Rahangdale (P24IS020)  
SVNIT Surat | Supervisor: Dr. Dhiren R. Patel | June 2026

---

## Overview

HinglishMSA addresses a critical gap in affective computing: no multimodal sentiment dataset existed for Hinglish, despite it being spoken by 600+ million people. This repository contains:

- **HinglishMSA Dataset** — 2,652 YouTube video clips with aligned text, audio, and visual modalities and continuous sentiment scores in [-3, +3]
- **MulTHinglish Model** — a 5.28M-parameter directional cross-modal attention transformer achieving 70% binary accuracy
- **Complete Pipeline** — scripts for data collection, transcription, Hinglish detection, LLM annotation, and feature extraction

---

## Results

| Configuration | Acc-2 ↑ | F1 ↑ | MAE ↓ | Corr ↑ |
|---|---|---|---|---|
| E1 — Baseline | 0.647 | 0.649 | 1.227 | 0.390 |
| E2 — Standard Training | 0.667 | 0.669 | 1.172 | 0.452 |
| **E3 — Proposed (Full)** | **0.700** | **0.702** | **1.100** | 0.479 |
| E4 — Text-Only Ablation | 0.413 | 0.242 | 1.301 | 0.274 |
| E5 — High-Confidence Labels | 0.720 | 0.721 | 1.099 | **0.546** |
| CMU-MOSI (English reference) | 0.797 | 0.797 | 0.887 | 0.706 |

> **Key finding:** Text-only model collapses to 41.3% accuracy. Adding audio + visual gives a 28.7 pp gain — Hinglish sentiment is carried in prosody and facial expression, not just words.

---

## Dataset

| Stat | Value |
|---|---|
| Total annotated clips | 2,652 |
| Source YouTube videos | 1,174 |
| Sentiment score range | [-3.0, +3.0] |
| Training set | 2,251 clips |
| Test set (human-verified) | 150 clips |

**Download on Kaggle:** [donisinghagrawal07/hinglishmsa-audio-clips](https://www.kaggle.com/datasets/donisinghagrawal07/hinglishmsa-audio-clips)

---

## Repository Structure

```
hinglish-msa/
├── features/                    # Pre-extracted NumPy feature arrays
│   ├── clip_ids.npy             #   (2652,)    ordered clip IDs
│   ├── text_muril.npy           #   (2652, 768)  MuRIL [CLS] embeddings
│   ├── audio_wav2vec2.npy       #   (2652, 1024) wav2vec2-XLSR embeddings
│   └── visual_clip.npy          #   (2652, 512)  CLIP ViT-B/32 embeddings
├── data/
│   ├── auto_labeled.csv         # Full annotations (2652 clips)
│   ├── train_set.csv            # Training split
│   ├── test_set_gold.csv        # Human-verified test set
│   └── clips/                   # 2652 WAV audio clips (16kHz mono)
├── scripts/                     # Data collection and processing scripts
│   ├── collect_videos.py
│   ├── download_audio.py
│   ├── segment_audio.py
│   ├── face_detection.py
│   ├── transcribe_whisper.py
│   ├── hinglish_detection.py
│   ├── annotate_groq.py
│   └── extract_features.py
├── model/                       # MulTHinglish model checkpoints
├── results/                     # Experiment result JSONs
├── Thesis_Report/               # LaTeX source for M.Tech dissertation
└── check_state.py               # Dataset integrity checker
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install torch transformers numpy pandas scikit-learn
```

### 2. Load features and train a baseline

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import accuracy_score

# Load features
clip_ids     = np.load("features/clip_ids.npy", allow_pickle=True)
text_feats   = np.load("features/text_muril.npy")      # (2652, 768)
audio_feats  = np.load("features/audio_wav2vec2.npy")  # (2652, 1024)
visual_feats = np.load("features/visual_clip.npy")     # (2652, 512)

# Load splits
train_df = pd.read_csv("data/train_set.csv")
test_df  = pd.read_csv("data/test_set_gold.csv")
id2idx   = {cid: i for i, cid in enumerate(clip_ids)}

def get_indices(df):
    return [id2idx[c] for c in df['clip_id'] if c in id2idx]

tr_idx, te_idx = get_indices(train_df), get_indices(test_df)

# Concatenate all modalities
X_train = np.concatenate([text_feats[tr_idx], audio_feats[tr_idx], visual_feats[tr_idx]], axis=1)
X_test  = np.concatenate([text_feats[te_idx], audio_feats[te_idx], visual_feats[te_idx]], axis=1)
y_train = train_df['score'].values
y_test  = test_df['score'].values

# Ridge regression baseline
model = Ridge(alpha=1.0).fit(X_train, y_train)
preds = model.predict(X_test)

acc2 = accuracy_score((y_test > 0), (preds > 0))
mae  = np.mean(np.abs(y_test - preds))
print(f"Acc-2: {acc2:.4f}  MAE: {mae:.4f}")
```

### 3. Train MulTHinglish (full model)

```bash
# Coming soon: training script
python scripts/train_multhilnglish.py --modalities text audio visual --epochs 100
```

---

## Pipeline Architecture

```
YouTube API (25 search queries, 8 domains)
        │ 1,174 videos
        ▼
pytubefix + ffmpeg
  → 16kHz WAV audio + 5 JPEG frames per video
        │ 50,695 clips after silence segmentation (3-15s)
        ▼
OpenCV Haar Cascade face detection
        │ 43,146 face-present clips (85.3%)
        ▼
faster-whisper large-v3 (CUDA float16)
        │ 29,500 transcriptions
        ▼
3-stage Hinglish detection
  Stage 1: Devanagari + Latin co-occurrence
  Stage 2: Loanword lexicon match
  Stage 3: langdetect dual-language probability (p_hi > 0.1 AND p_en > 0.1)
        │ 6,740 Hinglish clips (22.8%) — 6.6× over naive ASR label
        ▼
Groq API llama-3.1-8b-instant annotation
  Prompt: rate sentiment -3 to +3 (single number)
  Confidence filter: |s| ≥ 0.5 retained
        │ 2,652 usable annotations
        ▼
Feature extraction (offline, GPU)
  Text:   MuRIL-base [CLS] → 768-dim   (~15 min)
  Audio:  wav2vec2-XLSR-53 mean-pool → 1024-dim  (~40 min)
  Visual: CLIP ViT-B/32 5-frame mean-pool → 512-dim  (~20 min)
        │ features/*.npy
        ▼
MulTHinglish training
  6 cross-modal attention streams × 4 layers
  Regression head: 768 → 256 → 128 → 1
  Adam lr=1e-3, MSE loss, early stopping
        │ 70.0% Acc-2 / F1=0.702
```

---

## Model: MulTHinglish

Extends MulT ([Tsai et al., 2019](https://arxiv.org/abs/1906.00295)) with cross-lingual encoders for Hinglish.

| Component | Detail |
|---|---|
| Text encoder | MuRIL-base-cased (Google) — 17 Indian languages |
| Audio encoder | wav2vec2-large-xlsr-53 (Facebook) — 53 languages |
| Visual encoder | CLIP ViT-B/32 (OpenAI) |
| Fusion | 6 directional cross-modal attention streams |
| d_model | 128 |
| Attention heads | 8 |
| CMT layers per stream | 4 |
| Total parameters | 5,283,713 |
| Training hardware | NVIDIA RTX 4050 (6.4 GB VRAM) |

---

## How to Use for Further Research

### Re-extract features with a different encoder

```python
from transformers import AutoTokenizer, AutoModel
import torch, numpy as np, pandas as pd

df = pd.read_csv("data/auto_labeled.csv")
tokenizer = AutoTokenizer.from_pretrained("your/model")
model = AutoModel.from_pretrained("your/model").cuda().eval()

feats = []
with torch.no_grad():
    for text in df['text']:
        inp = tokenizer(text, return_tensors="pt", truncation=True, max_length=128).to("cuda")
        out = model(**inp).last_hidden_state[:, 0, :]  # [CLS]
        feats.append(out.cpu().numpy())

np.save("features/text_your_encoder.npy", np.vstack(feats))
```

### Add a new modality

The `clip_ids.npy` file is the alignment key. Extract any new features for each clip ID in that order and save as `features/your_modality.npy` with shape `(2652, dim)`.

### Reproduce experiments

```python
# All results in results/ as JSON
import json, glob
for f in glob.glob("results/*.json"):
    r = json.load(open(f))
    print(f, r)
```

---

## Limitations and Future Work

- **Annotation:** Single LLM annotator; future work should add human IAA measurement (Krippendorff's α)
- **Visual alignment:** Frames from full video, not utterance timestamps — utterance-aligned extraction would improve visual correlation
- **Scale:** 43,146 more face-detected clips remain unannotated — pipeline can be rerun at scale
- **Encoder fine-tuning:** All encoders frozen during MulTHinglish training; end-to-end fine-tuning is a clear next step
- **ASR quality:** Whisper large-v3 not designed for code-mixed speech; a Hinglish-specific ASR model would reduce noise

---

## Citation

```bibtex
@mastersthesis{rahangdale2026hinglishmsa,
  author  = {Piyush Rahangdale},
  title   = {{HinglishMSA}: A Multimodal Sentiment Analysis Dataset and
             Framework for Hindi-English Code-Mixed Speech},
  school  = {Sardar Vallabhbhai National Institute of Technology, Surat},
  year    = {2026},
  type    = {M.Tech. Dissertation}
}
```

---

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — Free to use, share, and adapt with attribution.
