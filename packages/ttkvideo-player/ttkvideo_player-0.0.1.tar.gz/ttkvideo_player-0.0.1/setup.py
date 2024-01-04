from setuptools import setup,find_packages

classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='ttkvideo_player',
    version='0.0.1',
    description='playing video (with audio) in tkinter label',
    long_description='readme.md',
    long_description_content_type='text/markdown',
    author='Coder-wis',
    author_email='vishalsharma.pypi@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['video-player','player','video','python','tkinter video player','tkinter video','ctk video','customtkinter'],
    packages=find_packages(),
    python_requires = ">=3.6",
    Homepage = "https://github.com/Coder-wis/ttkvideo_player/",
    Issues = "https://github.com/Coder-wis/ttkvideo_player/issues/"
)