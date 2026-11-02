from setuptools import find_packages, setup

package_name = 'dynamic_obstacle_avoidance'

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
            'lidar_obstacle_detector = dynamic_obstacle_avoidance.lidar_obstacle_detector:main',
            'tracked_lidar_detector = dynamic_obstacle_avoidance.tracked_lidar_detector:main',
        ],
    },
)
