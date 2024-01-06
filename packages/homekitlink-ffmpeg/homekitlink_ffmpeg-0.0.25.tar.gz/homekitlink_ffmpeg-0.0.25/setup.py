from setuptools import setup, find_namespace_packages, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# This function will collect all files within the specified directory
def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Call the function and specify the path to the binaries
binary_files = package_files('homekitlink_ffmpeg/ffmpeg_binaries')

print(f"{binary_files}")

setup(
    zip_safe=False,
    author='GlennNZ',
    description='Package providing FFmpeg binaries for specific system architectures, primarily for Indigo plugin usage',
    license='MIT',
    long_description=long_description,
    include_package_data=True,
    long_description_content_type="text/markdown",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # Instructing setuptools to include binary files found by MANIFEST.in
    package_data={
        'homekitlink_ffmpeg': ['ffmpeg_binaries/arm/*', 'ffmpeg_binaries/x86/*'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
    ],
    python_requires='>=3.10',
)