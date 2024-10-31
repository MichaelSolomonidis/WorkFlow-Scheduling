import numpy as np
import matplotlib.pyplot as plt



def egreedy(n_machines, n_levers, n_tasks, apoklisi, epsilon=0.1):                  #ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΗΝ ΕΠΙΛΟΓΗ ΕΝΕΡΓΕΙΩΝ ΜΕΣΩ ΤΗΣ EGREEDY 
  rewards = np.random.normal (loc=0, scale=apoklisi, size=(n_machines, n_levers))   #ΔΗΜΙΟΥΡΓΙΑ ΑΝΤΑΜΟΙΒΩΝ
  q_values = np.zeros((n_machines, n_levers))                                       #ΑΡΧΙΚΟΠΟΙΗΣΗ ΠΙΝΑΚΑ q_values
  counts = np.zeros((n_machines, n_levers))                                         #ΑΡΧΙΚΟΠΟΙΗΣΗ ΠΙΝΑΚΑ counts
  total_r = np.zeros(n_tasks)                                                       #ΑΡΧΙΚΟΠΟΙΗΣΗ ΠΙΝΑΚΑ total_r


  for action in range(n_tasks):
    if np.random.random() < epsilon:                                                #TYXAIA ΕΠΙΛΟΓΗ 
      machine = np.random.randint(0, n_machines)
      lever = np.random.randint(0, n_levers)
    else:
      machine, lever = np.unravel_index(np.argmax(q_values), q_values.shape)


    reward = np.random.normal(loc=rewards[machine, lever], scale=apoklisi)          #ΥΠΟΛΟΓΙΣΜΟΣ ΑΝΤΑΜΟΙΒΗΣ
    counts[machine, lever] = counts[machine, lever] + 1                             
    q_values[machine, lever] = q_values[machine, lever] + (reward - q_values[machine, lever]) / counts[machine, lever]     #ΥΠΟΛΟΓΙΣΜΟΣ VALUES
    total_r[action] = reward                                                        #AΠΟΘΗΚΕΥΣΗ ΤΗΣ ΑΝΤΑΜΟΙΒΗΣ

  return np.cumsum(total_r)                                                         #ΕΠΙΣΤΡΟΦΗ ΟΛΩΝ ΤΩΝ ΑΝΤΑΜΟΙΒΩΝ 



def softmax(x):                                                                     #SOFTMAX ΓΙΑ ΚΑΝΟΝΙΚΟΠΟΙΗΣΗ
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()



def softmax_method(n_machines, n_levers, n_tasks, apoklisi, tau=0.1):               #ΕΠΙΛΟΓΗ ΕΝΕΡΓΕΙΩΝ ΜΕΣΩ SOFTMAX (ΣΥΝΑΡΤΗΣΗ) - ΟΤΙ ΕΚΑΝΑ ΚΑΙ ΓΙΑ ΤΗΝ EGREEDY
   rewards = np.random.normal (loc=0, scale=apoklisi, size=(n_machines, n_levers))  
   q_values = np.zeros((n_machines, n_levers))
   counts = np.zeros((n_machines, n_levers))
   total_r = np.zeros(n_tasks)


   for action in range(n_tasks):
      probabilities = softmax(q_values / tau)                                       #ΕΥΡΕΣΗ ΠΙΘΑΝΟΤΗΤΩΝ ΜΕΣΩ ΤΗΣ ΚΑΝΟΝΙΚΟΠΟΙΗΣΗΣ ΤΗΣ q_values Με tau
      flat_index = np.random.choice(n_machines * n_levers, p=probabilities.ravel()) #ΕΠΙΛΕΓΩ ΜΙΑ ΘΕΣΗ ΜΕ ΒΑΣΗ ΤΙΣ ΠΙΘΑΝΟΤΗΤΕΣ ΠΟΥ ΕΓΡΑΨΑ ΠΑΡΑΠΑΝΩ
      machine, lever = np.unravel_index(flat_index, (n_machines, n_levers))         
      reward = np.random.normal(loc=rewards[machine, lever], scale=apoklisi)
      counts[machine, lever] = counts[machine, lever] + 1
      q_values[machine, lever] = q_values[machine, lever] + (reward - q_values[machine, lever]) / counts[machine, lever]
      total_r[action] = reward

   return np.cumsum(total_r)



def results_plot(egreedy_antamives, softmax_antamives):                                #ΑΥΤΗ Η ΣΥΝΑΡΤΗΣΗ ΜΑΣ ΒΟΗΘΑΕΙ ΩΣΤΕ ΝΑ ΕΜΦΑΝΙΣΟΥΜΕ ΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ ΜΕΤΑΞΥ ΤΗΣ ΣΥΓΚΡΙΣΗΣ ΤΩΝ ΜΕΘΟΔΩΝ 
  plt.plot(egreedy_antamives, label="egreedy")
  plt.plot(softmax_antamives, label="softmax")
  plt.xlabel("ενεργειες")
  plt.ylabel("πληρωμή/κερδος")
  plt.legend()
  plt.show()




if __name__ == "__main__":                                                             #ΒΑΣΙΚΗ ΣΥΝΑΡΤΗΣΗ
  n_machines = int(input("δωστε τον αριθμο των μηχανηματων: "))
  n_levers = int(input("δωσε αριθμο μοχλων για καθε μηχανημα: "))
  n_tasks = int(input("δωσε τον αριθμο των ενεργειων: "))
  apoklisi = float(input("δωσε τυπικη αποκλιση για τις ανταμιβες: "))

  egreedy_antamives = egreedy(n_machines, n_levers, n_tasks, apoklisi)
  softmax_antamives = softmax_method(n_machines, n_levers, n_tasks, apoklisi)

  results_plot(egreedy_antamives, softmax_antamives)
