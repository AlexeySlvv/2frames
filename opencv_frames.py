from os.path import basename
import cv2


def get_video_info(file_name: str):
    '''
    returns: 
      * frame_count
      * duration
    '''
    if not file_name:
        return None

    cap = cv2.VideoCapture(file_name)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps

    cv2.destroyAllWindows()

    return frame_count, duration


def save_frames(param: dict, set_progress=None) -> bool:
    '''
    param dictionary:
      * file_name: input video file name
      * folder_name: output folder name
      * step: frame step
      * from: from time (msec)
      * to: to time (msec)
    '''
    file_name = param.get('file_name')

    folder_name = param.get('folder_name')
    if not file_name or not folder_name:
        return False

    frame_step = int(param.get('step'))
    from_ms = int(param.get('from'))
    to_msec = int(param.get('to'))

    file_basename = basename(file_name)
    cap = cv2.VideoCapture(file_name)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = fps * (from_ms // 1000)
    end_frame = fps * (to_msec // 1000)

    frame_no = -1
    while True:
        for i in range(0, frame_step):
            success, image = cap.read()
            if not success:
                cv2.destroyAllWindows()
                return False
            frame_no += 1

        if frame_no < start_frame:
            continue
        else:
            if not success:
                cv2.destroyAllWindows()
                return False
            iname = f'{folder_name}/{file_basename}_frame_{frame_no}.jpg'
            cv2.imwrite(iname, image)
            if set_progress:
                set_progress(frame_no)
        if frame_no > end_frame:
            break

    if set_progress:
        set_progress(frame_count)

    cv2.destroyAllWindows()
    return True
