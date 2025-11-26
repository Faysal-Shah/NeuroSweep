from setuptools import find_packages, setup

package_name = 'neuro_analytics'

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
    maintainer='engineer',
    maintainer_email='shahfaysal6969@gmail.com',
    description='NeuroSweep Analytics Package',
    license='MIT',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'heatmap_node = neuro_analytics.heatmap_node:main',
        ],
    },
)
