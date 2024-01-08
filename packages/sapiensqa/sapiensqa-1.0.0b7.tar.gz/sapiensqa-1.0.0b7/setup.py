from setuptools import setup, find_packages
from setuptools.command.install import install
from os import environ, path, listdir, remove, rename
from subprocess import call
from shutil import move

class CustomInstall(install):
    def run(self):
        try:
            if 'COLAB_GPU' not in environ and 'KAGGLE_KERNEL_RUN_TYPE' not in environ:
                install.run(self)
                install_dir = self.install_lib
                core_file_path = path.join(install_dir, 'sapiensqa', 'core.py')
                call(['python', '-m', 'compileall', core_file_path])
                pycache_dir = path.join(install_dir, 'sapiensqa', '__pycache__')
                for filename in listdir(pycache_dir):
                    if filename.startswith('core'):
                        pycache_file = path.join(pycache_dir, filename)
                        new_file_path = path.join(install_dir, 'sapiensqa', filename)
                        move(pycache_file, new_file_path)
                        new_file_name = path.join(install_dir, 'sapiensqa', 'core.pyc')
                        rename(new_file_path, new_file_name)
                        remove(core_file_path)
                        break
            else: install.run(self)
        except Exception as error:
            print(f'ERROR while compiling the installation core: {error}')
            install.run(self)

setup(
    name = 'sapiensqa',
    version = '1.0.0-beta07',
    author = 'SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=[
        'requests==2.31.0',
        'PyPDF2==3.0.1',
        'pdfplumber==0.10.2',
        'docx2txt==0.8',
        'beautifulsoup4==4.12.2'
    ],
    description = 'SapiensQA (Question and Answer) is a proprietary Machine Learning algorithm for creating Natural Language Processing models where the answers are previously known.',
    long_description = "The SapiensQA, or Sapiens for Questions and Answers, is a proprietary algorithm distributed freely for personal and/or commercial use. It is an Artificial Intelligence code that employs Machine Learning in creating expert language models. As an expert model, SapiensQA is focused on a single type of task, which is generating ready-made answers for predefined questions. Unlike Generative AI technologies like Transformers, SapiensQA doesn't use such approaches. Instead, it  applies a simple semantic comparison based on the Euclidean distance between input tokens to replicate the registered answer linked to the question that is geometrically closest to the user's prompt. This makes it much faster than generalist models and easily executable on machines with low processing power (1 core/4 GB or less of RAM memory) without the need for a GPU. It is ideal for the building customer service chatbots, query algorithms, systems for answering questions, and semantic search in files or documents.",
    url = 'https://github.com/sapiens-technology/SapiensQA',
    project_urls = {
        'Source code': 'https://github.com/sapiens-technology/SapiensQA',
        'Download': 'https://github.com/sapiens-technology/SapiensQA/archive/refs/heads/main.zip'
    },
        package_data={
        'sapiensqa': ['requirements.txt'],
    },
    license = 'Proprietary Software',
    keywords = 'Sapiens, Artificial Intelligence, Machine Learning, Natural Language Processing, AI, ML, NLP, ChatBot',
    cmdclass={'install': CustomInstall}
)
