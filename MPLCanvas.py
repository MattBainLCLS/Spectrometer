import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):


    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.spectral_axes = self.fig.add_subplot(121)
        self.temporal_axes = self.fig.add_subplot(122)
        self.spectral_axes.set_xlabel("Wavelength / nm")
        self.temporal_axes.set_xlabel("Time / fs")
        super(MplCanvas, self).__init__(self.fig)

        self.pos_click_x = None
        self.pos_click_y = None
        self.pos_release_x = None
        self.pos_release_y = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pos_click_x = event.pos().x()/100
            self.pos_click_y = event.pos().y()/100
        else:
            pass
        
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.pos_release_x = event.pos().x()/100
            self.pos_release_y = event.pos().y()/100

            fig_width_x0 = 0
            fig_width_x1 = self.fig.get_figwidth()
            fig_width_y0 = 0
            fig_width_y1 = self.fig.get_figheight()

            x_bound_lower = self.axes.get_position().x0*fig_width_x1
            x_bound_upper = self.axes.get_position().x1*fig_width_x1
            y_bound_lower = self.axes.get_position().y0*fig_width_y1
            y_bound_upper = self.axes.get_position().y1*fig_width_y1

            ### Scale X
            if (self.pos_click_x > x_bound_lower) & (self.pos_click_x < x_bound_upper) & (self.pos_release_x > x_bound_lower) & (self.pos_release_x < x_bound_upper):

                xclick = (self.pos_click_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                xrelease = (self.pos_release_x - x_bound_lower) / (x_bound_upper - x_bound_lower)
                new_xlim_lower = (min([xclick, xrelease]) * (self.axes.get_xlim()[1] - self.axes.get_xlim()[0])) + self.axes.get_xlim()[0]
                new_xlim_upper = (max([xclick, xrelease]) * (self.axes.get_xlim()[1] - self.axes.get_xlim()[0])) + self.axes.get_xlim()[0]

                self.axes.set_xlim([new_xlim_lower, new_xlim_upper])
            ### Scale Y
            if (self.pos_click_y > y_bound_lower) & (self.pos_click_y < y_bound_upper) & (self.pos_release_y > y_bound_lower) & (self.pos_release_y < y_bound_upper):

                yclick = (self.pos_click_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                yrelease = (self.pos_release_y - y_bound_lower) / (y_bound_upper - y_bound_lower)
                new_ylim_lower = (min([yclick, yrelease]) * (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])) + self.axes.get_ylim()[0]
                new_ylim_upper = (max([yclick, yrelease]) * (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])) + self.axes.get_ylim()[0]
    
                self.axes.set_ylim([new_ylim_lower, new_ylim_upper])
                
            self.draw()
        else:
            pass
