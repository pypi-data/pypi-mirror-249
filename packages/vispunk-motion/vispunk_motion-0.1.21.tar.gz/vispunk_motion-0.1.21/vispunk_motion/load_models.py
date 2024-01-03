from utils.face_detector import FaceDetector
from utils.face_fixer import FaceFixer
from utils.face_parser import FaceParser

FaceFixer(
    FaceDetector("cpu"),
    FaceParser("cpu"),
    None,
)
