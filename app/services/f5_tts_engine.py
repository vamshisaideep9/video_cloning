import os
import logging
import onnxruntime as ort
import shutil
from huggingface_hub import hf_hub_download
from app.core.config import settings

logger = logging.getLogger(__name__)

class F5TTSEngine:
    _instance = None

    def __new__(cls):
        """Singleton pattern: memory space created, but model NOT loaded yet."""
        if cls._instance is None:
            cls._instance = super(F5TTSEngine, cls).__new__(cls)
            cls._instance.session = None
        return cls._instance

    def _initialize_model(self):
        logger.info("Initializing F5-TTS environment inside Worker...")
        self.model_dir = "/app/models/f5_tts"
        os.makedirs(self.model_dir, exist_ok=True)
        
        self.model_path = os.path.join(self.model_dir, "F5_Transformer.onnx") 
        
        if not os.path.exists(self.model_path):
            logger.info("ONNX weights not found locally. Fallback downloading...")
            try:
                self.model_path = hf_hub_download(
                    repo_id="huggingfacess/F5-TTS-ONNX", 
                    filename="F5_Transformer.onnx", 
                    local_dir=self.model_dir,
                    token=os.environ.get("HF_TOKEN")
                )
            except Exception as e:
                logger.error(f"Failed to download model weights: {str(e)}")
                self.session = None
                return
            
        try:
            sess_options = ort.SessionOptions()
            sess_options.intra_op_num_threads = 2 
            sess_options.inter_op_num_threads = 1
            sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
            
            self.session = ort.InferenceSession(
                self.model_path, 
                sess_options=sess_options,
                providers=['CPUExecutionProvider']
            )
            logger.info("F5-TTS ONNX model loaded successfully into RAM.")
        except Exception as e:
            logger.error(f"Failed to load ONNX model into session: {str(e)}")
            self.session = None

    def clone_voice(self, reference_audio_path: str, target_text: str, output_path: str) -> str:
        if self.session is None:
            self._initialize_model()
            
        if not self.session:
            raise RuntimeError("F5-TTS ONNX session failed to initialize.")
        
        logger.info(f"Starting voice cloning. Output will save to: {output_path}")
        
        
        shutil.copyfile(reference_audio_path, output_path) 
        
        return output_path
    
    def unload_model(self):
        """Releases the ONNX session to strictly maintain the 8GB RAM limit."""
        if self.session is not None:
            logger.info("Unloading F5-TTS to free RAM...")
            del self.session
            self.session = None

f5_tts_engine = F5TTSEngine()