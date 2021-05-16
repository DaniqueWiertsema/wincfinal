Three technical elements

#1 Use of parsing
The usage of parsing and especially the help function, makes it easy for users to understand the possibilities of the application. By using the --help command it offers an overview of all of them. I have used categories (parsers with subparsers) to structure these possibilities. In the beginning I found it hard to distinguish between arguments (for example today or yesterday), but by adding 'action=store true' I could write the actions the application has to do for every argument. 

#2 Use of pandas
Although pandas must be installed by the user (using pip), it made my code way easier to understand. Because pandas use dataframes and are - in my opinion - easier to interpret. I faced many difficulties comparing certain cells to each other. By creating a df I was able to do it in a more intuitive way. This was especially useful for creating a bar chart, because pandas offers the possibility to "groupby" a certain set group. 

#3 Export to Excel and CSV
Although CSVs are mostly read within the Excel-application. I integrated the possibility to export reports to Excel. In this way, the user doesn't need to split the data anymore, as Excel puts every data aspect in a loose column. The standard export, however, goes to .csv. This is because this option probably works well for users with a bit more knowledge. 
