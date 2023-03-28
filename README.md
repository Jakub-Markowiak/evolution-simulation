# evolution-simulation
Simple evolution simulation algorithm written in `Python`. Data analysis is performed using `R` with `Quarto`. More detailed information can be found in summary report: `reporting/summary/summary.html`.

### Instructions
Follow the steps below to run the project on your local device and reproduce  results (Windows syntax):

1. Download and install [`Python 3.9`](https://www.python.org/downloads/release/python-390/)
2. Download and install most recent [`R`](https://www.r-project.org) distribution
3. Download and install most recent [`Quarto`](https://quarto.org) version
4. Recommended IDE: [`Visual Studio Code`](https://code.visualstudio.com)
5. Clone repository: `git clone git@github.com:Jakub-Markowiak/evolution-simulation.git` (or download manually and extract to specific location)
6. Create virtual `python` environment and install required packages. Open command line and type:
```
cd evolution-simulation
python -m venv .evolution-simulation
```
7. Activate virtual environment in VSCode terminal and install required packages:
```
./.evolution-simulation/Scripts/activate.bat
pip install -r ./requirements.txt
```
8. 
    Run `reporting/summary/summary.qmd` to generate dynamic report. Run `python` cells manually to generate new simulation data. 

    **Warning**: new data generation may take up to **2** hours!

