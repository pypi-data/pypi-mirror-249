def RUN_DAV(exe_path = None):

    import subprocess

    if not exe_path:

        # Путь к исполняемому файлу .exe
        exe_path = 'DataVisualization.exe'

    # Запуск исполняемого файла
    subprocess.call(exe_path)


def LOAD_DAV():

    
    import urllib.request

    import os

    import requests

    import gdown

    os.mkdir('data')  # Если нет, создаем новую папку
    os.mkdir('data/Shaders')  # Если нет, создаем новую папку
    os.mkdir('data/Saves')  # Если нет, создаем новую папку
    os.mkdir('data/Examples')  # Если нет, создаем новую папку

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    
    url = 'https://drive.google.com/file/d/1SibDhJFTn5GE0jrhVUCHavCkpK_rYFpH/view?usp=sharing'  # замените на нужную ссылку
    file_id = '1SibDhJFTn5GE0jrhVUCHavCkpK_rYFpH'
    filename = 'visualinfo.exe'  # замените на желаемое имя файла
    #urllib.request.urlretrieve(url, filename)
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    

    url = 'https://drive.google.com/file/d/17PWBqn3Dt4cqYBu5OalxBJMPq7VhYtXl/view?usp=sharing'  # замените на нужную ссылку
    filename = 'data/Saves/UserPrefs.txt'  # замените на желаемое имя файла
    file_id = '17PWBqn3Dt4cqYBu5OalxBJMPq7VhYtXl'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    

    url = 'https://drive.google.com/file/d/1Fc4aOUWjyCRN7eH5-tI0IAnpRBw2DzCC/view?usp=sharing'  # замените на нужную ссылку
    filename = 'data/Shaders/SpheresVertex.glsl'  # замените на желаемое имя файла
    file_id = '1Fc4aOUWjyCRN7eH5-tI0IAnpRBw2DzCC'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1oYVS39FrAVO7fenciohz3skfwqBdeqv_/view?usp=sharing'  # замените на нужную ссылку
    filename = 'data/Shaders/SpheresFragment.glsl'  # замените на желаемое имя файла
    file_id = '1oYVS39FrAVO7fenciohz3skfwqBdeqv_'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1OkzVbsI4di2Oi4gL6rjLJAIZ8oMVyAm8/view?usp=sharing'  # замените на нужную ссылку
    filename = 'openal32.dll'  # замените на желаемое имя файла
    file_id = '1OkzVbsI4di2Oi4gL6rjLJAIZ8oMVyAm8'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)

    
    url = 'https://drive.google.com/file/d/1HV-pQbFJno4AChMFr2sL1YQ8SWj_fBR-/view?usp=sharing'  # замените на нужную ссылку
    filename = 'MANIFEST.in'  # замените на желаемое имя файла
    file_id = '1HV-pQbFJno4AChMFr2sL1YQ8SWj_fBR-'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)

    url = 'https://drive.google.com/file/d/17-YqKhB3twLHRn3cJgopg-5YopX4Oz1Y/view?usp=sharing'  # замените на нужную ссылку
    filename = 'imgui.ini'  # замените на желаемое имя файла
    file_id = '17-YqKhB3twLHRn3cJgopg-5YopX4Oz1Y'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)


    url = 'https://drive.google.com/file/d/1y5IVdbPGsMEIpxzV0XcUZ38NSX0C3Pwh/view?usp=sharing'  # замените на нужную ссылку
    filename = 'glfw3.dll'  # замените на желаемое имя файла
    file_id = '1y5IVdbPGsMEIpxzV0XcUZ38NSX0C3Pwh'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1qMI212q3_R9-IW9n5113gZlrN6bQIJwU/view?usp=sharing'  # замените на нужную ссылку
    filename = 'glewinfo.exe'  # замените на желаемое имя файла
    file_id = '1qMI212q3_R9-IW9n5113gZlrN6bQIJwU'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1H-SV5h2Q6nV_6jSZD4yL0ozVuAZdKvy4/view?usp=sharing'  # замените на нужную ссылку
    filename = 'glew32.dll'  # замените на желаемое имя файла
    file_id = '1H-SV5h2Q6nV_6jSZD4yL0ozVuAZdKvy4'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1uWDAvw8hIDgM3UA8hrCWFDZJ4jAspAub/view?usp=sharing'  # замените на нужную ссылку
    filename = 'freeglut.dll'  # замените на желаемое имя файла
    file_id = '1uWDAvw8hIDgM3UA8hrCWFDZJ4jAspAub'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1ugUk0poWCGJikdznR5AFS1MltDcq0dVl/view?usp=sharing'  # замените на нужную ссылку
    filename = 'DataVisualization.pdb'  # замените на желаемое имя файла
    file_id = '1ugUk0poWCGJikdznR5AFS1MltDcq0dVl'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/106qRdcaADqXXArFpdeOTlKb8-Y410mrG/view?usp=sharing'  # замените на нужную ссылку
    filename = 'DataVisualization.lib'  # замените на желаемое имя файла
    file_id = '106qRdcaADqXXArFpdeOTlKb8-Y410mrG'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)

    url = 'https://drive.google.com/file/d/1nZvDfvulQlR2_OHuf3JxthTa4jtM2llu/view?usp=sharing'  # замените на нужную ссылку
    filename = 'DataVisualization.exp'  # замените на желаемое имя файла
    file_id = '1nZvDfvulQlR2_OHuf3JxthTa4jtM2llu'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)

    url = 'https://drive.google.com/file/d/16ojngQF7uGIgO2VRfFo1pgEGD0Q17er_/view?usp=sharing'  # замените на нужную ссылку
    filename = 'DataVisualization.exe'  # замените на желаемое имя файла
    file_id = '16ojngQF7uGIgO2VRfFo1pgEGD0Q17er_'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)
    
    url = 'https://drive.google.com/file/d/1JQ1xVpgC85zg_eANecg6FdcYWsmL4dgW/view?usp=sharing'  # замените на нужную ссылку
    filename = 'data/Shaders/BackgroundFragment.glsl'  # замените на желаемое имя файла
    file_id = '1JQ1xVpgC85zg_eANecg6FdcYWsmL4dgW'
    gdown.download(f'https://drive.google.com/uc?id={file_id}', filename, quiet=False)

    print("The download of DataAnaliticVisor was successful. To get started, write RUN_DAV()")
