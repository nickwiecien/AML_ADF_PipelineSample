# Azure ML Pipeline/Azure Data Factory Sample
This repo contains sample code for creating an Azure Machine Learning pipeline that saves outputs to an AML-linked blob store can be readily adapted for batch scoring. Below we include instructions for deploying the pipeline in an Azure ML workspace, and configuring an Azure Data Factory pipeline to regularly execute this pipeline and copy results from the AML-linked blob store into an Azure SQL Database

## Azure Machine Learning Setup

The instructions below assume you have provisioned an Azure Machine Learning workspace and a Compute Instance within this workspace. You can clone the code within this repo to your workspace by executing the following command in a terminal.

```
git clone https://https://github.com/nickwiecien/AML_ADF_PipelineSample
```

After cloning this repo execute the notebooks `01_Demo_Env_Setup.ipynb` and `02_AML_Pipeline_Setup.ipynb` in sequence. <i>Note: In order to run all steps of this demo you will need access to an Azure SQL database which you can use SQL Authentication to log into. There is a section in the `01` notebook which contains a pyodbc snippet for creating a new table.</i>

Once you have run both notebooks you should see an Azure Machine Learning pipeline named 'Sample Scoring Pipeline' available under your Pipeline Endpoints tab.

