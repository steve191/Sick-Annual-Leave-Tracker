Tracks leave and sick leave accumulated and taken by employee.

<!-- ### <ins>Fixed Issues</ins> -->

<!-- - [ Date ]      [ patch ]       - [ Fixed ]   -->

<!-- ### <ins>Currently Working On [patch]</ins> -->

<!-- - Issue 24 [New feature add company logo on payslips] -->

### <ins>Currently Working On</ins>

##### <ins>GUI</ins>

###### <ins>Employee Setup</ins>
- ~Add employee~
	- ~Sort date format~

- ~Update emplyee~
	- ~Move to main.py delete employee setup~

- ~Clear button~

- Delete employee
	- ~Add Delete button and function~
	- When deleting employee make back up of leave acc and taken (excel)
	  also cascade deletion

###### <ins>Leave</ins>

- ~Add annual leave~

- ~Edit annual leave~

- ~Delete annual leave~

- Add sick leave

- Edit sick leave

- ~Show annual leave available in table~

- ~Show sick leave available in table~

- Show all leave and sick leave taken (excel)

##### <ins>Functionality</ins>

- See total leave acc and leave taken (Annual and Sick)

- Store medical certifcates

### <ins>How to install</ins>

Create environment:

```python
python -m venv <name>
```

Install poetry:

```python
pip install poetry
``` 

Install dependencies:

```python
poetry install
```

Run Script [main.py]:

```python
python main.py
``` 