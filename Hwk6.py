import numpy as np
import scr.FigureSupport as figureLibrary
import scr.StatisticalClasses as Stat

class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250

class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLosses = [] # create an empty list where loses will be stored
        self._value = self._gameRewards
        self._count_loss = 0

    def simulation(self, n_games, prob_head):
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

        for value in self._gameRewards:
            if value < 0:
                self._count_loss +=1
                i=1
                self._gameLosses.append(i)
            elif value >0:
                i = 0
                self._gameLosses.append(i)
        return SetOfGamesOutcomes(self)

    def get_loss_list(self):
        return self._gameLosses

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_max(self):
        """ returns maximum reward"""
        return max(self._gameRewards)

    def get_min(self):
        """ returns minimum reward"""
        return min(self._gameRewards)


class SetOfGamesOutcomes:
    def __init__(self, sim_cohort):
        self._simcohort = sim_cohort
        self._sumStat_expectedRewards = Stat.SummaryStat('Expected Game Rewards', self._simcohort.get_reward_list())
        self._sumStat_expectedLoses = Stat.SummaryStat('Expected Game Loses', self._simcohort.get_loss_list())

    def get_ci_reward(self,alpha):
        return self._sumStat_expectedRewards.get_t_CI(alpha)

    def get_ci_loss(self,alpha):
        return self._sumStat_expectedLoses.get_t_CI(alpha)


# through lens of casino owner who has to pay out the gamblers
trial = SetOfGames(prob_head=0.5, n_games=1000)
dasha=trial.simulation(n_games=1000, prob_head=0.5)
print('95% confidence interval of average expected losses', dasha.get_ci_loss(alpha=0.05))
print('95% confidence interval of average expected rewards', dasha.get_ci_reward(alpha=0.05))
# Problem 2:
# Within this stead-state simulation model, we can represent a real-life situation where we can obtain many observations
# and apply the Law of Large Numbers.
# In this case, we have 1000 games. If one repeats the set of games many times to construct a very large number of
# independent 100(1−alpha) confidence intervals, each based on observations, the proportion of these confidence intervals
# that cover the unknown but true mean is expected to be 1 - alpha. We call this proportion the coverage of
# the confidence interval.
#
# Problem 3:
# In case of casino owner who gets to play this game many times:
# The confidence intervals for the expected rewards is [-31.79297649475803, -20.007023505241968] and the expected
# losses is [0.5766762814896707, 0.6373237185103293]. The true mean of expected rewards and losses should fall into
# those intervals with 95% confidence. These CI shows evidence of the casino owner not paying out a lot to the gamblers
# and thus not losing out a lot of money.
#
# A gambler who gets to plays this game only 10 times:
# This is a transient-state simulation model which represents a real-life situation where the number of
# observations is too small to apply the Law of Large Numbers to make inference about E[x], or the estimate.
# As such, we are more interested in the distribution of X rather than only E[x]. With a transient-state simulation,
# we report the projection intervals. For this simulation, our projection intervals are
# [-135.73676311196448, -4.263236888035507], showing evidence of the the gambler losing money and falling within
# negative projection intervals.

trial2 = SetOfGames(prob_head=0.5, n_games=10)
gambler=trial2.simulation(n_games=10, prob_head=0.5)
print('95% projection interval of average expected rewards', gambler.get_ci_reward(alpha=0.05))