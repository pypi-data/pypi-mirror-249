from setuptools import setup, find_packages

setup(
    name="TransformerST",
    version="1.0.0",
    description="Innovative Super-Resolution in Spatial Transcriptomics- A Transformer Model Exploiting Histology Images and Spatial Gene Expression",
    author="Chris",
    author_email="zhaocy.research@gmail.com",
    packages=find_packages(),
    install_requires=[
        "anndata",
        "numpy",
        "opencv-python",
        "pandas",
        "python-louvain",
        "rpy2",
        "scanpy",
        "scipy",
        "seaborn",
        "torch",
        "torch-geometric",
        "torchvision",
        "tqdm",
        "umap-learn",
    ],
)
