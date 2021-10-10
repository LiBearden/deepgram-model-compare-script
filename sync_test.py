import requests
import time
import pathlib


# Establish request constants
url = "https://brain.deepgram.com/v2/listen"
querystrings = [{"model":"phonecall","language":"en-US"}, {"model":"voicemail","language":"en-US"}]
payload = {"url": "http://storage.googleapis.com/cloud-samples-data/speech/commercial_mono.wav"}
payload_path = pathlib.Path("/path/to/file.wav")
binary_payload = pathlib.Path('/path/to/file.wav').read_bytes()
binary_filename = payload_path.name


# Set Headers for url and file transcription requests
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic {BASE64_ENCODED_USER_PASS}"
}
binary_headers = {
    "Content-Type": "application/octet-stream",
    "Authorization": "Basic {BASE64_ENCODED_USER_PASS}"
}

# Create results files for tests
url_results_file = open("sync_url_results.txt", "w")
file_results_file = open("sync_file_results.txt", "w")

# Create lists to contain url voicemail and phonecall metrics
url_phonecall_metrics = []
url_voicemail_metrics = []

# Create lists to contain file voicemail and phonecall metrics
file_phonecall_metrics = []
file_voicemail_metrics = []


# Define function to test and log the speed of synchronous url transcription requests
def url_sync_test():
    # Print descriptive status message, and loop through tests in defined range to generate metrics data
    print("Testing synchronous transcription request speed for {audio_file} [URL]...".format(audio_file=binary_filename))
    for i in range(1, 21):
        # Loop through each model type defined in querystrings for comparison to one another
        for querystring in querystrings:
            # Start the request timer and begin the POST request to the Deepgram transcription API)
            start_time = time.time()
            resp = requests.request("POST", url, json=payload, headers=headers, params=querystring)
            # Note the response time and save it to the "transcript" variable and then capture the elasped time
            response_time = time.time() - start_time
            transcript = resp.json()
            # Note the request ID and open the method results file to append to it
            request_id = transcript["metadata"]["request_id"]
            url_results_file = open("sync_url_results.txt", "a")
            print("[Run #{run}]: \nModel - {model} \nResponse Time - {response_time} seconds \nID - {id}\n".format(run=i, model=querystring["model"], response_time=response_time, id=request_id),file=url_results_file)
            # Append the response timing to the appropriate model and close the results file
            if querystring["model"] == "phonecall":
                url_phonecall_metrics.append(response_time)
            elif querystring["model"] == "voicemail":
                url_voicemail_metrics.append(response_time)
        url_results_file.close()
    return url_results_file, url_voicemail_metrics, url_phonecall_metrics


# Define function to test and log the speed of synchronous file transcription requests (file sync)
def file_sync_test():
    print("Testing synchronous transcription request speed for {audio_file} [FILE]...".format(audio_file=binary_filename))
    for i in range(1, 21):
        for querystring in querystrings:
            start_time = time.time()
            resp = requests.request("POST", url, data=binary_payload, headers=binary_headers, params=querystring)
            response_time = time.time() - start_time
            transcript = resp.json()
            request_id = transcript["metadata"]["request_id"]
            file_results_file = open("sync_file_results.txt", "a")
            print("[Run #{run}]: \nModel - {model} \nResponse Time - {response_time} seconds \nID - {id}\n".format(run=i, model=querystring["model"], response_time=response_time, id=request_id),file=file_results_file)
            if querystring["model"] == "phonecall":
                file_phonecall_metrics.append(response_time)
            elif querystring["model"] == "voicemail":
                file_voicemail_metrics.append(response_time)
        file_results_file.close()
    return file_results_file, file_voicemail_metrics, file_phonecall_metrics

# Visual Test Validation Checks
# url_sync_test()
# print(url_voicemail_metrics, url_phonecall_metrics)

# file_sync_test()
# print(file_voicemail_metrics, file_phonecall_metrics)
