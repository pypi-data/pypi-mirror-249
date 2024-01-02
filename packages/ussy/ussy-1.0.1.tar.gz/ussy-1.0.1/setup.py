from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='ussy',
      version='1.0.1',
      description='Funny little ussifier.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ellipse-liu/ussy',
      author='Timothy-Liu',
      author_email='timothys.new.email@gmail.com',
      license='MIT',
      packages=['ussy'],
      package_data={'eng_syl': ['*.pkl', '*.h5']},
      install_requires=[
          'eng-syl'
      ],
      keywords=['Ussy'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
      ],
      zip_safe=False)
