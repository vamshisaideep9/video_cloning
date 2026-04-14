import os
from huggingface_hub import hf_hub_download
from dotenv import load_dotenv 

load_dotenv() 

def download_f5_tts():
    print("Starting F5-TTS ONNX weights download...")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_dir, "models", "f5_tts")
    os.makedirs(model_dir, exist_ok=True)
    
    token = os.environ.get("HF_TOKEN")

    try:
        file_path = hf_hub_download(
            repo_id="huggingfacess/F5-TTS-ONNX", 
            filename="F5_Transformer.onnx", 
            local_dir=model_dir,
            token=token
        )
        print(f"✅ Success! Weights downloaded to: {file_path}")
    except Exception as e:
        print(f"❌ Download failed: {str(e)}")

if __name__ == "__main__":
    download_f5_tts()