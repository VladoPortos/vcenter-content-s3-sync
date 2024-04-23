import requests
import time
import os
import threading
requests.packages.urllib3.disable_warnings()

# define the download function as a separate thread
def download_file(url, dest, timeout):
    global download_finished
    try:
        MB = 1024 * 1024  # 1MB in bytes
        chunk_size_mb = 512 * MB  # change this to change chunk size

        response = requests.get(url, stream=True, timeout=timeout, verify=False)  # ignore SSL errors)
        response.raise_for_status()  # Raise an exception if the GET request failed
        with open(dest, 'wb') as file:
            for chunk in response.iter_content(chunk_size=chunk_size_mb):
                file.write(chunk)
    except Exception as e:
        print(f"An error occurred during download: {str(e)}")
        download_finished = True
        exit(1)  # exit the script with non-zero status
    finally:
        download_finished = True



# define the keep-alive function
def keep_alive(vmware_host, download_session_data, login_json, client_token, keepalive_progress):
    url = f"https://{vmware_host}/api/content/library/item/download-session/{download_session_data}?action=keep-alive"
    headers = {
        'vmware-api-session-id': login_json,
        'client_token': client_token
    }
    data = {"progress": keepalive_progress}
    while not download_finished:
        requests.post(url, headers=headers, json=data, verify=False)  # ignore SSL errors)
        time.sleep(10)

# define variables from Ansible
modified_download_url = os.getenv('MODIFIED_DOWNLOAD_URL')
local_temp_directory = os.getenv('LOCAL_TEMP_DIRECTORY')
folder_name = os.getenv('FOLDER_NAME')
item_name = os.getenv('ITEM_NAME')
local_download_temp_directory = os.getenv('LOCAL_DOWNLOAD_TEMP_DIRECTORY')
vmware_host = os.getenv('VMWARE_HOST')
download_session_data = os.getenv('DOWNLOAD_SESSION_DATA')
login_json = os.getenv('LOGIN_JSON')
client_token = os.getenv('CLIENT_TOKEN')
keepalive_progress = os.getenv('KEEPALIVE_PROGRESS')

# start the download as a separate thread
dest = f"{local_temp_directory}/{folder_name}/{item_name}"
download_finished = False
# start the download as a separate thread
download_thread = threading.Thread(target=download_file, args=(modified_download_url, dest, 900))
download_thread.start()

# start sending keep-alive messages
keep_alive_thread = threading.Thread(target=keep_alive, args=(vmware_host, download_session_data, login_json, client_token, keepalive_progress))
keep_alive_thread.start()

# wait for the download to finish
download_thread.join()
keep_alive_thread.join()  # Ensure the keep-alive thread also finishes

