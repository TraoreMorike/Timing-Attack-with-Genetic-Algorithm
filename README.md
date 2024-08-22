**Title:** Proof of concept of Genetic Algorithm for Password Cracking

**Description:**
This script implements a genetic algorithm to crack passwords using a combination of elitism, tournament selection, and crossover mutation. The goal is to find the correct password by iteratively generating new populations of candidate passwords.

**Features:**

* Generates an initial population of candidate passwords
* Evaluates each password in the population based on its fitness (similarity to the target password)
* Selects parents from the population using elitism and tournament selection
* Performs crossover and mutation operations to generate new offspring
* Iteratively updates the population until the correct password is found

**Usage:**

1. Run the script with Python interpreter (`python Timing_Attack_w_GA_Master.py`)
2. The script will output the progress of each iteration, including the evaluated fitness of each password in the population
3. When the correct password is found, an exception will be raised with the details of the found password and the number of iterations taken

**Note:**

* This script assumes that the target password is a fixed-length string consisting only of ASCII characters (letters and digits)
* The `verifyPassword` function simulates a timing attack by comparing characters in the candidate password to the target password, returning a ratio of matching characters
* The mutation rate can be adjusted to control the frequency of changes in the offspring passwords
* Even if this Genetic Algorithm is able to retrieve the password, this attack method is poorly effective compared to traditional attack.  
