import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

requirements = ["numpy == 1.26.2", "sklearn == 1.2.1", "genser == 1.0.1"]

setuptools.setup(name="pamsbel",
	version="0.0.1",
	author="Sergei Zuev",
	author_email="shoukhov@mail.ru",
	description="A module for the multiple signals predictive analysis",
	packages=setuptools.find_packages(),
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
		"Programming Language :: Python :: 3.10",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.7',
)

#"License :: OSI Approved :: GNU", (in classifiers)
install_requires=requirements