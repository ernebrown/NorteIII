# Combined Cycle Twin

## To setup on AWS Redhat 7 
- in AWS select AWS market place and search for RHEL 7 HVM
- Choose t2.large machine (8GB) or Larger
- In Security create a custom tcp and open port 8000
### Setup Docker on Redhat instance
-Get RHEL extras (those are needed to install docker)
```bash
sudo yum-config-manager --enable "Red Hat Enterprise Linux Server 7 Extra(RPMs)"
```
- Install Docker
```bash
sudo yum install docker -y
```
- Enable and start docker service
```bash
sudo systemctl enable docker
sudo systemctl start  docker
```
- Create a folder called cctwin
- Move cctwin project files under cctwin folder
- Go to to cctwin folder
```bash
cd cctwin
```
- Need to build docker instead of docker compose
```bash
sudo docker build -t cctwin:tag .
```
- Run docker to create container
```bash
sudo docker run -p 8000:8000 cctwin:tag
```
## Model building
- To generate models and save them as pickle files on your computer, please run all relevant files ending with "*model_build.ipynb"
- Clone/Download the repo to a directory on your computer.
- Open *Terminal* / *Command Prompt* / *PowerShell* in that directory.
- Activate your BASE python environment. Example, for **conda**:
```.bash
conda activate base
```
- Install **pipenv** environment by running:
```.bash
pip install pipenv
```
- Install all project dependencies by running following command:
```bash
pipenv install --ignore-pipfile
```
- To start the virtual environment:
```bash
pipenv shell
```

- Set up a git filter at global level to strip out outputs in jupyter notebooks for all git repos. (**Recommended**). For more information, visit: https://pypi.org/project/nbstripout/
```bash
nbstripout --install --global
```
- Set up a git filter to strip out outputs in jupyter notebooks for current git repo:
```bash
nbstripout --install --attributes .gitattributes
```

- start Jupyter Notebook in the virtual environment:

```bash
jupyter notebook
```
## Generate Models
- To generate models and save them as pickle files on your computer, please run all relevant files ending with "*model_build.ipynb"

## Running the tests
- To run all the tests in the project, run following command in your terminal in your project directory (CombinedCycleTwin directory):
```bash
py.test cctwin/tests
```
- To run tests in a specific file (*test_ctg8_base_load.py*), use following command as an example:
```bash
py.test cctwin/tests/ctg/test_ctg8_base_load.py
```
