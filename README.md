# Azure ML Pipeline/Azure Data Factory Sample

This repo contains sample code for creating an Azure Machine Learning pipeline that saves outputs to an AML-linked blob store can be readily adapted for batch scoring. Below we include instructions for deploying the pipeline in an Azure ML workspace, and configuring an Azure Data Factory pipeline to regularly execute this pipeline and copy results from the AML-linked blob store into an Azure SQL Database

## Setting up your Virtual Environment

### Azure Machine Learning

A requirements.txt file is included with then necessary packages that need to be installed in your working environment. To install these packages you can execute a command line argument from your notebook cell by entering `% pip install -r requirements.txt`.

### VS Code

A vscode_environment.yml file is included in this repository for creating a virtual environment for this projects. You can create a conda environment using the terminal in vs code using the following commands: `conda create -n name_of_env -y` and then you need to activate the environment by entering the next set of commands `conda activate name_of_env` and then follow up with the last set by entering  `conda env update --name name_of_env --file vscode_environment.yml`. This will install the proper version of python for the environment and all of the conda and pip packages.

### Cloning the code into your project

The instructions below assume you have provisioned an Azure Machine Learning workspace and a Compute Instance within this workspace. You can clone the code within this repo to your workspace by executing the following command in a terminal.

```
git clone https://https://github.com/nickwiecien/AML_ADF_PipelineSample
```

After cloning this repo execute the notebooks `01_Demo_Env_Setup.ipynb` and `02_AML_Pipeline_Setup.ipynb` in sequence. `<i>`Note: In order to run all steps of this demo you will need access to an Azure SQL database which you can use SQL Authentication to log into. There is a section in the `01` notebook which contains a pyodbc snippet for creating a new table. `</i>`

Once you have run both notebooks you should see an Azure Machine Learning pipeline named 'Sample Scoring Pipeline' available under your Pipeline Endpoints tab.

![Published Pipeline Endpoint](img/img01.png?raw=true "Published Pipeline Endpoint")

## Azure Data Factory Pipeline Setup

### Update Linked Services

Inside your Azure Data Factory workspace, create linked services for Azure Machine Learning, the associated Default Datastore (Azure Storage Account), and the target Azure SQL Database. Instructions for creating linked services [can be found here](https://docs.microsoft.com/en-us/azure/data-factory/concepts-linked-services).

- AML_Workspace (Azure ML Workspace)
- AML_BlobStore (Azure ML-Linked Storage Account)
- AzSQLDB (Azure SQL Database)

![Azure Data Factory Linked Services](img/img02.png?raw=true "Azure Data Factory Linked Services")

### Create Datasets

Create a new dataset inside ADF from your linked `AML_BlobStore` account - select 'Delimited text' under file options. Configure your dataset to read from the default blobstore location (should have syntax like `azureml-blobstore-xxxxxxxxxxxx...`) and the `scored_data` subdirectory.

![CSV Dataset](img/img03.png?raw=true "CSV Dataset")

Create a new dataset from your linked `AzSQLDB` database pointing at the `dbo.mydata` table created in your execution of the attached notebooks.

![SQL Dataset](img/img04.png?raw=true "SQL Dataset")

### Create ADF Pipeline

Create a new ADF pipeline and before adding any steps configure a pipeline variable called `filename`. Set the type as 'string' and default value as 'test_file.csv'.

![Pipeline Variable](img/img05.png?raw=true "Pipeline Variable")

Add a 'Set variable' step to your pipeline. Under the settings listed under the 'Variables' tab select the `filename` variable and add the following as dynamic content:

```
@concat(formatDateTime(convertTimeZone(utcNow(),'UTC','Eastern Standard Time'),'yyyyMMddHHmmss'), '.csv')
```

![Set Variable](img/img06.png?raw=true "Set Variable")

As a second step, add a 'Machine Learning Execute Pipeline' step. Under the settings tab, select your linked AML workspace resource, select the 'Pipeline endpoint ID' and nagivate to 'Sample Scoring Pipeline.' Under the 'Machine Learning pipeline parameters' section, add a single key-value pair with `filename` as the key, and `@variables('filename') as the value. This will effectively pass the pipeline variable set in the previous step into your AML pipeline.

![Machine Learning Execute Pipeline](img/img07.png?raw=true "Machine Learning Execute Pipeline")

As a final step, add a 'Copy data' step. Here we will configure the file written by the AML pipeline to the linked datastore as a source, and the Azure SQL DB table as a sink.

Under 'Source' select your configured CSV dataset as a source. Under File path type, select 'Wilecard file path' and enter the default blob storage container + `scored_data` + `@variables('filename')` as your effective path.

![Configure Source](img/img08.png?raw=true "Configure Source")

Under 'Sink' select your Azure SQL Database table dataset as a sink dataset. Under Write behavior select 'Insert.'

![Configure Sink](img/img09.png?raw=true "Configure Sink")

Finally, under 'Mapping' you can either manually update mapping or upload samples and complete a link between columns as shown below.

![Configure Mapping](img/img10.png?raw=true "Configure Mapping")

Once complete, click 'Publish all' to save changes to your pipeline. Once completed configure your pipeline to run on a regular schedule.

![Configure Schedule](img/img11.png?raw=true "Configure Schedule")
