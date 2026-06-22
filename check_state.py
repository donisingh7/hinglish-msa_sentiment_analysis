import pandas as pd, numpy as np, os, json

print('=== DATA FILES ===')
for f, p in [('train_set', 'data/train_set.csv'), ('auto_labeled', 'data/auto_labeled.csv'), ('test_set_gold', 'data/test_set_gold.csv'), ('transcriptions_hinglish', 'data/transcriptions_hinglish.csv')]:
    if os.path.exists(p):
        print(f'{f}: {len(pd.read_csv(p))} rows')

print('\n=== FEATURES ===')
for name, path in [('text_muril', 'features/text_muril.npy'), ('audio_wav2vec2', 'features/audio_wav2vec2.npy'), ('visual_clip', 'features/visual_clip.npy')]:
    if os.path.exists(path):
        arr = np.load(path)
        print(f'{name}: {arr.shape}')

print('\n=== EXPERIMENT RESULTS ===')
for f in sorted(os.listdir('results/experiments')):
    if f.endswith('_results.json'):
        d = json.load(open(f'results/experiments/{f}'))
        m = d['test_metrics']
        print(f"{d['experiment']}: Acc2={m['acc2']} F1={m['f1']} MAE={m['mae']} Corr={m['corr']}")
