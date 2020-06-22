env_var = os.environ
import os
import sys
sys.path.append(os.getcwd())
import pprint
import processMeerKAT
import config_parser
from config_parser import validate_args as va
import cal_scripts
from cal_scripts import bookkeeping
import glob
PLOT_DIR = 'plots'
EXTN = 'pdf'

def sort_by_antenna(fname):
    """Sort list of plot files by antenna number with format "PLOT_DIR/caltype_xaxis_yaxis_antXX~YY.EXTN",
    to be passed into key parameter of list.sort.
    Arguments:
    ----------
    fname : str
        Filename of plot file.
    Returns:
    --------
    ant : int
        Antenna numbers."""
    #Remove everything but antenna numbers from filename
    for sub in ['/','freq','cal','amp','phase','time','all','bpass','ant','_','~','.',EXTN,PLOT_DIR]:
        fname = fname.replace(sub,'')
    return int(fname)
def plot_antennas(caltype,fields,calfiles,xaxis='freq',yaxis='amp'):
    """Write multi-page PDF with each page containing plots of solutions
    for individual antennas of input calibrator in 3x2 panels, using plotcal.
    Arguments:
    ----------
    caltype : str
        Type of calibrator being plot ['bpass' | 'phasecal'].
    fields : namedtuple
        Field IDs extracted from config file.
    calfiles : namedtuple
        Filepaths of calibration solution derived from name of MS
    xaxis : str, optional
        X-axis to plot.
    yaxis : str, optional
        Y-axis to plot."""
    calfile = 'caltables/'
    if caltype == 'bpass':
        calfile += os.path.split(calfiles.bpassfile)[1]
        field = fields.bpassfield
    elif caltype == 'phasecal':
        calfile += os.path.split(calfiles.gainfile)[1]
        field = fields.secondaryfield
    else:
        print('Unknown caltype: {0}'.format(caltype))
        return
    #Extract list of antennas for this field (assume all present in first scan)
    scans = msmd.scansforfield(int(field))
    ants = msmd.antennasforscan(scans[0])
    #Iterate through all antennas and plot 3x2 at a time
    i = 0
    while i < ants.size:
        high = i+6
        if high > ants.size-1:
            high = ants.size-1
        antenna='{0}~{1}'.format(ants[i],ants[high])
        figfile='{0}/{1}_{2}_{3}_ant{4}.{5}'.format(PLOT_DIR,caltype,xaxis,yaxis,antenna,EXTN)
        plotcal(caltable=calfile,xaxis=xaxis,yaxis=yaxis,antenna=antenna,subplot=321,
                iteration='antenna',plotsymbol='.',markersize=1,fontsize=5,showgui=False,figfile=figfile)
        i += 6
    #Combine all plots into multi-page PDF and remove individual plots
    plots = glob.glob('{0}/{1}_{2}_{3}_ant*.{4}'.format(PLOT_DIR,caltype,xaxis,yaxis,EXTN))
    plots.sort(key=sort_by_antenna,reverse=False)
    command = 'gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -dAutoRotatePages=/None -sOutputFile={0}/{1}_{2}_{3}_all.pdf {4}'.format(PLOT_DIR,caltype,xaxis,yaxis,' '.join(plots))
    print('Combining all plots into multi-page PDF "{0}/{1}_{2}_{3}_all.pdf"'.format(PLOT_DIR,caltype,xaxis,yaxis))
    os.system(command)
    os.system('rm {0}'.format(' '.join(plots)))
def main():
    config = config_parser.parse_args()['config']
    # Parse config file
    taskvals, config = config_parser.parse_config(config)
    visname = va(taskvals, 'data', 'vis', str)
    keepmms = va(taskvals, 'crosscal', 'keepmms', bool)
    calfiles, caldir = bookkeeping.bookkeeping(visname)
    fields = bookkeeping.get_field_ids(taskvals['fields'])
    msmd.open(visname)
    if not os.path.exists(PLOT_DIR):
        os.mkdir(PLOT_DIR)
    #Plot solutions for bandpass calibrator
    plotms(vis=calfiles.bpassfile, xaxis='Real', yaxis='Imag', coloraxis='corr', plotfile='{0}/bpass_real_imag.png'.format(PLOT_DIR),showgui=False)
    plotms(vis=calfiles.bpassfile, xaxis='freq', yaxis='Amp', coloraxis='antenna1', plotfile='{0}/bpass_freq_amp.png'.format(PLOT_DIR),showgui=False)
    plotms(vis=calfiles.bpassfile, xaxis='freq', yaxis='Phase', coloraxis='antenna1', plotfile='{0}/bpass_freq_phase.png'.format(PLOT_DIR),showgui=False)
    #Plot solutions for phase calibrator
    plotms(vis=calfiles.gainfile, xaxis='Real', yaxis='Imag', coloraxis='corr', plotfile='{0}/phasecal_real_imag.png'.format(PLOT_DIR),showgui=False)
    plotms(vis=calfiles.gainfile, xaxis='Time', yaxis='Amp', coloraxis='antenna1', plotfile='{0}/phasecal_time_amp.png'.format(PLOT_DIR),showgui=False)
    plotms(vis=calfiles.gainfile, xaxis='Time', yaxis='Phase', coloraxis='antenna1', plotfile='{0}/phasecal_time_phase.png'.format(PLOT_DIR),showgui=False)
    #Plot solutions for individual antennas of bandpass and phase calibrator in 3x2 panels
    plot_antennas('bpass',fields,calfiles,xaxis='freq',yaxis='amp')
    plot_antennas('bpass',fields,calfiles,xaxis='freq',yaxis='phase')
    plot_antennas('phasecal',fields,calfiles,xaxis='time',yaxis='amp')
    plot_antennas('phasecal',fields,calfiles,xaxis='time',yaxis='phase')
    extn = 'mms' if keepmms else 'ms'
    for field in fields:
        for subf in field.split(','):
            fname = msmd.namesforfields(int(subf))[0]
            inname = '%s.%s.%s' % (os.path.splitext(visname)[0], fname, extn)
            if not os.path.exists('{0}/{1}_freq_amp.png'.format(PLOT_DIR,fname)):
                plotms(vis=inname, xaxis='freq', yaxis='Amp', coloraxis='corr', plotfile='{0}/{1}_freq_amp.png'.format(PLOT_DIR,fname),showgui=False)
                plotms(vis=inname, xaxis='Real', yaxis='Imag', coloraxis='corr', plotfile='{0}/{1}_real_imag.png'.format(PLOT_DIR,fname),showgui=False)
    msmd.close()
    msmd.done()
if __name__ == "__main__":
    main()