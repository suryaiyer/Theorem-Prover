# Theorem-Prover

Aim: To parse the expressions and convert them into CNF form and to evaluate the statements

Python files: in src folder
- CNF-converter.py: 
	- Contains the parser 
	- Contains the evaluate function
	- Convert the knowledge base to cnf (Not perfectly working for all cases)
- model_checking.py: implement model checking function
- resolution.py: implement resolution function
- main.py


To run:
- python main.py
	- This executes all the problems and provides the output in output.txt (Also Prints the output).
	- The problem 4 takes about 15 min to give the solution, so you might have to wait. (Also shared the output file)
To check parser.
	-In CNF-converter.py
	- The last few lines which are commented can be uncommented and you can test on some expressions (Make sure to comment those lines when running main else that output will also be shown)
