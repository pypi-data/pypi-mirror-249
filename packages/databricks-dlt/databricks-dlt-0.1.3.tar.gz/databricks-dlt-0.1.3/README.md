# Python stub for Delta Live Tables

The Databricks Delta Live Tables (DLT) Python stub makes local development of DLT pipelines easier by:
* Providing API specs and docstring references for autocomplete features in IDEs.
* Providing Python data type hints to the library to enable type checking for DLT projects.

# Getting Started
This package is available on [PyPi](https://pypi.org/project/databricks-dlt/). To start your local DLT pipelines development, 
install the library with the following command: 

```
pip install databricks-dlt
```

In your local environment, `import dlt` to access the DLT module.

# Documentation

The `databricks-dlt` library is provided to help you write your DLT pipeline code in your local development environment. Because this library 
only has interfaces to the DLT Python API and does not contain any functional implementations, you cannot use this library to create or run a DLT pipeline locally. 

Instead, after you've finished writing your code, use one of the following methods to create and run a pipeline in your Databricks workspace:

* Copy your code to a databricks notebook, and create a new pipeline in the DLT UI. See [Run your first DLT Pipeline](https://docs.databricks.com/en/delta-live-tables/tutorial-pipelines.html).
* Use a Databricks repo or workspace files to store your code, and create a new pipeline in the DLT UI. See [Import Python modules from Databricks repos or workspace files](https://docs.databricks.com/delta-live-tables/import-workspace-files.html).
* Use the Databricks extension for Visual Studio Code to sync your local repository with your Databricks workspace. See [The Databricks extension for Visual Studio Code](https://docs.databricks.com/dev-tools/vscode-ext/index.html).
* Use a Databricks Asset Bundle (DAB) to manage, deploy, and run your pipeline from your local machine. See [Develop a DLT pipeline by using DABs](https://docs.databricks.com/delta-live-tables/tutorial-bundles.html).

To learn more about the DLT Python programming interface, see the [DLT Python language reference]( https://docs.databricks.com/en/delta-live-tables/python-ref.html).
# DB license

Copyright (2024) Databricks, Inc.

**Definitions.**

Agreement: The agreement between Databricks, Inc., and you governing the use of the Databricks Services, as that term is defined in the Master Cloud Services Agreement (MCSA) located at www.databricks.com/legal/mcsa.

Licensed Materials: The source code, object code, data, and/or other works to which this license applies.

**Scope of Use.** You may not use the Licensed Materials except in connection with your use of the Databricks Services pursuant to the Agreement. Your use of the Licensed Materials must comply at all times with any restrictions applicable to the Databricks Services, generally, and must be used in accordance with any applicable documentation. You may view, use, copy, modify, publish, and/or distribute the Licensed Materials solely for the purposes of using the Licensed Materials within or connecting to the Databricks Services. If you do not agree to these terms, you may not view, use, copy, modify, publish, and/or distribute the Licensed Materials.

**Redistribution.** You may redistribute and sublicense the Licensed Materials so long as all use is in compliance with these terms. In addition:

* You must give any other recipients a copy of this License;
* You must cause any modified files to carry prominent notices stating that you changed the files;
* You must retain, in any derivative works that you distribute, all copyright, patent, trademark, and attribution notices, excluding those notices that do not pertain to any part of the derivative works; and
* If a "NOTICE" text file is provided as part of its distribution, then any derivative works that you distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the derivative works.

You may add your own copyright statement to your modifications and may provide additional license terms and conditions for use, reproduction, or distribution of your modifications, or for any such derivative works as a whole, provided your use, reproduction, and distribution of the Licensed Materials otherwise complies with the conditions stated in this License.

**Termination.** This license terminates automatically upon your breach of these terms or upon the termination of your Agreement. Additionally, Databricks may terminate this license at any time on notice. Upon termination, you must permanently delete the Licensed Materials and all copies thereof.

**DISCLAIMER; LIMITATION OF LIABILITY.**

THE LICENSED MATERIALS ARE PROVIDED “AS-IS” AND WITH ALL FAULTS. DATABRICKS, ON BEHALF OF ITSELF AND ITS LICENSORS, SPECIFICALLY DISCLAIMS ALL WARRANTIES RELATING TO THE LICENSED MATERIALS, EXPRESS AND IMPLIED, INCLUDING, WITHOUT LIMITATION, IMPLIED WARRANTIES, CONDITIONS AND OTHER TERMS OF MERCHANTABILITY, SATISFACTORY QUALITY OR FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. DATABRICKS AND ITS LICENSORS TOTAL AGGREGATE LIABILITY RELATING TO OR ARISING OUT OF YOUR USE OF OR DATABRICKS’ PROVISIONING OF THE LICENSED MATERIALS SHALL BE LIMITED TO ONE THOUSAND ($1,000) DOLLARS.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE LICENSED MATERIALS OR THE USE OR OTHER DEALINGS IN THE LICENSED MATERIALS.