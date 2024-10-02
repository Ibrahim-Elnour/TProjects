import java.util.*;

public class MedicationReminderApp {
    static Scanner scanner = new Scanner(System.in);
    public static void main(String[] args) {
        captureMedications();
    }

    static void captureMedications() {
        boolean addList = false;
        ArrayList<String> medList = new ArrayList<>();
        ArrayList<Integer> timeList = new ArrayList<>();
        do {
            System.out.println("Please enter a medication");
            String medication = scanner.nextLine();
            medList.add(medication);
            System.out.println("Please enter a # of minutes to be waited before the reminder alerts.");
            int time = scanner.nextInt();
            scanner.nextLine();
            timeList.add(time);
            System.out.println("Would you like to add any more reminders? (Y/N)");
            String addMore = scanner.nextLine();
            if (addMore.equalsIgnoreCase("Y")) {
                addList = true;
            } else {
            addList = false;
            }

        } while (addList);
        System.out.println("Medications added.");
        // helped past here
        ReminderThread reminderThread = new ReminderThread(medList, timeList);
        reminderThread.start();
    }
    // need to parse time var for float and pass val as argument into thread.sleep method
    // step one parse time var into a readable int format
    // pass into thread.sleep
    // Custom thread class extending Thread
static class ReminderThread extends Thread {
    private final ArrayList<String> medList;
    private final ArrayList<Integer> timeList;

    // Constructor
    public ReminderThread(ArrayList<String> medList, ArrayList<Integer> timeList) {
        this.medList = medList;
        this.timeList = timeList;
    }

    // Override the run method
    @Override
    public void run() {
        for (int i = 0; i < medList.size(); i++) {
            try {
                // Convert minutes to milliseconds (1 minute = 60000 milliseconds)
                long waitTime = timeList.get(i) * 60000L; 
                Thread.sleep(waitTime); // Sleep before showing the reminder
                System.out.println("Reminder: It's time to take your medication: " + medList.get(i) + "!");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break; // Exit if the thread is interrupted
            }
        }
      }
    }
}