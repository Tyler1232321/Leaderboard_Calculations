from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import random
import copy

# globals
player_list = []
player_dict = {}

def get_player(name):
	for player in player_list:
		if player.name == name:
			return player

class player(object):
	def __init__(self, **kwargs):
		self.name = kwargs['name']
		self.wins = kwargs['wins']
		self.losses = kwargs['losses']
		self.rating = kwargs['rating']
		self.temp_rating = self.rating # for the algorithm
		self.rating_sample_list = []

	def get_new_rating(self):
		if len(self.rating_sample_list) > 0:
			self.rating = sum(self.rating_sample_list) / len(self.rating_sample_list)
			self.rating_sample_list = []
			self.temp_rating = self.rating
		else:
			self.rating = self.temp_rating

def insert_new_player(**kwargs):
	if kwargs['name'] == None:
		return False
	if kwargs['name'] not in player_dict:
		temp_player = player(name=kwargs['name'], wins=kwargs['wins'], losses=kwargs['losses'], \
			rating=kwargs['rating'])
		player_list.append(temp_player)
		player_dict[temp_player.name] = temp_player
		return True
	return False

class game(object):
	def __init__(self, **kwargs):
		self.type = kwargs['game_type']
		self.result = kwargs['result']
		self.player1 = kwargs['p1']
		self.player2 = kwargs['p2']
		self.player3 = kwargs['p3']
		self.player4 = kwargs['p4']

	def one_vs_one(self):
		Rating1 = float(player_dict[self.player1].temp_rating)
		Rating2 = float(player_dict[self.player3].temp_rating)
		Result = int(self.result)

		r1 = 10 ** ( Rating1 / 400 )
		r2 = 10 ** ( Rating2 / 400 )
		e1 = r1 / ( r1 + r2 )
		e2 = r2 / ( r1 + r2 )

		if Result == 1:
			s1 = 1
			s2 = 0
		else:
			s1 = 0
			s2 = 1

		Rating1 = Rating1 + 32 * ( s1 - e1 )
		Rating2 = Rating2 + 32 * ( s2 - e2 )

		player_dict[self.player1].temp_rating = Rating1
		player_dict[self.player3].temp_rating = Rating2

	def two_vs_two(self):
		Rating1 = float(player_dict[self.player1].temp_rating)
		Rating2 = float(player_dict[self.player2].temp_rating)
		Rating3 = float(player_dict[self.player3].temp_rating)
		Rating4 = float(player_dict[self.player4].temp_rating)
		Result = int(self.result)

		r1 = 10 ** ( (Rating1 + Rating2) / ( 2 * 400 ) )
		r2 = 10 ** ( (Rating3 + Rating4) / ( 2 * 400 ) )
		e1 = r1 / ( r1 + r2 )
		e2 = r2 / ( r1 + r2 )

		if Result == 1:
			s1 = 1
			s2 = 0
		else:
			s1 = 0
			s2 = 1

		Rating1 = Rating1 + ( 32 * (s1 - e1) ) / 2
		Rating2 = Rating2 + ( 32 * (s1 - e1) ) / 2
		Rating3 = Rating3 + ( 32 * (s2 - e2) ) / 2
		Rating4 = Rating4 + ( 32 * (s2 - e2) ) / 2

		player_dict[self.player1].temp_rating = Rating1
		player_dict[self.player2].temp_rating = Rating2
		player_dict[self.player3].temp_rating = Rating3
		player_dict[self.player4].temp_rating = Rating4

	def one_vs_two(self):
		Rating1 = float(player_dict[self.player1].temp_rating)
		Rating3 = float(player_dict[self.player3].temp_rating)
		Rating4 = float(player_dict[self.player4].temp_rating)
		Result = int(self.result)

		r1 = 10 ** ( Rating1 / 400 )
		r2 = 10 ** ( ( Rating3 + Rating4 ) / ( 2 * 400 ) )
		e1 = r1 / ( r1 + r2 )
		e2 = r2 / ( r1 + r2 )

		if Result == 1:
			s1 = 1
			s2 = 0
		else:
			s1 = 0
			s2 = 1

		Rating1 = Rating1 + 32 * (s1 - e1)
		Rating3 = Rating3 + ( 32 * (s2 - e2) ) / 2
		Rating4 = Rating4 + ( 32 * (s2 - e2) ) / 2

		player_dict[self.player1].temp_rating = Rating1
		player_dict[self.player3].temp_rating = Rating3
		player_dict[self.player4].temp_rating = Rating4

	def two_vs_one(self):
		Rating1 = float(player_dict[self.player1].temp_rating)
		Rating2 = float(player_dict[self.player2].temp_rating)
		Rating3 = float(player_dict[self.player3].temp_rating)
		Result = int(self.result)

		r1 = 10 ** ( (Rating1 + Rating2) / ( 2 * 400 ) )
		r2 = 10 ** ( Rating3 / 400 )
		e1 = r1 / ( r1 + r2 )
		e2 = r2 / ( r1 + r2 )

		if Result == 1:
			s1 = 1
			s2 = 0
		else:
			s1 = 0
			s2 = 1

		Rating1 = Rating1 + ( 32 * (s1 - e1) ) / 2
		Rating2 = Rating2 + ( 32 * (s1 - e1) ) / 2
		Rating3 = Rating3 + 32 * (s2 - e2)

		player_dict[self.player1].temp_rating = Rating1
		player_dict[self.player2].temp_rating = Rating2
		player_dict[self.player3].temp_rating = Rating3

	def evaluate_game(self):
		if self.type == '2vs2':
			self.two_vs_two()
		elif self.type == '1vs1':
			self.one_vs_one()
		elif self.type == '1vs2':
			self.one_vs_two()
		elif self.type == '2vs1':
			self.two_vs_one()


class popupWindow(object):
	def __init__(self, master, main_window):
		self.big_boss = main_window
		self.top = Toplevel(master)
		self.top.title('Play Game')

		self.player1_name = StringVar()
		self.player2_name = StringVar()
		self.player3_name = StringVar()
		self.player4_name = StringVar()

		self.player1_name_entry = Entry(self.top, textvariable=self.player1_name)
		self.player2_name_entry = Entry(self.top, textvariable=self.player2_name)
		self.player3_name_entry = Entry(self.top, textvariable=self.player3_name)
		self.player4_name_entry = Entry(self.top, textvariable=self.player4_name)
		self.team_1_wins_button = Button(self.top, text='Team 1 Wins', command= lambda: self.evaluate_game(1) )
		self.team_2_wins_button = Button(self.top, text='Team 2 Wins', command= lambda: self.evaluate_game(0) )

		self.player1_name_entry.grid(column=2, row=2)
		self.player2_name_entry.grid(column=2, row=3)
		self.player3_name_entry.grid(column=4, row=2)
		self.player4_name_entry.grid(column=4, row=3)
		self.team_1_wins_button.grid(column=1, row=4, columnspan=2)
		self.team_2_wins_button.grid(column=3, row=4, columnspan=2)

		Label(self.top, text='Team 1').grid(column=1, row=1, columnspan=2)
		Label(self.top, text='Team 2').grid(column=3, row=1, columnspan=2)
		Label(self.top, text='Player 1').grid(column=1, row=2)
		Label(self.top, text='Player 2').grid(column=1, row=3)
		Label(self.top, text='Player 3').grid(column=3, row=2)
		Label(self.top, text='Player 4').grid(column=3, row=3)

	def error_message(self):
		pass

	def evaluate_game(self, result):
		self.player1 = self.player1_name.get()
		self.player2 = self.player2_name.get()
		self.player3 = self.player3_name.get()
		self.player4 = self.player4_name.get()

		# if p1 or p3 weren't entered, no game can occur
		if self.player1 == '' or self.player3 == '':
			self.error_message()
			return
		# create the players if they dont exist
		self.big_boss.insert_player(name=self.player1, wins=0, losses=0, rating=1200)
		self.big_boss.insert_player(name=self.player3, wins=0, losses=0, rating=1200)
		game_type = ''
		if self.player2 == '':
			game_type += '1'
		else:
			self.big_boss.insert_player(name=self.player2, wins=0, losses=0, rating=1200)
			game_type += '2'
		if self.player4 == '':
			game_type += 'vs1'
		else:
			self.big_boss.insert_player(name=self.player4, wins=0, losses=0, rating=1200)
			game_type += 'vs2'


		my_game = game(game_type=game_type, p1=self.player1, p2=self.player2, p3=self.player3, \
			p4=self.player4, result=result)
		my_game.evaluate_game()
			
		if result == 1:
			p1 = get_player(self.player1)
			p1.wins += 1
			p1.get_new_rating()
			player_dict[self.player1] = p1
			if game_type[0] == '2':
				p2 = get_player(self.player2)
				p2.wins += 1
				p2.get_new_rating()
				player_dict[self.player2] = p2
			p3 = get_player(self.player3)
			p3.losses += 1
			p3.get_new_rating()
			player_dict[self.player3] = p3
			if game_type[3] == '2':
				p4 = get_player(self.player4)
				p4.losses += 1
				p4.get_new_rating()
				player_dict[self.player4] = p4
		else:
			p1 = get_player(self.player1)
			p1.losses += 1
			p1.get_new_rating()
			player_dict[self.player1] = p1
			if game_type[0] == '2':
				p2 = get_player(self.player2)
				p2.losses += 1
				p2.get_new_rating()
				player_dict[self.player2] = p2
			p3 = get_player(self.player3)
			p3.wins += 1
			p3.get_new_rating()
			player_dict[self.player3] = p3
			if game_type[3] == '2':
				p4 = get_player(self.player4)
				p4.wins += 1
				p4.get_new_rating()
				player_dict[self.player4] = p4

		player_list.sort(key=lambda x: x.rating, reverse=True)

		#display_new_stats(result, p1, p2, p3, p4)

class mainWindow(object):
	def __init__(self, master):
		########################
		# initialize
		########################
		self.master = master
		self.main_window = Frame(master)
		self.main_window.grid(column=0, row=0, sticky=(N, W, E, S))
		self.tools = Frame(master)

		#########################
		# format the outer section
		#########################
		self.main_window.pack(side='left')
		self.tools.pack(side='left')

		#####################
		# define our variables
		#####################

		self.player_listbox = Listbox(self.main_window, width=20, height=20)
		self.player_listbox.pack()
		self.player_listbox.bind('<<ListboxSelect>>', self.onSelect)

		self.cur_player = StringVar()
		self.cur_player_name = StringVar()
		self.cur_player_rating = StringVar()
		self.cur_player_wins = StringVar()
		self.cur_player_losses = StringVar()

		######################
		# formatting
		######################

		self.player_entry = Entry(self.tools, width=7, textvariable=self.cur_player)

		self.add_player_button = Button(self.tools, text='Add Player', \
			command=lambda: self.insert_player(self.cur_player.get()))
		self.save_player_data = Button(self.tools, text='save all players data to file', command=self.save_player_data)
		self.import_players_from_file_button = Button(self.tools, text='import players from file', command=self.import_players)
		self.import_games_from_file_button = Button(self.tools, text='import games from file', command=self.import_games)
		self.play_game_button = Button(self.tools, text='Play Game', command=self.play_game)

		# format the tools section
		self.player_entry.grid(column=1, row=1)
		self.add_player_button.grid(column=2, row=1)
		self.import_players_from_file_button.grid(column=1, row=2)
		self.save_player_data.grid(column=2, row=2)
		self.import_games_from_file_button.grid(column=1, row=8, columnspan=3)
		self.play_game_button.grid(column=1, row=9, columnspan=3)

		# defining the player information section
		Label(self.tools, text='Player Information').grid(column=1, row=3, columnspan=3)
		Label(self.tools, text='Name:').grid(column=1, row=4)
		Label(self.tools, textvariable=self.cur_player_name).grid(column=2, row=4)
		Label(self.tools, text='Rating:').grid(column=1, row=5)
		Label(self.tools, textvariable=self.cur_player_rating).grid(column=2, row=5)
		Label(self.tools, text='Wins:').grid(column=1, row=6)
		Label(self.tools, textvariable=self.cur_player_wins).grid(column=2, row=6)
		Label(self.tools, text='Losses:').grid(column=1, row=7)
		Label(self.tools, textvariable=self.cur_player_losses).grid(column=2, row=7)

	def play_game(self):
		self.w = popupWindow(self.master, self)
		self.play_game_button["state"] = "disabled" 
		self.master.wait_window(self.w.top)
		self.play_game_button["state"] = "normal"

	def save_player_data(self):
		file_path = filedialog.askopenfilename()
		f = open(file_path, 'w')
		f.write("{name: <10}| {rating: <20}| {wins: <10}| {losses: <10}\n".format(name='NAME', rating='RATING', wins='WINS', losses='LOSSES'))
		for player in player_list:
			f.write("{name: <10}| {rating: <20}| {wins: <10}| {losses: <10}\n".format(name=player.name, rating=player.rating, wins=player.wins, losses=player.losses))
		f.close()

	# when we select a player
	def onSelect(self, *args):
		name = self.player_listbox.get(self.player_listbox.curselection()[0])
		cur_player = player_dict[name]
		self.cur_player_name.set(cur_player.name)
		self.cur_player_rating.set(cur_player.rating)
		self.cur_player_wins.set(cur_player.wins)
		self.cur_player_losses.set(cur_player.losses)

	# inserting a player into the database
	def insert_player(self, **kwargs):
		if insert_new_player(name=kwargs['name'], wins=kwargs['wins'], losses=kwargs['losses'], \
		 					rating=kwargs['rating']):
			self.player_listbox.insert(END, kwargs['name'])
	
	# importing a list of players into the database
	def import_players(self):
		file_path = filedialog.askopenfilename()
		with open(file_path) as f:
			for line in f:
				line = line.rstrip()
				self.insert_player(name=line, wins=0, losses=0, rating=1200)

	def import_games(self):
		file_path = filedialog.askopenfilename()
		game_list = []
		with open(file_path) as f:
			for line in f:
				line = line.rstrip()
				team1, team2 = line.split(' vs ')
				team2, record = team2.split(' - ')
				wins, losses = record.split('/')
				game_type = ''

				try:
					p1, p2 = team1.split(' & ')
					self.insert_player(name=p1, wins=0, losses=0, rating=1200)
					self.insert_player(name=p2, wins=0, losses=0, rating=1200)
					game_type +='2'
				except:
					p1 = team1
					p2 = None
					self.insert_player(name=p1, wins=0, losses=0, rating=1200)
					game_type += '1'

				try:
					p3, p4 = team2.split(' & ')
					self.insert_player(name=p3, wins=0, losses=0, rating=1200)
					self.insert_player(name=p4, wins=0, losses=0, rating=1200)
					game_type +='vs2'
				except:
					p3 = team2
					p4 = None
					self.insert_player(name=p3, wins=0, losses=0, rating=1200)
					game_type += 'vs1'


				for i in range(int(wins)):
					game_list.append(game(p1=p1, p2=p2, p3=p3, p4=p4, game_type=game_type, result=1))
					
					player_dict[p1].wins += 1
					player_dict[p3].losses += 1
					
					if p2 != None:
						player_dict[p2].wins +=1
					if p4 != None:
						player_dict[p4].losses +=1

				for i in range(int(losses)):
					game_list.append(game(p1=p1, p2=p2, p3=p3, p4=p4, game_type=game_type, result=0))

					player_dict[p1].losses += 1
					player_dict[p3].wins += 1
					
					if p2 != None:
						player_dict[p2].losses +=1
					if p4 != None:
						player_dict[p4].wins +=1


		game_num = len(game_list)
		
		for i in range(game_num*10):
			game_list_temp = copy.copy(game_list)
			for j in range(game_num-1):
				ind = random.randint(0, len(game_list_temp) - 1)
				game_list_temp[ind].evaluate_game()
				game_list_temp.pop(ind)

			for player in player_list:
				player.rating_sample_list.append(player_dict[player.name].temp_rating)
				player.temp_rating = player.rating

		for player in player_list:
			player.get_new_rating()
			player.wins = player_dict[player.name].wins
			player.losses = player_dict[player.name].losses
			player_dict[player.name] = player

		player_list.sort(key=lambda x: x.rating, reverse=True)
		for player in player_list:
			print(player.name)




if __name__ == "__main__":
	root=Tk()
	root.title("Player List")
	root.columnconfigure(0, weight=1)
	root.rowconfigure(0, weight=1)
	m=mainWindow(root)
	root.mainloop()