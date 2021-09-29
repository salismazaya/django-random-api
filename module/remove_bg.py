from django.utils.crypto import get_random_string
import subprocess, os

def remove_bg(image_bytes: bytes):
    file = f'temp/{get_random_string()}.jpg'
    output_file = f'temp/{get_random_string()}.png'
    open(file, 'wb').write(image_bytes)
    process = subprocess.Popen(['backgroundremover', '-i', file, '-o', output_file])
    output, error = process.communicate()
    if error:
        raise Exception(error)
    
    os.remove(file)
    file_bytes = open(output_file, 'rb').read()
    os.remove(output_file)
    return file_bytes
