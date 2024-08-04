#!/usr/bin/python3
# coding:utf-8            
"""
 Copyright (C) 2024 - 2024 Meteor， Inc. All Rights Reserved 
 @Time    : 2024/8/4 下午4:57
 @Author  : Meteor
 @Email   : xxx130032@gmail.com
 @Website : https://0meteor0.pythonanywhere.com/
 @File    : test.py
 @IDE     : PyCharm
"""
from dowmload import download_file
from moviepy.editor import concatenate_videoclips, VideoFileClip
import os

# 下载ts
dowmload_list = ['0000.ts', '0001.ts', '0002.ts', '0003.ts', '0004.ts', '0005.ts', '0006.ts', '0007.ts', '0008.ts']
for i in dowmload_list:
    download_file(f"https://www.4k-av.com/movie/003571-your-name/720P/{i}", "./video/" + i,
                  porxy={"http": "http://117.139.124.182:9091"})


# 合并mp4
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


output_file = 'output.mp4'
input_directory = './video/'  # 替换为实际的目录路径
ts_files = [os.path.join(input_directory, filename) for filename in dowmload_list]
merge_ts_files(ts_files, output_file)
