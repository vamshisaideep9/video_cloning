"""Do Not Run This"""
# import os
# import logging
# from huggingface_hub import hf_hub_download
# from dotenv import load_dotenv

# load_dotenv()

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# def download_live_portrait():
#     logger.info("🚀 Starting LivePortrait ONNX weights download...")
    
#     model_dir = os.path.join(os.getcwd(), "models", "live_portrait")
#     os.makedirs(model_dir, exist_ok=True)
    
#     repo = "myn0908/Live-Portrait-ONNX" 
#     token = os.getenv("HF_TOKEN")

#     files = [
#         "appearance_feature_extractor.onnx",
#         "motion_extractor.onnx",
#         "spade_generator.onnx",
#         "warping.onnx", 
#         "landmark.onnx",
#         "2d106det.onnx" # Required for face detection/alignment
#     ]

#     for f in files:
#         target_path = os.path.join(model_dir, f)
#         if not os.path.exists(target_path):
#             try:
#                 logger.info(f"Downloading {f}...")
#                 hf_hub_download(
#                     repo_id=repo, 
#                     filename=f, 
#                     local_dir=model_dir,
#                     token=token
#                 )
#                 logger.info(f"✅ Successfully downloaded {f}")
#             except Exception as e:
#                 logger.error(f"❌ Failed to download {f}: {str(e)}")
#         else:
#             logger.info(f"⏩ {f} already exists, skipping.")

# if __name__ == "__main__":
#     download_live_portrait()
""" Dont RUN Above One"""







import os
import urllib.request
from urllib.error import URLError, HTTPError

def download_file_with_fallback(primary_url, backup_url, dest_path):
    if os.path.exists(dest_path):
        print(f"⏩ {os.path.basename(dest_path)} already exists.")
        return

    print(f"Downloading {os.path.basename(dest_path)}...")
    req = urllib.request.Request(primary_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"✅ Saved to {dest_path} (from Primary URL)")
    except (HTTPError, URLError) as e:
        print(f"⚠️ Primary URL failed ({e}). Trying Backup Mirror...")
        req_backup = urllib.request.Request(backup_url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req_backup) as response, open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ Saved to {dest_path} (from Backup Mirror)")
        except Exception as backup_e:
            print(f"❌ Both servers failed. Backup error: {backup_e}")

def setup_wav2lip():
    model_dir = os.path.join(os.getcwd(), "models", "wav2lip")
    os.makedirs(model_dir, exist_ok=True)
    gan_url = "https://huggingface.co/camenduru/Wav2Lip/resolve/main/checkpoints/wav2lip_gan.pth"
    download_file_with_fallback(gan_url, gan_url, os.path.join(model_dir, "wav2lip_gan.pth"))
    s3fd_dir = os.path.join(os.getcwd(), "app", "vendor", "Wav2Lip", "face_detection", "detection", "sfd")
    os.makedirs(s3fd_dir, exist_ok=True)
    s3fd_primary = "https://www.adrianbulat.com/downloads/python-fan/s3fd-619a316812.pth"
    s3fd_backup = "https://huggingface.co/camenduru/Wav2Lip/resolve/main/checkpoints/s3fd-619a316812.pth"
    
    download_file_with_fallback(s3fd_primary, s3fd_backup, os.path.join(s3fd_dir, "s3fd.pth"))

if __name__ == "__main__":
    print("🚀 Setting up Wav2Lip weights...")
    setup_wav2lip()