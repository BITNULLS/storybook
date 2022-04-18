# General Checklist

- [ ] Think critically: Could this database update break backend or frontend code? If so, @ the issue creator, and start a conversation.

# Checklist for exporting the DDL to docs/499_Schema.sql

- [ ] Open **SQLDeveloper**
- [ ] Go to **Tools** menu from top
- [ ] Click on **Database Export** under **Tools** menu
- [ ] Select the name of our connection (*CISC498-EDU*) from the *Connection* drop down menu in the Step 1 of **Export Wizard**
- [ ] In that same step, uncheck *Show Schema* and *Storage* options (first two items in the last row of the first three rows under *Export DDL* checkbox)
- [ ] Uncheck *Export Data* option (beneath *Show Schema* and *Storage* options) as well in that same step. This would make sure that we don't include the data from the tables as part of final DDL
- [ ] Hit **Next**
- [ ] A warning pop-up dialog will open up and asking if we want to overwrite the existing .sql file in some directory. Say *Yes* in that pop-up box
- [ ] Step 2 of the **Export Wizard** is about selecting what objects (*Tables, Views, Sequences, etc.*) of our Database we want to export in our DDL. Uncheck everything except *Tables*, *Sequences*, *Indexes*, *Triggers*, *Procedures*, *Functions*, *Constraints*, and *Referential Constraints*. Those are all the things we want in our final DDL
- [ ] Hit **Next**
- [ ] Step 3 of the **Export Wizard** is choosing particular items(exactly what tables, sequences, triggers etc.) from the objects we chose in Step 2 of the wizard. We want all the items of the objects we chose in Step 2. So click on *Lookup* button (one with the binocular image) and wait until it loads all the items
- [ ] Click *blue color double arrow* button (*>>*) indicating that we want all the items of the DB objects in our final DDL. Clicking the button would push those items to the second part of window (right side of *>>*)
- [ ] Hit **Next**
- [ ] This is the final step of the **Export Wizard**. Do nothing and click **Finish**
- [ ] Depending on the number of objects and items of those objects we have in our DB, it would take some time before it loads our DDL. Eventually, we would get our DDL
- [ ] As a final step, add some comments to differentiate the DDL for the DB objects and edit the top of the file comment to match with what we used to have in our *499_Schema.sql* file. 
- [ ] Copy the complete DDL from SQL Editor to the *499_Schema.sql* file in the *docs* folder and completing the checklist

# Checklist for updating the docs/Schema_Diagram.png

- [ ] Open **SQLDeveloper**
- [ ] Go to **File** menu from top 
- [ ] Under **Data Modeler** and then **Import**, click on **Data Dictionary**
- [ ] The **Data Dictionary Import Wizard** will open up. As a Step 1 of the **Import Wizard**, click the *CISC498-EDU* as the *Connection Name* that should already be given
- [ ] Hit **Next** 
- [ ] You will be in the Step 2 of the **Import Wizard**. This step is about selecting a *Schema Name*. Type *kpelster* (or just first few letters) in the *Filter* box to easily retrieve our *Schema Name*. Select the checkbox next to *KPELSTER* 
- [ ] Hit **Next**
- [ ] You will be in the Step 3 of the **Import Wizard**. This step is about selecting objects to include in our final Schema Diagram. Select all the checkboxes that are given to include all the Tables in our final Schema Diagram
- [ ] Hit **Next**
- [ ] You will be in the Step 4 of the **Import Wizard**. You don't have to do anything in this step other than verifying that the DB Object imported is *Table* and it includes all the tables (Right now, it's *15* so *15* would be that value)
- [ ] Click **Close** in the final dialog box that opens up
- [ ] The Schema Diagram will get generated and opens in a new tab in SQL Editor
- [ ] Rearrange all the Tables in the Schema Diagram to properly see the relationship among those Tables
- [ ] After the rearrangement is done, minimize the Schema Diagram window to make everything fit to window 
- [ ] As a final step for this checklist, screenshot the Schema Diagram window and replace it with the one that's already in *docs* folder
