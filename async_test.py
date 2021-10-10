import aiohttp
import pathlib
import time

# Establish request constants
url = "https://brain.deepgram.com/v2/listen"
querystrings = [{"model": "phonecall", "language": "en-US"}, {"model": "voicemail", "language": "en-US"}]
url_payload = "{\"url\": \"http://storage.googleapis.com/cloud-samples-data/speech/commercial_mono.wav\"}"
payload_path = pathlib.Path("/path/to/file.wav")
binary_payload = pathlib.Path('/path/to/file.wav').read_bytes()
binary_filename = payload_path.name


# Set Headers for url and file transcription requests
url_headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic {BASE64_ENCODED_USER_PASS}"
}
binary_headers = {
    "Content-Type": "application/octet-stream",
    "Authorization": "Basic {BASE64_ENCODED_USER_PASS}"
}

# Create lists to contain url voicemail and phonecall metrics
url_phonecall_metrics = []
url_voicemail_metrics = []

file_phonecall_metrics = []
file_voicemail_metrics = []

# Create results files for tests
url_results_file = open("async_url_results.txt", "w")
file_results_file = open("async_file_results.txt", "w")


# Define function to test and log the speed of asynchronous url transcription requests
async def url_async_test():
    async with aiohttp.ClientSession() as session:
        # Instantiate an Async.io HTTP Client Session
        print("Testing asynchronous transcription request speed for {audio_file} [URL]...".format(audio_file=binary_filename))
        # Loop through tests in defined range to generate metrics data
        for i in range(1, 21):
            # Loop through each model type defined in querystrings for comparison to one another
            for querystring in querystrings:
                # Start the request timer and begin the POST request to the Deepgram transcription API)
                start_time = time.time()
                async with session.post(url, headers=url_headers, params=querystring, data=url_payload) as resp:
                    # Await the API response (formatted as JSON), and then save to the "transcript" variable
                    print(resp.text)
                    transcript = await resp.json()
                    # Capture elapsed time
                    response_time = time.time() - start_time
                    # Note the request ID and open the method results file to append to it
                    request_id = transcript["metadata"]["request_id"]
                    url_results_file = open("async_url_results.txt", "a")
                    print("[Run #{run}]: \nModel - {model} \nResponse Time - {response_time} seconds \nID - {id}\n".format(run=i, model=querystring["model"], response_time=response_time, id=request_id), file=url_results_file)
                    # Append the response timing to the appropriate model and close the results file
                    if querystring["model"] == "phonecall":
                        url_phonecall_metrics.append(response_time)
                    elif querystring["model"] == "voicemail":
                        url_voicemail_metrics.append(response_time)
                url_results_file.close()
        return url_results_file, url_voicemail_metrics, url_phonecall_metrics


# Define function to test and log the speed of synchronous url transcription requests (stepwise functionality same as above!)
async def file_async_test():

    async with aiohttp.ClientSession() as session:
        print("Testing asynchronous transcription request speed for {audio_file} [FILE]...".format(audio_file=binary_filename))
        for i in range(1, 21):
            for querystring in querystrings:
                start_time = time.time()
                async with session.post(url, headers=binary_headers, params=querystring, data=binary_payload) as resp:
                    transcript = await resp.json()
                    response_time = time.time() - start_time
                    request_id = transcript['metadata']['request_id']
                    file_results_file = open("async_file_results.txt", "a")
                    print("[Run #{run}]: \nModel - {model} \nResponse Time - {response_time} seconds \nID - {id}\n".format(run=i, model=querystring["model"], response_time=response_time, id=request_id),file=file_results_file)
                    if querystring["model"] == "phonecall":
                        file_phonecall_metrics.append(response_time)
                    elif querystring["model"] == "voicemail":
                        file_voicemail_metrics.append(response_time)
                file_results_file.close()
        return file_results_file, file_phonecall_metrics, file_voicemail_metrics


# Visual Test Validation Checks
# asyncio.run(url_async_test())
# print(url_voicemail_metrics, url_phonecall_metrics)

# asyncio.run(file_async_test())
# print(file_voicemail_metrics, file_phonecall_metrics)