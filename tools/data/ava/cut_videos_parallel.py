# Copyright (c) OpenMMLab. All rights reserved.
import argparse
import os.path as osp
import subprocess

import mmengine
from joblib import Parallel, delayed
import os


def cut_video(video_url, output_dir, num_attempts=5):
    video_file = osp.basename(video_url)
    output_file = osp.join(output_dir, video_file)

    status = False

    if not osp.exists(output_file):
        command = ['ffmpeg', '-ss', '900', 
                             '-t', '901', 
                             '-i', video_url, 
                             '-r', '30', 
                             '-strict', 'experimental', 
                             output_file]
        command = ' '.join(command)
        # print(command)
        attempts = 0
        while True:
            try:
                subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                attempts += 1
                if attempts == num_attempts:
                    return status, 'Cutting Failed'
            else:
                break

    status = osp.exists(output_file)
    return status, 'Cut'


def main(source_file, output_dir, num_jobs=24, num_attempts=5):
    mmengine.mkdir_or_exist(output_dir)
    video_list = [os.path.join(source_file, x) for x in os.listdir(source_file) if os.path.isfile(os.path.join(source_file, x))]

    if num_jobs == 1:
        status_list = []
        for video in video_list:
            video_list.append(cut_video(video, output_dir, num_attempts))
    else:
        status_list = Parallel(n_jobs=num_jobs, verbose=10)(
            delayed(cut_video)(video, output_dir, num_attempts)
            for video in video_list)

    mmengine.dump(status_list, 'cut_report.json')


if __name__ == '__main__':
    description = 'Helper script for cutting AVA videos'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-s', '--source_file', type=str, help='TXT file containing the video filename', default="../../../data/ava/videos")
    parser.add_argument(
        '-o', '--output_dir',
        type=str,
        help='Output directory where videos will be saved', default="../../../data/ava/videos_15min")
    parser.add_argument('-n', '--num-jobs', type=int, default=24)
    parser.add_argument('--num-attempts', type=int, default=5)
    main(**vars(parser.parse_args()))
