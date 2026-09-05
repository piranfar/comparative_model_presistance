README FILE 
COMPLETE_DATA_1_2_EXP_06.csv:
This csv file holds E. coli strain MG1655 information on the Age at death, the experiment number, the line (unique growth channel) of the microfluidic device, the Ampicillin concentration (applied recurrently), the image (x-y position the microscope took images at; i.e. field of view), and the growth rate, division events and cell size, as well as the age at death information on 2598 individual cells (rows). Size measurements from onset of the experiment to the end of the experiment is provided in columns 7:356; Growth rates of each cell is reported in columns 358:706; Divisions (coded as 1 when a division is observed) are reported in Columns 707:1056. Time steps are 4 Minute intervals. Sequences of NA in a row indicate that the cell has died.  
For the growth rate data analyses, we excluded measurements of unrealistic shrinkage or growth, that is, growth of cells that shrank more than 0.8 or grew more than 1.4, these measurements were replaced with NA. 
All cell sizes >450 were set to NA as such large cells are not feasible.

Oikos_MG1655-deathrates.csv:
This csv file contains combined survival data of 899 cells for E. coli strain MG1655 without any antibiotics. The data has been collected using a microfluidic device, called the mother machine. The discrete time step is 4 min. “ID” determines the time step (each row one four minute time step), “dx” provides number cells dying between two consecutive time steps, “surv” provides number of surviving cells, “lx” number of alive cells at each time step, age in minutes, “qx” probability of dying at interval, “sx” survival probability to age x, m.av is the moving average, prop.cells provides the percentage of cells.

CON128deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 128 ?g/ml Ampicillin.

CON64deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 64 ?g/ml Ampicillin.
CON32deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 32 ?g/ml Ampicillin.
CON24deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 24 ?g/ml Ampicillin.
CON16deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 16 ?g/ml Ampicillin.
CON4deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 4 ?g/ml Ampicillin.

CON2deathrate_07.csv:
Time after start of experiment and death rate at that time for recurrent exposure experiment at 2 ?g/ml Ampicillin.

Oikos_longdata-div.csv:
This csv file contains division rate data of 1017 cell for E. coli strain MG1655 without any antibiotics. Only the MG1655 cells were used for analyses, so data was subsetted to these data, and only up to the end of the experiment the data was selected (v1<1400). For the analysis only the age at death (ToD), the age (V1/3) and the Div, divisions were used. 

R long data Alex and Sara CFU counts.csv:
This csv file contains colony forming unit data for E. coli strain MG1655 with recurrent exposure to antibiotics. Time is the sampling number, TimeMin is the time during the experiment the sampling was done, Column is the column in the 96 well plate, each column had one concentration of antibiotics, Conc is the antibiotic concentration applied recurrently, Replicates_Row is the replicate, each row in a 96 well plate was one replicate, N_of_colonies is the number of colonies counted, Dilution_factor is how much the sample to be evaluated has been diluted, Vol_plated_mL is the volume that has been plated to count CFU, CFU_mL are the number of colony forming units per mL.

Kopie von Uli ampi-killing-curve.csv:
This csv file contains optical density measurements (OD_600) for E. coli strain MG1655 at constant levels of antibiotics. Measurements (Time) were done every 20 minutes for 24 hours. The temperature was automatically recorded (Temp). Each column A1:H9 was one treatment and replicate combination. The values are the OD. Column letters identify which replicate within a 96 well plate column the measurement was taken from, the Column Number identifies the concentration. Column labels containing a 1 were exposed to concentrations of 128 ?g/ml Ampicillin. Column labels containing a 1 were exposed to concentrations of 128 ?g/ml Ampicillin. Column labels containing a 2 were exposed to concentrations of 64 ?g/ml Ampicillin. Column labels containing a 3 were exposed to concentrations of 32 ?g/ml Ampicillin. Column labels containing a 4 were exposed to concentrations of 16 ?g/ml Ampicillin. Column labels containing a 5 were exposed to concentrations of 8 ?g/ml Ampicillin. Column labels containing a 6 were exposed to concentrations of 4 ?g/ml Ampicillin. Column labels containing a 7 were exposed to concentrations of 2 ?g/ml Ampicillin. Column labels containing a 8 were exposed to concentrations of 0 ?g/ml Ampicillin. Column labels containing a 9 were Negative Control, i.e., no bacteria added to medium. For instance, A1 is the first replicate for 128 ?g/ml Ampicillin, B1 is the second replicate for 128 ?g/ml Ampicillin, etc. 




