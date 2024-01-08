
import subprocess
from ptrack.urlDeconstruct import get_urls
from ptrack.methods import CustomFileSizeColumn, format_file_size
import ptrack
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, Task, DownloadColumn, TimeElapsedColumn, FileSizeColumn
from rich.console import Console
import threading
import time
import os

console = Console()

def run_ffmpeg(ffmpeg_command):
    with subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        while True:
            line = process.stderr.readline()
            if not line:
                break

def get_file_size(filename):
    return os.path.getsize(filename) if os.path.exists(filename) else 0


#def FileSizeColumn(file):
#    global file_size
#    file_size = get_file_size(file) if os.path.exists(file) else 0
#
#    return f"[bold green]{format_file_size(file_size)}[/bold green]"


def download_with_progress(ffmpeg_command, title, size, accuracy, progress, wipe):
    output_file = ffmpeg_command[-1]
    downloaded_size = format_file_size(get_file_size(output_file))
    total_size = format_file_size(size)

    if not accuracy:
        title = f"[bold purple]- [/bold purple]⚠  [#ea2a6f]Filesize may be inaccurate[/#ea2a6f][bold purple] - [/bold purple][bold yellow]{title}[/bold yellow]"
    else:
        title = f"[bold purple]- [/bold purple][bold yellow]{title}[/bold yellow]"

    ffmpeg_command.extend(['-flush_packets', '1'])

    custom_columns = [
        BarColumn(bar_width=50),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        "[#ea2a6f][[/#ea2a6f]",
        FileSizeColumn(),
        "[#ea2a6f]/[/#ea2a6f]",
        TextColumn(f"[bold cyan]{total_size}[/bold cyan]"),
        "[#ea2a6f]][/#ea2a6f]",
        TextColumn(title, justify="left"),
    ]

    progress.stop()
    wipe()

    with Progress(*custom_columns) as progress:
        task = progress.add_task("", total=size, downloaded_size=format_file_size(get_file_size(output_file)))
        process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                progress.update(task, completed=get_file_size(output_file))

            time.sleep(0.3)

        if process.returncode == 0:
            progress.columns = list(progress.columns)
            progress.columns[-1].renderable = TextColumn(f"[bold yellow]{title}i[/bold yellow][bold green] ✓[/bold green]")
            progress.columns = tuple(progress.columns)
        else:
            progress.columns = list(progress.columns)
            progress.columns[-1].renderable = TextColumn(f"[bold yellow]{title}[/bold yellow][bold red] ✗[/bold red]")
            progress.columns = tuple(progress.columns)



        progress.stop()


def mediaDownload(url, progress, wipe):

    fetched_urls = get_urls([url])

    print()

    for fetched_url in fetched_urls:
        if fetched_url:
            video_url, audio_url, title, size, accuracy = fetched_url
            safe_name = make_filename_safe(title)
            ffmpeg_command = [
                'ffmpeg', '-i', video_url, '-i', audio_url,
                '-c:v', 'libx264', '-c:a', 'aac', '-strict', 'experimental',
                '-b:v', '1M', '-b:a', '128k', f'{safe_name}.mp4'
            ] if video_url.endswith('.m3u8') else [
                'ffmpeg', '-i', video_url, '-i', audio_url,
                '-c:v', 'copy', '-c:a', 'copy', f'{safe_name}.mp4'
            ]

            download_with_progress(ffmpeg_command, title, size, accuracy, progress, wipe)
        else:
            print("Error: Unable to fetch URLs for one of the videos.")



def make_filename_safe(name):
    return name.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')

