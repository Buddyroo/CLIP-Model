import json

# Load data from the JSON file
with open('detailed_stat_video.json', 'r') as file:
    data = json.load(file)

# Initialize variables for calculations
total_frames = 0
total_processing_time = 0
total_videos = len(data)

# Iterate over each video entry in the data
for video_id, stats in data.items():
    total_frames += stats['frames_count']
    total_processing_time += stats['processing_time']

# Calculate averages
average_frames_per_video = total_frames / total_videos
average_processing_time_per_frame = total_processing_time / total_frames
average_processing_time_per_video = total_processing_time / total_videos

# Prepare the result
result = {
    "Среднее количество кадров на видео": average_frames_per_video,
    "Среднее время обработки одного кадра (секунды)": average_processing_time_per_frame,
    "Среднее время обработки одного видео (секунды)": average_processing_time_per_video
}

# Print results
print(f"Среднее количество кадров на видео: {result['Среднее количество кадров на видео']:.7f}")
print(f"Среднее время обработки одного кадра (секунды): {result['Среднее время обработки одного кадра (секунды)']:.7f}")
print(f"Среднее время обработки одного видео (секунды): {result['Среднее время обработки одного видео (секунды)']:.7f}")

# Save results to stat_video.json
with open('stat_video.json', 'w', encoding='utf-8') as outfile:
    json.dump(result, outfile, ensure_ascii=False, indent=4)
