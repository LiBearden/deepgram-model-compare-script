import asyncio
import async_test
import sync_test
from statistics import mean

__author__ = "Elliot B."


# Define function for comparison report
def comparison_calculations(audio_filename, model1_name, model2_name, model1_metrics, model2_metrics, method_results_file):
    # Compute the average request response time per model for the method
    model1_average_compute_time = mean(model1_metrics)
    model2_average_compute_time = mean(model2_metrics)
    # Open the applicable results file for the method
    method_results_file = open(method_results_file, "a")
    # Print a formatted string to denote the aggregate results for the applicable model and audio file, in seconds
    print("-- Average Compute Time [{model} - {audio_file}]: {time} seconds --".format(model=model1_name,time=model1_average_compute_time, audio_file=audio_filename), file=method_results_file)
    print("-- Average Compute Time [{model} - {audio_file}]: {time} seconds --".format(model=model2_name, time=model2_average_compute_time, audio_file=audio_filename), file=method_results_file)
    # Close the applicable results file for the method
    method_results_file.close()

# Run Asynchronous Model Comparison Tests
asyncio.run(async_test.url_async_test())
comparison_calculations(async_test.binary_filename, async_test.querystrings[0]["model"], async_test.querystrings[1]["model"], async_test.url_phonecall_metrics, async_test.url_voicemail_metrics, async_test.url_results_file.name)
asyncio.run(async_test.file_async_test())
comparison_calculations(async_test.binary_filename, async_test.querystrings[0]["model"], async_test.querystrings[1]["model"], async_test.file_phonecall_metrics, async_test.file_voicemail_metrics, async_test.file_results_file.name)


# Run Synchronous Model Comparison Tests
sync_test.url_sync_test()
comparison_calculations(sync_test.binary_filename, sync_test.querystrings[0]["model"], sync_test.querystrings[1]["model"], sync_test.url_phonecall_metrics, sync_test.url_voicemail_metrics, sync_test.url_results_file.name)
sync_test.file_sync_test()
comparison_calculations(sync_test.binary_filename, sync_test.querystrings[0]["model"], sync_test.querystrings[1]["model"], sync_test.file_phonecall_metrics, sync_test.file_voicemail_metrics, sync_test.file_results_file.name)
