#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to implement the CGame class for the the BBC Football Manager program.
'''

# System libraries.
import random
import math

# Application Libraries.
import modANSI
import modInkey
import modTeam
import modPlayer



class CGame:
    ''' Class to represent the BBC Football Manager game. '''



    def __init__(self):
        ''' Class constructor for the BBC Football manager game. '''
        self.player_name = ''
        self.level = 1
        self.team_name = ''
        self.team_colour = modANSI.WHITE
        self.team_index = None
        self.num_squad = 0
        self.num_team = 0
        self.num_injured = 0
        self.formation = [0, 0, 0]



    def Run(self):
        ''' Execute the football manager game. '''
        self.keyboard = modInkey.CInkey()
        random.seed()

        modANSI.CLS()
        self.Football()

        # Get the player settings.
        print()
        self.player_name = input('Please enter your name: ')

        # Select the level.
        print('Enter level [1-4]')
        self.level = int(self.GetKeyboardCharacter(['1', '2', '3', '4']))
        print('Level {} was selected'.format(self.level))

        # Load a game.
        print('Do you want to load a game?')
        if self.YesNo():
            print('Yes')
        else:
            print('No')
            self.NewGame()

        # Play the game.
        self.match = 0
        while self.match < 30:
            modANSI.CLS()
            print('{} MANAGER: {}'.format(self.team.GetColouredName(), self.player_name))
            print('LEVEL: {}'.format(self.level))
            print()
            print('1 .. Sell Players / View Squad')
            print('2 .. Bank')
            print('3 .. Rename Player')
            print('4 .. Continue')
            print('5 .. Save Game')
            print('6 .. Restart')
            print('7 .. League Table')
            print('8 .. Quit')
            sKey = self.GetKeyboardCharacter(['1', '2', '3', '4', '5', '6', '7', '8'])
            if sKey == '1':
                self.SellPlayer()
            elif sKey == '2':
                self.Bank()
            elif sKey == '3':
                # PROCRENAME
                pass
            elif sKey == '4':
                # Continue.
                self.PlayWeek()
            elif sKey == '5':
                # PROCSAVE
                pass
            elif sKey == '6':
                # PROCRESTART
                pass
            elif sKey == '7':
                self.ShowLeague()
                self.Wait()
            elif sKey == '8':
                # Confirm with the user.
                print('Are you sure you want to exit the program (Y/N) ?')
                if self.YesNo():
                    return

        # Season has finished.
        print('Season has finished.')



    def PlayWeek(self):
        ''' This is the block of code that was after the menu in the week loop of the BBC Basic version. Line 740 onward.'''
        self.match = self.match+1

        # Decide and play any cup matches.

        # Choose an opponent for the league match.
        self.team.played_home = True
        self.team.played_away = True
        while True:
            nOpponent = random.randint(0, 15)
            bHome = (self.match & 1) == 1
            if bHome:
                if self.teams[nOpponent].played_home == False:
                    self.teams[nOpponent].played_home = True
                    break;
            else:
                if self.teams[nOpponent].played_away == False:
                    self.teams[nOpponent].played_away = True
                    break;

        # Let the player select the players for the team.
        while True:
            modANSI.CLS()
            if bHome:
                self.DisplayMatch(self.team_index, nOpponent)
            else:
                self.DisplayMatch(nOpponent, self.team_index)
            sKey = self.GetKeyboardCharacter(['c', '\t'])
            if sKey == '\t':
                break;
            # Pick the player.
            self.PickPlayers()

        # Play the match.
        if bHome:
            nPlayerGoals, nOpponentGoals = self.PlayMatch(self.team_index, nOpponent, 0.5, 0)
            self.ApplyPoints(self.team_index, nOpponent, nPlayerGoals, nOpponentGoals)
        else:
            nOpponentGoals, nPlayerGoals = self.PlayMatch(nOpponent, self.team_index, 0.5, 0)
            self.ApplyPoints(nOpponent, self.team_index, nOpponentGoals, nPlayerGoals)

        # PROCPLAYERS
        # PROCINJ
        # Decided the fixtures for the league was at half time of the playmatch.
        self.Fixtures(nOpponent)

        self.Wait()

        self.Rest()
        self.PlayerEngergy()
        self.SortDivison()
        self.Wait()

        self.ShowLeague()
        self.Wait()

        self.Market()
        # PROCREPORT
        # PROCPROGRESS



    def ApplyPoints(self, nHome, nAway, nHomeGoals, nAwayGoals):
        ''' Apply the points to the league. '''
        if nHomeGoals == nAwayGoals:
            self.teams[nHome].pts = self.teams[nHome].pts + 1
            self.teams[nAway].pts = self.teams[nAway].pts + 1
            self.teams[nHome].draw = self.teams[nHome].draw + 1
            self.teams[nAway].draw = self.teams[nAway].draw + 1
        else:
            if nHomeGoals > nAwayGoals:
                self.teams[nHome].pts = self.teams[nHome].pts + 3
                self.teams[nHome].win  = self.teams[nHome].win  + 1
                self.teams[nAway].lost = self.teams[nAway].lost + 1
            else:
                self.teams[nAway].pts = self.teams[nAway].pts + 3
                self.teams[nHome].lost = self.teams[nHome].lost + 1
                self.teams[nAway].win  = self.teams[nAway].win + 1
            self.teams[nHome].difference = self.teams[nHome].difference + nHomeGoals - nAwayGoals
            self.teams[nAway].difference = self.teams[nAway].difference + nAwayGoals - nHomeGoals



    def PlayerEngergy(self):
        ''' Replacement for PROCRESET (line 3200) in the BBC Basic version. '''
        self.teams[self.team_index].energy = 0
        for oPlayer in self.players:
            if oPlayer.in_squad:
                if oPlayer.in_team:
                    oPlayer.energy = oPlayer.energy - random.randint(1, 2)
                    if oPlayer.energy < 1:
                        oPlayer.energy = 1
                    self.teams[self.team_index].energy = self.teams[self.team_index].energy + oPlayer.energy
                else:
                    oPlayer.energy = oPlayer.energy + 9
                    if oPlayer.energy > 20:
                        oPlayer.energy = 20



    def DisplaySquad(self):
        ''' Replacement for PROCPTEAM (line 2130) in the BBC Basic version. '''
        print('   Player Skill Energy')
        for oPlayer in self.players:
            if oPlayer.in_squad:
                oPlayer.WriteRow()



    def PickPlayers(self):
        ''' Replacement for PROCPICK (line 2260) in the BBC Basic version. '''
        while True:
            modANSI.CLS()
            self.DisplaySquad()
            if self.num_team <= 11:
                nNumber = self.EnterNumber('>')
                if nNumber == 0:
                    break;
                nNumber = nNumber - 1
                if self.players[nNumber].in_squad:
                    self.AddPlayer(nNumber)
            else:
                nNumber = self.EnterNumber('Enter Player to Drop ')
                if nNumber >= 1 and nNumber <= 26:
                    self.DropPlayer(nNumber - 1)



    def DropPlayer(self, nIndex):
        ''' Replacement for PROCDROP (line ????) in the BBC Basic version. '''
        oPlayer = self.players[nIndex]
        if oPlayer.in_team == False:
            return
        oPlayer.in_team = False
        if oPlayer.position == modPlayer.DEFENSE:
            self.team.defence = self.team.defence - oPlayer.skill
        elif oPlayer.position == modPlayer.MIDFIELD:
            self.team.midfield = self.team.midfield - oPlayer.skill
        else:
            self.team.attack = self.team.attack - oPlayer.skill
        self.team.energy = self.team.energy - oPlayer.energy
        self.num_team = self.num_team - 1
        self.formation[oPlayer.position] = self.formation[oPlayer.position] - 1
        self.team.formation = '{}-{}-{}'.format(self.formation[modPlayer.DEFENSE]-1, self.formation[modPlayer.MIDFIELD], self.formation[modPlayer.ATTACK])



    def AddPlayer(self, nIndex):
        ''' Replacement for PROCIN (line 1580) in the BBC Basic version. '''
        oPlayer = self.players[nIndex]
        if oPlayer.in_team:
            return
        oPlayer.in_team = True
        if oPlayer.position == modPlayer.DEFENSE:
            self.team.defence = self.team.defence + oPlayer.skill
        elif oPlayer.position == modPlayer.MIDFIELD:
            self.team.midfield = self.team.midfield + oPlayer.skill
        else:
            self.team.attack = self.team.attack + oPlayer.skill
        self.team.energy = self.team.energy + oPlayer.energy
        self.num_team = self.num_team + 1
        self.formation[oPlayer.position] = self.formation[oPlayer.position] + 1
        self.team.formation = '{}-{}-{}'.format(self.formation[modPlayer.DEFENSE]-1, self.formation[modPlayer.MIDFIELD], self.formation[modPlayer.ATTACK])



    def SellPlayer(self):
        ''' Replacement for PROCSELL (line 1950) in the BBC Basic version. '''
        modANSI.CLS()
        self.DisplaySquad()
        print('Enter <RETURN> to return to menu.')
        print('Else enter player number to be sold')
        nPlayerNumber = self.EnterNumber('>')
        if nPlayerNumber >= 1 and nPlayerNumber <= 26:
            nPlayerNumber = nPlayerNumber - 1
            if self.players[nPlayerNumber].in_squad:
                nPrice = int((self.players[nPlayerNumber].skill + random.uniform(0, 1)) * 5000 * (5 - self.division))
                print('You are offered £{:,.2f}'.format(nPrice))
                print('Do you accept (Y/N)?')
                if self.YesNo():
                    self.num_squad = self.num_squad - 1
                    self.DropPlayer(nPlayerNumber)
                    self.players[nPlayerNumber].in_squad = False
                    self.players[nPlayerNumber].skill = 5
            else:
                print('On range')
            self.Wait()




    def Market(self):
        ''' Replacement for PROCMARKET (line 3330) in the BBC Basic version. '''
        if self.num_squad >= 18:
            # modANSI.CLS()
            print('{}F.A. rules state that one team may not have more that 18 players. You already have 18 players therefore you may not buy another.{}'.format(modANSI.RED, modANSI.RESET_ALL))
        else:
            while True:
                nPlayer = random.randint(0, 25)
                if self.players[nPlayer].in_squad == False:
                    break;
            # modANSI.CLS()
            if self.players[nPlayer].position == modPlayer.DEFENSE:
                print('Defence')
            elif self.players[nPlayer].position == modPlayer.MIDFIELD:
                print('Mid-field')
            else:
                print('Attack')
            self.players[nPlayer].WriteRow(5000 * (5 - self.division))
            print('You have £{:,.2f}'.format(self.money))
            nBid = self.EnterNumber('Enter your bid: ')
            if nBid <= 0:
                return
            nPrice = self.players[nPlayer].skill * (5000 * (5 - self.division)) + random.randint(1, 10000) - 5000
            if nBid > self.money:
                print('{}You do not have enough money{}'.format(modANSI.RED, modANSI.RESET_ALL))
            elif nBid > nPrice:
                print('{}{} is added to your squad.{}'.format(modANSI.GREEN, self.players[nPlayer].name, modANSI.RESET_ALL))
                self.num_squad = self.num_squad + 1
                self.players[nPlayer].in_squad = True
                self.money = self.money - nBid
            else:
                if nBid > 0:
                    print('{}Your bid is turned down.{}'.format(modANSI.RED, modANSI.RESET_ALL))
        self.Wait()



    def Bank(self):
        ''' Replacement for PROCLEND (line 4170) in the BBC Basic version. '''
        modANSI.CLS()
        print('Bank')
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        print('Do you want to Deposit, Withdraw or Exit (D/W/E)?')
        sKey = self.GetKeyboardCharacter(['d', 'w', 'e'])
        if sKey == 'e':
            return
        if sKey == 'd':
            print('Deposit')
        else:
            print('Withdraw')
        nAmount = self.EnterNumber('Enter the amount >')
        if sKey == 'd':
            nAmount = -nAmount
        self.money = self.money + nAmount
        self.debt = self.debt + nAmount
        if self.debt > 1e6:
            print('You can not have that much')
            self.money = self.money - (self.debt-1e6)
            self.debt = 1e6
        if self.money < 0:
             self.debt = self.debt - self.money
             self.money = 0
        print('You have £{:,.2f}'.format(self.money))
        if self.debt > 0:
            print('You owe £{:,.2f}'.format(self.debt))
        else:
            print('In Bank £{:,.2f}'.format(-self.debt))
        self.Wait()



    def DisplayMatch(self, nHome, nAway):
        ''' Replacement for PROCDISPLAY in the BBC Basic version. '''
        print('   {}{:^18}{}{:^18}{}'.format(self.teams[nHome].colour, self.teams[nHome].name, self.teams[nAway].colour, self.teams[nAway].name, modANSI.RESET_ALL))
        if True:
            print('Pos{:^18}{:^18}'.format(self.teams[nHome].position, self.teams[nAway].position))
        print('Eng{:^18}{:^18}'.format(self.teams[nHome].energy, self.teams[nAway].energy))
        print('Mor{:^18}{:^18}'.format(self.teams[nHome].moral, self.teams[nAway].moral))
        print('For{:^18}{:^18}'.format(self.teams[nHome].formation, self.teams[nAway].formation))
        print('Def{:^18}{:^18}'.format(self.teams[nHome].defence, self.teams[nAway].defence))
        print('Mid{:^18}{:^18}'.format(self.teams[nHome].midfield, self.teams[nAway].midfield))
        print('Att{:^18}{:^18}'.format(self.teams[nHome].attack, self.teams[nAway].attack))
        print()
        print('{} Picked, {} Squad, {} Injured.'.format(self.num_team, self.num_squad, self.num_injured))
        print('Press C to change team')
        print('Press TAB to play match.')



    def Wait(self):
        ''' Replacement for PROCWAIT in the BBC Basic version. '''
        print('----- Press SPACE to continue -----')
        self.GetKeyboardCharacter([' '])



    def ShowLeague(self):
        ''' Replacement for PROCLEAGUE in the BBC Basic version. '''
        modANSI.CLS()
        print('Division {}'.format(self.division))
        print('   Team             W  D  L Pts Dif')
        for oTeam in self.teams:
            oTeam.WriteTableRow()
        print('Matches Played: {}'.format(self.match))
        print('{} position: {}'.format(self.team.GetColouredName(), self.team_index+1))



    def SortDivison(self):
        ''' Replacement for PROCSORT in the BBC Basic version. '''
        self.teams = sorted(self.teams, key=lambda CTeam: (CTeam.pts, CTeam.difference), reverse=True)
        nPosition = 1
        for oTeam in self.teams:
            oTeam.position = nPosition
            if oTeam.name == self.team_name:
                self.team_index = nPosition-1
                self.team = oTeam
            nPosition = nPosition + 1



    def NewGame(self):
        ''' Initialise a new game. '''
        self.PickTeam()

        # Initialise variables
        self.money = 50000
        self.debt = 200000

        # Initialise the players.
        self.players = []
        for nIndex in range(1, 27):
            oPlayer = modPlayer.CPlayer()
            oPlayer.GetPlayer(nIndex)
            oPlayer.skill = random.randint(1, 5)
            oPlayer.energy = random.randint(1, 20)
            self.players.append(oPlayer)
        for nIndex in range(4):
            nPlayer = random.randint(0, 25)
            self.players[nPlayer].skill = 5

        # Pick 12 players.
        self.num_squad = 12
        for nIndex in range(self.num_squad):
            nPlayer = random.randint(0, 25)
            while self.players[nPlayer].in_squad:
                nPlayer = random.randint(0, 25)
            self.players[nPlayer].in_squad = True

        # Initialise the teams.
        self.teams = None
        self.division = 4
        self.SetTeamsForDivision()
        self.SortDivison()



    def SetTeamsForDivision(self):
        ''' Replacement for PROCDIVISON (line 3520) in the BBC Basic version. '''
        if self.teams == None:
            self.teams = []
            for nTeam in range(16):
                oTeam = modTeam.CTeam()
                oTeam.name = ''
                self.teams.append(oTeam)
            self.teams[0].name = self.team_name
            self.teams[0].colour = self.team_colour
            self.teams[0].position = 1
        nDivision = self.division

        nNewTeam = 1
        for oTeam in self.teams:
            if oTeam.name == '':
                oTeam.GetTeam(nDivision, nNewTeam)
                # Check that this team is unique.
                nNewTeam = nNewTeam+1
            if oTeam.name == self.team_name:
                # Initialise the players team.
                oTeam.Zero()
            else:
                # Initialise the opponent team.
                oTeam.Initialise(self.division)



    def MultiRandomInt(self, nRange, nNumber):
        ''' Replacement for FNRND() (Line 6640) in the BBC Basic version. This gives an integer result. '''
        nTotal = 0
        for nCount in range(nNumber):
            nTotal = nTotal + random.randint(1, nRange)
        return nTotal



    def MultiRandom(self, dRange, nNumber):
        ''' Replacement of FNRND (Line 6640) in the BBC Basic version. This gives a floating point result.  It is usually expected that dRange will be 1.'''
        dTotal = 0
        for nCount in range(nNumber):
            dTotal = dTotal + random.uniform(0, dRange)
        return dTotal



    def PickTeam(self):
        ''' Replacement for PROCPICKTEAM in the BBC Basic version. '''
        nDivision = 1
        while True:
            modANSI.CLS()
            print(' 0 More Teams')
            print(' 1 Own Team')
            for nIndex in range(2, 17):
                oTeam = modTeam.CTeam()
                oTeam.GetTeam(nDivision, nIndex - 1)
                print('{:2} {}'.format(nIndex, oTeam.GetColouredName()))
            nNumber = self.EnterNumber('Enter Team Number ')
            if nNumber >= 2 and nNumber <= 17:
                oTeam.GetTeam(nDivision, nNumber - 1)
                self.team_name = oTeam.name
                self.team_colour = oTeam.colour
                break;
            if nNumber == 1:
                self.team_name = input('Enter Team name ')
                self.team_colour = modANSI.CYAN
                break;
            nDivision = 1 + (nDivision & 3)
        print('You manage {}{}{}'.format(self.team_colour, self.team_name, modANSI.RESET_ALL))



    def EnterNumber(self, sMessage):
        ''' Enter a number at the keyboard. '''
        nNumber = 0
        try:
            nNumber = int(input(sMessage))
        except:
            nNumber = 0
        return nNumber



    def YesNo(self):
        ''' Replacement for FNYES in the BBC Basic version.  Returns True if 'Y' is pressed or False if 'N' is pressed. '''
        sCharacter = self.GetKeyboardCharacter(['y', 'n'])
        if sCharacter == 'y':
            return True
        return False



    def GetKeyboardCharacter(self, allowed):
        ''' Return a keyboard character from the allowed characters. '''
        # No Repeat Until in Python.
        sCharacter = modInkey.getwch()
        while not (sCharacter in allowed):
            sCharacter = modInkey.getwch()
        self.keyboard.Stop()
        return sCharacter



    def Football(self):
        ''' Implementation of DEFPROCfootball().  Display a title. '''
        print('┏━━             ┃       ┃ ┃   ┏━┳━┓')
        print('┃            ┃  ┃       ┃ ┃   ┃ ┃ ┃' )
        print('┣━━ ┏━┓ ┏━┓ ━#━ ┣━┓ ━━┓ ┃ ┃   ┃   ┃ ━━┓ ━┳━┓ ━━┓ ┏━┓ ┏━┓ ┏━')
        print('┃   ┃ ┃ ┃ ┃  ┃  ┃ ┃ ┏━┫ ┃ ┃   ┃   ┃ ┏━┃  ┃ ┃ ┏━┫ ┃ ┃ ┣━┛ ┃')
        print('┃   ┗━┛ ┗━┛  ┃  ┗#┛ ┗━┛ ┃ ┃   ┃   ┃ ┗━┛  ┃ ┃ ┗━┛ ┗━┫ ┗━━ ┃')
        print('                                                   ┃')
        print('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛')
        print('By Steve Walton BBC BASIC 1982-1989, 2000, Python 2018.')



    def Fixtures(self, nOpponent):
        ''' Replacement for PROCFIXTURES (line 247) in the BBC Basic version. '''
        for oTeam in self.teams:
            oTeam.fixture = 0

        self.teams[self.team_index].fixture = -1
        self.teams[nOpponent].fixture = -1
        for nMatch in range(1, 8):
            while True:
                nHome = random.randint(0, 15)
                if self.teams[nHome].fixture == 0:
                    break;
            self.teams[nHome].fixture = nMatch * 2 - 1
            while True:
                nAway = random.randint(0, 15)
                if self.teams[nAway].fixture == 0:
                    break;
            self.teams[nAway].fixture = nMatch * 2

            # Swap if the away team has fewer month matches.



    def Rest(self):
        '''
        Replacement for DEFPROCREST (line 2710) in the BBC Basic version.
        This is play and display the rest of the matches in the league.
        '''
        for nMatch in range(1, 8):
            for nIndex in range(16):
                if self.teams[nIndex].fixture == 2 * nMatch -1:
                    nHome = nIndex
                if self.teams[nIndex].fixture == 2 * nMatch:
                    nAway = nIndex

            nHomeGoals, nAwayGoals = self.Match(nHome, nAway, 0.5, 0)
            print('{} {} - {} {}'.format(self.teams[nHome].GetColouredName(), nHomeGoals, nAwayGoals, self.teams[nAway].GetColouredName()))
            self.ApplyPoints(nHome, nAway, nHomeGoals, nAwayGoals)



    def PlayMatch(self, nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus):
        ''' Replacement for DEFPROCPLAYMATCH (Line 1680) in the BBC Basic version. '''
        nHomeGoals, nAwayGoals = self.Match(nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus)
        # Not implemented yet.

        print('{} {} - {} {}'.format(self.teams[nHomeTeam].GetColouredName(), nHomeGoals, nAwayGoals, self.teams[nAwayTeam].GetColouredName()))

        # Decided the fixtures for the league at half time.
        # PROCFIXTURES

        return nHomeGoals, nAwayGoals



    def Pois(self, U, C):
        ''' Replacement for DEFNPOIS (Line 7040) in the BBC Basic version. '''
        nT = 0
        P = math.exp(-U)
        if C < P:
            return 0
        S = P
        while True:
            nT = nT + 1
            P = P * U / nT
            S = S + P
            if C < S:
                break;
        return nT



    def Match(self, nHomeTeam, nAwayTeam, dHomeBonus, dAwayBonus):
        ''' Replacement for DEFPROCMATCH (Line 6920) in the BBC Basic version. '''
        oHome = self.teams[nHomeTeam]
        oAway = self.teams[nAwayTeam]
        dHomeAverageGoals = dHomeBonus + (4.0 * oHome.attack / oAway.defence) * oHome.midfield / (oHome.midfield + oAway.midfield) + (oHome.moral - 10.0) / 40.0 - (oAway.energy - 100.0) / 400.0
        dAwayAverageGoals = dAwayBonus + (4.0 * oAway.attack / oHome.defence) * oAway.midfield / (oAway.midfield + oHome.midfield) + (oAway.moral - 10.0) / 40.0 - (oHome.energy - 100.0) / 400.0
        nHomeGoals = self.Pois(dHomeAverageGoals, self.MultiRandom(1, 2) / 2)
        nAwayGoals = self.Pois(dAwayAverageGoals, self.MultiRandom(1, 2) / 2)

        # Set the moral for the teams.
        if nHomeGoals == nAwayGoals:
            oHome.moral = 10
            oAway.moral = 10
        else:
            if nHomeGoals > nAwayGoals:
                oHome.moral = max(oHome.moral, 10)
                oAway.moral = min(oAway.moral, 10)
                oHome.moral = min(oHome.moral + nHomeGoals - nAwayGoals, 20)
                oAway.moral = max(oAway.moral + nAwayGoals - nHomeGoals, 1)
            else:
                oHome.moral = min(oHome.moral, 10)
                oAway.moral = max(oAway.moral, 10)
                oHome.moral = max(oHome.moral + nHomeGoals - nAwayGoals, 1)
                oAway.moral = min(oAway.moral + nAwayGoals - nHomeGoals, 20)
        return nHomeGoals, nAwayGoals
