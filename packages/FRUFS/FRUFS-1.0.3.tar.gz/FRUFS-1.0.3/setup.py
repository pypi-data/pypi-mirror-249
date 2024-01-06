import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

    
setuptools.setup(
     name = 'FRUFS',  
     version = '1.0.3',
     author = "Atif Hassan",
     author_email = "atif.hit.hassan@gmail.com",
     description = "FRUFS stands for Feature Relevance based Unsupervised Feature Selection and is an unsupervised feature selection technique using supervised algorithms such as XGBoost",
     long_description = long_description,
     long_description_content_type = "text/markdown",
     url = "https://github.com/atif-hassan/FRUFS",
     py_modules = ["FRUFS"],
     install_requires = ["pandas", "scikit-learn", "numpy", "joblib", "matplotlib", "seaborn", "tqdm"],
     include_package_data = True,
     classifiers = [
         "Programming Language :: Python :: 3",
         "Programming Language :: Python :: 3.6",
         "Programming Language :: Python :: 3.7",
         #"License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ]
 )
