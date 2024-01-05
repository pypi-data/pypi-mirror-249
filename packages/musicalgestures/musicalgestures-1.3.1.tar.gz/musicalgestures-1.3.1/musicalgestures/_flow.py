import os
import cv2
import numpy as np
import math
import weakref
import matplotlib.pyplot as plt
from scipy.stats import entropy

import musicalgestures
from musicalgestures._utils import MgFigure, extract_wav, embed_audio_in_video, MgProgressbar, convert_to_avi, generate_outfilename


class Flow:
    """
    Class container for the sparse and dense optical flow processes.
    """

    def __init__(self, parent, filename, color, has_audio):
        """
        Initializes the Flow class.

        Args:
            parent (MgVideo): the parent MgVideo.
            filename (str): Path to the input video file. Passed by parent MgVideo.
            color (bool): Set class methods in color or grayscale mode. Passed by parent MgVideo.
            has_audio (bool): Indicates whether source video file has an audio track. Passed by parent MgVideo.
        """
        self.parent = weakref.ref(parent)
        self.filename = filename
        self.color = color
        self.has_audio = has_audio
    
    def dense(
            self,
            filename=None,
            pyr_scale=0.5,
            levels=3,
            winsize=15,
            iterations=3,
            poly_n=5,
            poly_sigma=1.2,
            flags=0,
            velocity=False,
            distance=None, 
            timestep=1,
            move_step=1, 
            angle_of_view=0, 
            scaledown=1,      
            skip_empty=False,
            target_name=None,
            overwrite=False):
        """
        Renders a dense optical flow video of the input video file using `cv2.calcOpticalFlowFarneback()`. The description of the matching parameters are taken from the cv2 documentation.

        Args:
            filename (str, optional): Path to the input video file. If None the video file of the MgVideo is used. Defaults to None.
            pyr_scale (float, optional): Specifies the image scale (<1) to build pyramids for each image. `pyr_scale=0.5` means a classical pyramid, where each next layer is twice smaller than the previous one. Defaults to 0.5.
            levels (int, optional): The number of pyramid layers including the initial image. `levels=1` means that no extra layers are created and only the original images are used. Defaults to 3.
            winsize (int, optional): The averaging window size. Larger values increase the algorithm robustness to image noise and give more chances for fast motion detection, but yield more blurred motion field. Defaults to 15.
            iterations (int, optional): The number of iterations the algorithm does at each pyramid level. Defaults to 3.
            poly_n (int, optional): The size of the pixel neighborhood used to find polynomial expansion in each pixel. Larger values mean that the image will be approximated with smoother surfaces, yielding more robust algorithm and more blurred motion field, typically poly_n =5 or 7. Defaults to 5.
            poly_sigma (float, optional): The standard deviation of the Gaussian that is used to smooth derivatives used as a basis for the polynomial expansion. For `poly_n=5`, you can set `poly_sigma=1.1`, for `poly_n=7`, a good value would be `poly_sigma=1.5`. Defaults to 1.2.
            flags (int, optional): Operation flags that can be a combination of the following: - **OPTFLOW_USE_INITIAL_FLOW** uses the input flow as an initial flow approximation. - **OPTFLOW_FARNEBACK_GAUSSIAN** uses the Gaussian \\f$\\texttt{winsize}\\times\\texttt{winsize}\\f$ filter instead of a box filter of the same size for optical flow estimation. Usually, this option gives z more accurate flow than with a box filter, at the cost of lower speed. Normally, `winsize` for a Gaussian window should be set to a larger value to achieve the same level of robustness. Defaults to 0.
            velocity (bool, optional): Whether to compute optical flow velocity or not. Defaults to False.
            distance (int, optional): Distance in meters to image (focal length) for returning flow in meters per second. Defaults to None.
            timestep (int, optional): Time step in seconds for returning flow in meters per second. Defaults to 1.
            move_step (int, optional): step size in pixels for sampling the flow image. Defaults to 1.
            angle_of_view (int, optional): angle of view of camera, for reporting flow in meters per second. Defaults to 0.
            scaledown (int, optional): factor to scaledown frame size of the video. Defaults to 1.
            skip_empty (bool, optional): If True, repeats previous frame in the output when encounters an empty frame. Defaults to False.
            target_name (str, optional): Target output name for the video. Defaults to None (which assumes that the input filename with the suffix "_flow_dense" should be used).
            overwrite (bool, optional): Whether to allow overwriting existing files or to automatically increment target filenames to avoid overwriting. Defaults to False.

        Returns:
            MgVideo: A new MgVideo pointing to the output video file.
        """

        if filename == None:
            filename = self.filename

        of, fex = os.path.splitext(filename)

        # Convert to avi if the input is not avi - necesarry for cv2 compatibility on all platforms
        if fex != '.avi':
            # first check if there already is a converted version, if not create one and register it to the parent self
            if "as_avi" not in self.parent().__dict__.keys():
                file_as_avi = convert_to_avi(of + fex, overwrite=overwrite)
                # register it as the avi version for the file
                self.parent().as_avi = musicalgestures.MgVideo(file_as_avi)
            # point of and fex to the avi version
            of, fex = self.parent().as_avi.of, self.parent().as_avi.fex
            filename = self.parent().as_avi.filename

        vidcap = cv2.VideoCapture(filename)

        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        size = (int(width/scaledown), int(height/scaledown))

        if velocity:
            pb = MgProgressbar(total=length, prefix='Rendering dense optical flow velocity:')

        else:
            pb = MgProgressbar(total=length, prefix='Rendering dense optical flow video:')

            if target_name == None:
                target_name = of + '_flow_dense' + fex
            if not overwrite:
                target_name = generate_outfilename(target_name)

            fourcc = cv2.VideoWriter_fourcc(*'MJPG')
            out = cv2.VideoWriter(target_name, fourcc, fps, (width, height))

        ret, frame1 = vidcap.read()
        prev_frame = cv2.cvtColor(cv2.resize(frame1, size), cv2.COLOR_BGR2GRAY)
        
        prev_rgb = None
        hsv = np.zeros_like(frame1)
        hsv[..., 1] = 255

        ii = 0
        # Create two lists for storing optical flow velocity values
        xvel, yvel = [], []

        while(vidcap.isOpened()):
            ret, frame2 = vidcap.read()
            xsum, ysum = 0, 0
            
            if ret == True:
                next_frame = cv2.cvtColor(cv2.resize(frame2, size), cv2.COLOR_BGR2GRAY)

                flow = cv2.calcOpticalFlowFarneback(prev_frame, next_frame, None, pyr_scale, levels, winsize, iterations, poly_n, poly_sigma, flags)

                if velocity:
                    # Cumulative sum of optical flow vectors        
                    for y in range(0, flow.shape[0]):
                        for x in range(0, flow.shape[1]):
                            fx, fy = flow[y, x]
                            xsum += fx
                            ysum += fy
                            
                    # Compute average velocity of pixels by dividing the cumulative sum of optical flow vectors by timesteps        
                    xvel.append(self.get_velocity(flow, xsum, flow.shape[1], distance, timestep, move_step, angle_of_view))
                    yvel.append(self.get_velocity(flow, ysum, flow.shape[0], distance, timestep, move_step, angle_of_view))

                else:
                    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
                    hsv[..., 0] = ang*180/np.pi/2
                    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
                    rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

                    if skip_empty:
                        if np.sum(rgb) > 0:
                            out.write(rgb.astype(np.uint8))
                        else:
                            if ii == 0:
                                out.write(rgb.astype(np.uint8))
                            else:
                                out.write(prev_rgb.astype(np.uint8))
                    else:
                        out.write(rgb.astype(np.uint8))

                    if skip_empty:
                        if np.sum(rgb) > 0 or ii == 0:
                            prev_rgb = rgb
                    else:
                        prev_rgb = rgb
                
                prev_frame = next_frame

            else:
                pb.progress(length)
                break

            pb.progress(ii)
            ii += 1

        if velocity:

            fig, ax = plt.subplots(figsize=(12, 4), dpi=300)

            # make sure background is white
            fig.patch.set_facecolor('white')
            fig.patch.set_alpha(1)

            # add title
            title = 'Dense optical flow velocity: ' + os.path.basename(of + fex)
            fig.suptitle(title, fontsize=16)

            time = np.linspace(0, len(xvel)/fps, len(xvel))
            acceleration = self.get_acceleration(xvel, fps)
            acceleration_entropy = entropy(acceleration)

            ax.plot(time, xvel, label=f'Average acceleration: {round(np.mean(acceleration),3)} m/s\nEntropy of acceleration: {round(acceleration_entropy,3)}')
            ax.set_xlabel('Time [Seconds]')
            ax.set_ylabel('Velocity [Meters]')
            ax.margins(x=0)
            ax.legend(handlelength=0, handletextpad=0, fancybox=True)

            fig.tight_layout()

            if target_name == None:
                target_name = of + '_velocity.png'

            else:
                # enforce png
                target_name = os.path.splitext(target_name)[0] + '.png'
            if not overwrite:
                target_name = generate_outfilename(target_name)

            plt.savefig(target_name, format='png', transparent=False)
            plt.close()

            # create MgFigure
            data = {
                "FPS": fps,
                "path": of,
                "xvel": xvel,
                "yvel": yvel,
            }

            mgf = MgFigure(
                figure=fig,
                figure_type='video.velocity',
                data=data,
                layers=None,
                image=target_name)

            return mgf
        
        else:
            out.release()
            destination_video = target_name

            if self.has_audio:
                source_audio = extract_wav(of + fex)
                embed_audio_in_video(source_audio, destination_video)
                os.remove(source_audio)

            # save result at flow_dense_video at parent MgVideo
            self.parent().flow_dense_video = musicalgestures.MgVideo(
                destination_video, color=self.color, returned_by_process=True)

            return self.parent().flow_dense_video

    def get_acceleration(self, velocity, fps):

        acceleration = np.zeros(len(velocity))
        velocity = np.abs(velocity)
        
        for i in range(len(acceleration)-1):
            acceleration[i] = ((velocity[i+1] + velocity[i]) - velocity[i]) / (1/fps)
            
        return acceleration[:-1]

    def get_velocity(self, flow, sum_flow_pixels, flow_shape, distance_meters, timestep_seconds, move_step, angle_of_view):

        pixel_count = (flow.shape[0] * flow.shape[1]) / move_step**2
        average_velocity_pixels_per_second = (sum_flow_pixels / pixel_count / timestep_seconds)

        return (self.velocity_meters_per_second(average_velocity_pixels_per_second, flow_shape, distance_meters, angle_of_view)
                if angle_of_view and distance_meters else average_velocity_pixels_per_second)

    def velocity_meters_per_second(self, velocity_pixels_per_second, flow_shape, distance_meters, angle_of_view):

        distance_pixels = ((flow_shape / 2) / math.tan(angle_of_view / 2))
        pixels_per_meter = distance_pixels / distance_meters

        return velocity_pixels_per_second / pixels_per_meter

    def sparse(
            self,
            filename=None,
            corner_max_corners=100,
            corner_quality_level=0.3,
            corner_min_distance=7,
            corner_block_size=7,
            of_win_size=(15, 15),
            of_max_level=2,
            of_criteria=(cv2.TERM_CRITERIA_EPS |
                         cv2.TERM_CRITERIA_COUNT, 10, 0.03),
            target_name=None,
            overwrite=False):
        """
        Renders a sparse optical flow video of the input video file using `cv2.calcOpticalFlowPyrLK()`. `cv2.goodFeaturesToTrack()` is used for the corner estimation. The description of the matching parameters are taken from the cv2 documentation.

        Args:
            filename (str, optional): Path to the input video file. If None, the video file of the MgVideo is used. Defaults to None.
            corner_max_corners (int, optional): Maximum number of corners to return. If there are more corners than are found, the strongest of them is returned. `maxCorners <= 0` implies that no limit on the maximum is set and all detected corners are returned. Defaults to 100.
            corner_quality_level (float, optional): Parameter characterizing the minimal accepted quality of image corners. The parameter value is multiplied by the best corner quality measure, which is the minimal eigenvalue (see cornerMinEigenVal in cv2 docs) or the Harris function response (see cornerHarris in cv2 docs). The corners with the quality measure less than the product are rejected. For example, if the best corner has the quality measure = 1500, and the qualityLevel=0.01, then all the corners with the quality measure less than 15 are rejected. Defaults to 0.3.
            corner_min_distance (int, optional): Minimum possible Euclidean distance between the returned corners. Defaults to 7.
            corner_block_size (int, optional): Size of an average block for computing a derivative covariation matrix over each pixel neighborhood. See cornerEigenValsAndVecs in cv2 docs. Defaults to 7.
            of_win_size (tuple, optional): Size of the search window at each pyramid level. Defaults to (15, 15).
            of_max_level (int, optional): 0-based maximal pyramid level number. If set to 0, pyramids are not used (single level), if set to 1, two levels are used, and so on. If pyramids are passed to input then the algorithm will use as many levels as pyramids have but no more than `maxLevel`. Defaults to 2.
            of_criteria (tuple, optional): Specifies the termination criteria of the iterative search algorithm (after the specified maximum number of iterations criteria.maxCount or when the search window moves by less than criteria.epsilon). Defaults to (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03).
            target_name (str, optional): Target output name for the video. Defaults to None (which assumes that the input filename with the suffix "_flow_sparse" should be used).
            overwrite (bool, optional): Whether to allow overwriting existing files or to automatically increment target filenames to avoid overwriting. Defaults to False.

        Returns:
            MgVideo: A new MgVideo pointing to the output video file.
        """

        if filename == None:
            filename = self.filename

        of, fex = os.path.splitext(filename)

        # Convert to avi if the input is not avi - necesarry for cv2 compatibility on all platforms
        if fex != '.avi':
            # first check if there already is a converted version, if not create one and register it to the parent self
            if "as_avi" not in self.parent().__dict__.keys():
                file_as_avi = convert_to_avi(of + fex, overwrite=overwrite)
                # register it as the avi version for the file
                self.parent().as_avi = musicalgestures.MgVideo(file_as_avi)
            # point of and fex to the avi version
            of, fex = self.parent().as_avi.of, self.parent().as_avi.fex
            filename = self.parent().as_avi.filename

        vidcap = cv2.VideoCapture(filename)
        ret, frame = vidcap.read()
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

        pb = MgProgressbar(
            total=length, prefix='Rendering sparse optical flow video:')

        if target_name == None:
            target_name = of + '_flow_sparse' + fex
        if not overwrite:
            target_name = generate_outfilename(target_name)

        out = cv2.VideoWriter(target_name, fourcc, fps, (width, height))

        # params for ShiTomasi corner detection
        feature_params = dict(maxCorners=corner_max_corners,
                              qualityLevel=corner_quality_level,
                              minDistance=corner_min_distance,
                              blockSize=corner_block_size)

        # Parameters for lucas kanade optical flow
        lk_params = dict(winSize=of_win_size,
                         maxLevel=of_max_level,
                         criteria=of_criteria)

        # Create some random colors
        color = np.random.randint(0, 255, (100, 3))

        # Take first frame and find corners in it
        ret, old_frame = vidcap.read()
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

        # Create a mask image for drawing purposes
        mask = np.zeros_like(old_frame)

        ii = 0

        while(vidcap.isOpened()):
            ret, frame = vidcap.read()
            if ret == True:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # calculate optical flow
                p1, st, err = cv2.calcOpticalFlowPyrLK(
                    old_gray, frame_gray, p0, None, **lk_params)

                # Select good points
                good_new = p1[st == 1]
                good_old = p0[st == 1]

                # draw the tracks
                for i, (new, old) in enumerate(zip(good_new, good_old)):
                    a, b = new.ravel()
                    c, d = old.ravel()
                    mask = cv2.line(mask, (int(a), int(b)),
                                    (int(c), int(d)), color[i].tolist(), 2)

                    if self.color == False:
                        frame = cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2BGR)

                    frame = cv2.circle(
                        frame, (int(a), int(b)), 5, color[i].tolist(), -1)

                img = cv2.add(frame, mask)

                out.write(img.astype(np.uint8))

                # Now update the previous frame and previous points
                old_gray = frame_gray.copy()
                p0 = good_new.reshape(-1, 1, 2)

            else:
                pb.progress(length)
                break

            pb.progress(ii)
            ii += 1

        out.release()

        destination_video = target_name

        if self.has_audio:
            source_audio = extract_wav(of + fex)
            embed_audio_in_video(source_audio, destination_video)
            os.remove(source_audio)

        # save result at flow_sparse_video at parent MgVideo
        self.parent().flow_sparse_video = musicalgestures.MgVideo(
            destination_video, color=self.color, returned_by_process=True)

        return self.parent().flow_sparse_video