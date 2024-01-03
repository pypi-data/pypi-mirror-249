from setuptools import setup, find_packages

setup(
    name='hailstone_calculator',
    version='0.0.6',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='package for automatically measurement of facial features for loupes manufacturing',
    author='Daniel Fiuza & Ibrahim Animashaun',
    # install_requires=['mediapipe', 'numpy', 'matplotlib', 'pandas', 'plotly', 'Pillow', 'opencv-contrib-python', 'segment-anything', 'boto3', 'imageio[ffmpeg]', 'imageio[pyav]', 'dotenv'],
    # install_requires=['mediapipe', 'segment-anything', 'boto3', 'python-dotenv', 'statsmodels', 'imageio', 'protobuf>=3.11,<4'],
    # install_requires=[
    #     'mediapipe==0.8.9.1',
    #     'segment-anything==1.0',
    #     'boto3==1.26.126',
    #     'python-dotenv==1.0.0',
    # ]
    # package_data={
    #     # 'ipd_modules': ['model/sam_vit_h_4b8939.pth']
    #     'ipd': ['models/pose_landmarker.task']
        
    # }
)