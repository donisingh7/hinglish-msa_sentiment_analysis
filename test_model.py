"""Quick sanity check — model forward pass."""
import torch
from model.mult_model import MulTHinglish, count_parameters
from model.dataset import HinglishDataset

model = MulTHinglish()
print(f"Model parameters: {count_parameters(model):,}")

batch = {
    'text'  : torch.randn(4, 768),
    'audio' : torch.randn(4, 1024),
    'visual': torch.randn(4, 512),
    'label' : torch.randn(4, 1)
}
output = model(batch['text'], batch['audio'], batch['visual'])
print(f"Output shape: {output.shape}")  # Should be torch.Size([4])
assert output.shape == torch.Size([4]), f"Expected (4,), got {output.shape}"
print("OK - Model working!")
