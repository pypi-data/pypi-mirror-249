import base64
import cv2
import time
from google_nest_client.device import Device


class Camera(Device):
    def get_last_motion_event(self) -> dict:
        return self.get_event('CameraMotion.Motion')

    def get_last_person_event(self) -> dict:
        return self.get_event('CameraPerson.Person')

    def get_last_sound_event(self) -> dict:
        return self.get_event('CameraSound.Sound')

    def generate_image(self, event_id: str) -> dict:
        return self.api_client.execute_command(
            self.device_id,
            'sdm.devices.commands.CameraEventImage.GenerateImage',
            {'eventId': event_id},
        )

    def capture_still_frame_as_base64(self, retries: int = 3) -> str:
        rtsp_url = self.api_client.execute_command(
            self.device_id,
            'sdm.devices.commands.CameraLiveStream.GenerateRtspStream',
            {},
        )["results"]["streamUrls"]["rtspUrl"]

        for i in range(retries):
            cap = cv2.VideoCapture(rtsp_url)
            if cap.isOpened():
                break
            time.sleep(1.5 ** i)
        else:
            raise ValueError("Cannot open camera live stream")

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                base64_image = base64.b64encode(buffer).decode('utf-8')
                break

        cap.release()
        cv2.destroyAllWindows()

        return base64_image
