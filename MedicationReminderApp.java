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
        ReminderThread reminderThread = new ReminderThread(medList, timeList);
        reminderThread.start();
    }
static class ReminderThread extends Thread {
    private final ArrayList<String> medList;
    private final ArrayList<Integer> timeList;

    public ReminderThread(ArrayList<String> medList, ArrayList<Integer> timeList) {
        this.medList = medList;
        this.timeList = timeList;
    }

    @Override
    public void run() {
        for (int i = 0; i < medList.size(); i++) {
            try {
                long waitTime = timeList.get(i) * 60000L; 
                Thread.sleep(waitTime); 
                System.out.println("Reminder: It's time to take your medication: " + medList.get(i) + "!");
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break; 
            }
        }
      }
    }
}
