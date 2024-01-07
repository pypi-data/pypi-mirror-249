import math
import matplotlib.pyplot as plt
from scipy.special import comb
from .Generaldistribution import Distribution

class Binomial(Distribution):
    """ Binomial distribution class for calculating and 
    visualizing a Binomial distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) the total number of trials
            
    """
    
    def __init__(self, prob=.5, size=20):
        
        self.p = prob
        self.n = size

        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
                
        return self.p * self.n 



    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        return math.sqrt(self.n * self.p * (1 - self.p))
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        

        self.n = len(self.data)
        self.p = self.data.count(1)/self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return (self.p, self.n)
            
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        zero_count = self.data.count(0)
        one_count = self.data.count(1)
        
        plt.bar([0,1], [zero_count, one_count])
        plt.title('Binomial Count of Results')
        plt.xlabel('Value')
        plt.ylabel('count')
        plt.show()
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        
        return (comb(self.n, k)) * (self.p ** k) * ((1 - self.p) ** (self.n - k))         

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        x = range(self.n + 1)
        y = []
        for k in x:
            y.append(self.pdf(k))
            
        plt.bar(x, y)
        plt.xlabel('Number of Successes (k)')
        plt.ylabel('Probability')
        plt.title('Binomial PDF')
        plt.show()
        
        return x,y
                
    def __add__(self, other):
        
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        
        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise
        
        new_binomial = Binomial()
        new_binomial.p = self.p
        new_binomial.n = self.n + other.n
        new_binomial.calculate_mean()
        new_binomial.calculate_stdev()
        
        return new_binomial
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """
    
        return "mean {}, standard deviation {:.2f}, p {:.2f} n {}".format(self.mean, self.stdev, self.p, self.n)
    
