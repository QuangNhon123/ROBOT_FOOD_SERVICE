import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'dynamic_obstacle_demo'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
         (
        os.path.join(
            'share', package_name, 'models', 'moving_obstacle'
        ),
        glob('models/moving_obstacle/*.sdf')
    ),
        (
    os.path.join('share', package_name, 'launch'),
    glob('launch/*.launch.py')
         ),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ngan',
    maintainer_email='trannguyenthuyngancv@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
    'console_scripts': [
        'moving_obstacle = dynamic_obstacle_demo.moving_obstacle:main',
    ],
},
)
