/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package schedulingkitt;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.logging.Level;
import java.util.logging.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 *
 * @author Duarte
 */
public class SchedulingKITT {

    //Converts a Date into a double in seconds
    //This function takes a Date object as an argument and returns the number of seconds
    //since the Unix epoch (January 1, 1970, 00:00:00 GMT) as a double value. 
    //The getTime method of the Date class returns the number of milliseconds since
    //the Unix epoch, which is then divided by 1000.0 to convert it to seconds.
    public static double dateToSeconds(Date startDate, Date deadline){
        
         return (double) (deadline.getTime() - startDate.getTime()) / 1000.0;
    }
    
    //Converts a double in seconds into a Date
    //This function takes a double value in seconds as an argument and returns a Date 
    //object. The double value is first multiplied by 1000 to convert it to milliseconds
    public static Date secondsToDate(double deadline){
        return new Date((long)(deadline * 1000.0));
    }
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        
        BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
        String jsonInput = "";
        try {
            jsonInput = reader.readLine();
            
            jsonInput = jsonInput.replace("\"", "'");
            
            //System.out.print(jsonInput);
            
        } catch (IOException e) {
            System.out.print("Error reading input!");
        }
        
        HashMap<String, Resource> resourcesList = new HashMap<>();
        
        // ------Manage data------
        
        //String from broker
        //WARNING: Cannot be white spaces between elements. E.g. "'74104345-4eab-415f-a630-6bc52996534a','Product'" instead of "'74104345-4eab-415f-a630-6bc52996534a', 'Product'"
        //String input = "{'Productions': [{'Production': '74104345-4eab-415f-a630-6bc52996534a','Product': 'GARRAFA 800 ML CRISTAL TRITAN','Quantity': 10000,'Deadline': '2023-01-26 16:35:47+00:00','Machines': 'Nissei ASB 12M 3','CycleTimes': '20.00000'}, {'Production': '775601ea-e71b-4239-82a7-9a68c21bb1f9','Product': 'CAP BOTTOM MH500','Quantity': 5000,'Deadline': '2023-01-27 16:02:52+00:00','Machines': 'Negri Bossi','CycleTimes': '50.70000'}, {'Production': '88dcf7c0-2198-4a45-9573-090bef780107','Product': 'GARRAFA 800 ML CRISTAL ECOZEN','Quantity': 5000,'Deadline': '2023-01-27 14:02:04+00:00','Machines': 'Nissei ASB 12M 4','CycleTimes': '20.00000'}, {'Production': '9b2acd8f-a094-47e5-acaf-60a8e34335c5','Product': 'GARRAFA 800 ML CRISTAL ECOZEN','Quantity': 1000,'Deadline': '2023-01-27 17:50:32+00:00','Machines': 'Nissei ASB 12M 3','CycleTimes': '20.00000'},{'Production': '9470d998-3af6-435e-8980-ed4e8d880c05','Product': 'GARRAFA 800 ML CRISTAL ECOZEN','Quantity': 1000,'Deadline': '2023-01-28 16:08:43+00:00','Machine': 'Nissei ASB 12M 3','CycleTime': '20.00000'}]}";
        
        /*String input1 = "{'Productions': [{'Production': '74104345-4eab-415f-a630-6bc52996534a', 'Product': 'GARRAFA 800 ML CRISTAL TRITAN', 'Quantity': 10000, 'Deadline': '2023-01-26 16:35:47+00:00', 'Machines': 'Nissei ASB 12M 3', 'CycleTime': '20.00000'},"
                + "{'Production': '775601ea-e71b-4239-82a7-9a68c21bb1f9', 'Product': 'GARRAFA 800 ML CRISTAL TRITAN', 'Quantity': 5000, 'Deadline': '2023-01-27 16:02:52+00:00', 'Machines': 'Nissei ASB 12M 3', 'CycleTime': '55.70000'},"
                + "{'Production': '88dcf7c0-2198-4a45-9573-090bef780107', 'Product': 'GARRAFA 800 ML CRISTAL ECOZEN', 'Quantity': 5000, 'Deadline': '2023-01-27 14:02:04+00:00', 'Machines': 'Nissei ASB 12M 4', 'CycleTime': '15.00000'},"
                + "{'Production': 'ffdcf7c0-2198-4a45-9573-090bef780107', 'Product': 'GARRAFA 800 ML CRISTAL ECOZEN', 'Quantity': 5000, 'Deadline': '2023-01-27 14:02:04+00:00', 'Machines': 'Nissei ASB 12M 4', 'CycleTime': '44.00000'},"
                + "{'Production': 'xcdcf7c0-2198-4a45-9573-090bef780107', 'Product': 'GARRAFA 800 ML CRISTAL ECOZEN', 'Quantity': 2000, 'Deadline': '2023-01-27 14:02:04+00:00', 'Machines': 'Nissei ASB 12M 4', 'CycleTime': '44.00000'},"
                + "{'Production': 'hsdff7c0-2198-4a45-9573-090bef780107', 'Product': 'CAP BOTTOM MH500', 'Quantity': 2000, 'Deadline': '2023-01-27 14:02:04+00:00', 'Machines': 'Negri Bossi', 'CycleTime': '33.00000'},"
                + "{'Production': '9b2acd8f-a094-47e5-acaf-60a8e34335c5', 'Product': 'CAP BOTTOM MH500', 'Quantity': 1000, 'Deadline': '2023-01-27 17:50:32+00:00', 'Machines': 'Negri Bossi', 'CycleTime': '20.00000'}]}";    //,{'Production': '9470d998-3af6-435e-8980-ed4e8d880c05','Product': 'GARRAFA 800 ML CRISTAL ECOZEN','Quantity': 1000,'Deadline': '2023-01-28 16:08:43+00:00','Machine': 'Nissei ASB 12M 4','CycleTime': '20.00000'}]}";
        String input = input1.replace(", ", ",");*/
        
        
        String input = jsonInput;
        
        Task task;
        Resource resource = null;
                
        //Split string to get all production orders in a list
        String[] results = input.split("[{}]", 0);
        ArrayList<String> cleanInput = new ArrayList<String>();
        int r = 0;
        while(results.length > r){
            if(results[r].length() > 30)
                cleanInput.add(results[r]);
            r++;
        }
        
        for(int i = 0; i < cleanInput.size(); i++){
            String taskId = "";
            String resourceId = "";
            String associatedProduct = "";
            int quantity = -1;
            double cycleTime = -1;
            SimpleDateFormat formatter = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss+00:00"); //2023-01-26 16:35:47+00:00
            //Date deadline;
            double deadlineDouble = -1;
            Date deadlineDate = null;
            Date startDate = null;
            try {
                startDate = formatter.parse("2023-01-24 00:00:00+00:00");
            } catch (ParseException ex) {
                Logger.getLogger(SchedulingKITT.class.getName()).log(Level.SEVERE, null, ex);
            }
            
            String[] strOrders = cleanInput.get(i).split("[,]", 0);
            int q = 0;
            while(strOrders.length > q){                
                //Remove quotes
                strOrders[q] = strOrders[q].replaceAll("'", "");
                //Split string in key and value
                String[] strProduction = strOrders[q].split(" ", 2);
                //Remove : from key
                strProduction[0] = strProduction[0].replaceAll(":", "");
                                
                switch(q) {
                    case 0:
                      taskId = strProduction[1];
                      break;
                    case 1:
                      associatedProduct = strProduction[1];
                      break;
                    case 2:
                      quantity = Integer.parseInt(strProduction[1]);
                      break;
                    case 3:
                        {
                            try {
                                deadlineDate = formatter.parse(strProduction[1]);
                            } catch (ParseException ex) {
                                Logger.getLogger(SchedulingKITT.class.getName()).log(Level.SEVERE, null, ex);
                            }
                            
                            //deadline = Double.parseDouble(strProduction[1]);
                            deadlineDouble = dateToSeconds(startDate, deadlineDate);
                        }
                      break;
                    case 4:                  
                      resourceId = strProduction[1];
                      //System.out.println("Resource ID being parsed" + " -> " + resourceId);
                      
                      break;
                    case 5:
                      cycleTime = Double.parseDouble(strProduction[1]);
                      break;
                    default:
                        System.err.println("Too many parameteres in JSON string");
                        System.exit(0);
                }
                
                q++;
            }
            
            //Create resource if there isn't yet
            if(!resourcesList.containsKey(resourceId)){
                
                resource = new Resource(resourceId);
                resourcesList.put(resource.getId(), resource);
                
            }
            //else{
                
            //    resourcesList.put(resource.getId(), resource);
               
            //}
            
     
            //Create task
            task = new Task(taskId, associatedProduct, resource, cycleTime, quantity, deadlineDouble);
            resourcesList.get(resource.getId()).getTasksList().add(task);
            ScheduleManager.addTask(task);
            
            System.out.println("");
            
        }

        // ------ End of Managing Json Data ------
        
        
        // Initialize population
        Population pop = new Population(50, true, resourcesList);
        //System.out.println("Initial makespan: " + pop.getFittest().getMakespan() + " fitness: " + pop.getFittest().getFitness());
        
        
        
        int x = 0;
        
        //for(x = 0; x < 10; x++ ) {
        //    System.out.println(pop.getSchedule(x));
        //}
        
        //SAVE THE FITTEST ONE
        //COMPARE THIS ONE WITH THE FITTEST WITHIN THE NEXT FOR LOOP
        Schedule fittest = pop.getFittest();
        
        // Evolve population for X generations
        //**WARNING: There must always be elitism (i.e. Crossover<1), otherwise 
        //the fittest solution will be lost, since it is not saved. It is kept 
        //on the top of the population when it is sorted by fittest**
        
        double previousMakespan = 0;
        for (int i = 0; i < 100; i++){
            pop = Algorithm.evolvePopulation(pop, resourcesList);
            
            //Estava !=, mas alterei para >, uma vez que só queremos soluções com fitness maior
            if(pop.getFittest().getFitness() > fittest.getFitness()){
                double makespan = pop.getFittest().getMakespan();
                double fitness = pop.getFittest().getFitness();
                //System.out.println("Generation " + i + " makespan: " + makespan + " fitness: " + fitness);
                fittest = pop.getFittest();
            }
            //previousMakespan = pop.getFittest().getMakespan();
        }
                
        //Para imprimir o fittest, é necessário correr o defineExecutionTimes() outra vez
        for(int i = 0; i < fittest.scheduleSize(); i++)
            fittest.getTask(i).setTaskAllocated(false);
        fittest.defineExecutionTimes();
        
        // Print final results
        /**
        System.out.println("Finished");
        System.out.println("Final makespan: " + fittest.getMakespan());
        System.out.println("Final fitness: " + fittest.getFitness());
        System.out.println("Solution: ");
        */
        System.out.print(fittest);
        //System.out.print(input);
        
        /**
        System.out.println("\nNissei ASB 12M 3: " + fittest.getResourcesList().get("Nissei ASB 12M 3").getMakespan() + "\n" + fittest.getResourcesList().get("Nissei ASB 12M 3"));
        System.out.println("Negri Bossi: " + fittest.getResourcesList().get("Negri Bossi").getMakespan() + "\n" + fittest.getResourcesList().get("Negri Bossi"));
        System.out.println("Nissei ASB 12M 4: " + fittest.getResourcesList().get("Nissei ASB 12M 4").getMakespan() + "\n" + fittest.getResourcesList().get("Nissei ASB 12M 4"));
        */ 
    }
    
    
    
}
