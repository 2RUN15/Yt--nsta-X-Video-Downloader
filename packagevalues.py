from dataclasses import dataclass

@dataclass
class vidoe_settings:
    video_format: str
    video_quality: str
    file_path: str
    video_url: str
    file_name: str

@dataclass
class auido_settings:
    auido_format: str
    file_path: str
    video_url: str
    file_name: str