from PyQt6.QtCore import *
import subprocess
from packagevalues import vidoe_settings, auido_settings
import time

class FileFormatView(QThread):
    log_text = pyqtSignal(str)
    finished = pyqtSignal(bool)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
    
    def run(self):
        self.result = subprocess.Popen(
            ["yt-dlp","-F",f"{self.url}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in self.result.stdout:
            clean_line = line.strip()
            if clean_line:
                self.log_text.emit(clean_line)
        
        self.result.wait()
        self.finished.emit(True)
        
class DownloadWideo(QThread):
    log_text = pyqtSignal(str)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, conf: vidoe_settings):
        super().__init__()
        
        #None Values
        self.result = None
        self.video_quality_arg = None
        self.output_template = None
        self.resulttxt = None
        self.header = None
        
        #Conf Values
        self.video_url = conf.video_url
        self.file_path = conf.file_path
        self.file_name = conf.file_name
        self.video_quality = conf.video_quality
        self.video_format = conf.video_format
        
        self.is_killed = False
        
        if conf.file_name:
            self.output_template = f"{self.file_path}/{self.file_name}.%(ext)s" 
        else:
            self.output_template = f"{self.file_path}/%(title)s.%(ext)s"
            
        if self.video_quality == "The Bes" or self.video_quality is None:
            self.video_quality_arg = "bestvideo+bestaudio/best"
        else:
            self.video_quality_arg = f"bestvideo[height={conf.video_quality}]+bestaudio/best"
        
        self.command = [
            "yt-dlp",
            "-f", self.video_quality_arg,
            "--remux-video", f"{self.video_format}",
            "-o", self.output_template,
            f"{self.video_url}"
        ]
        
    def run(self):
        try:
            self.is_killed = False
            if self.video_url[-4:] == ".txt":
                return self.run_txt()
            
            self.result = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in self.result.stdout:
                clean_line = line.strip()
                if clean_line:
                    self.log_text.emit(clean_line)
            
            return_code = self.result.poll()
            
            if return_code == 0:
                self.log_text.emit("\nDownload completed successfully.")
            elif self.is_killed:
                self.log_text.emit("\nThe download was canceled by User")
            
            self.result.wait()
            self.finished.emit(True)
        except Exception as e:
            self.error.emit(f"ERROR\n{e}")
            raise e
    
    def stop(self):
        if self.result and self.result.poll() is None:
            self.is_killed = True      
            self.result.kill()
        if self.resulttxt and self.resulttxt.poll() is None:
            self.is_killed = True
            self.resulttxt.kill()
    
    def run_txt(self):
        try:
            with open(f"{self.video_url}","r",encoding="utf-8") as f:
                urls = f.readlines()
            
            count = len(urls)
            for i, url in enumerate(urls):
                self.command = [
                    "yt-dlp",
                    "-f", self.video_quality_arg,
                    "--remux-video", f"{self.video_format}",
                    "-o", self.output_template,
                    f"{url}"
                ]
                self.resulttxt = subprocess.Popen(
                    self.command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                
                for line in self.resulttxt.stdout:
                    clean_line = line.strip()
                    if clean_line:
                        self.log_text.emit(clean_line)
                
                returncode = self.resulttxt.poll()
                if returncode == 0:
                    self.log_text.emit(f"\nThe Download was completed {i+1} / {count}\n")
                    time.sleep(0.8)
                elif self.is_killed:
                    self.log_text.emit("\nThe download was canceled by User\n")
                    break
                self.resulttxt.wait()
            self.finished.emit(True)
        except Exception as e:
            self.error.emit(f"ERROR\n{e}")
            raise e

class DownloadAuido(QThread):
    log_text = pyqtSignal(str)
    finished = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, conf: auido_settings):
        super().__init__()
        self.result = None
        self.is_killed = False
    
        target_audio_format = conf.auido_format 
        
        if conf.file_name:
            output_template = f"{conf.file_path}/{conf.file_name}.%(ext)s"
        else:
            output_template = f"{conf.file_path}/%(title)s.%(ext)s"

        self.command = [
            "yt-dlp",
            "-f", "bestaudio/best",            
            "-x",                               
            "--audio-format", target_audio_format,
            "-o", output_template,
            f"{conf.video_url}"              
        ]
        
    def run(self):
        try:
            self.is_killed = False
            self.result = subprocess.Popen(
                self.command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            for line in self.result.stdout:
                clean_line = line.strip()
                if clean_line:
                    self.log_text.emit(clean_line)
            
            return_code = self.result.poll()
            
            if return_code == 0:
                self.log_text.emit("\nDownload completed successfully.")
            elif self.is_killed:
                self.log_text.emit("\nThe download was canceled by User")
            
            self.result.wait()
            self.finished.emit(True)
        except Exception as e:
            self.error.emit(f"ERROR\n{e}")
            raise e
        
    def stop(self):
        if self.result and self.result.poll() is None:
            self.is_killed = True      
            self.result.kill()