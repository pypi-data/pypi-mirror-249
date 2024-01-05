"""Face Authentication module"""
import json
import requests
from bs4 import BeautifulSoup
from yk_utils.images import allowed_base64_image
from .api_result import ApiResult


class FaceAuthentication:
    """This class is a wrapper for the YouAuth product, an API for face authentication.
    """
    def __init__(self, api_url: str, api_key: str):
        """Class initializer
        :param api_url:
            YouAuth API URL.
        :param api_key:
            YouAuth API Key.
        """
        self.api_url = api_url
        self.api_key = api_key

    @staticmethod
    def parse_response_error(html_text: str, extra_response_codes: dict = None) -> str:
        """Parse error response
        :param html_text:
            Error message.
        :param extra_response_codes:
            Dictionary with additional response codes and description pairs, to search on html_text.

        :return:
            Parsed error message.
        """
        try:
            message = json.loads(html_text)['message']
        except Exception:
            html = BeautifulSoup(markup=html_text, features="html.parser")
            message = html.text
            if html.p:
                inner_html = BeautifulSoup(markup=html.p.text, features="html.parser")
                message = inner_html.text if inner_html.p is None else inner_html.p.text

        if "face_not_found" in message:
            message = "Could not find a face in the image."
        elif "multiple_faces" in message:
            message = "The image has more than one person."
        elif "brightness_failed" in message:
            message = "Avoid glare or extreme light conditions."
        elif "light_uniformity_failed" in message:
            message = "Avoid having parts of your face shadowed."
        elif "face_too_far" in message:
            message = "Move a little closer to the camera."
        elif "face_too_close" in message:
            message = "Move a little further from the camera."
        elif "quality_failed" in message:
            message = "The provided image does not have enough quality."
        elif "mobile_app_no_response" in message:
            message = "Could not receive result from mobile app."
        elif extra_response_codes:
            for code in extra_response_codes:
                if code in message:
                    message = extra_response_codes[code]
                    break
        else:
            message = f"An error occurred: {message}"
        return message

    @staticmethod
    def parse_response_status(status: str) -> str:
        """Create a message from the response status data
        :param status:
            Status of the operation.
        :return:
            Resulting message to be sent to the UI.
        """
        message = status
        if status == 'SUCCESS':
            message = "Face authentication successful"
        elif status == 'NEW_USER':
            message = "Face signup successful"
        elif status == 'USER_NOT_FOUND':
            message = "User not registered"
        elif status == 'FAILED':
            message = "Face authentication failed"
        return message

    def request_face_authentication(self,
                                    user_id: str,
                                    user_photo: str,
                                    user_attributes: dict = None,
                                    create_if_new: bool = True) -> ApiResult:
        """Perform a face authentication request to YouAuth API.
        :param user_id:
            User ID to be authenticated.
        :param user_photo:
            User selfie image.
        :param user_attributes:
            User attributes to be saved.
        :param create_if_new:
            Create new user if the provided user ID doesn't exist.
        :return:
            Face authentication result object.
        """
        face_authentication_result = ApiResult(status='FAILED', message_class='text-danger',
                                               message='Face authentication failed')

        if allowed_base64_image(user_photo):
            yoonik_request_data = {
                'user_id': user_id,
                'user_photo': user_photo.split('base64,')[1],
                'create_if_new': create_if_new
            }
            if user_attributes:
                yoonik_request_data['user_attributes'] = user_attributes
            response = requests.post(
                self.api_url,
                headers={'x-api-key': self.api_key},
                json=yoonik_request_data
            )
            if response.ok:
                result = json.loads(response.text)
                face_authentication_result.status = result['status']
                face_authentication_result.message_class = 'text-success' if \
                    face_authentication_result.status in ('SUCCESS', 'NEW_USER') else 'text-danger'
                face_authentication_result.message = \
                    self.parse_response_status(face_authentication_result.status)
            else:
                face_authentication_result.message = \
                    f'Ups! {self.parse_response_error(response.text)}'

        return face_authentication_result

    def request_account_deletion(self, user_id: str) -> bool:
        """Delete a user from YouAuth API.
        :param user_id:
            User ID to be deleted.
        :return:
            True if user successfully deleted.
        """
        response = requests.delete(
            self.api_url,
            headers={'x-api-key': self.api_key},
            json={'user_id': user_id}
        )
        return response.ok
