import requests
import os


class Daios:
    _base_url = "https://andrew-roci--completion.modal.run"

    def __init__(self, token=None):
        self.token = token
        if self.token is None:
            if "daios_token" in os.environ:
                self.token = os.environ["daios_token"]

    def completion(self, question, stream=True):
        headers = {
            "x-api-key": self.token
        }
        params = {
            "question": question
        }

        response = requests.get(self._base_url, headers=headers, params=params, stream=stream)

        return response


def main():
    token = ""
    daios = Daios(token=token)
    query = "Write a brief slack message to my boss telling him that my coworker was unnecessarily chastised"
    response = daios.completion(query, stream=True)
    for chunk in response:
        print(chunk)


if __name__ == '__main__':
    main()
