from distutils.core import setup
setup(
  name = 'pySQLWrapper',         # How you named your package folder (MyLib)
  packages = ['pySQLWrapper'],   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A SQL wrapper library to make easy to build SQL interfaces',   # Give a short description about your library
  author = 'Lukas Grüdtner',                   # Type in your name
  author_email = 'lukasgrudtner@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/LukasGrudtner/sql-wrapper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/LukasGrudtner/sql-wrapper/archive/refs/tags/v0.1.tar.gz',    # I explain this later on
  keywords = ['SQL', 'SQL Wrapper', 'PostgreSQL'],   # Keywords that define your package best
  install_requires=[],            # I get to this in a second
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)