import h5py
import numpy as np
import pandas as pd
import logging
from typing import Optional, Tuple

from .. import io


logger = logging.getLogger(__name__)


@io.register_provider
class CamStamps(io.BaseProvider):
    KIND = "timestamps"
    NAME = "camera"
    SUFFIXES = ["_timestamps.h5"]

    def load(self, filename: Optional[str] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Reads from timestamps generated by ETHO Camera system

        Expected structure of the CSV file:
        - 'timeStamps' - time stamps for each frame in an associated video. In a weird format...

        Args:
            filename (Optional[str], optional): Defaults to None.

        Returns:
            Tuple[np.ndarray, np.ndarray]: index (sample number, frame number,...), time stamp in seconds for each index.
        """

        if filename is None:
            filename = self.path

        with h5py.File(filename, "r") as f:
            cam_stamps = f["timeStamps"][:]

        # time stamps at idx 0 can be a little wonky - so use the information embedded in the image
        if cam_stamps.shape[1] > 2:  # time stamps from flycapture (old point grey API)
            shutter_times = cam_stamps[:, 1] + cam_stamps[:, 2] / 1_000_000  # time of "Shutter OFF"
        elif cam_stamps.shape[1] == 2:  # time stamps from other camera drivers (spinnaker (new point grey/FLIR API) and ximea)
            # cut off empty time stamps
            last_frame_idx = np.argmax(cam_stamps[:, 1] == 0) - 1
            cam_stamps = cam_stamps[:last_frame_idx]

            # fix jumps from overflow in timestamp counter for ximea cameras
            frame_intervals = np.diff(cam_stamps[:, 1])
            frame_interval_median = np.median(frame_intervals)
            idxs = np.where(frame_intervals < -10 * frame_interval_median)[0]
            while len(idxs):
                idx = idxs[0]
                df_wrong = cam_stamps[idx + 1, 1] - cam_stamps[idx, 1]
                df_inferred = cam_stamps[idx + 1, 0] - cam_stamps[idx, 0]
                cam_stamps[idx + 1 :, 1] = cam_stamps[idx + 1 :, 1] - df_wrong + df_inferred

                frame_intervals = np.diff(cam_stamps[:, 1])
                idxs = np.where(frame_intervals < -10 * frame_interval_median)[0]

            shutter_times = cam_stamps[:, 1]

        last_frame_idx = np.argmax(shutter_times == 0) - 1
        timestamps = shutter_times[:last_frame_idx]
        indices = np.arange(len(shutter_times))

        return indices, timestamps


@io.register_provider
class DaqStamps(io.BaseProvider):
    KIND = "timestamps"
    NAME = "daq"
    SUFFIXES = [".h5"]

    def load(self, filename: Optional[str] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Reads from timestamps from H5 generated by ETHO DAQ system.

        Expected structure of the CSV file:
        - 'systemtime' - time stamps in seconds
        - 'samplenumber' (optional) - number of samples that have passed from the previous time stamp. The cumulative sum yields the indices for each timestamps.

        Args:
            filename (Optional[str], optional): Defaults to None.

        Returns:
            Tuple[np.ndarray, np.ndarray]: index (sample number, frame number,...), time stamp in seconds for each index.
        """

        if filename is None:
            filename = self.path

        with h5py.File(filename, "r") as f:
            daq_stamps = f["systemtime"][:]
            daq_sampleinterval = f["samplenumber"][:]

        # remove trailing zeros - may be left over if recording didn't finish properly
        if 0 in daq_stamps:
            last_valid_idx = np.argmax(daq_stamps == 0)
        else:
            last_valid_idx = len(daq_stamps) - 1  # in case there are no trailing zeros

        daq_samplenumber = np.cumsum(daq_sampleinterval)[:last_valid_idx, np.newaxis]

        indices = daq_samplenumber[:last_valid_idx, 0]
        timestamps = daq_stamps[:last_valid_idx, 0]

        return indices, timestamps


@io.register_provider
class CsvStamps(io.BaseProvider):
    KIND = "timestamps"
    NAME = "generic"
    SUFFIXES = ["_timestamps.csv"]

    def load(self, filename: Optional[str] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Reads from timestamps from CSV

        Expected structure of the CSV file:
        - 'timestamp' - time stamps in seconds
        - 'index' (optional) - the index for each time stamp, if missing we assume time stamps are for subsequence indices.

        Args:
            filename (Optional[str], optional): Defaults to None.

        Returns:
            Tuple[np.ndarray, np.ndarray]: index (sample number, frame number,...), time stamp in seconds for each index.
        """

        if filename is None:
            filename = self.path

        df = pd.read_csv(filename)

        timestamps = df["timestamp"]
        if "index" in df:
            indices = df["index"]
        else:
            indices = np.arange(len(timestamps))

        return indices, timestamps
