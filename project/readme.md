#Readme
##Introduction
The project score-management-subsystem is divided into four apps.

1. Score manage
2. Score commit
3. score query
4. score modification

Install the app into website, you need:

1. Remove the annotation in .score_subsystem_management/score_subsystem_management/setting.py INSALL
2. Carefully implement four apps, you may edit model.py url.py views.py in .score_subsystem_management/xxx/
3. Debugging app one by one is highly recommended.


##Framework(beta)
###Views
1. Score manage
	* index(parse&check&upload)
	* preview
2. Score commit
	* index
3. Score query
	* index
4. Score modification
	* index(select course&notify)
	* modify(modify in preview mode and create a new event)
	* vote(display vote event and vote)
	
###Models
A beta version of model is given in corresponding file(models.py). But it seems different models may access the same table in database.
	