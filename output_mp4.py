from moviepy.editor import concatenate_videoclips, VideoFileClip
import os


def merge_ts_files(ts_files, output_file):
    """
    合并一组 .ts 文件并保存为 .mp4 文件

    :param ts_files: 包含 .ts 文件路径的列表
    :param output_file: 合并后输出的 .mp4 文件路径
    """
    # 确保 .ts 文件按顺序排列
    ts_files.sort()

    # 加载所有 .ts 文件为 VideoFileClip 对象
    clips = []
    for ts_file in ts_files:
        if os.path.exists(ts_file):
            print(f"加载 {ts_file}")
            clip = VideoFileClip(ts_file)
            clips.append(clip)
        else:
            print(f"文件 {ts_file} 不存在")

    # 合并所有视频片段
    if clips:
        final_clip = concatenate_videoclips(clips, method="compose")
        final_clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        print(f"合并完成，输出文件为 {output_file}")
    else:
        print("没有可合并的 .ts 文件")
