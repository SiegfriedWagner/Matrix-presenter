try:
    import imageio.core.fetching
except ModuleNotFoundError:
    import pip._internal as pip
    pip.main(['install', "imageio"])
    import imageio.core.fetching
import os
try:
    import moviepy
except ModuleNotFoundError:
    import pip._internal as pip
    pip.main(['install', "moviepy"])

try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
except imageio.core.fetching.NeedDownloadError:
    imageio.plugins.ffmpeg.download()
finally:
    from moviepy.video.io.VideoFileClip import VideoFileClip
length = 2 # seconds
resources_dir = os.path.join(os.path.dirname(__file__))
input_video_path = os.path.join(resources_dir, 'test.mp4')
os.makedirs(os.path.join(resources_dir, 'videos'), exist_ok=True)
with VideoFileClip(input_video_path) as video:
    for i in range(1,10):
        new = video.subclip(i*length, (i+1)*length)
        new.write_videofile(os.path.join(resources_dir, "videos", str(i).zfill(3) + ".mp4"), codec='mpeg4')
