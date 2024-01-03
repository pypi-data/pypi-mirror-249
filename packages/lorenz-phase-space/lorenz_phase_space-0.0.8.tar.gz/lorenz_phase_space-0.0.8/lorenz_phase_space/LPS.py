# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    LPS.py                                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: daniloceano <danilo.oceano@gmail.com>      +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/29 16:13:35 by daniloceano       #+#    #+#              #
#    Updated: 2024/01/02 19:18:46 by daniloceano      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import cmocean
import numpy as np

def get_max_min_values(series):
    max_val = series.max()
    min_val = series.min()

    if max_val < 0:
        max_val = 0

    if min_val > 0:
        min_val = 0

    return max_val, min_val

class LorenzPhaseSpace:
    def __init__(self,
                x_axis: np.ndarray,
                y_axis: np.ndarray,
                marker_color: np.ndarray,
                marker_size: np.ndarray,
                LPS_type: str='mixed',
                zoom: bool=False,
                title: str=False,
                datasource: str=False,
                start: pd.Timestamp=False,
                end: pd.Timestamp=False,
                **kwargs):
        
        # Standardize input data
        self.x_axis = pd.Series(x_axis).reset_index(drop=True)
        self.y_axis = pd.Series(y_axis).reset_index(drop=True)
        self.marker_color = pd.Series(marker_color).reset_index(drop=True)
        self.marker_size = pd.Series(marker_size).reset_index(drop=True)


        # Plotting options
        self.LPS_type = LPS_type
        self.zoom = zoom

        # Optional attributes
        self.title = title
        self.datasource = datasource
        self.start = start
        self.end = end
        self.kwargs = kwargs

    @staticmethod
    def calculate_marker_size(term, zoom=False):
        if zoom:
            # Calculate dynamic intervals based on quantiles if zoom is True
            intervals = list(term.quantile([0.2, 0.4, 0.6, 0.8]))

            # Determine the order of magnitude of the minimum interval value
            min_val = min(intervals)
            order_of_magnitude = 10 ** int(np.floor(np.log10(min_val))) if min_val != 0 else 1

            # Round intervals to two orders of magnitude lower than the minimum value
            round_to = order_of_magnitude / 100
            intervals = [round(v, -int(np.log10(round_to))) for v in intervals]
        else:
            # Default intervals
            intervals = [3e5, 4e5, 5e5, 6e5]

        msizes = [200, 400, 600, 800, 1000]
        sizes = pd.Series([msizes[next(i for i, v in enumerate(intervals) if val <= v)] if val <= intervals[-1] else msizes[-1] for val in term])
        return sizes, intervals
        
    def set_limits(self, ax):    
        if not self.zoom:
            ax.set_xlim(-70, 70)
            y_limits = {
                'mixed': (-20, 20),
                'baroclinic': (-20, 20),
                'barotropic': (-200, 200)
            }
            ax.set_ylim(*y_limits.get(self.LPS_type, (-20, 20)))

    def get_labels(self):
        labels_dict = {}

        if self.LPS_type == 'mixed':
            labels_dict['y_upper'] = 'Eddy is gaining potential energy \n from the mean flow'
            labels_dict['y_lower'] = 'Eddy is providing potential energy \n to the mean flow'
            labels_dict['x_left'] = 'Eddy is gaining kinetic energy \n from the mean flow'
            labels_dict['x_right'] = 'Eddy is providing kinetic energy \n to the mean flow'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Barotropic instability'
            labels_dict['upper_left'] = 'Barotropic and baroclinic instabilities'
            labels_dict['lower_right'] = 'Eddy is feeding the local atmospheric circulation'
            labels_dict['upper_right'] = 'Baroclinic instability'

            if not self.zoom:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Conversion from zonal to eddy Potential Energy (Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n     (Ke - $J m^{-2})$'
            else:
                labels_dict['x_label'] = 'Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'

        elif self.LPS_type == 'baroclinic':
            labels_dict['y_upper'] = 'Zonal temperature gradient feeds \n eddy potential energy'
            labels_dict['y_lower'] = 'Eddy potential energy feeds \n zonal temperature gradient'
            labels_dict['x_left'] = 'Meridional temperature gradient feeds \n eddy kinetic energy'
            labels_dict['x_right'] = 'Eddy kinetic energy consumes \n meridional temperature gradient'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Baroclinic stability'
            labels_dict['upper_left'] = ''
            labels_dict['lower_right'] = ''
            labels_dict['upper_right'] = 'Baroclinic instability'
            
            if self.zoom == False:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ce - $W m^{-2})$'
                labels_dict['y_label'] = 'Conversion from zonal to eddy Potential Energy (Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n     (Ke - $J m^{-2})$'
            elif self.zoom == True:
                labels_dict['x_label'] = 'Ce - $W m^{-2})$'
                labels_dict['y_label'] = 'Ca - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'

        elif self.LPS_type == 'barotropic':
            labels_dict['y_upper'] = 'Importation of Kinectic Energy'
            labels_dict['y_lower'] = 'Exportation of Kinectic Energy'
            labels_dict['x_left'] = 'Eddy is gaining kinetic energy \n from the mean flow'
            labels_dict['x_right'] = 'Eddy is providing kinetic energy \n to the mean flow'
            labels_dict['col_lower'] = 'Subsidence decreases \n eddy potential energy'
            labels_dict['col_upper'] = 'Latent heat release feeds \n eddy potential energy'
            labels_dict['lower_left'] = 'Barotropic instability wihtout \n downstream development'
            labels_dict['upper_left'] = 'Barotropic instability and \n downstream development'
            labels_dict['lower_right'] = 'Barotropic stability without \n downstream development'
            labels_dict['upper_right'] = 'Barotropic stability and \n downstream development'
            
            if self.zoom == False:
                labels_dict['x_label'] = 'Conversion from zonal to eddy Kinetic Energy (Ck - $Wm^{-2})$'
                labels_dict['y_label'] = ' Kinetic Energy transport across boundaries (BKz - $Wm^{-2})$'
                labels_dict['color_label'] = 'Generation of eddy Potential Energy (Ge - $Wm^{-2})$'
                labels_dict['size_label'] = 'Eddy Kinect\n    Energy\n     (Ke - $J m^{-2})$'
            elif self.zoom == True:
                labels_dict['x_label'] = 'Ck - $W m^{-2})$'
                labels_dict['y_label'] = 'Bkz - $W m^{-2})$'
                labels_dict['color_label'] = 'Ge - $W m^{-2})$'
                labels_dict['size_label'] = 'Ke - $J m^{-2})$'

        return labels_dict
    
    def annotate_plot(self, ax, cbar, **kwargs):
        labelpad = kwargs.get('labelpad', 5) if self.zoom else kwargs.get('labelpad', 38)
        annotation_fontsize = kwargs.get('fontsize', 10)
        label_fontsize = kwargs.get('label_fontsize', 14) if self.zoom else kwargs.get('label_fontsize', 10)

        title = self.title
        datasource = self.datasource
        start = self.start
        end = self.end

        if title and datasource:
            ax.text(0,1.12,'System: '+title+' - Data from: '+datasource,
                    fontsize=16,c='#242424',horizontalalignment='left',
                    transform=ax.transAxes)
        if start:
            ax.text(0,1.07,'Start (A):',fontsize=14,c='#242424',
                    horizontalalignment='left',transform=ax.transAxes)
            ax.text(0.14,1.07,str(start),fontsize=14,c='#242424',
                    horizontalalignment='left',transform=ax.transAxes)
        if end:
            ax.text(0,1.025,'End (Z):',fontsize=14,c='#242424',
                    horizontalalignment='left',transform=ax.transAxes)
            ax.text(0.14,1.025,str(end),fontsize=14,c='#242424',
                    horizontalalignment='left',transform=ax.transAxes)
        
        labels = self.get_labels()
            
        # Centering text annotations on y-axis
        yticks, xticks = ax.get_yticks(), ax.get_xticks()
        y_tick_0 = len(yticks) // 2
        y_offset = 0.5 * (yticks[y_tick_0] - yticks[-1])  # Half the distance between two consecutive y-ticks
        x_tick_pos = xticks[0] - ((xticks[1] - xticks[0])/12)

        if not self.zoom:
            ax.text(x_tick_pos, yticks[0] - y_offset, labels['y_lower'], rotation=90, fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#19616C', verticalalignment='center')
            ax.text(x_tick_pos, yticks[-1] + y_offset, labels['y_upper'], rotation=90, fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', verticalalignment='center')
            
            ax.text(0.22,-0.07, labels['x_left'], fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', transform=ax.transAxes)
            ax.text(0.75,-0.07,labels['x_right'], fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#19616C', transform=ax.transAxes)
            
            ax.text(1.13,0.49, labels['col_lower'], rotation=270, fontsize=annotation_fontsize, 
                    horizontalalignment='center', c='#19616C', transform=ax.transAxes)
            ax.text(1.13,0.75, labels['col_upper'], rotation=270,fontsize=annotation_fontsize,
                    horizontalalignment='center', c='#CF6D66', transform=ax.transAxes)
            
            ax.text(0.22,0.03, labels['lower_left'], fontsize=annotation_fontsize, horizontalalignment='center',
                    c='#660066', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.22,0.97, labels['upper_left'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#800000', verticalalignment='center', transform=ax.transAxes)
            
            ax.text(0.75,0.03, labels['lower_right'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#000066', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.75,0.97,labels['upper_right'], fontsize=annotation_fontsize,horizontalalignment='center',
                    c='#660066', verticalalignment='center', transform=ax.transAxes)
        
        # Write labels
        ax.set_xlabel(labels['x_label'], fontsize=label_fontsize,labelpad=labelpad,c='#383838')
        ax.set_ylabel(labels['y_label'], fontsize=label_fontsize,labelpad=labelpad,c='#383838')
        cbar.ax.set_ylabel(labels['color_label'], rotation=270,fontsize=label_fontsize,
                        verticalalignment='bottom', c='#383838',
                        labelpad=labelpad, y=0.59)
        
    @staticmethod
    def plot_legend(ax, intervals, msizes):
        labels = ['< ' + str(intervals[0]),
                  '< ' + str(intervals[1]),
                  '< ' + str(intervals[2]),
                  '< ' + str(intervals[3]),
                  '> ' + str(intervals[3])]

        # Create separate scatter plots for each size category
        for i in range(len(msizes)):
            ax.scatter([], [], c='#383838', s=msizes[i], label=labels[i])

        ax.legend(title='Eddy Kinetic Energy \n      (Ke - $Jm^{-2}$)',
                  fontsize=10, loc='lower left', bbox_to_anchor=(0.97, 0, 0.5, 1),
                  labelcolor='#383838', frameon=False, handlelength=0.3, handleheight=4,
                  borderpad=1.5, scatteryoffsets=[0.1], framealpha=1,
                  handletextpad=1.5, scatterpoints=1)
        
    def plot_lines(self, ax, **kwargs):
        alpha = kwargs.get('alpha', 0.2)
        linewidth = kwargs.get('lw', 20)
        color = kwargs.get('c', '#383838')

        ax.axhline(y=0,linewidth=linewidth, c=color, alpha=alpha,zorder=1)
        ax.axvline(x=0,linewidth=linewidth, c=color, alpha=alpha,zorder=1)

        # Vertical lines for mixed LPS
        if self.LPS_type == 'mixed':
            min_x = int(round(ax.get_xlim()[0],-1)+5)
            max_y = int(round(ax.get_ylim()[1],-1)-5)
            if abs(min_x) > abs(max_y):
                max_y = -min_x
            else:
                min_x = -max_y
            ax.plot(range(0, min_x,-1),range(0, max_y, 1), linewidth=linewidth / 3,
                    c=color, alpha=alpha, zorder=1)
                
    def plot_gradient_lines(self, ax):
        LPS_type = self.LPS_type
        lw, c = 0.5, '#383838'
        num_lines = 20
        x_ticks = ax.get_xticks()
        y_ticks = ax.get_yticks()

        x_previous0 = x_ticks[int((len(x_ticks))/2)-1] * 0.17
        y_previous0 = y_ticks[int((len(y_ticks))/2)-1] * 0.17

        x_offsets = np.linspace(x_previous0, 0, num_lines)
        y_offsets = np.linspace(y_previous0, 0, num_lines)

        alpha_values = np.linspace(0, 0.6, num_lines)

        for i, alpha in enumerate(alpha_values):
            ax.axhline(y=0 + y_offsets[i], linewidth=lw, alpha=alpha, c=c)
            ax.axhline(y=0 - y_offsets[i], linewidth=lw, alpha=alpha, c=c)
            ax.axvline(x=0 + x_offsets[i], linewidth=lw, alpha=alpha, c=c)
            ax.axvline(x=0 - x_offsets[i], linewidth=lw, alpha=alpha, c=c)

        # Diagonal line
        if LPS_type == 'mixed':
            y_ticks = -x_ticks
            for i, alpha in enumerate(alpha_values):
                x, y = x_offsets[i], y_offsets[i]
                ax.plot([x, -x_ticks[-1] + x], [y, -y_ticks[-1] + y], linewidth=lw, alpha=alpha, c=c)
                ax.plot([-x, -x_ticks[-1] - x], [-y, -y_ticks[-1] - y], linewidth=lw, alpha=alpha, c=c)
    
    def plot(self):
        # Logic for plotting
        plt.close('all')
        fig = plt.figure(figsize=(10, 10))
        ax = plt.gca()

        self.set_limits(ax)

        if self.zoom:
            max_colors, min_colors = get_max_min_values(self.marker_color)
            norm = colors.TwoSlopeNorm(vmin=min_colors, vcenter=0, vmax=max_colors)
            extend = 'neither'
        else:
            extend = 'both'
            norm = colors.TwoSlopeNorm(vmin=-30, vcenter=0, vmax=30)

        # arrows connecting dots
        ax.quiver(self.x_axis[:-1], self.y_axis[:-1],
                (self.x_axis[1:].values - self.x_axis[:-1].values) * .97,
                (self.y_axis[1:].values - self.y_axis[:-1].values) * .97,
                angles='xy', scale_units='xy', scale=1, color='k')
        
        # Compute marker sizes and intervals
        sizes, intervals = self.calculate_marker_size(self.marker_size, self.zoom)
        msizes = [200, 400, 600, 800, 1000]

        # Add legend with dynamic intervals and sizes
        self.plot_legend(ax, intervals, msizes)

        # plot the moment of maximum intensity
        ax.scatter(self.x_axis.loc[sizes.idxmax()], self.y_axis.loc[sizes.idxmax()],
                c='None', s=sizes.loc[sizes.idxmax()] * 1.1, zorder=100, edgecolors='k', linewidth=3)

        dots = ax.scatter(self.x_axis, self.y_axis, c=self.marker_color, cmap=cmocean.cm.curl,
                        s=sizes, zorder=100, edgecolors='grey', norm=norm)
        
        # Marking start and end of the system
        ax.text(self.x_axis[0], self.y_axis[0], 'A', zorder=101, fontsize=22, 
                horizontalalignment='center', verticalalignment='center')
        ax.text(self.x_axis.iloc[-1], self.y_axis.iloc[-1], 'Z', zorder=101, fontsize=22,
                horizontalalignment='center', verticalalignment='center')

        # Colorbar
        cax = ax.inset_axes([ax.get_position().x1 + 0.12, ax.get_position().y0 + 0.35, 0.02, ax.get_position().height / 1.5])
        cbar = plt.colorbar(dots, extend=extend, cax=cax)
        for t in cbar.ax.get_yticklabels():
            t.set_fontsize(10)

        self.annotate_plot(ax, cbar)
        self.plot_lines(ax) if self.zoom else self.plot_gradient_lines(ax)

        plt.subplots_adjust(right=0.84, bottom=0.1)

        return fig, ax
        
if __name__ == '__main__':
    sample_file = 'samples/sample_results_1.csv'
    df = pd.read_csv(sample_file, parse_dates={'Datetime': ['Date', 'Hour']}, date_format='%Y-%m-%d %H')

    x_axis = df['Ck'].values
    y_axis = df['Ca'].values
    marker_color = df['Ge'].values
    marker_size = df['Ke'].values

    title = 'sample'
    datasource = 'sample'
    start = pd.to_datetime(df['Datetime'].iloc[0]).strftime('%Y-%m-%d %H:%M')
    end = pd.to_datetime(df['Datetime'].iloc[-1]).strftime('%Y-%m-%d %H:%M')

    # test without zoom
    lps_mixed = LorenzPhaseSpace(x_axis, y_axis, marker_color, marker_size, title=title, datasource=datasource, start=start, end=end)
    fig, ax = lps_mixed.plot()
    plt.savefig('samples/sample_1_LPS_mixed.png', dpi=300)

    # test with zoom
    lps_zoom = LorenzPhaseSpace(x_axis, y_axis, marker_color, marker_size, zoom=True, title=title, datasource=datasource, start=start, end=end)
    fig_zoom, ax_zoom = lps_zoom.plot()
    plt.savefig('samples/sample_1_LPS_mixed_zoom.png', dpi=300)

    # test LPS_type
    lps_baroclinic = LorenzPhaseSpace(x_axis, y_axis, marker_color, marker_size, LPS_type='baroclinic', title=title, datasource=datasource, start=start, end=end)
    lps_baroclinic, ax_mixed = lps_baroclinic.plot()
    plt.savefig('samples/sample_1_LPS_baroclinic.png', dpi=300)

    lps_barotropic = LorenzPhaseSpace(x_axis, y_axis, marker_color, marker_size, LPS_type='barotropic', title=title, datasource=datasource, start=start, end=end)
    lps_barotropic, ax_mixed = lps_barotropic.plot()
    plt.savefig('samples/sample_1_LPS_barotropic.png', dpi=300)


