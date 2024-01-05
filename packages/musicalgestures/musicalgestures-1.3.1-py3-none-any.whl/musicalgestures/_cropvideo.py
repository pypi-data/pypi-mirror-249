import cv2
import os
import numpy as np
import time
import asyncio
from musicalgestures._utils import MgProgressbar, get_length, get_widthheight, get_first_frame_as_image, get_box_video_ratio, roundup, crop_ffmpeg, wrap_str, unwrap_str, in_colab
from musicalgestures._filter import filter_frame

def find_motion_box_ffmpeg(filename, motion_box_thresh=0.1, motion_box_margin=12):
    """
    Helper function to find the area of motion in a video, using ffmpeg.

    Args:
        filename (str): Path to the video file.
        motion_box_thresh (float, optional): Pixel threshold to apply to the video before assessing the area of motion. Defaults to 0.1.
        motion_box_margin (int, optional): Margin (in pixels) to add to the detected motion box. Defaults to 12.

    Raises:
        KeyboardInterrupt: In case we stop the process manually.

    Returns:
        int: The width of the motion box.
        int: The height of the motion box.
        int: The X coordinate of the top left corner of the motion box.
        int: The Y coordinate of the top left corner of the motion box.
    """

    import subprocess
    import os
    import matplotlib
    import numpy as np
    total_time = get_length(filename)
    width, height = get_widthheight(filename)
    crop_str = ''

    thresh_color = matplotlib.colors.to_hex(
        [motion_box_thresh, motion_box_thresh, motion_box_thresh])
    thresh_color = '0x' + thresh_color[1:]

    pb = MgProgressbar(total=total_time, prefix='Finding area of motion:')

    command = ['ffmpeg', '-y', '-i', filename, '-f', 'lavfi', '-i', f'color={thresh_color},scale={width}:{height}', '-f', 'lavfi', '-i', f'color=black,scale={width}:{height}', '-f',
               'lavfi', '-i', f'color=white,scale={width}:{height}', '-lavfi', 'format=gray,tblend=all_mode=difference,threshold,cropdetect=round=2:limit=0:reset=0', '-f', 'null', '/dev/null']

    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    try:
        while True:
            out = process.stdout.readline()
            if out == '':
                process.wait()
                break
            else:
                out_list = out.split()
                crop_and_time = sorted(
                    [elem for elem in out_list if elem.startswith('t:') or elem.startswith('crop=')])
                if len(crop_and_time) != 0:
                    crop_str = crop_and_time[0]
                    time_float = float(crop_and_time[1][2:])
                    pb.progress(time_float)

        pb.progress(total_time)

        crop_width, crop_height, crop_x, crop_y = [
            int(elem) for elem in crop_str[5:].split(':')]

        motion_box_margin = roundup(motion_box_margin, 4)

        crop_width = np.clip(crop_width+motion_box_margin, 4, width)
        crop_height = np.clip(crop_height+motion_box_margin, 4, height)
        crop_x = np.clip(crop_x-(motion_box_margin/2), 4, width)
        crop_y = np.clip(crop_y-(motion_box_margin/2), 4, height)

        if crop_x + crop_width > width:
            crop_x = width - crop_width
        else:
            crop_x = np.clip(crop_x, 0, width)
        if crop_y + crop_height > height:
            crop_y = height - crop_height
        else:
            crop_y = np.clip(crop_y, 0, height)

        crop_width, crop_height, crop_x, crop_y = [
            int(elem) for elem in [crop_width, crop_height, crop_x, crop_y]]

        return crop_width, crop_height, crop_x, crop_y

    except KeyboardInterrupt:
        try:
            process.terminate()
        except OSError:
            pass
        process.wait()
        raise KeyboardInterrupt

drawing = False # True if mouse is pressed
xi, yi = -1, -1

def cropping_window(filename):

    def draw_rectangle(event, x, y, flags, param):
        # grab references to the global variables
        global ref_point, crop, drawing, xi, yi

        # check if the left mouse button is clicked
        if event == cv2.EVENT_LBUTTONDOWN:
            # record the starting (x, y) coordinates 
            ref_point = [(x, y)]
            drawing = True
            xi, yi = x, y
            
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            copy = frame.copy()
            cv2.rectangle(copy, (xi, yi), (x, y), (0,255,0), 5)
            cv2.imshow('Draw rectangle with the mouse. Press "c" to crop or "r" to reset the window', copy)

        # check if the left mouse button is released
        elif event == cv2.EVENT_LBUTTONUP:
            # record the ending (x, y) coordinates
            ref_point.append((x, y))
            drawing = False
            # draw a rectangle around the region of interest
            cv2.rectangle(frame, ref_point[0], ref_point[1], (0, 255, 0), 5)

    # Load the video, get the first frame and setup the mouse callback function
    cap = cv2.VideoCapture(filename)
    cv2.namedWindow('Draw rectangle with the mouse. Press "c" to crop or "r" to reset the window', cv2.WINDOW_NORMAL)
    cv2.setMouseCallback('Draw rectangle with the mouse. Press "c" to crop or "r" to reset the window', draw_rectangle)
        
    # keep looping until the 'c' key is pressed
    firstFrame = True
    while True: 
        ret, frame = cap.read()  
        clone = frame.copy()
        
        print('Draw rectangle with the mouse. Press "c" to crop or "r" to reset the window')
        while firstFrame: 
            # display the first frame and wait for a keypress
            cv2.imshow('Draw rectangle with the mouse. Press "c" to crop or "r" to reset the window', frame)
            key = cv2.waitKey(1) & 0xFF
            
            # if the 'c' key is pressed, break from the loop
            if key == ord("c"):
                firstFrame = False       
                break
            # press 'r' to reset the window
            elif key == ord("r"):
                frame = clone.copy()
        break

    # close all open windows
    cv2.destroyAllWindows()

    y_start = ref_point[0][1]
    y_stop = ref_point[1][1]
    x_start = ref_point[0][0]
    x_stop = ref_point[1][0] 

    if x_stop < x_start:
        temp = x_start
        x_start = x_stop
        x_stop = temp
    if y_stop < y_start:
        temp = y_start
        y_start = y_stop
        y_stop = temp

    w, h, x, y = x_stop - x_start, y_stop - y_start, x_start, y_start
    return w, h, x, y

def mg_cropvideo_ffmpeg(
        filename,
        crop_movement='Auto',
        motion_box_thresh=0.1,
        motion_box_margin=12,
        target_name=None,
        overwrite=False):
    """
    Crops the video using ffmpeg.

    Args:
        filename (str): Path to the video file.
        crop_movement (str, optional): 'Auto' finds the bounding box that contains the total motion in the video. Motion threshold is given by motion_box_thresh. 'Manual' opens up a simple GUI that is used to crop the video manually by looking at the first frame. Defaults to 'Auto'.
        motion_box_thresh (float, optional): Only meaningful if `crop_movement='Auto'`. Takes floats between 0 and 1, where 0 includes all the motion and 1 includes none. Defaults to 0.1.
        motion_box_margin (int, optional): Only meaningful if `crop_movement='Auto'`. Adds margin to the bounding box. Defaults to 12.
        target_name (str, optional): The name of the output video. Defaults to None (which assumes that the input filename with the suffix "_crop" should be used).
        overwrite (bool, optional): Whether to allow overwriting existing files or to automatically increment target filenames to avoid overwriting. Defaults to False.

    Returns:
        str: Path to the cropped video.
    """

    global x, y, w, h

    pb = MgProgressbar(total=get_length(filename), prefix='Rendering cropped video:')

    if crop_movement.lower() == 'manual':
        if not in_colab():

            # scale_ratio = get_box_video_ratio(filename)
            # width, height = get_widthheight(filename)
            # scaled_width, scaled_height = [int(elem * scale_ratio) for elem in [width, height]]
            # first_frame_as_image = get_first_frame_as_image(filename, pict_format='.jpg')

            # Cropping UI moved to another subprocess to avoid cv2.waitKey crashing Python with segmentation fault on Linux in Terminal
            import threading
            import queue

            que = queue.Queue()
            t = threading.Thread(target=lambda q, arg1:q.put(cropping_window(arg1)), args=(que, filename))

            t.start()
            t.join()

            w, h, x, y = que.get()          

            # x = threading.Thread(target=run_cropping_window, args=(first_frame_as_image, scale_ratio, scaled_width, scaled_height))
            # run_cropping_window(first_frame_as_image, scale_ratio, scaled_width, scaled_height)
            # x.start()
            # x.join()

        else:
            x, y, w, h = manual_text_input()

    elif crop_movement.lower() == 'auto':
        w, h, x, y = find_motion_box_ffmpeg(filename, motion_box_thresh=motion_box_thresh, motion_box_margin=motion_box_margin)

    cropped_video = crop_ffmpeg(filename, w, h, x, y, target_name=target_name, overwrite=overwrite)

    # if crop_movement.lower() == 'manual':
    #     cv2.destroyAllWindows()
    #     if not in_colab():
    #         os.remove(first_frame_as_image)

    return cropped_video


async def async_subprocess(command):

    global w, h, x, y

    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    # print(f'[{command} exited with {process.returncode}]')
    if stdout:
        res = stdout.decode()
        res_array = res.split(' ')
        res_array_int = [int(elem) for elem in res_array]
        w, h, x, y = res_array_int
        # print(f'[stdout]\n{stdout.decode()}')

    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

def run_cropping_window(imgpath, scale_ratio, scaled_width, scaled_height):

    import platform
    import musicalgestures
    import os
    module_path = os.path.abspath(os.path.dirname(musicalgestures.__file__))
    the_system = platform.system()
    pythonkw = "python"
    if the_system != "Windows":
        pythonkw += "3"
    pyfile = wrap_str(module_path + '/_cropping_window.py')
    imgpath = wrap_str(imgpath)

    command = f'{pythonkw} {pyfile} {imgpath} {scale_ratio} {scaled_width} {scaled_height}'

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # if cleanup: 'RuntimeError: There is no current event loop..'
        loop = None
    if loop and loop.is_running():
        tsk = loop.create_task(async_subprocess(command))
    else:
        asyncio.run(async_subprocess(command))

def manual_text_input():
    """
    Helper function for mg_crop_video_ffmpeg when its crop_movement is 'manual', but the environment is in Colab.
    In this case we can't display the windowed cropping UI, so we ask for the values as a text input.

    Returns:
        list: x, y, w, h for crop_ffmpeg. 
    """
    print("Looks like we are in Colab, can't run the cropping GUI here.")
    print("Please add the parameters of the cropping rectangle (in pixels): x, y, width, height")
    print("""
        x (int): The horizontal coordinate of the top left pixel of the cropping rectangle.
        y (int): The vertical coordinate of the top left pixel of the cropping rectangle.
        width (int): The desired width.
        height (int): The desired height.
    """)
    res = input()
    res = res.replace(",", " ")
    res_list = ' '.join(res.split()).split(" ")
    try:
        res_list_int = [abs(int(float(item))) for item in res_list]
    except ValueError:
        raise ValueError("Invalid parameter(s) found. Try only integer numbers.")

    if len(res_list_int) < 4:
        raise RuntimeError(f"Not enough parameters in {res_list_int}")

    res_list_int = res_list_int[:4]

    return res_list_int