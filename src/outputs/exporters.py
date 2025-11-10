thonimport json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONExporter:
    def __init__(self, output_file: str):
        self.output_file = output_file

    def export(self, data):
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info(f"Data exported successfully to {self.output_file}")
        except Exception as e:
            logger.error(f"Failed to export data: {e}")