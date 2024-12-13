import requests
from pathlib import Path
from tqdm import tqdm
import os

def download_whisper_model(model_size="base", cache_dir=None):
    """
    Download Whisper model files without loading the model.
    
    model_size options: tiny, base, small, medium, large, large-v2, large-v3
    """
    # Model size to download URL and expected size (in bytes) mapping
    models = {
        "tiny": ("https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.pt", 151550711),
        "base": ("https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt", 290239887),
        "small": ("https://openaipublic.azureedge.net/main/whisper/models/9ecf779972d90ba49c06d968637d720dd632c55bbf19d441fb42bf17a411e794/small.pt", 493953680),
        "medium": ("https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt", 1573340160),
        "large-v1": ("https://openaipublic.azureedge.net/main/whisper/models/e4b87e7e0bf463eb8e6956e646f1e277e901512310def2c24bf0e11bd3c28e9a/large-v1.pt", 2952538531),
        "large-v2": ("https://openaipublic.azureedge.net/main/whisper/models/81f7c96c852ee8fc832187b0132e569d6c3065a3252ed18e56effd0b6a73e524/large-v2.pt", 2952538531),
        "large-v3": ("https://openaipublic.azureedge.net/main/whisper/models/e5b1a55b89c1367dacf97e3e19bfd829a01529dbfdebc2c32af0889790a2a5a5/large-v3.pt", 2952538531)
    }
    
    if model_size not in models:
        raise ValueError(f"Model size must be one of: {', '.join(models.keys())}")
    
    # Set default cache directory if none provided
    if cache_dir is None:
        cache_dir = os.path.join(os.path.expanduser("~"), ".cache", "whisper")
    
    # Create cache directory if it doesn't exist
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    model_url, expected_size = models[model_size]
    model_path = cache_dir / f"whisper-{model_size}.pt"
    
    # Check if model already exists and has correct size
    if model_path.exists() and model_path.stat().st_size == expected_size:
        print(f"Model {model_size} already downloaded at {model_path}")
        return model_path
    
    # Download the model
    print(f"Downloading Whisper {model_size} model...")
    response = requests.get(model_url, stream=True)
    response.raise_for_status()
    
    # Get total size for progress bar
    total_size = int(response.headers.get('content-length', 0))
    
    # Download with progress bar
    with open(model_path, 'wb') as f, tqdm(
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as pbar:
        for data in response.iter_content(chunk_size=8192):
            size = f.write(data)
            pbar.update(size)
    
    # # Verify downloaded size
    # if model_path.stat().st_size != expected_size:
    #     model_path.unlink()  # Delete incomplete download
    #     raise RuntimeError(f"Downloaded model size doesn't match expected size")
    
    print(f"Successfully downloaded model to {model_path}")
    return model_path

# Example usage:
if __name__ == "__main__":
    # Download base model
    model_path = download_whisper_model("base")