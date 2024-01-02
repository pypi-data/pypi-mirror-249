from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="vnnlib._tokenizer",
            sources=["vnnlib/_tokenizer.c"],
        ),
    ]
)
