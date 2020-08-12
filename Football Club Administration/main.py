import mysql.connector as mc

db = mc.connect(host='localhost', user='root', passwd='anas')
dbCursor = db.cursor()
dbExec = dbCursor.execute

dbExec('create database if not exists fc_admin')
dbExec('use fc_admin')
dbExec('create table if not exists players(jersey_no int primary key, name char(20), position char(3))')
dbExec('create table if not exists fixtures(date_time datetime, stadium char(20), oponent char(30))')

def insert(tableName, *args):
	executeLine = "insert into " + tableName + " values("

	for column in args:
		if type(column) == int:
			executeLine += str(column) + ", "
		else:
			executeLine += "'" + str(column) + "', "

	executeLine = executeLine[0:-2]

	executeLine += ")"
	dbExec(executeLine)
	db.commit()

def update(tableName, updateItem, newValue, whereItem, whereValue):
	executeLine = "update " + str(tableName) + " set " + str(updateItem) + "="
	if type(newValue) == int:
		executeLine += str(newValue)
	else:
		executeLine += "'" + str(newValue) + "'" 

	executeLine += " where " + str(whereItem) + "=" + str(whereValue) if type(whereValue) == int else " where " + str(whereItem) + "='" + str(whereValue) +"'"

	dbExec(executeLine)
	db.commit()
	print("Successfully Updated!")

def addPlayer():
	num = int(input("Number of players: "))

	for i in range(num):
		name = input("Player Name: ")
		name = name.capitalize()

		jersey_no = int(input("Jersey Number: "))

		position = input("Player position: ")
		position = position.upper()

		insert('players', jersey_no, name, position)

		print("Player details added Successfully")

	main()

def removePlayer():
	print("Enter the Jersey Number of the player you want to remove")
	jersey_no = int(input(":"))

	dbExec('select name from players where jersey_no=' + str(jersey_no))
	name = dbCursor.fetchone()[0]
	print("Are you sure you want to remove " + str(name) + ".")

	ch = input("(y/n): ")

	if ch.lower() in ['y', 'yes']:
		dbExec('delete from players where jersey_no=' + str(jersey_no))
		print(str(name) + " has been removed from the database")
	
	else:
		print("Player Removal Cancelled")

	db.commit()

	main()

def updatePlayer():
	print("Enter the Jersey Number of the player whose details you want to update")
	jersey_no = int(input(":"))

	dbExec("select name from players where jersey_no=" + str(jersey_no))
	name = dbCursor.fetchone()[0]

	while True:
		print("Enter corresponding character of your choice")
		print("Change Name(n)")
		print("Change Jersey Number(j)")
		print("Change Position(p)")
		ch = input(":")

		if ch.lower() in ['n']:
			print("Enter new Name for " + name)
			new_name = input(":")
			update('players', 'name', new_name, 'jersey_no', jersey_no)
			break

		elif ch.lower() in ['j']:
			print("Enter new Jersey Number for " + name)
			new_jersery_no = input(":")
			update('players', 'jersey_no', new_jersery_no, 'jersey_no', jersey_no)
			break

		elif ch.lower() in ['p']:
			print("Enter new Position for " + name)
			new_position = input(":")
			update('players', 'position', new_position, 'jersey_no', jersey_no)
			break

		else:
			print("Invalid Input!")
			continue
	main()

def newFixture():
	num = int(input("Number of Matches:"))
	for i in range(num):
		date = input("Date format(YYYY-MM-DD): ")
		time = input("Time 24hrs-format(HH:MM): ")
		stadium = input("Stadium: ")
		oponent = input("Oponent Club: ")
		date_time = str(date.strip()) + ' ' + str(time.strip())

		insert('fixtures', date_time, stadium, oponent)
		print("Match details added Successfully")

	main()

def displayPlayers():
	dbExec("select * from players")
	players = dbCursor.fetchall()
	i = 1
	for player in players:
		player = list(player)
		jersey_no, name, position = player
		print("*************************Player " + str(i) + "*********************************")
		print("Name: " + str(name))
		print("Jersey Number: " + str(jersey_no))
		print("Position: " + str(position))
		i += 1
	print("***********************************************")

	main()

def displayFixtures():
	dbExec("select * from fixtures")
	all_fixtures = dbCursor.fetchall()
	i = 1
	for fixture in all_fixtures:
		print("***************************" + str(i) + "*******************************")
		fixture = list(fixture)
		date_time, stadium, oponent = fixture[0], fixture[1], fixture[2]
		date_time = str(date_time)
		date, time = date_time.split(' ')
		print("Date: " + date)
		print("Time: " + time[0:-3])
		print("Stadium: " + stadium)
		print("Oponent: " + oponent)
	    i += 1
	print("***********************************************")

	main()

def main():
	print("Enter corresponding number of your choice")
	print("1. Display Players")
	print("2. Update Player")
	print("3. Add new Player")
	print("4. Remove Player")
	print("5. Display Fixtures")
	print("6. Add new Fixture")
	print("Press Enter to exit")
	ch = input(":")

	if ch.lower() in ['', 'q', 'quit', 'e', 'exit']:
		print("Thank You!")
		quit()
	elif int(ch) == 1:
		displayPlayers()
	elif int(ch) == 2:
		updatePlayer()
	elif int(ch) == 3:
		addPlayer()
	elif int(ch) == 4:
		removePlayer()
	elif int(ch) == 5:
		displayFixtures()
	elif int(ch) == 6:
		newFixture()
	else:
		print("Invalid Input!")
		main()

main()
