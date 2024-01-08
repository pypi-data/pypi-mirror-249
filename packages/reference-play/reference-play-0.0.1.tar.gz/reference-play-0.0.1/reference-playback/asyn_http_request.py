import requests
import asyncio
from functools import partial

class AsyncHttpRequest:
    async def make_post_request(self, url, headers, payload):
        try:
            loop = asyncio.get_running_loop()

            # ADDING 10 SECONDS TIMEOUT
            request_func = partial(
                requests.post, url, headers=headers, json=payload, timeout=10
            )
            response = await loop.run_in_executor(None, request_func)
            response.raise_for_status()

            # RESPONSE SUCCESSFULL
            if response.status_code == 200:
                print("\nPOST request successful!")
                print(response.json())
                return response.json()

        except requests.exceptions.Timeout:
            print("Request timed out: No response received within 10 seconds.")
        except requests.HTTPError as err:
            print(err.response.json())
            self.handle_http_error(err)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    # HANDLING DIFFERENT HTTP ERRORS
    def handle_http_error(self, err):
        error_messages = {
            400: "Bad Request (400): The server could not understand the request.",
            401: "Authentication error (401): Invalid mail or password",
            403: "Authorization error (403): Access forbidden.",
            404: "Not Found (404): The requested resource was not found.",
            500: "Internal Server Error (500): The server encountered an unexpected condition.",
        }
        status_code = err.response.status_code if err.response else None
        if status_code in error_messages:
            print(error_messages[status_code])

        else:
            print(f"HTTP error occurred: {err}")



