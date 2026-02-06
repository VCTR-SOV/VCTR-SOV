import hashlib
import json
import numpy as np
from typing import List, Dict, Union
from datetime import datetime

class VCTRProtocol:
    """
    VCTR-SOV CORE LOGIC v2.1
    Standard: 975ad5a | License: Sovereign Implementation
    """
    
    # IMMUTABLE CONSTANTS
    ANCHOR_HASH: str = "975ad5a"
    LEWIS_THRESHOLD: float = 0.82
    PROTOCOL_FEE: float = 0.015  # 1.5% Hardened Constant
    GENESIS_RESERVE: str = "85p7LyG8cG7qk12s3hCwSGVq75AHgQFvrSCfFnCVmeQi"

    @staticmethod
    def _calculate_shannon_entropy(data: np.array) -> float:
        """
        LAYER 1: PHYSICS CHECK
        Computes thermodynamic entropy to verify stochastic movement.
        """
        if len(data) == 0: return 0.0
        probabilities, _ = np.histogram(data, bins=10, density=True)
        probabilities = probabilities[probabilities > 0]
        entropy = -np.sum(probabilities * np.log2(probabilities))
        return float(entropy)

    @staticmethod
    def _detect_mechanical_spoof(data: np.array, sampling_rate=100) -> tuple:
        """
        LAYER 2: ADVERSARIAL CHECK (The Paint Shaker Protocol)
        Analyzes Frequency Domain to reject mechanical actuators.
        """
        # Convert Time Domain to Frequency Domain (FFT)
        fft_vals = np.fft.rfft(data)
        
        # Calculate Power Spectral Density (PSD)
        psd = np.abs(fft_vals) ** 2
        
        # Peak Detection: Machines concentrate energy in one band.
        total_energy = np.sum(psd)
        if total_energy == 0: return True, "NO_ENERGY"
        
        peak_energy = np.max(psd)
        concentration_ratio = peak_energy / total_energy
        
        # THE LAW: If >50% of energy is in one frequency, it's a motor.
        if concentration_ratio > 0.50:
            return True, f"MECHANICAL_ARTIFACT (Ratio: {concentration_ratio:.2f})"
            
        return False, "BIOLOGICAL_SIGNATURE"

    @classmethod
    def verify_session(cls, user_uuid: str, imu_data: List[float]) -> Dict:
        """
        EXECUTION: Runs both Logic Layers to mint a session.
        """
        # Data Prep
        data_array = np.array(imu_data)
        
        # STEP 1: The Lewis Threshold (Entropy)
        entropy_score = cls._calculate_shannon_entropy(data_array)
        if entropy_score < cls.LEWIS_THRESHOLD:
            return cls._reject_session("LOW_ENTROPY", entropy_score)

        # STEP 2: The Paint Shaker Protocol (FFT)
        # We explicitly CALL the function here. Before, this was missing.
        is_mechanical, mech_reason = cls._detect_mechanical_spoof(data_array)
        if is_mechanical:
            return cls._reject_session(mech_reason, entropy_score)
        
        # STEP 3: Cryptographic Signing (Success)
        timestamp = datetime.utcnow().isoformat()
        raw_payload = f"{user_uuid}|{timestamp}|{entropy_score:.4f}|{cls.ANCHOR_HASH}"
        session_hash = hashlib.sha256(raw_payload.encode()).hexdigest()

        return {
            "status": "VERIFIED",
            "protocol": "VCTR-SOV",
            "anchor": cls.ANCHOR_HASH,
            "session_id": session_hash,
            "metrics": {
                "entropy": round(entropy_score, 4),
                "lewis_threshold": cls.LEWIS_THRESHOLD,
                "signal_type": "BIOLOGICAL"
            },
            "fee_remittance": f"{cls.PROTOCOL_FEE * 100}%"
        }

    @staticmethod
    def _reject_session(reason: str, entropy: float) -> Dict:
        return {
            "status": "REJECTED",
            "reason": reason,
            "metrics": {"entropy": round(entropy, 4)},
            "code": 403
        }

# --- TEST EXECUTION ---
if __name__ == "__main__":
    # Simulate a "Human" Wiggle
    human_data = np.random.normal(loc=0.0, scale=1.0, size=100).tolist()
    
    print("TESTING ENGINE...")
    result = VCTRProtocol.verify_session("USER_GENESIS", human_data)
    print(json.dumps(result, indent=2))
