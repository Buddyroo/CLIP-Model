import whisper
import inspect

for name, obj in inspect.getmembers(whisper):
    if inspect.isfunction(obj) and 'load_model' in name:
        print(f'Found load_model in whisper module: {name}')