import matplotlib.pyplot as plt
import matplotlib.animation as animation
from NeuroController import NeuroController

# Settings
LABEL_OF_INTEREST = 'leftFoot'  # The label you're interested in monitoring

class DataVisualizer:
    def __init__(self, neuro_controller):
        self.neuro_controller = neuro_controller
        self.fig, self.ax = plt.subplots()
        self.ln, = self.ax.plot([], [], 'r-', animated=True)
        self.xdata, self.ydata = [], []
        self.ax.set_xlim(0, 50)  # Initial x-axis limit
        self.ax.set_ylim(0, 1)   # Probability ranges from 0 to 1
        self.ax.set_title(f'Real-time Probability for {LABEL_OF_INTEREST}')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Probability')

    def init_plot(self):
        self.ln.set_data([], [])
        return self.ln,

    def update_plot(self, frame):
        data = self.neuro_controller.get_latest_data()
        if data and data['label'] == LABEL_OF_INTEREST:
            # Append the current length of xdata as the new x-value, simulating time points
            self.xdata.append(len(self.xdata))  
            # Extract probability, defaulting to 0 if not found
            probability = data.get('predictions', [{}])[0].get('probability', 0)
            self.ydata.append(probability)
            self.ln.set_data(self.xdata, self.ydata)
            # Automatically adjust the x-axis to accommodate new data points
            self.ax.set_xlim(0, max(50, len(self.xdata)))
        return self.ln,

    def start(self):
        # Start the data stream for the specified label
        self.neuro_controller.start_stream(LABEL_OF_INTEREST)
        # Setup the animation
        ani = animation.FuncAnimation(self.fig, self.update_plot, init_func=self.init_plot, blit=True)
        plt.show()

    def stop(self):
        # Stop the data stream when closing the visualizer
        self.neuro_controller.stop_stream()

if __name__ == '__main__':
    neuro_controller = NeuroController()
    visualizer = DataVisualizer(neuro_controller)
    try:
        visualizer.start()
    finally:
        visualizer.stop()
