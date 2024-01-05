import setuptools 
  
setuptools.setup( 
    name="cv_sample_package", 
    version="0.0.1", 
    author="Arulvadivel S", 
    author_email="arulvadivel@cloudvalleytech.com", 
    description="A sample test package", 
    long_description="Package to Encrypt and Decrypt", 
    long_description_content_type="text/markdown",
    packages=["cv_sample_package"],
    python_requires='>=3.8', 
    install_requires=[
        'pycryptodome>=3.19.1',
    ] 
)