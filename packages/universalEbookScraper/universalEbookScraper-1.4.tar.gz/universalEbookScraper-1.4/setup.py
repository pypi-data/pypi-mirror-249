from setuptools import setup, find_packages


setup(
    name='universalEbookScraper',
    version='1.4',
    scripts=['src/universalEbookScraper.py'],
    license='MIT',
    author="Gianni135",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Gianni135/universalEbookScraper',
    keywords='scraper, ebook, universa, pdf',
    install_requires=[
          'Pillow==10.1.0',
          'PyAutoGUI==0.9.54'
      ],

)