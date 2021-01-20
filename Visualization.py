import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

#changes the matplotlib's figure to black (optional)
style.use('dark_background')


class TradingGraph:
    def __init__(self, dfs, title=None):
        self.dfs = dfs
        
        #Needed to be able to iteratively update the figure
        plt.ion()    
        
        #Define our subplots
        self.fig, self.axs = plt.subplots(2,2)

        #Show the plots
        plt.show()
        
    def plot_candles(self, ax, ohlc, idx):
        #iterate over each ohlc value along with the index
       for row, ix in zip(ohlc, idx):
           if row[3]<row[0]:
               clr = "red"
           else:
               clr = "green"

           #plots a thin line to represent high and low values 
           ax.plot([ix, ix], [row[1], row[2]], lw=1, color=clr)
           #plot a wider line to represent open and close
           ax.plot([ix, ix], [row[3], row[0]], lw=3, color=clr)
           
                
    def render_prices(self, current_step, lbw):     
        for splot, df in zip(self.axs.flatten(), self.dfs):
            splot.clear()
            
            step_range = range(current_step-lbw, current_step)
            idx = np.array(step_range)
            
            #prepare a 3-d numpy array to be used by our plot_candles function
            candlesticks = zip(df['open'].values[step_range], 
                               df['high'].values[step_range],
                               df['low'].values[step_range], 
                               df['close'].values[step_range])
    
            #Plot price using candlestick graph
            self.plot_candles(splot, candlesticks, idx)
            
         
    def render_trades(self,  current_step, lbw, trades):
        for splot, coin in zip(self.axs.flatten(), trades):
            for trade in coin:
                if current_step>trade[1]>current_step-lbw:
                    #plot the point at which the trade happened
                    if trade[0]=='buy':
                        clr = 'red'
                        splot.plot(trade[1], trade[2], 'ro')
                    else:
                        clr = 'green'
                        splot.plot(trade[1], trade[2], 'go')
                
                #the plotted dot won't appear after the look back window is passed so a horizontal line keeps tracks at any time
                splot.hlines(trade[2], current_step-lbw, current_step, linestyle='dashed', colors=[clr])

    def render(self, current_step, window_size, trades):
        self.render_prices(current_step, window_size)
        self.render_trades(current_step, window_size, trades)

        #the draw function redraws the figure after all plots have been executed
        self.fig.canvas.draw() 
        self.fig.canvas.flush_events()
        
        #the pause is necessary to view the frame and allow the live updating mechanism on our figure
        plt.pause(0.1)

    def close(self):
        plt.close()

    
    
    
    
    
