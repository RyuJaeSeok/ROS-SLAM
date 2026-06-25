from setuptools import find_packages, setup

package_name = '1_pub_sub'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/pub_sub_launch.py']),
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
            "publisher = 1_pub_sub.publisher:main",
            "processor = 1_pub_sub.processor:main",
            "subscriber = 1_pub_sub.subscriber:main",
        ],
    },
)
