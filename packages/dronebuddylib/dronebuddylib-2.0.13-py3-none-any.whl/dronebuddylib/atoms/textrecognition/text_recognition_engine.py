from dronebuddylib.models.engine_configurations import EngineConfigurations
from dronebuddylib.models.enums import  TextRecognitionAlgorithm


class TextRecognitionEngine:
    """
    The TextRecognitionEngine class handles text recognition operations.
    """
    def __init__(self, algorithm: TextRecognitionAlgorithm, config: EngineConfigurations):
        """
        Initialize the TextRecognitionEngine class.

        Args:
            algorithm (TextRecognitionAlgorithm): The algorithm to be used for text recognition.
            config (EngineConfigurations): The configurations for the engine.
        """
        self.text_recognition_model = algorithm

        if algorithm == TextRecognitionAlgorithm.GOOGLE_VISION:
            from dronebuddylib.atoms.textrecognition.google_text_recognition_impl import GoogleTextRecognitionImpl
            self.text_recognition_engine = GoogleTextRecognitionImpl(config)
        else:
            # Optionally handle other algorithms if you have any.
            raise ValueError("Unsupported face recognition algorithm")

    def recognize_text(self, image):
        """
        Recognize faces in an image.

        Args:
            image: The image containing faces to be recognized.

        Returns:
            A list of recognized faces.
        """
        return self.text_recognition_engine.recognize_text(image)

