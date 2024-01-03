"""Youtube and UI module."""
from tkinter import filedialog
import customtkinter
from pytube import YouTube

class YouTubeDownloader(customtkinter.CTk):
    """Class is inherit from customtkinter."""

    def __init__(self, *args, **kwargs):
        """Initilization."""
        super().__init__(*args, **kwargs)
        self.geometry("720x480")
        self.title("Simple Youtube Downloader")
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")
        self.create_widgets()

    def create_widgets(self):
        """Create customtkinter UI."""
        self.title_label = customtkinter.CTkLabel(self, text="Input video URL")
        self.title_label.pack(padx=10, pady=10)

        self.link_entry = customtkinter.CTkEntry(self, width=350, height=40)
        self.link_entry.pack()
        self.link_entry.bind('<Control-a>', self.on_select_all)

        self.finish_label = customtkinter.CTkLabel(self, text="")
        self.finish_label.pack(padx=10, pady=10)

        self.progress_label = customtkinter.CTkLabel(self, text="0%")
        self.progress_label.pack()

        self.progress_bar = customtkinter.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(padx=10, pady=10)

        self.download_button = customtkinter.CTkButton(
            self,
            text="Download video",
            command=self.start_download
        )
        self.download_button.pack(padx=10, pady=10)

    def on_select_all(self, event):
        """Enable CTRL+A in input field."""
        event.widget.select_range(0, 'end')
        event.widget.icursor('end')
        return 'break'

    def start_download(self):
        """Download video."""
        try:
            download_link = self.link_entry.get()
            yt = YouTube(download_link, on_progress_callback=self.on_progress)
            video = yt.streams.get_highest_resolution()
            self.finish_label.configure(text="")

            save_path = filedialog.askdirectory()
            if not save_path:
                self.finish_label.configure(text="Cancel downloading", text_color="red")
                return

            video.download(save_path)
            self.finish_label.configure(
                text=f"Downloaded in: {save_path}\nName: {yt.title}",
                text_color="black"
            )
        except Exception as err:
            self.finish_label.configure(
                text=f"Downloaded error: {err}",
                text_color="red"
            )

    def on_progress(self, stream, chunk, bytes_remaining):
        """Progress bar."""
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_completed = bytes_downloaded / total_size * 100
        per = str(int(percentage_completed))
        self.progress_label.configure(text=per + "%")
        self.progress_label.update()
        self.progress_bar.set(float(percentage_completed) / 100)
