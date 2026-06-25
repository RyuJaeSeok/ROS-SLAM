import os
from glob import glob

from setuptools import find_packages, setup

package_name = '6_localize_map'


def package_files(directory):
    paths = []
    for path, _, filenames in os.walk(directory):
        files = [os.path.join(path, filename) for filename in filenames]
        if files:
            paths.append((os.path.join('share', package_name, path), files))
    return paths


setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
        ('share/' + package_name + '/worlds', glob('worlds/*.world')),
        ('share/' + package_name + '/map', glob('map/*')),
        ('share/' + package_name + '/config', glob('config/*')),
    ] + package_files('models'),
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user08',
    maintainer_email='user08@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'simple_yaw_oa = 6_localize_map.simple_yaw_oa:main',
            'random_moition = 6_localize_map.random_moition:main',
            'initial_pose_pub = 6_localize_map.initial_pose_pub:main',
        ],
    },
)
