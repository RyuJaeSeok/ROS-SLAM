from setuptools import find_packages, setup

package_name = '4_avoild_obstacle'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
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
            "lidar_listener = 4_avoild_obstacle.lidar_listener:main",
            "avoid_processor = 4_avoild_obstacle.avoid_processor:main",
        ],
    },
)
