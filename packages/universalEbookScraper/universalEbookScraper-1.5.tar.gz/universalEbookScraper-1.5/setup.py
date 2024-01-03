from setuptools import setup, find_packages


setup(
    name='universalEbookScraper',
    version='1.5',
    scripts=['universalEbookScraper.py'],
    license='MIT',
    author="Gianni135",
    url='https://github.com/Gianni135/universalEbookScraper',
    keywords='scraper, ebook, universa, pdf',
    install_requires=[
          'Pillow==10.1.0',
          'PyAutoGUI==0.9.54'
      ],

)