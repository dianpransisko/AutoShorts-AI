import obsws_python as obs

class OBSManager:
    def __init__(self):
        self.client = None

    def connect(self, host, port, pwd):
        # Digunakan untuk validasi di awal dan koneksi rutin
        self.client = obs.ReqClient(host=host, port=int(port), password=pwd, timeout=3)
        return self.client.get_version()

    def start_clip(self):
        """Menyuruh OBS mulai merekam"""
        if self.client:
            self.client.start_record()
            return "RECORDING..."

    def stop_clip(self):
        """Menyuruh OBS berhenti merekam"""
        if self.client:
            self.client.stop_record()
            return "SAVED"