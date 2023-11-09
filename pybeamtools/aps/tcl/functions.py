import tkinter
from .helpers import exec_with_tcl

class Lib:

    @staticmethod
    def APSSelectADLFont(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['height', 'type']

        """
        return exec_with_tcl('APSSelectADLFont', *args, **kwargs)

    @staticmethod
    def APSCreateToplevelADLScreen(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: widget args
        APS parsed args: ['filename', 'macro']

        """
        return exec_with_tcl('APSCreateToplevelADLScreen', *args, **kwargs)

    @staticmethod
    def APSCreateADLScreen(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
         Usage: APSCreateADLScreen widget
        [-parent <string>]
        [-filename <file>]
        [-macro <string>]

        Creates	$parent$widget
        TCL function args: widget args
        APS parsed args: ['filename', 'parent', 'macro', 'uniqueID']

        """
        return exec_with_tcl('APSCreateADLScreen', *args, **kwargs)

    @staticmethod
    def APSInitiateADLLinks(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['uniqueID']

        """
        return exec_with_tcl('APSInitiateADLLinks', *args, **kwargs)

    @staticmethod
    def APSMonitorADLLinks(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['uniqueID']

        """
        return exec_with_tcl('APSMonitorADLLinks', *args, **kwargs)

    @staticmethod
    def APSADLEventHandler(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['type', 'uniqueID', 'index']

        """
        return exec_with_tcl('APSADLEventHandler', *args, **kwargs)

    @staticmethod
    def APSSetADLValue(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['type', 'uniqueID', 'index']

        """
        return exec_with_tcl('APSSetADLValue', *args, **kwargs)

    @staticmethod
    def APSPrepADLElementFormat(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data macro
        APS parsed args: None

        """
        return exec_with_tcl('APSPrepADLElementFormat', *args, **kwargs)

    @staticmethod
    def APSConvertADLElementFormat(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSConvertADLElementFormat', *args, **kwargs)

    @staticmethod
    def APSParseADLFileElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLFileElement', *args, **kwargs)

    @staticmethod
    def APSParseADLDisplayElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLDisplayElement', *args, **kwargs)

    @staticmethod
    def APSParseADLColormapElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLColormapElement', *args, **kwargs)

    @staticmethod
    def APSParseADLRectangleElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLRectangleElement', *args, **kwargs)

    @staticmethod
    def APSParseADLOvalElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLOvalElement', *args, **kwargs)

    @staticmethod
    def APSParseADLPolylineElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLPolylineElement', *args, **kwargs)

    @staticmethod
    def APSParseADLPolygonElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLPolygonElement', *args, **kwargs)

    @staticmethod
    def APSParseADLArcElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLArcElement', *args, **kwargs)

    @staticmethod
    def APSParseADLImageElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLImageElement', *args, **kwargs)

    @staticmethod
    def APSParseADLCompositeElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data uniqueID
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLCompositeElement', *args, **kwargs)

    @staticmethod
    def APSParseADLValuatorElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLValuatorElement', *args, **kwargs)

    @staticmethod
    def APSParseADLTextElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLTextElement', *args, **kwargs)

    @staticmethod
    def APSParseADLRelateddisplayElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLRelateddisplayElement', *args, **kwargs)

    @staticmethod
    def APSParseADLShellcommandElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLShellcommandElement', *args, **kwargs)

    @staticmethod
    def APSParseADLTextupdateElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLTextupdateElement', *args, **kwargs)

    @staticmethod
    def APSParseADLTextentryElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLTextentryElement', *args, **kwargs)

    @staticmethod
    def APSParseADLMessagebuttonElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLMessagebuttonElement', *args, **kwargs)

    @staticmethod
    def APSParseADLChoicebuttonElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLChoicebuttonElement', *args, **kwargs)

    @staticmethod
    def APSParseADLBarElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLBarElement', *args, **kwargs)

    @staticmethod
    def APSParseADLIndicatorElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLIndicatorElement', *args, **kwargs)

    @staticmethod
    def APSParseADLStripChartElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLStripChartElement', *args, **kwargs)

    @staticmethod
    def APSParseADLPlotElement(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLPlotElement', *args, **kwargs)

    @staticmethod
    def APSCartesianPlot(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args:  widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'title', 'xlabel', 'ylabel', 'backgroundColor', 'foregroundColor', 'axisColor', 'plotBackgroundColor', 'plotForegroundColors', 'selectionColor', 'xmin', 'xmax', 'ymin', 'ymax', 'width', 'height', 'gridPack', 'xVariables', 'yVariables', 'contextHelp']

        """
        return exec_with_tcl('APSCartesianPlot', *args, **kwargs)

    @staticmethod
    def APSCartesianPlotUpdate(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: widget index lines plane var element action
        APS parsed args: None

        """
        return exec_with_tcl('APSCartesianPlotUpdate', *args, **kwargs)

    @staticmethod
    def APSStripChart(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args:  widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'title', 'xlabel', 'ylabel', 'backgroundColor', 'foregroundColor', 'axisColor', 'plotBackgroundColor', 'plotForegroundColors', 'selectionColor', 'xmin', 'xmax', 'ymin', 'ymax', 'width', 'height', 'gridPack', 'xVariables', 'yVariables', 'contextHelp', 'period', 'units']

        """
        return exec_with_tcl('APSStripChart', *args, **kwargs)

    @staticmethod
    def APSStripChartUpdate(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: widget index lines plane var period
        APS parsed args: None

        """
        return exec_with_tcl('APSStripChartUpdate', *args, **kwargs)

    @staticmethod
    def APSParseADLData(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: data uniqueID
        APS parsed args: None

        """
        return exec_with_tcl('APSParseADLData', *args, **kwargs)

    @staticmethod
    def APSParseADLFile(*args, **kwargs):
        """
        Location: APSADLscreen.tcl
        TCL function args: args
        APS parsed args: ['filename', 'uniqueID', 'canvas', 'macro']

        """
        return exec_with_tcl('APSParseADLFile', *args, **kwargs)

    @staticmethod
    def APSAlertBox(*args, **kwargs):
        """
        Location: APSAlertBox.tcl
        Usage: APSAlertBox widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-contextHelp <string>]
        [-errorMessage <string>]
        [-modeless 1]
        [-type {error | warning | done}]
        [-name <string>]
        [-beep {no | once | continuous | backoff}]
        [-volume <fraction>]
        [-announceWorkstion {0|1}]
        [-toneType {sr|booster|linac|par|default}]

        Creates	$parent$widget.
        	msg
        	buttonRow.ok.button
        	TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'errorMessage', 'modeless', 'contextHelp', 'type', 'name', 'beep', 'announceWorkstation', 'toneType', 'volume']

        """
        return exec_with_tcl('APSAlertBox', *args, **kwargs)

    @staticmethod
    def APSAlertBeep(*args, **kwargs):
        """
        Location: APSAlertBox.tcl
        TCL function args: args
        APS parsed args: ['beep', 'interval', 'widget', 'announceWorkstation', 'toneType', 'volume']

        """
        return exec_with_tcl('APSAlertBeep', *args, **kwargs)

    @staticmethod
    def APSDebugPath(*args, **kwargs):
        """
        Location: APSDebugPath.tcl
        Usage: APSDebugPath

        This routine reconfigures both the Tcl/Tk auto_path (for procedures) and the search PATH (for executables) so that debugging can be done from different locations than those used by users.

        If the environment variable OAG_DEBUG_AUTO_PATH is set, then it preappends the paths in OAG_DEBUG_AUTO_PATH to the auto_path and causes
        auto_load to reinitialize the next time it is used.

        If the environment variable OAG_DEBUG_PATH is set, then it preappends the paths in OAG_DEBUG_PATH to the environment variable PATH, except that if . was the first element in PATH, then it remains the first.

        Otherwise it does nothing, so it can safely be left in the script.

        The paths in both OAG_DEBUG_AUTO_PATH and OAG_DEBUG_PATH are colon delimited if there are more than one.
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDebugPath', *args, **kwargs)

    @staticmethod
    def APSExecLog(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSExecLog widget
        [-name <string>]
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-unixCommand <string>]
        [-callback <script>]
        [-abortCallback <script>]
        [-cancelCallback <script>]
        [-width <string>]
        [-height <string>]
        [-contextHelp <string>]
        [-lineLimit <number>]

        Creates	$parent$widget.
        	userFrame
        	buttonRow.ok.button
        	buttonRow.cancel.button
        	buttonRow.print.button
        	userFrame.text.text
        	userFrame.text.scroll

        Returns an <id> for subsequent use in APSExecLogAbort procedure, or -1 if open failed.TCL function args: widget args
        APS parsed args: ['parent', 'unixCommand', 'noPack', 'packOption', 'contextHelp', 'callback', 'name', 'width', 'height', 'abortCallback', 'cancelCallback', 'lineLimit', 'font', 'killSignal', 'closeInput']

        """
        return exec_with_tcl('APSExecLog', *args, **kwargs)

    @staticmethod
    def APSExecLogAbort(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSExecLogAbort [-id <id>] [-destroy 1]TCL function args: args
        APS parsed args: ['id', 'destroy']

        """
        return exec_with_tcl('APSExecLogAbort', *args, **kwargs)

    @staticmethod
    def APSExecLogCallback(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: widget input log callback
        APS parsed args: None

        """
        return exec_with_tcl('APSExecLogCallback', *args, **kwargs)

    @staticmethod
    def APSExecLogStop(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: widget input pipePid callback signal
        APS parsed args: None

        """
        return exec_with_tcl('APSExecLogStop', *args, **kwargs)

    @staticmethod
    def APSExecLogAbortInternal(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: input pipePid callback signal closeInput
        APS parsed args: None

        """
        return exec_with_tcl('APSExecLogAbortInternal', *args, **kwargs)

    @staticmethod
    def APSExecLogPrint(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: textwidget cmd
        APS parsed args: None

        """
        return exec_with_tcl('APSExecLogPrint', *args, **kwargs)

    @staticmethod
    def APSExec(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSExec
        [-unixCommand <string>]
        [-callback <script>]
        [-outputVariable <variable>]

        Executes command given by -unixCommand option.
        If -callback is given, <script> will be executed upon
        completion of unixCommand. Output of unixCommand
        is normally thrown away. If -outputVariable is given,
        command output will be stored in global <variable>.TCL function args: args
        APS parsed args: ['unixCommand', 'callback', 'outputVariable']

        """
        return exec_with_tcl('APSExec', *args, **kwargs)

    @staticmethod
    def APSExecCallback(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: input callback outputVariable saveOutput
        APS parsed args: None

        """
        return exec_with_tcl('APSExecCallback', *args, **kwargs)

    @staticmethod
    def APSBGExec(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSBGExec
        [-command <string>]
        [-output <variable>]
        [-error <variable>]
        [-status <variable>]

        Executes command given by -command option.
        Works like the normal exec command where you can catch the results and errors. If the -output, -error, and or status variables are used the related information will be stored in those global variables. One advantage of using APSBGExec over exec is that there will be a busy indicator in the menu bar and the executable is killable if necessary.TCL function args: args
        APS parsed args: ['output', 'error', 'status', 'command']

        """
        return exec_with_tcl('APSBGExec', *args, **kwargs)

    @staticmethod
    def APSBusyIndicatorStart(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSBusyIndicatorStart
        [-killVariable <variable>]

        This procedure is used to start the busy indicator ont he menu bar. If the killVariable option is passed it is assumed that the bgexec command is being called and that setting this variable will kill the bgexec command. This is done by the user pressing the stop sign button.TCL function args:  args
        APS parsed args: ['killVariable']

        """
        return exec_with_tcl('APSBusyIndicatorStart', *args, **kwargs)

    @staticmethod
    def APSBusyIndicatorContinue(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args:  args
        APS parsed args: None

        """
        return exec_with_tcl('APSBusyIndicatorContinue', *args, **kwargs)

    @staticmethod
    def APSBusyIndicatorStop(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSBusyIndicatorStop

        Used with APSBusyIndicatorStart to stop the busy indicator.TCL function args:  args
        APS parsed args: None

        """
        return exec_with_tcl('APSBusyIndicatorStop', *args, **kwargs)

    @staticmethod
    def APSExecReplacement(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSExecReplacement', *args, **kwargs)

    @staticmethod
    def APSRenameExecToAPSBGExec(*args, **kwargs):
        """
        Location: APSExecLog.tcl
        Usage: APSRenameExectoAPSBGExec

        After this is called every exec command is actually using APSBGExec. The original exec command will be renamed to aps_tcl_exec.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRenameExecToAPSBGExec', *args, **kwargs)

    @staticmethod
    def APSFindPVDataFiles(*args, **kwargs):
        """
        Location: APSFindDatedFiles.tcl
        Usage: APSFindPVDataFiles -ReadbackName <string>
        -StartTime <epochTime> -EndTime <epochTime>
        -startDateList <dateList> -endDateList <dateList>
        -SampleIntervals <list>

        where <dateList> contains year and Julian day.TCL function args: args
        APS parsed args: ['ReadbackName', 'StartTime', 'EndTime', 'SampleIntervals', 'startDateList', 'endDateList']

        """
        return exec_with_tcl('APSFindPVDataFiles', *args, **kwargs)

    @staticmethod
    def APSFindFilesBetweenDates(*args, **kwargs):
        """
        Location: APSFindDatedFiles.tcl
        Usage: APSFindFilesBetweenDates -rootname <string>
        -startDateList <dateList> -endDateList <dateList> [-extensionList <list>]
        [-suffix <string>] [-directory <string>] [-tailsOnly 1] [-filter <filter>]

        where <dateList> contains year and Julian day.TCL function args: args
        APS parsed args: ['rootname', 'directory', 'startDateList', 'endDateList', 'extensionList', 'tailsOnly', 'suffix', 'filter', 'excludeList']

        """
        return exec_with_tcl('APSFindFilesBetweenDates', *args, **kwargs)

    @staticmethod
    def APSFindMonthlyFilesBetweenDates(*args, **kwargs):
        """
        Location: APSFindDatedFiles.tcl
        Usage: APSFindMonthlyFilesBetweenDates -rootname <string>
        -startDateList <dateList> -endDateList <dateList> [-extensionList <list>]
        [-suffix <string>] [-directory <string>] [-tailsOnly 1]

        where <dateList> contains year and month.TCL function args: args
        APS parsed args: ['rootname', 'directory', 'startDateList', 'endDateList', 'extensionList', 'tailsOnly', 'suffix']

        """
        return exec_with_tcl('APSFindMonthlyFilesBetweenDates', *args, **kwargs)

    @staticmethod
    def APSReturnOldestFile(*args, **kwargs):
        """
        Location: APSFindDatedFiles.tcl
        usage: APSReturnOldestFile -fileList <list>

        Returns the name of the oldest file in the list.TCL function args: args
        APS parsed args: ['fileList']

        """
        return exec_with_tcl('APSReturnOldestFile', *args, **kwargs)

    @staticmethod
    def APSReturnYoungestFile(*args, **kwargs):
        """
        Location: APSFindDatedFiles.tcl
        usage: APSReturnYoungestFile -fileList <list>

        Returns the name of the youngest file in the list.TCL function args: args
        APS parsed args: ['fileList']

        """
        return exec_with_tcl('APSReturnYoungestFile', *args, **kwargs)

    @staticmethod
    def APSClipROI(*args, **kwargs):
        """
        Location: APSImageProcess.tcl
        Usage: APSClipROI
        [-input <inputfile>]
        [-output <outputfile>]
        [-imageColumns <string>]
        [-plot <0|1>]
        [-formatString <string>]
        [-xSpotMin <number>]
        [-xSpotMax <number>]
        [-ySpotMin <number>]
        [-ySpotMax <number>]
        Clips the region of interest from an image file.TCL function args: args
        APS parsed args: ['input', 'output', 'imageColumns', 'plot', 'formatString', 'xSpotMin', 'xSpotMax', 'ySpotMin', 'ySpotMax']

        """
        return exec_with_tcl('APSClipROI', *args, **kwargs)

    @staticmethod
    def APSKnobOpen(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobOpen [-fileName <configFileName>]
        Starts an instance of tclKnobs in server mode using given config file.
        Returns a unique <id> required by the other APSKnob procedures. Note you
        must perform an APSKnobClose, lest ye leave a number of resources hanging.TCL function args: args
        APS parsed args: ['fileName']

        """
        return exec_with_tcl('APSKnobOpen', *args, **kwargs)

    @staticmethod
    def APSKnobGetKnobList(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobGetKnobList [-id <id>]
        Returns the list of knobs which were configured by APSKnobOpen.TCL function args: args
        APS parsed args: ['id']

        """
        return exec_with_tcl('APSKnobGetKnobList', *args, **kwargs)

    @staticmethod
    def APSKnobChildUp(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        TCL function args: tclKnobsID
        APS parsed args: None

        """
        return exec_with_tcl('APSKnobChildUp', *args, **kwargs)

    @staticmethod
    def APSKnobClose(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobClose [-id <id>]
        Closes knob session, terminating the tclKnob server and cleaning up resources.TCL function args: args
        APS parsed args: ['id']

        """
        return exec_with_tcl('APSKnobClose', *args, **kwargs)

    @staticmethod
    def APSKnobTick(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobTick [-id <id>] [-knob <knobName>] [-direction <dir>]
        Tick the given <knobName> "up" or "down"
        The knob offset after the tick is returned.TCL function args: args
        APS parsed args: ['id', 'knob', 'direction']

        """
        return exec_with_tcl('APSKnobTick', *args, **kwargs)

    @staticmethod
    def APSKnobGain(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobGain [-id <id>] [-knob <knobName>] [-direction <dir>]
        Tick the given <knobName> gain "up" or "down" TCL function args: args
        APS parsed args: ['id', 'knob', 'direction']

        """
        return exec_with_tcl('APSKnobGain', *args, **kwargs)

    @staticmethod
    def APSKnobGetGain(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobGetGain [-id <id>] [-knob <knobName>]
        Returns the current gain setting for <knobName>.TCL function args: args
        APS parsed args: ['id', 'knob']

        """
        return exec_with_tcl('APSKnobGetGain', *args, **kwargs)

    @staticmethod
    def APSKnobGetOffset(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobGetOffset [-id <id>] [-knob <knobName>]
        Returns the current offset of <knobName>.TCL function args: args
        APS parsed args: ['id', 'knob']

        """
        return exec_with_tcl('APSKnobGetOffset', *args, **kwargs)

    @staticmethod
    def APSKnobRestoreGain(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobRestoreGain [-id <id>] [-knob <knobName>]
        Restore the gain of <knobName> to what it was at time of APSKnobOpen.TCL function args: args
        APS parsed args: ['id', 'knob']

        """
        return exec_with_tcl('APSKnobRestoreGain', *args, **kwargs)

    @staticmethod
    def APSKnobSave(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobSave [-id <id>] [-knob <knobName>] [-all 1]
        Save complete state of <knobName>, or all knobs if -all option is set.TCL function args: args
        APS parsed args: ['id', 'knob', 'all']

        """
        return exec_with_tcl('APSKnobSave', *args, **kwargs)

    @staticmethod
    def APSKnobRestore(*args, **kwargs):
        """
        Location: APSKnobs.tcl
        Usage: APSKnobRestore [-id <id>] [-knob <knobName>] [-all 1]
        Save complete state of <knobName>, or all knobs if -all option is set.TCL function args: args
        APS parsed args: ['id', 'knob', 'all']

        """
        return exec_with_tcl('APSKnobRestore', *args, **kwargs)

    @staticmethod
    def APSMeasureOneVariableResponse(*args, **kwargs):
        """
        Location: APSMeasureOneVariableResponse.tcl
        TCL function args: args
        APS parsed args: ['readback', 'control', 'average', 'changePause', 'interval', 'steps', 'initialValue', 'finalValue', 'output', 'relativeToOrig', 'interactive', 'destroyWindow']

        """
        return exec_with_tcl('APSMeasureOneVariableResponse', *args, **kwargs)

    @staticmethod
    def processGain(*args, **kwargs):
        """
        Location: APSMeasureOneVariableResponse.tcl
        TCL function args: args
        APS parsed args: ['filename', 'readback', 'control', 'output']

        """
        return exec_with_tcl('processGain', *args, **kwargs)

    @staticmethod
    def APSMpxBTSMatrixInfo(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpxBTSMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpxBTSMatrix(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxBTSMatrix', *args, **kwargs)

    @staticmethod
    def APSMpxBTSMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxBTSMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpyBTSMatrixInfo(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpyBTSMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpyBTSMatrix(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyBTSMatrix', *args, **kwargs)

    @staticmethod
    def APSMpyBTSMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpBTSMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyBTSMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchLatticeInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchLatticeInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchLatticeInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchLatticeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchLattice(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['Hz', 'ShortFilename', 'IRamp']

        """
        return exec_with_tcl('APSMpBoosterSwitchLattice', *args, **kwargs)

    @staticmethod
    def APSMpRestoreBoosterSettings(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSMpRestoreBoosterSettings', *args, **kwargs)

    @staticmethod
    def APSMpChooseBoosterRefFile(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpChooseBoosterRefFile', *args, **kwargs)

    @staticmethod
    def APSMpLoadBoosterRampTable(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['rampTable']

        """
        return exec_with_tcl('APSMpLoadBoosterRampTable', *args, **kwargs)

    @staticmethod
    def APSMpSwitchDefaultLattice(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['lattice', 'energy', 'IRamp', 'Hz', 'scrFile']

        """
        return exec_with_tcl('APSMpSwitchDefaultLattice', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRampAFG(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['filename', 'rampSteps', 'rampPause', 'restoreBM']

        """
        return exec_with_tcl('APSMpBoosterRampAFG', *args, **kwargs)

    @staticmethod
    def APSMpCheckBoosterLattice(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['qf', 'qd']

        """
        return exec_with_tcl('APSMpCheckBoosterLattice', *args, **kwargs)

    @staticmethod
    def APSCheckBControlStatus(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCheckBControlStatus', *args, **kwargs)

    @staticmethod
    def APSMpBoosterChangeRampDelayInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterChangeRampDelayInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterChangeRampDelayInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterChangeRampDelayInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterChangeRampDelay(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['deltaDelay']

        """
        return exec_with_tcl('APSMpBoosterChangeRampDelay', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToVRampInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToVRampInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToVRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToVRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToIRampInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToIRampInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToIRampInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToIRampInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToIRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToIRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo2HzIRampInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo2HzIRampInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo2HzIRampInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo2HzIRampInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo1HzIRampInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo1HzIRampInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo1HzIRampInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo1HzIRampInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchIRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['switchTo', 'scrFile', 'popup', 'energy']

        """
        return exec_with_tcl('APSMpSwitchIRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo1HzIRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo1HzIRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo2HzIRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo2HzIRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToLongIRampInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToLongIRampInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchToLongIRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchToLongIRamp', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo1HzIRampFromLongRampInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo1HzIRampFromLongRampInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchTo1HzIRampFromLongRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchTo1HzIRampFromLongRamp', *args, **kwargs)

    @staticmethod
    def APSCheckBoosterIRampMode(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCheckBoosterIRampMode', *args, **kwargs)

    @staticmethod
    def APSMpSwitchBTXBeamEnergyInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchBTXBeamEnergyInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchBTXBeamEnergyInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchBTXBeamEnergyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSwitchBTXBeamEnergy(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchBTXBeamEnergy', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRampRFFrequencyInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRampRFFrequencyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterUpdateRFFreq(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['saveFile']

        """
        return exec_with_tcl('APSMpBoosterUpdateRFFreq', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRampRFFrequencyInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRampRFFrequencyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRampRFFrequency(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRampRFFrequency', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRFFreqScanReviewInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRFFreqScanReviewInfo', *args, **kwargs)

    @staticmethod
    def SetRFFreqScanReviewFile(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: index
        APS parsed args: None

        """
        return exec_with_tcl('SetRFFreqScanReviewFile', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRFFreqScanReviewInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRFFreqScanReviewInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterRFFreqScanReview(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterRFFreqScanReview', *args, **kwargs)

    @staticmethod
    def APSMpStartParTimingFeedforward(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartParTimingFeedforward', *args, **kwargs)

    @staticmethod
    def APSMpStopParTimingFeedforward(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopParTimingFeedforward', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchSDInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchSDInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchSDInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchSDInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchSD(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['ShortFilename']

        """
        return exec_with_tcl('APSMpBoosterSwitchSD', *args, **kwargs)

    @staticmethod
    def APSBoosterLoadSDUSafetyRamp(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSBoosterLoadSDUSafetyRamp', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSDUSetFullPower(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['SCRFile', 'magnet']

        """
        return exec_with_tcl('APSMpBoosterSDUSetFullPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSDUSetStandbyPower(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterSDUSetStandbyPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSDUSetNoPower(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterSDUSetNoPower', *args, **kwargs)

    @staticmethod
    def APSCheckBoosterInjectionControllaw(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['xControllaw', 'injControllaw', 'longControlla']

        """
        return exec_with_tcl('APSCheckBoosterInjectionControllaw', *args, **kwargs)

    @staticmethod
    def APSStartLongBoosterControllawFull(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['subDir']

        """
        return exec_with_tcl('APSStartLongBoosterControllawFull', *args, **kwargs)

    @staticmethod
    def APSMpOperator1Hz2HzSwitchInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOperator1Hz2HzSwitchInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpOperator1Hz2HzSwitchInfo(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOperator1Hz2HzSwitchInfo', *args, **kwargs)

    @staticmethod
    def APSMpOperator1Hz2HzSwitch(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: ['boosterSCR', 'LPLSCR', 'Hz']

        """
        return exec_with_tcl('APSMpOperator1Hz2HzSwitch', *args, **kwargs)

    @staticmethod
    def APSMpVerifyInjectorFileLinks(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpVerifyInjectorFileLinks', *args, **kwargs)

    @staticmethod
    def APSMpVerifyInjectorFileLinksInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterSwitchLattice.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpVerifyInjectorFileLinksInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpParBypassShutdownInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassShutdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassShutdown(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: args
        APS parsed args: ['Q', 'H', 'V', 'DCPS']

        """
        return exec_with_tcl('APSMpParBypassShutdown', *args, **kwargs)

    @staticmethod
    def APSMpParBypassShutdownInitDialog(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassShutdownInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpParBypassZeroDCPSSetpointsInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassZeroDCPSSetpointsInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassZeroDCPSSetpoints(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: args
        APS parsed args: ['Q', 'H', 'V']

        """
        return exec_with_tcl('APSMpParBypassZeroDCPSSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpParBypassTurnOffDCPSInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassTurnOffDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassTurnOffDCPS(*args, **kwargs):
        """
        Location: APSMpBypassTurnOff.tcl
        TCL function args: args
        APS parsed args: ['Q', 'H', 'V']

        """
        return exec_with_tcl('APSMpParBypassTurnOffDCPS', *args, **kwargs)

    @staticmethod
    def APSMpConfigInjControllawBPMsInfo(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigInjControllawBPMsInfo', *args, **kwargs)

    @staticmethod
    def APSMpConfigInjControllawBPMsInitDialog(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigInjControllawBPMsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpConfigInjControllawBPMs(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigInjControllawBPMs', *args, **kwargs)

    @staticmethod
    def APSMpConfigLongControllawActuatorsInfo(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigLongControllawActuatorsInfo', *args, **kwargs)

    @staticmethod
    def APSMpConfigLongControllawActuatorsInitDialog(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigLongControllawActuatorsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpConfigLongControllawActuators(*args, **kwargs):
        """
        Location: APSMpConfigInjControllawBPMs.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpConfigLongControllawActuators', *args, **kwargs)

    @staticmethod
    def APSMpReturn(*args, **kwargs):
        """
        Location: APSMpDummy.tcl
        Usage: APSMpReturn code [results]
        where code may be ok or error

        This procedure should be called in place of usual tcl return when creating
        machine procedures. Note that a code of error will generate a catchable
        error in the calling procedure.TCL function args: code {results ""}
        APS parsed args: None

        """
        return exec_with_tcl('APSMpReturn', *args, **kwargs)

    @staticmethod
    def APSMpStep(*args, **kwargs):
        """
        Location: APSMpDummy.tcl
        Usage: APSMpStep stepName
        [-vars <varList>]
        [-promptDialog <procName>] where <procName> is of form
        	  proc <procName> {frame} {}

        Defines a step within a machine procedure. When executed from PEM,
        each step name is displayed as it is executed. When a procedure is
        executed in Automatic mode or outside of the PEM, steps are ignored.
        See document for details on use of -vars and -promptDialog options.TCL function args: stepName args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStep', *args, **kwargs)

    @staticmethod
    def APSMpxLTPMatrixInfo(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpxLTPMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpxLTPMatrix(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxLTPMatrix', *args, **kwargs)

    @staticmethod
    def APSMpxLTPMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxLTPMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpyLTPMatrixInfo(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpyLTPMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpyLTPMatrix(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyLTPMatrix', *args, **kwargs)

    @staticmethod
    def APSMpyLTPMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyLTPMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTPShutdownInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPShutdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPShutdown(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampdownTime', 'Q', 'H', 'V', 'B1', 'DCPS']

        """
        return exec_with_tcl('APSMpLTPShutdown', *args, **kwargs)

    @staticmethod
    def APSMpLTPShutdownInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPShutdownInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTPZeroDCPSSetpointsInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPZeroDCPSSetpointsInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPZeroDCPSSetpoints(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: args
        APS parsed args: ['Q', 'H', 'V', 'B1']

        """
        return exec_with_tcl('APSMpLTPZeroDCPSSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpLTPTurnOffDCPSInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPTurnOffDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPTurnOffDCPS(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: args
        APS parsed args: ['Q', 'H', 'V', 'B1']

        """
        return exec_with_tcl('APSMpLTPTurnOffDCPS', *args, **kwargs)

    @staticmethod
    def APSMpLTPRampdown(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: args
        APS parsed args: ['rampdownTime', 'block', 'Q', 'H', 'V', 'B1']

        """
        return exec_with_tcl('APSMpLTPRampdown', *args, **kwargs)

    @staticmethod
    def APSMpLTPRampdownWait(*args, **kwargs):
        """
        Location: APSMpLTPTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPRampdownWait', *args, **kwargs)

    @staticmethod
    def APSMpPARLETShutdownInfo(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETShutdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETShutdown(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampdownTime', 'DCPS', 'PulsedPS', 'rfSystems', 'LTPB1']

        """
        return exec_with_tcl('APSMpPARLETShutdown', *args, **kwargs)

    @staticmethod
    def APSMpPARLETShutdownInitDialog(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETShutdownInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARLETZeroDCPSSetpoints(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETZeroDCPSSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpPARLETTurnOffDCPS(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETTurnOffDCPS', *args, **kwargs)

    @staticmethod
    def APSMpPARLETRampdownInfo(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETRampdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStartRampdown(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: args
        APS parsed args: ['rampdownTime']

        """
        return exec_with_tcl('APSMpPARLETStartRampdown', *args, **kwargs)

    @staticmethod
    def APSMpPARLETCheckRampdown(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOff.tcl
        TCL function args: args
        APS parsed args: ['partList', 'warnOnly', 'LTP_Q', 'LTP_B1']

        """
        return exec_with_tcl('APSMpPARLETCheckRampdown', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStartUpInfo(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStartUp(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'conditioningTime', 'restoreFile', 'DCPS', 'PulsedPS', 'rfSystems', 'particle', 'standardizeLTPB1', 'PARdipole', 'PARquads', 'PARsextupoles', 'PARcorrectors', 'LTPdipole', 'LTPquads', 'LTPcorrectors', 'PTBdipole', 'PTBquads', 'PTBcorrectors']

        """
        return exec_with_tcl('APSMpPARLETStartUp', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARLETRemoveFlags(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries', 'beamline']

        """
        return exec_with_tcl('APSMpPARLETRemoveFlags', *args, **kwargs)

    @staticmethod
    def APSMpPARLETClearAperture(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries', 'beamline']

        """
        return exec_with_tcl('APSMpPARLETClearAperture', *args, **kwargs)

    @staticmethod
    def APSMpLTPPTBOpenValves(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries', 'beamline']

        """
        return exec_with_tcl('APSMpLTPPTBOpenValves', *args, **kwargs)

    @staticmethod
    def APSPLETMPEOBsAreOut(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPLETMPEOBsAreOut', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStopConditioningInfo(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETStopConditioningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETStopConditioning(*args, **kwargs):
        """
        Location: APSMpPARLETTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPARShutdownInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARShutdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARShutdown(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampdownTime', 'DCPS', 'PulsedPS', 'rfSystems', 'BM']

        """
        return exec_with_tcl('APSMpPARShutdown', *args, **kwargs)

    @staticmethod
    def APSMpPARZeroDCPSSetpoints(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: args
        APS parsed args: ['BM']

        """
        return exec_with_tcl('APSMpPARZeroDCPSSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpPARShutdownInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARShutdownInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffDCPS(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: args
        APS parsed args: ['BM']

        """
        return exec_with_tcl('APSMpPARTurnOffDCPS', *args, **kwargs)

    @staticmethod
    def APSMpPARRampdown(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: args
        APS parsed args: ['rampdownTime', 'block']

        """
        return exec_with_tcl('APSMpPARRampdown', *args, **kwargs)

    @staticmethod
    def APSMpPARRampdownWait(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARRampdownWait', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffRf12Info(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffRf12Info', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffRf12(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffRf12', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffRf1Info(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffRf1Info', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffRf1(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffRf1', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffKickers(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffKickers', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOffSeptum(*args, **kwargs):
        """
        Location: APSMpPARTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOffSeptum', *args, **kwargs)

    @staticmethod
    def APSMpxPTBMatrixInfo(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpxPTBMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpxPTBMatrix(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxPTBMatrix', *args, **kwargs)

    @staticmethod
    def APSMpxPTBMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpxPTBMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpyPTBMatrixInfo(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpyPTBMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpyPTBMatrix(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyPTBMatrix', *args, **kwargs)

    @staticmethod
    def APSMpyPTBMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpyPTBMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPTBShutdownInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBShutdownInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBShutdown(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampdownTime', 'DCPS']

        """
        return exec_with_tcl('APSMpPTBShutdown', *args, **kwargs)

    @staticmethod
    def APSMpPTBShutdownInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBShutdownInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPTBZeroDCPSSetpointsInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBZeroDCPSSetpointsInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBZeroDCPSSetpoints(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBZeroDCPSSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpPTBTurnOffDCPSInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBTurnOffDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBTurnOffDCPS(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBTurnOffDCPS', *args, **kwargs)

    @staticmethod
    def APSMpPTBRampdown(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: args
        APS parsed args: ['rampdownTime', 'block']

        """
        return exec_with_tcl('APSMpPTBRampdown', *args, **kwargs)

    @staticmethod
    def APSMpPTBRampdownWait(*args, **kwargs):
        """
        Location: APSMpPTBTurnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBRampdownWait', *args, **kwargs)

    @staticmethod
    def APSMpPromptInitDialog(*args, **kwargs):
        """
        Location: APSMpPromptInitDialog.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPromptInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixDoExperiment(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList', 'templateFile']

        """
        return exec_with_tcl('APSMpRespMatrixDoExperiment', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixCalcSlopes(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList']

        """
        return exec_with_tcl('APSMpRespMatrixCalcSlopes', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixFormMatrix(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList', 'badBpms', 'badActuators', 'outFile', 'beamlineFile', 'filterColumns', 'excludeColumns']

        """
        return exec_with_tcl('APSMpRespMatrixFormMatrix', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixCalcInverse(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['inFile', 'outFile', 'minimum']

        """
        return exec_with_tcl('APSMpRespMatrixCalcInverse', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixSetParameterDefaults(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpRespMatrixSetParameterDefaults', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixRemoveColons(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: word
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRespMatrixRemoveColons', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixSetActuatorParameters(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuator']

        """
        return exec_with_tcl('APSMpRespMatrixSetActuatorParameters', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixSetActuatorParametersByDialog(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'actuator']

        """
        return exec_with_tcl('APSMpRespMatrixSetActuatorParametersByDialog', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixInstallDialog(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'fileName', 'installName', 'installDir']

        """
        return exec_with_tcl('APSMpRespMatrixInstallDialog', *args, **kwargs)

    @staticmethod
    def APSMpRespMatrixInstall(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'installName', 'installDir', 'comment']

        """
        return exec_with_tcl('APSMpRespMatrixInstall', *args, **kwargs)

    @staticmethod
    def APSMpSerialNumbers(*args, **kwargs):
        """
        Location: APSMpRespMatrix.tcl
        TCL function args: path
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSerialNumbers', *args, **kwargs)

    @staticmethod
    def APSCollectDPCorrectorHistoryInfo(*args, **kwargs):
        """
        Location: APSMpSRDatapool.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCollectDPCorrectorHistoryInfo', *args, **kwargs)

    @staticmethod
    def APSCollectDPCorrectorHistory(*args, **kwargs):
        """
        Location: APSMpSRDatapool.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSCollectDPCorrectorHistory', *args, **kwargs)

    @staticmethod
    def APSCollectVideoWaveform(*args, **kwargs):
        """
        Location: APSMpSRDatapool.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSCollectVideoWaveform', *args, **kwargs)

    @staticmethod
    def APSCollectInUseDPCorrectorHistory(*args, **kwargs):
        """
        Location: APSMpSRDatapool.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSCollectInUseDPCorrectorHistory', *args, **kwargs)

    @staticmethod
    def APSCollectDPBPMs(*args, **kwargs):
        """
        Location: APSMpSRDatapool.tcl
        TCL function args: args
        APS parsed args: ['rootname']

        """
        return exec_with_tcl('APSCollectDPBPMs', *args, **kwargs)

    @staticmethod
    def APSMpSRTurnOnKickersDialog(*args, **kwargs):
        """
        Location: APSMpSRKicker.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTurnOnKickersDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRTurnOnKickers(*args, **kwargs):
        """
        Location: APSMpSRKicker.tcl
        TCL function args: args
        APS parsed args: ['IK1', 'IK2', 'IK3', 'IK4', 'IK5', 'IS1', 'IS2']

        """
        return exec_with_tcl('APSMpSRTurnOnKickers', *args, **kwargs)

    @staticmethod
    def APSMpSRTurnOffKickersDialog(*args, **kwargs):
        """
        Location: APSMpSRKicker.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTurnOffKickersDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRTurnOffKickers(*args, **kwargs):
        """
        Location: APSMpSRKicker.tcl
        TCL function args: args
        APS parsed args: ['IK1', 'IK2', 'IK3', 'IK4', 'IK5', 'IS1', 'IS2']

        """
        return exec_with_tcl('APSMpSRTurnOffKickers', *args, **kwargs)

    @staticmethod
    def APSSRStartStandardCorrection(*args, **kwargs):
        """
        Location: APSMpSROrbitControllaw.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRStartStandardCorrection', *args, **kwargs)

    @staticmethod
    def APSStartSROrbitControllaw(*args, **kwargs):
        """
        Location: APSMpSROrbitControllaw.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSStartSROrbitControllaw', *args, **kwargs)

    @staticmethod
    def APSAbortControllaw(*args, **kwargs):
        """
        Location: APSMpSROrbitControllaw.tcl
        TCL function args: args
        APS parsed args: ['runControlPV', 'clear', 'statusCallback', 'sourceID', 'timeout']

        """
        return exec_with_tcl('APSAbortControllaw', *args, **kwargs)

    @staticmethod
    def APSSuspendControllaw(*args, **kwargs):
        """
        Location: APSMpSROrbitControllaw.tcl
        TCL function args: args
        APS parsed args: ['runControlPV']

        """
        return exec_with_tcl('APSSuspendControllaw', *args, **kwargs)

    @staticmethod
    def APSResumeControllaw(*args, **kwargs):
        """
        Location: APSMpSROrbitControllaw.tcl
        TCL function args: args
        APS parsed args: ['runControlPV']

        """
        return exec_with_tcl('APSResumeControllaw', *args, **kwargs)

    @staticmethod
    def APSMpSRRestoreFBfiltersInfo(*args, **kwargs):
        """
        Location: APSMpSRRTFB.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRRestoreFBfiltersInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSetFBfilters(*args, **kwargs):
        """
        Location: APSMpSRRTFB.tcl
        TCL function args: args
        APS parsed args: ['ramp', 'steps', 'interval', 'restore', 'hFactor', 'vFactor']

        """
        return exec_with_tcl('APSMpSRSetFBfilters', *args, **kwargs)

    @staticmethod
    def APSRTFBSampleAndCollect(*args, **kwargs):
        """
        Location: APSMpSRRTFB.tcl
        TCL function args: args
        APS parsed args: ['monfile', 'datafile', 'clearMode', 'wait', 'statusCallback', 'autoRestore', 'waitWhileInjecting', 'restoreTiming', 'restoreChannels', 'scalarsFile', 'description']

        """
        return exec_with_tcl('APSRTFBSampleAndCollect', *args, **kwargs)

    @staticmethod
    def APSArmDSPscope(*args, **kwargs):
        """
        Location: APSMpSRRTFB.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'waitWhileInjecting']

        """
        return exec_with_tcl('APSArmDSPscope', *args, **kwargs)

    @staticmethod
    def APSWaitForDSPtrigger(*args, **kwargs):
        """
        Location: APSMpSRRTFB.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSWaitForDSPtrigger', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDump24SingletsInfo(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDump24SingletsInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDump24SingletsInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDump24SingletsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDump24Singlets(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: args
        APS parsed args: ['initialFrequencyChange', 'frequencyChange', 'dumpCondition', 'thresholdCurrentReduction', 'pauseBetweenSteps', 'thresholdLifetime', 'thresholdRadiationLevel']

        """
        return exec_with_tcl('APSMpSRSlowBeamDump24Singlets', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDumpHybridInfo(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDumpHybridInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDumpHybridInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDumpHybridInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDumpHybrid(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: args
        APS parsed args: ['initialFrequencyChange', 'frequencyChange', 'dumpCondition', 'thresholdCurrentReduction', 'pauseBetweenSteps', 'thresholdLifetime', 'thresholdRadiationLevel']

        """
        return exec_with_tcl('APSMpSRSlowBeamDumpHybrid', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDump(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: args
        APS parsed args: ['initialFrequencyChange', 'frequencyChange', 'dumpCondition', 'thresholdCurrentReduction', 'pauseBetweenSteps', 'thresholdLifetime', 'thresholdRadiationLevel']

        """
        return exec_with_tcl('APSMpSRSlowBeamDump', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDumpFreqRestoreInfo(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDumpFreqRestoreInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSlowBeamDumpFreqRestore(*args, **kwargs):
        """
        Location: APSMpSRSlowBeamDump.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSlowBeamDumpFreqRestore', *args, **kwargs)

    @staticmethod
    def APSMpSRUpDoubleSectorInfo(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUpDoubleSectorInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRUpDoubleSectorDialog(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUpDoubleSectorDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRUpDoubleSector(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpSRUpDoubleSector', *args, **kwargs)

    @staticmethod
    def APSMpSRConditionDoubleSectorInfo(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRConditionDoubleSectorInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRConditionDoubleSectorDialog(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRConditionDoubleSectorDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRConditionDoubleSector(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpSRConditionDoubleSector', *args, **kwargs)

    @staticmethod
    def APSMpSRDownDoubleSectorInfo(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRDownDoubleSectorInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRDownDoubleSectorDialog(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRDownDoubleSectorDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRDownDoubleSector(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpSRDownDoubleSector', *args, **kwargs)

    @staticmethod
    def APSMpSRUpDownDoubleSector(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUpDownDoubleSector', *args, **kwargs)

    @staticmethod
    def WaitForTaskToFinish(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: ['cavget', 'waitLimit', 'updateInterval', 'checkExpression', 'message']

        """
        return exec_with_tcl('WaitForTaskToFinish', *args, **kwargs)

    @staticmethod
    def APSFindSCROperationFile(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: ['machine', 'preference', 'arrayName']

        """
        return exec_with_tcl('APSFindSCROperationFile', *args, **kwargs)

    @staticmethod
    def APSRampPVs(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: ['PVList', 'valueList', 'steps', 'pause', 'prefix', 'suffix']

        """
        return exec_with_tcl('APSRampPVs', *args, **kwargs)

    @staticmethod
    def APSMpSRDumpBeam(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRDumpBeam', *args, **kwargs)

    @staticmethod
    def APSMpSRResetMPS(*args, **kwargs):
        """
        Location: APSMpSRUpDownDoubleSector.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRResetMPS', *args, **kwargs)

    @staticmethod
    def APSParseArguments(*args, **kwargs):
        """
        Location: APSParse.tcl
        Usage: APSParseArguments <optionKeywordList>
         <optionKeywordList> is a list of option keywords that are accepted
         by the procedure requesting the parsing.  The parsing scans the args
         list of the calling procedure.  Only options from the keyword list
         will be processed; others are left in the args list.
         The effect of APSParseArguments is to translate a sequence like
         "-keyword value" into "set keyword value"; that is, the keyword
         names are variable names in the calling procedure.
        TCL function args: optlist
        APS parsed args: None

        """
        return exec_with_tcl('APSParseArguments', *args, **kwargs)

    @staticmethod
    def APSStrictParseArguments(*args, **kwargs):
        """
        Location: APSParse.tcl
        Usage: APSStrictParseArguments <optionKeywordList>
         Same as APSParseArguments, only it prints an error to stderr if user
         passes extra or unknown options not given in optlist. Also, returns
         -1 if unknown option given, 0 otherwise.
         <optionKeywordList> is a list of option keywords that are accepted
         by the procedure requesting the parsing.  The parsing scans the args
         list of the calling procedure.  Only options from the keyword list
         will be processed; others are left in the args list.
         The effect of APSParseArguments is to translate a sequence like
         "-keyword value" into "set keyword value"; that is, the keyword
         names are variable names in the calling procedure.
        TCL function args: optlist
        APS parsed args: None

        """
        return exec_with_tcl('APSStrictParseArguments', *args, **kwargs)

    @staticmethod
    def APSClearOptions(*args, **kwargs):
        """
        Location: APSParse.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSClearOptions', *args, **kwargs)

    @staticmethod
    def APSPlotCanvas(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        Usage: APSPlotCanvas widget
        [-parent <string>]
        [-packOption <list>]
        [-background <color>]
        [-width <integer>]
        [-height <integer>]
        [-dataFile <sddsplot output file>]
        [-sddsplotOptions <sddsplot commandline>]
        [-sddscontourOptions <sddscontour commandline>]

        Creates	$parent$widget.canvas
        	$parent$widget.labelTCL function args: widget args
        APS parsed args: ['parent', 'packOptions', 'background', 'width', 'height', 'dataFile', 'sddsplotOptions', 'sddscontourOptions']

        """
        return exec_with_tcl('APSPlotCanvas', *args, **kwargs)

    @staticmethod
    def APSToggleMouseTrackerTime(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plotVar']

        """
        return exec_with_tcl('APSToggleMouseTrackerTime', *args, **kwargs)

    @staticmethod
    def APSToggleMouseTracker(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'background']

        """
        return exec_with_tcl('APSToggleMouseTracker', *args, **kwargs)

    @staticmethod
    def APSMouseTracker(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: x y args
        APS parsed args: ['plot', 'plotVar']

        """
        return exec_with_tcl('APSMouseTracker', *args, **kwargs)

    @staticmethod
    def APSPlotFirst(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'plotLabel']

        """
        return exec_with_tcl('APSPlotFirst', *args, **kwargs)

    @staticmethod
    def APSPlotLast(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'plotLabel']

        """
        return exec_with_tcl('APSPlotLast', *args, **kwargs)

    @staticmethod
    def APSPlotNext(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'plotLabel']

        """
        return exec_with_tcl('APSPlotNext', *args, **kwargs)

    @staticmethod
    def APSPlotSetUserCoords(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plotVar']

        """
        return exec_with_tcl('APSPlotSetUserCoords', *args, **kwargs)

    @staticmethod
    def APSPlotPrevious(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'plotLabel']

        """
        return exec_with_tcl('APSPlotPrevious', *args, **kwargs)

    @staticmethod
    def APSPlotUnZoom(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar']

        """
        return exec_with_tcl('APSPlotUnZoom', *args, **kwargs)

    @staticmethod
    def APSPlotZoom(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar']

        """
        return exec_with_tcl('APSPlotZoom', *args, **kwargs)

    @staticmethod
    def APSPlotZoomBoxStart(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: x y args
        APS parsed args: ['plot', 'plotVar', 'outline']

        """
        return exec_with_tcl('APSPlotZoomBoxStart', *args, **kwargs)

    @staticmethod
    def APSPlotZoomBoxMove(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: x y args
        APS parsed args: ['plot', 'plotVar']

        """
        return exec_with_tcl('APSPlotZoomBoxMove', *args, **kwargs)

    @staticmethod
    def APSPlotZoomBoxRelease(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: x y args
        APS parsed args: ['plot', 'plotVar']

        """
        return exec_with_tcl('APSPlotZoomBoxRelease', *args, **kwargs)

    @staticmethod
    def APSPlotMovie(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: args
        APS parsed args: ['plot', 'plotVar', 'plotLabel']

        """
        return exec_with_tcl('APSPlotMovie', *args, **kwargs)

    @staticmethod
    def APSRGB(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: r g b
        APS parsed args: None

        """
        return exec_with_tcl('APSRGB', *args, **kwargs)

    @staticmethod
    def APSPlotDrawLine(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: plot line color width tag state
        APS parsed args: None

        """
        return exec_with_tcl('APSPlotDrawLine', *args, **kwargs)

    @staticmethod
    def APSUpdatePlotCanvas(*args, **kwargs):
        """
        Location: APSPlotWidgets.tcl
        TCL function args: width height args
        APS parsed args: ['plot', 'background', 'plotVar', 'plotLabel', 'updateLabel', 'clicks']

        """
        return exec_with_tcl('APSUpdatePlotCanvas', *args, **kwargs)

    @staticmethod
    def APSLaunchPoissonJob(*args, **kwargs):
        """
        Location: APSPoissonSuperfish.tcl
        Usage: APSLaunchPoissonJob
        -inputfile <string>
        [-sf7inputfile <string>]
        [-outputDir <string>]
        [-workDirLinux <string>]
        [-workDirWindows <string>]
        [-windowsIP <IP address>]
        [-automesh <string>]
        [-poisson <string>]
        [-sf7 <string>]

        This procedure allows you to execute a Poisson job on a remote Windows computer using the tclDPServer/tclDPClient communication tool.TCL function args: args
        APS parsed args: ['inputfile', 'outputDir', 'workDirLinux', 'workDirWindows', 'windowsIP', 'automesh', 'poisson', 'sf7', 'sf7inputfile']

        """
        return exec_with_tcl('APSLaunchPoissonJob', *args, **kwargs)

    @staticmethod
    def APSQueryPoissonJob(*args, **kwargs):
        """
        Location: APSPoissonSuperfish.tcl
        Usage: APSQueryPoissonJob
        [-windowsIP <IP address>]

        This procedure is used to check if there is a Poisson job running.TCL function args: args
        APS parsed args: ['windowsIP']

        """
        return exec_with_tcl('APSQueryPoissonJob', *args, **kwargs)

    @staticmethod
    def APSKillPoissonJob(*args, **kwargs):
        """
        Location: APSPoissonSuperfish.tcl
        Usage: APSKillPoissonJob
        [-windowsIP <IP address>]

        This procedure is used to kill an running Poisson job.TCL function args: args
        APS parsed args: ['windowsIP']

        """
        return exec_with_tcl('APSKillPoissonJob', *args, **kwargs)

    @staticmethod
    def APSQuickOptimize(*args, **kwargs):
        """
        Location: APSQuickOptimize.tcl
        TCL function args: args
        APS parsed args: ['variableList', 'startValueList', 'stepList', 'lowerList', 'upperList', 'readbackList', 'tolerance', 'average', 'interval', 'pauseChange', 'minimize', 'interactive', 'destroyWindow']

        """
        return exec_with_tcl('APSQuickOptimize', *args, **kwargs)

    @staticmethod
    def APSMakeSRConfigFrame(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSRConfigFrame', *args, **kwargs)

    @staticmethod
    def APSMakeSRConfigButtons(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSRConfigButtons', *args, **kwargs)

    @staticmethod
    def APSMakeSrBpmCorrList(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSrBpmCorrList', *args, **kwargs)

    @staticmethod
    def APSReadSRConfigFile(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: filename options
        APS parsed args: None

        """
        return exec_with_tcl('APSReadSRConfigFile', *args, **kwargs)

    @staticmethod
    def APSSetSConfigLabel(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSConfigLabel', *args, **kwargs)

    @staticmethod
    def APSSetSRNonexist(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSRNonexist', *args, **kwargs)

    @staticmethod
    def APSSetSRButtonsDefaults(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSRButtonsDefaults', *args, **kwargs)

    @staticmethod
    def APSSetSRButtonsFlags(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: val args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSRButtonsFlags', *args, **kwargs)

    @staticmethod
    def APSToggleSRButtonsFlags(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: w position args
        APS parsed args: None

        """
        return exec_with_tcl('APSToggleSRButtonsFlags', *args, **kwargs)

    @staticmethod
    def APSWriteSRConfigFile(*args, **kwargs):
        """
        Location: APSSRConfig.tcl
        TCL function args: filename args
        APS parsed args: None

        """
        return exec_with_tcl('APSWriteSRConfigFile', *args, **kwargs)

    @staticmethod
    def APSSendCommandToScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: command
        APS parsed args: None

        """
        return exec_with_tcl('APSSendCommandToScope', *args, **kwargs)

    @staticmethod
    def APSSetValueOnScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: name value
        APS parsed args: None

        """
        return exec_with_tcl('APSSetValueOnScope', *args, **kwargs)

    @staticmethod
    def APSGetValueFromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: name
        APS parsed args: None

        """
        return exec_with_tcl('APSGetValueFromScope', *args, **kwargs)

    @staticmethod
    def APSGetValuesFromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: names
        APS parsed args: None

        """
        return exec_with_tcl('APSGetValuesFromScope', *args, **kwargs)

    @staticmethod
    def APSGetValue2FromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: name option
        APS parsed args: None

        """
        return exec_with_tcl('APSGetValue2FromScope', *args, **kwargs)

    @staticmethod
    def APSResetScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSResetScope', *args, **kwargs)

    @staticmethod
    def APSInitializeScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSInitializeScope', *args, **kwargs)

    @staticmethod
    def APSAcquireDataFromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSAcquireDataFromScope', *args, **kwargs)

    @staticmethod
    def APSMeasurementsFromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMeasurementsFromScope', *args, **kwargs)

    @staticmethod
    def APSTransferDataFromScope(*args, **kwargs):
        """
        Location: APSScopeControl.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSTransferDataFromScope', *args, **kwargs)

    @staticmethod
    def APSSetCorrectorInUse(*args, **kwargs):
        """
        Location: APSSetCorrectorInUse.tcl
        TCL function args: args
        APS parsed args: ['plane', 'configDC', 'configRTFB', 'resetUnspecified']

        """
        return exec_with_tcl('APSSetCorrectorInUse', *args, **kwargs)

    @staticmethod
    def APSSound(*args, **kwargs):
        """
        Location: APSSound.tcl
        Usage: APSSound
        [-type <string>] where <string> is working, alert, or emergency
        [-volume <string>] from 1 to 100
        [-iterations <string>]
        [-period <string>] where <string> is in milliseconds or "continuous".
        Plays given sound type in background.TCL function args: args
        APS parsed args: ['type', 'volume', 'iterations', 'period']

        """
        return exec_with_tcl('APSSound', *args, **kwargs)

    @staticmethod
    def APSPlaySound(*args, **kwargs):
        """
        Location: APSSound.tcl
        TCL function args: type volume iteration period
        APS parsed args: None

        """
        return exec_with_tcl('APSPlaySound', *args, **kwargs)

    @staticmethod
    def APSSwitchMux(*args, **kwargs):
        """
        Location: APSSwitchMux.tcl
        TCL function args: args
        APS parsed args: ['flag', 'location', 'monitor', 'system', 'statusCallback', 'trackMV200']

        """
        return exec_with_tcl('APSSwitchMux', *args, **kwargs)

    @staticmethod
    def APSSetMuxPVs(*args, **kwargs):
        """
        Location: APSSwitchMux.tcl
        TCL function args: args
        APS parsed args: ['epicsPV', 'epicsValue', 'satMuxPV', 'satMuxValue', 'muxPVList', 'muxValueList', 'trackMV200', 'statusCallback']

        """
        return exec_with_tcl('APSSetMuxPVs', *args, **kwargs)

    @staticmethod
    def APSConfigureCameraPVs(*args, **kwargs):
        """
        Location: APSSwitchMux.tcl
        TCL function args: args
        APS parsed args: ['flagIn', 'lampOn', 'flag', 'system', 'statusCallback', 'actuatorNumber', 'ignoreFlagReadback', 'cameraType']

        """
        return exec_with_tcl('APSConfigureCameraPVs', *args, **kwargs)

    @staticmethod
    def APSAddToTagValueList(*args, **kwargs):
        """
        Location: APSTaggedList.tcl
        TCL function args: args
        APS parsed args: ['listID', 'tag', 'value']

        """
        return exec_with_tcl('APSAddToTagValueList', *args, **kwargs)

    @staticmethod
    def APSRemoveFromTagValueList(*args, **kwargs):
        """
        Location: APSTaggedList.tcl
        TCL function args: args
        APS parsed args: ['listID', 'tag', 'value']

        """
        return exec_with_tcl('APSRemoveFromTagValueList', *args, **kwargs)

    @staticmethod
    def APSRetrieveTaggedValue(*args, **kwargs):
        """
        Location: APSTaggedList.tcl
        TCL function args: args
        APS parsed args: ['listID', 'tag', 'mustBeFile']

        """
        return exec_with_tcl('APSRetrieveTaggedValue', *args, **kwargs)

    @staticmethod
    def APSOpenTelnetStream(*args, **kwargs):
        """
        Location: APSTelnet.tcl
        Usage: APSOpenTelnetStream -IPaddress <address>
        [-GreetingLines <number>]
        Returns a value for the stream ID which should be used in subsequent calls to related procedures APSWriteToTelnetStream and CloseTelnetStream.

        IPaddress is an IP address that can be used by a telnet command;
        GreetingLines is the number of greeting lines expected when logging on to telnet for the particular machine. The default value is 5, which corresponds to the hp VSA. If the actual number of telnet greeting lines is different from what is specified then the procedure will hang up or garbage will be returned in APSWriteToTelnetStream commands.

        example of APS<...>Telnet commands:
        set streamID [APSOpenTelnetStream -IPaddress hpvecsr]
        APSWriteToTelnetStream -streamID $streamID -command freq:Cent 2e9
        APSCloseTelnetStream -streamID $streamIDTCL function args: args
        APS parsed args: ['IPaddress', 'GreetingLines']

        """
        return exec_with_tcl('APSOpenTelnetStream', *args, **kwargs)

    @staticmethod
    def APSWriteToTelnetStream(*args, **kwargs):
        """
        Location: APSTelnet.tcl
        Usage: APSWriteToTelnetStream -command <string> -streamID <value>

        writes a command to the telnet stream. If the command is a query command, then the results of the query is the value returned.TCL function args: args
        APS parsed args: ['command', 'streamID']

        """
        return exec_with_tcl('APSWriteToTelnetStream', *args, **kwargs)

    @staticmethod
    def APSCloseTelnetStream(*args, **kwargs):
        """
        Location: APSTelnet.tcl
        Usage: APSCloseTelnetStreamHelp -streamID <value>

        Closes the telnet session connected to the stream ID specified.TCL function args: args
        APS parsed args: ['streamID']

        """
        return exec_with_tcl('APSCloseTelnetStream', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjuster(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        Usage: APSWaveformAdjuster widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-title <string>]
        [-xlabel <label>]
        [-ylabel <label>]
        [-backgroundColor <color>]
        [-foregroundColor <color>]
        [-axisColor <color>]
        [-plotBackgroundColor <color>]
        [-plotForegroundColor <color>]
        [-selectionColor <color>]
        [-xmin <real>]
        [-xmax <real>]
        [-ymin <real>]
        [-ymax <ymax>]
        [-width <integer>]
        [-height <integer>]
        [-leftmargin <pixels>]
        [-pixelSize <integer>]
        [-waveformVariable <variable>]
        [-handleSpacing <integer>]
        [-selectedYCoordVar <variable>]
        [-selectedXCoordVar <variable>]
        [-static 1]
        [-autoscale 1]
        [-positionVariable <variable>]
        [-gridPack <list>]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	graph
        	ycoord.label
        	ycoord.entry
        	TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'title', 'xlabel', 'ylabel', 'backgroundColor', 'foregroundColor', 'axisColor', 'plotBackgroundColor', 'plotForegroundColor', 'selectionColor', 'xmin', 'xmax', 'ymin', 'ymax', 'width', 'height', 'pixelSize', 'gridPack', 'waveformVariable', 'showPrevious', 'handleSpacing', 'contextHelp', 'selectedYCoordVar', 'selectedXCoordVar', 'static', 'autoscale', 'positionVariable', 'leftmargin']

        """
        return exec_with_tcl('APSWaveformAdjuster', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterUpdate(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W handleSpacing waveformVariable tmp op
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterUpdate', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterSetY(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W waveformVariable selectedYCoordVar handleSpacing autoscale
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterSetY', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterLocator(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W x y positionVariable selectedYCoordVar selectedXCoordVar
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterLocator', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterSelectorAdd(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W x y positionVariable
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterSelectorAdd', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterSelect(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W x y positionVariable selectedYCoordVar selectedXCoordVar
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterSelect', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterMotion(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W x y waveformVariable selectedYCoordVar transform handleSpacing autoscale
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterMotion', *args, **kwargs)

    @staticmethod
    def APSWaveformAdjusterZoom(*args, **kwargs):
        """
        Location: APSWaveform.tcl
        TCL function args: W x y
        APS parsed args: None

        """
        return exec_with_tcl('APSWaveformAdjusterZoom', *args, **kwargs)

    @staticmethod
    def APSSwapInWidget(*args, **kwargs):
        """
        Location: APSWidgetSwapFrame.tcl
        Usage: APSSwapInWidget widget
        [-parent <string>]
        [-swapIn <fullWidgetName>]
        TCL function args: widget args
        APS parsed args: ['parent', 'swapIn']

        """
        return exec_with_tcl('APSSwapInWidget', *args, **kwargs)

    @staticmethod
    def APSWidgetSwapFrame(*args, **kwargs):
        """
        Location: APSWidgetSwapFrame.tcl
        Usage: APSSwapInWidget widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-label <string>]
        [-width <num>]
        [-height <num>]
        [-orientation <string>] where <string> is horizontal or vertical (default)
        [-geometry <string>]
        [-contextHelp <string>]
        [-widgetList <list>]
        [-labelList <list>]
        [-commandList <list>]	[-contextHelpList <list>]
        [-buttonPosition {0|1}]
        [-buttonSize {small|medium}]
        [-buttonLimitPerRow <number>]

        Creates	$parent$widget.
        	label
        	frame
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'name', 'width', 'height', 'orientation', 'geometry', 'contextHelp', 'widgetList', 'labelList', 'commandList', 'variable', 'valueList', 'contextHelpList', 'buttonPosition', 'buttonSize', 'buttonLimitPerRow']

        """
        return exec_with_tcl('APSWidgetSwapFrame', *args, **kwargs)

    @staticmethod
    def APSSaveSRFBDspScope(*args, **kwargs):
        """
        Location: APSsrfb.tcl
        TCL function args: args
        APS parsed args: ['filename', 'description']

        """
        return exec_with_tcl('APSSaveSRFBDspScope', *args, **kwargs)

    @staticmethod
    def APSRestoreSRFBDspScope(*args, **kwargs):
        """
        Location: APSsrfb.tcl
        TCL function args: args
        APS parsed args: ['filename', 'clearMode', 'verbose', 'timing', 'channels']

        """
        return exec_with_tcl('APSRestoreSRFBDspScope', *args, **kwargs)

    @staticmethod
    def APSTrigReadSRFBDspScope(*args, **kwargs):
        """
        Location: APSsrfb.tcl
        TCL function args: args
        APS parsed args: ['datafile', 'monitorfile', 'verbose', 'scalars', 'comment']

        """
        return exec_with_tcl('APSTrigReadSRFBDspScope', *args, **kwargs)

    @staticmethod
    def APSCreateMoreFrame(*args, **kwargs):
        """
        Location: APSsrfb.tcl
        TCL function args: widget args
        APS parsed args: ['window', 'parent', 'label', 'relief', 'buttonsize']

        """
        return exec_with_tcl('APSCreateMoreFrame', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrAndRampsOnOffInfo(*args, **kwargs):
        """
        Location: BCorr_Init_Ramps.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrAndRampsOnOffInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrAndRampsOnOffDialog(*args, **kwargs):
        """
        Location: BCorr_Init_Ramps.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrAndRampsOnOffDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrAndRampsOnOff(*args, **kwargs):
        """
        Location: BCorr_Init_Ramps.tcl
        TCL function args: args
        APS parsed args: ['state1', 'selection', 'Fast', 'RawOnly', 'SCRFile']

        """
        return exec_with_tcl('APSMpBoosterSetCorrAndRampsOnOff', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSDecreaseGainToStandbyInfo(*args, **kwargs):
        """
        Location: BPSDecreaseGainToStandby.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSDecreaseGainToStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSDecreaseGainToStandbyDialog(*args, **kwargs):
        """
        Location: BPSDecreaseGainToStandby.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSDecreaseGainToStandbyDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSDecreaseGainToStandby(*args, **kwargs):
        """
        Location: BPSDecreaseGainToStandby.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterPSDecreaseGainToStandby', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSEnableDisableRamps(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['magnet', 'state1', 'coldStart', 'standbyGainLevel', 'BM', 'QF', 'QD', 'SF', 'SD', 'BMgain', 'QFgain', 'QDgain', 'SFgain', 'SDgain']

        """
        return exec_with_tcl('APSMpBoosterPSEnableDisableRamps', *args, **kwargs)

    @staticmethod
    def loadSafetyRamps2(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'noWarning']

        """
        return exec_with_tcl('loadSafetyRamps2', *args, **kwargs)

    @staticmethod
    def APSMpBoosterResetAfterIOCReboot(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterResetAfterIOCReboot', *args, **kwargs)

    @staticmethod
    def APSMpBoosterResetAfterIOCRebootOld(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterResetAfterIOCRebootOld', *args, **kwargs)

    @staticmethod
    def APSMpBoosterDisableSlopeAndZero(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['magnet', 'BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterDisableSlopeAndZero', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetGain(*args, **kwargs):
        """
        Location: BPSEnableDisableRamps.tcl
        TCL function args: args
        APS parsed args: ['magnet', 'value', 'BM', 'QF', 'QD', 'SF', 'SD', 'BMgain', 'QFgain', 'QDgain', 'SFgain', 'SDgain']

        """
        return exec_with_tcl('APSMpBoosterPSSetGain', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSStartKillBControlInfo(*args, **kwargs):
        """
        Location: BPSStartBcontrol.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSStartKillBControlInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSStartKillBControlDialog(*args, **kwargs):
        """
        Location: BPSStartBcontrol.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSStartKillBControlDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSStartKillBControl(*args, **kwargs):
        """
        Location: BPSStartBcontrol.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'slope', 'zero', 'action1', 'action2']

        """
        return exec_with_tcl('APSMpBoosterPSStartKillBControl', *args, **kwargs)

    @staticmethod
    def cavputMakeCommand(*args, **kwargs):
        """
        Location: BPSStartBcontrol.tcl
        TCL function args: commandList
        APS parsed args: None

        """
        return exec_with_tcl('cavputMakeCommand', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSResetAFGTriggers(*args, **kwargs):
        """
        Location: BPSStartBcontrol.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterPSResetAFGTriggers', *args, **kwargs)

    @staticmethod
    def APSSetBoosterRampToCurrent(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSSetBoosterRampToCurrent', *args, **kwargs)

    @staticmethod
    def APSSetBoosterCorrPowerSupplies(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['plane', 'switch', 'fast', 'rawOnly', 'statusVar']

        """
        return exec_with_tcl('APSSetBoosterCorrPowerSupplies', *args, **kwargs)

    @staticmethod
    def APSInitializeBoosterCorrector(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['plane', 'statusVar']

        """
        return exec_with_tcl('APSInitializeBoosterCorrector', *args, **kwargs)

    @staticmethod
    def APSSetBoosterCorrectorValue(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['rampbias', 'rampload', 'setfg', 'corrector', 'value', 'plane', 'statusVar']

        """
        return exec_with_tcl('APSSetBoosterCorrectorValue', *args, **kwargs)

    @staticmethod
    def APSSetBoosterForeground(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['corrname', 'plane']

        """
        return exec_with_tcl('APSSetBoosterForeground', *args, **kwargs)

    @staticmethod
    def APSWaitForBoosterCorrectorLight(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['color', 'corrname']

        """
        return exec_with_tcl('APSWaitForBoosterCorrectorLight', *args, **kwargs)

    @staticmethod
    def APSWaitForBoosterCorrectorPact(*args, **kwargs):
        """
        Location: Booster.tcl
        TCL function args: args
        APS parsed args: ['corrname']

        """
        return exec_with_tcl('APSWaitForBoosterCorrectorPact', *args, **kwargs)

    @staticmethod
    def APSMakeFourDigitYear(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSMakeFourDigitYear <year>
        Returns four-digit version of <year>, assuming that the actual year is
        later than 1989.TCL function args: year
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeFourDigitYear', *args, **kwargs)

    @staticmethod
    def APSFormatDate(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSFormatDate
        {-year <year> {-month <month> -day <day> | -julianDay <jDay>} | -dateList <list>}
        [-twoDigitYear 1] [-dateFormat {Y-J-MD YMD Y-M-D MDY list}] [leadingZeros 0]
        For -dateFormat list, the information is returned in the form <year> <julianDay> <month> <day>.TCL function args: args
        APS parsed args: ['year', 'month', 'day', 'julianDay', 'dateList', 'twoDigitYear', 'dateFormat', 'leadingZeros']

        """
        return exec_with_tcl('APSFormatDate', *args, **kwargs)

    @staticmethod
    def APSDateBreakDown(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSDateBreakDown [-dayVariable <string>] [-monthVariable <string>] [-yearVariable <string>]
        [-hourVariable <string>] [-julianDayVariable <string>] [-twoDigitYear 0] [-leadingZeros 0]
        Puts the day, month, year, hour, and/or Julian day for the present date into the given variables.TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSDateBreakDown', *args, **kwargs)

    @staticmethod
    def APSLeapYear(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSLeapYear <year>
        Returns 1 (0) if <year> is (is not) a leap year.TCL function args: year
        APS parsed args: None

        """
        return exec_with_tcl('APSLeapYear', *args, **kwargs)

    @staticmethod
    def APSDefineDaysInMonths(*args, **kwargs):
        """
        Location: DateConversion.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDefineDaysInMonths', *args, **kwargs)

    @staticmethod
    def APSJulianDay(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSJulianDay -day <number> -month <number> -year <number>
        Returns the Julian day (day of year between 1 and 366) for the given date.TCL function args: args
        APS parsed args: ['day', 'month', 'year']

        """
        return exec_with_tcl('APSJulianDay', *args, **kwargs)

    @staticmethod
    def APSMonthDay(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSMonthDay -year <number> -julianDay <number>
        Returns a list of the month and day for the given year and day-of-year.TCL function args: args
        APS parsed args: ['julianDay', 'year']

        """
        return exec_with_tcl('APSMonthDay', *args, **kwargs)

    @staticmethod
    def APSDateConversionTest(*args, **kwargs):
        """
        Location: DateConversion.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDateConversionTest', *args, **kwargs)

    @staticmethod
    def APSTodaysDateInfo(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSTodaysDateInfo [-dateFormat {Y-J-MD YMD Y-M-D MDY list}] [-twoDigitYear 1]
        Obsolete. Returns date information for today.  APSOffsetDateInfo is the preferred routine.
        For -dateFormat list, the information is returned in the form <year> <julianDay> <month> <day>.TCL function args: args
        APS parsed args: ['dateFormat', 'twoDigitYear']

        """
        return exec_with_tcl('APSTodaysDateInfo', *args, **kwargs)

    @staticmethod
    def APSOffsetDateInfo(*args, **kwargs):
        """
        Location: DateConversion.tcl
        Usage: APSOffsetDateInfo [-offset <integer>]
        {-today 1 | -year <year> {-month <month> -day <day> | -julianDay <jDay>} | -dateList <list>}
        [-twoDigitYear 1] [-dateFormat {Y-J-MD YMD Y-M-D MDY list}] [leadingZeros 0]
        For -dateFormat list, the information is returned in the form <year> <julianDay> <month> <day>.TCL function args: args
        APS parsed args: ['julianDay', 'year', 'month', 'day', 'dateFormat', 'twoDigitYear', 'dateList', 'offset', 'today', 'leadingZeros']

        """
        return exec_with_tcl('APSOffsetDateInfo', *args, **kwargs)

    @staticmethod
    def APSDateOffsetTest(*args, **kwargs):
        """
        Location: DateConversion.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDateOffsetTest', *args, **kwargs)

    @staticmethod
    def APSIncrementDateVariables(*args, **kwargs):
        """
        Location: DateConversion.tcl
        APSIncrementDateVariables
        [-dayVariable <name>]
        [-monthVariable <name>] [-yearVariable <name>]
        [-offset <number>] [-units {day | month | year}]TCL function args: args
        APS parsed args: ['dayVariable', 'monthVariable', 'yearVariable', 'offset', 'unit']

        """
        return exec_with_tcl('APSIncrementDateVariables', *args, **kwargs)

    @staticmethod
    def ActOnSelectedDiagnostics(*args, **kwargs):
        """
        Location: LDC.tcl
        TCL function args: action args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('ActOnSelectedDiagnostics', *args, **kwargs)

    @staticmethod
    def PerformActionOnSelectedDiagnostics(*args, **kwargs):
        """
        Location: LDC.tcl
        TCL function args: action args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('PerformActionOnSelectedDiagnostics', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForUndulatorHallStudiesInfo(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForUndulatorHallStudiesInfo', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForUndulatorHallStudiesDialog(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForUndulatorHallStudiesDialog', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForUndulatorHallStudies(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: args
        APS parsed args: ['SCRFile', 'cycles', 'turnOffLTPAndPTB', 'LTP:Q', 'LTP:V', 'LTP:H', 'PB:Q', 'PB:V', 'PB:H', 'PTB:Q', 'PTB:V', 'PTB:H', 'BB:Q', 'BB:V', 'BB:H', 'BB:BM', 'BB:BD:Q1', 'LA:Q', 'LS:Q', 'LS:V', 'LS:H', 'LS:BM', 'LU:Q', 'LU:V', 'LU:H', 'ConditionLTP:Q', 'ConditionLTP:V', 'ConditionLTP:H', 'ConditionPB:Q', 'ConditionPB:V', 'ConditionPB:H', 'ConditionPTB:Q', 'ConditionPTB:V', 'ConditionPTB:H', 'ConditionBB:Q', 'ConditionBB:V', 'ConditionBB:H', 'ConditionBB:BM', 'ConditionBB:BD:Q1', 'ConditionLA:Q', 'ConditionLS:Q', 'ConditionLS:V', 'ConditionLS:H', 'ConditionLS:BM', 'ConditionLU:Q', 'ConditionLU:V', 'ConditionLU:H']

        """
        return exec_with_tcl('LEUTL_SetupForUndulatorHallStudies', *args, **kwargs)

    @staticmethod
    def APSPEMExec(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: args
        APS parsed args: ['command']

        """
        return exec_with_tcl('APSPEMExec', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForOperationsInfo(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForOperationsInfo', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForOperationsDialog(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForOperationsDialog', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForOperations(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: args
        APS parsed args: ['energy', 'particle', 'SCRFile', 'conditioningTime', 'DCPS', 'PulsedPS', 'rfSystems', 'standardizeLTPB1', 'conditionLTP', 'conditionPAR', 'conditionPTB']

        """
        return exec_with_tcl('LEUTL_SetupForOperations', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForPARBypassToBoosterInfo(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForPARBypassToBoosterInfo', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForPARBypassToBoosterDialog(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LEUTL_SetupForPARBypassToBoosterDialog', *args, **kwargs)

    @staticmethod
    def LEUTL_SetupForPARBypassToBooster(*args, **kwargs):
        """
        Location: PCGUN_Studies.tcl
        TCL function args: args
        APS parsed args: ['SCRFile']

        """
        return exec_with_tcl('LEUTL_SetupForPARBypassToBooster', *args, **kwargs)

    @staticmethod
    def ProcessVLDData(*args, **kwargs):
        """
        Location: ProcessVLD.tcl
        TCL function args: args
        APS parsed args: ['group', 'output', 'statusCallback', 'configFile', 'ROISizex', 'ROISizey', 'ROIx0', 'ROIx1', 'ROIy0', 'ROIy1', 'blankOutx0', 'blankOutx1', 'blankOuty0', 'blankOuty1', 'sizeLinesx', 'sizeLinesy', 'removeHDF', 'backgroundHalfWidth', 'haloRemoval', 'symmetricBackgroundRemoval', 'lonerRemoval', 'spotImages']

        """
        return exec_with_tcl('ProcessVLDData', *args, **kwargs)

    @staticmethod
    def RFGun_KickerValidationInfo(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('RFGun_KickerValidationInfo', *args, **kwargs)

    @staticmethod
    def RFGun_KickerValidationDialog(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('RFGun_KickerValidationDialog', *args, **kwargs)

    @staticmethod
    def RFGun_KickerValidation(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('RFGun_KickerValidation', *args, **kwargs)

    @staticmethod
    def APSConfigureL1Scope(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['configuration', 'average']

        """
        return exec_with_tcl('APSConfigureL1Scope', *args, **kwargs)

    @staticmethod
    def SetGlobals(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('SetGlobals', *args, **kwargs)

    @staticmethod
    def APSTestCapture(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun', 'nameList', 'setupDir']

        """
        return exec_with_tcl('APSTestCapture', *args, **kwargs)

    @staticmethod
    def ProcessExpDataAndSetCorrector(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['filename', 'corrector']

        """
        return exec_with_tcl('ProcessExpDataAndSetCorrector', *args, **kwargs)

    @staticmethod
    def RestoreRFGunAndL1Correctors(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['filename', 'gun']

        """
        return exec_with_tcl('RestoreRFGunAndL1Correctors', *args, **kwargs)

    @staticmethod
    def SweepCorrectors(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['inputDir', 'stepSize', 'postChange', 'gun', 'numToAve', 'tolerance', 'kickerOff']

        """
        return exec_with_tcl('SweepCorrectors', *args, **kwargs)

    @staticmethod
    def RFGun_KickerReValidation(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['snapshot3', 'gun', 'badCorrectors']

        """
        return exec_with_tcl('RFGun_KickerReValidation', *args, **kwargs)

    @staticmethod
    def ChangeCorrLimits(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['correctorList', 'lowerLimitList', 'upperLimitList', 'gun']

        """
        return exec_with_tcl('ChangeCorrLimits', *args, **kwargs)

    @staticmethod
    def ReadLeakage(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('ReadLeakage', *args, **kwargs)

    @staticmethod
    def APSGetL1ScopeWaveforms(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'gun', 'setupDir', 'calFactor', 'rgCal']

        """
        return exec_with_tcl('APSGetL1ScopeWaveforms', *args, **kwargs)

    @staticmethod
    def APSProcessL1ScopeWaveforms(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'gun', 'nameList', 'pvList']

        """
        return exec_with_tcl('APSProcessL1ScopeWaveforms', *args, **kwargs)

    @staticmethod
    def PlotReference(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('PlotReference', *args, **kwargs)

    @staticmethod
    def LogValidationResult(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun', 'maxLeakage', 'startTime', 'endTime', 'result']

        """
        return exec_with_tcl('LogValidationResult', *args, **kwargs)

    @staticmethod
    def SetupLeakageLog(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('SetupLeakageLog', *args, **kwargs)

    @staticmethod
    def WriteToLogFile(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['step', 'logFID', 'gun', 'leakage', 'worstCorrector', 'description']

        """
        return exec_with_tcl('WriteToLogFile', *args, **kwargs)

    @staticmethod
    def GetL1L2DriveKryston(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('GetL1L2DriveKryston', *args, **kwargs)

    @staticmethod
    def GetRFGunSelection(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('GetRFGunSelection', *args, **kwargs)

    @staticmethod
    def TestCorrectors(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun', 'needScanCorrList']

        """
        return exec_with_tcl('TestCorrectors', *args, **kwargs)

    @staticmethod
    def StartRFGun_LeakageMonitorInfo(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('StartRFGun_LeakageMonitorInfo', *args, **kwargs)

    @staticmethod
    def StopRFGun_LeakageMonitorInfo(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('StopRFGun_LeakageMonitorInfo', *args, **kwargs)

    @staticmethod
    def StartRFGun_LeakageMonitorInitDialog(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('StartRFGun_LeakageMonitorInitDialog', *args, **kwargs)

    @staticmethod
    def StartRFGun_LeakageMonitor(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('StartRFGun_LeakageMonitor', *args, **kwargs)

    @staticmethod
    def StopRFGun_LeakageMonitor(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('StopRFGun_LeakageMonitor', *args, **kwargs)

    @staticmethod
    def AbortSweepingCorrectors(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('AbortSweepingCorrectors', *args, **kwargs)

    @staticmethod
    def APSMpShutdownDrive2(*args, **kwargs):
        """
        Location: RFGUN_Kicker_Validation.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpShutdownDrive2', *args, **kwargs)

    @staticmethod
    def RFGUN_Switch_for_RFConditioingInfo(*args, **kwargs):
        """
        Location: RFGUN_Switch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_Switch_for_RFConditioingInfo', *args, **kwargs)

    @staticmethod
    def RFGUN_Switch_for_RFConditioing(*args, **kwargs):
        """
        Location: RFGUN_Switch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_Switch_for_RFConditioing', *args, **kwargs)

    @staticmethod
    def APSBPLDglobals(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSBPLDglobals', *args, **kwargs)

    @staticmethod
    def APSBPLDScan(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: ['sector', 'IsDigital', 'statusCallback']

        """
        return exec_with_tcl('APSBPLDScan', *args, **kwargs)

    @staticmethod
    def ExecuteNext(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: ['sector', 'IsDigital']

        """
        return exec_with_tcl('ExecuteNext', *args, **kwargs)

    @staticmethod
    def ControllawInfoButton(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('ControllawInfoButton', *args, **kwargs)

    @staticmethod
    def StartControllaw(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'restartOnly']

        """
        return exec_with_tcl('StartControllaw', *args, **kwargs)

    @staticmethod
    def StopControllaw(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('StopControllaw', *args, **kwargs)

    @staticmethod
    def resetBPLDTrips(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('resetBPLDTrips', *args, **kwargs)

    @staticmethod
    def WaitForControllaw(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: ['sector', 'statusCallback', 'ultimateCallback']

        """
        return exec_with_tcl('WaitForControllaw', *args, **kwargs)

    @staticmethod
    def DisableScanButtons(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('DisableScanButtons', *args, **kwargs)

    @staticmethod
    def EnableScanButtons(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('EnableScanButtons', *args, **kwargs)

    @staticmethod
    def CheckRunControls(*args, **kwargs):
        """
        Location: SRBPLDVerification.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('CheckRunControls', *args, **kwargs)

    @staticmethod
    def MakeSRBPMCheckoutStatusWidget(*args, **kwargs):
        """
        Location: SRBPMSelfTestWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'system']

        """
        return exec_with_tcl('MakeSRBPMCheckoutStatusWidget', *args, **kwargs)

    @staticmethod
    def MakeSRBPMSelfTestWidget(*args, **kwargs):
        """
        Location: SRBPMSelfTestWidgets.tcl
        TCL function args: widget args
        APS parsed args: None

        """
        return exec_with_tcl('MakeSRBPMSelfTestWidget', *args, **kwargs)

    @staticmethod
    def UpdateSelfTestNumber(*args, **kwargs):
        """
        Location: SRBPMSelfTestWidgets.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('UpdateSelfTestNumber', *args, **kwargs)

    @staticmethod
    def MakeLabelledEntryWidgets(*args, **kwargs):
        """
        Location: SRBPMSelfTestWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'fileWidth', 'system']

        """
        return exec_with_tcl('MakeLabelledEntryWidgets', *args, **kwargs)

    @staticmethod
    def DoIOCBunchTrainInjection(*args, **kwargs):
        """
        Location: SRBunchTrainIOC.tcl
        TCL function args: args
        APS parsed args: ['start', 'interval', 'number', 'dwell', 'callback', 'fast', 'stopAt', 'stopAtSum', 'useSum', 'cycles', 'multiplet', 'stopMode', 'keepWarm', 'manageLinacBunches', 'pattern']

        """
        return exec_with_tcl('DoIOCBunchTrainInjection', *args, **kwargs)

    @staticmethod
    def APSSRSetBucketPattern(*args, **kwargs):
        """
        Location: SRBunchTrainIOC.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRSetBucketPattern', *args, **kwargs)

    @staticmethod
    def APSLevelBunchCharge(*args, **kwargs):
        """
        Location: SRBunchTrainIOC.tcl
        TCL function args: args
        APS parsed args: ['desiredCurrent', 'bpmGroupCurrent', 'keepWarm', 'bpmGroupBuckets', 'otherBuckets', 'deficitThreshold', 'manageLinacBunches', 'cycles', 'BBCMAverages', 'statusCallback', 'doubleFirst', 'uniformCurrent']

        """
        return exec_with_tcl('APSLevelBunchCharge', *args, **kwargs)

    @staticmethod
    def DoIOCBucketFilling(*args, **kwargs):
        """
        Location: SRBunchTrainIOC.tcl
        TCL function args: args
        APS parsed args: ['bucketList', 'statusCallback', 'stopAt', 'stopMode', 'manageLinacBunches', 'doubleFirst']

        """
        return exec_with_tcl('DoIOCBucketFilling', *args, **kwargs)

    @staticmethod
    def RestartIOCBunchTrainInjection(*args, **kwargs):
        """
        Location: SRBunchTrainIOC.tcl
        TCL function args: args
        APS parsed args: ['stopAt', 'useSum', 'stopAtSum', 'callback', 'keepWarm', 'manageLinacBunches']

        """
        return exec_with_tcl('RestartIOCBunchTrainInjection', *args, **kwargs)

    @staticmethod
    def APSSRCompareMSSCDU(*args, **kwargs):
        """
        Location: SRCompareMSSCDU.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRCompareMSSCDU', *args, **kwargs)

    @staticmethod
    def APSSRCheckHVCurrentCheck(*args, **kwargs):
        """
        Location: SRHVCheck.tcl
        TCL function args: args
        APS parsed args: ['samples', 'interval', 'fileName', 'statusCallback', 'flagSuffix']

        """
        return exec_with_tcl('APSSRCheckHVCurrentCheck', *args, **kwargs)

    @staticmethod
    def APSAcquireSROrbit(*args, **kwargs):
        """
        Location: SROrbit.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAcquireSROrbit', *args, **kwargs)

    @staticmethod
    def APSSROrbitGlitchPlots(*args, **kwargs):
        """
        Location: SROrbitGlitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSROrbitGlitchPlots', *args, **kwargs)

    @staticmethod
    def APSSRFindOrbitGlitchSource(*args, **kwargs):
        """
        Location: SROrbitGlitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRFindOrbitGlitchSource', *args, **kwargs)

    @staticmethod
    def APSSRFindOrbitSource(*args, **kwargs):
        """
        Location: SROrbitGlitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRFindOrbitSource', *args, **kwargs)

    @staticmethod
    def APSSRCorrectorGlitchPlots(*args, **kwargs):
        """
        Location: SROrbitGlitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRCorrectorGlitchPlots', *args, **kwargs)

    @staticmethod
    def APSSRFindOrbitGlitchSourceSVD(*args, **kwargs):
        """
        Location: SROrbitGlitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRFindOrbitGlitchSourceSVD', *args, **kwargs)

    @staticmethod
    def APSSRAcquireSlowHistories(*args, **kwargs):
        """
        Location: SRSlowBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['sectorList', 'startSector', 'endSector', 'BPM', 'historyBufferSize', 'acquisitionPlane', 'outputFile', 'statusCallback', 'abortVariable', 'BPMList', 'excludeScalars']

        """
        return exec_with_tcl('APSSRAcquireSlowHistories', *args, **kwargs)

    @staticmethod
    def APSProcessSlowHistoryData(*args, **kwargs):
        """
        Location: SRSlowBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['inputFile', 'outputFile', 'rmsOnly', 'useMedian']

        """
        return exec_with_tcl('APSProcessSlowHistoryData', *args, **kwargs)

    @staticmethod
    def FillForVIP(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('FillForVIP', *args, **kwargs)

    @staticmethod
    def TopUpForVIP(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('TopUpForVIP', *args, **kwargs)

    @staticmethod
    def StopForVIP(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('StopForVIP', *args, **kwargs)

    @staticmethod
    def DumpForVIP(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('DumpForVIP', *args, **kwargs)

    @staticmethod
    def APSVIPEmulationDoDamping(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSVIPEmulationDoDamping', *args, **kwargs)

    @staticmethod
    def APSMakeVIPFillInterface(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['emulation']

        """
        return exec_with_tcl('APSMakeVIPFillInterface', *args, **kwargs)

    @staticmethod
    def VIPDemoLoggerAndDisplay(*args, **kwargs):
        """
        Location: VIPSRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['emulation']

        """
        return exec_with_tcl('VIPDemoLoggerAndDisplay', *args, **kwargs)

    @staticmethod
    def bccheckpause(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bccheckpause', *args, **kwargs)

    @staticmethod
    def bccontrol(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('bccontrol', *args, **kwargs)

    @staticmethod
    def bcfinish(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcfinish', *args, **kwargs)

    @staticmethod
    def bcfinishplane(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: point plane
        APS parsed args: None

        """
        return exec_with_tcl('bcfinishplane', *args, **kwargs)

    @staticmethod
    def bcfinishpoint(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: point
        APS parsed args: None

        """
        return exec_with_tcl('bcfinishpoint', *args, **kwargs)

    @staticmethod
    def bcfinishstep(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: step
        APS parsed args: None

        """
        return exec_with_tcl('bcfinishstep', *args, **kwargs)

    @staticmethod
    def bcinitialize(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcinitialize', *args, **kwargs)

    @staticmethod
    def bcinitializepoint(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: point
        APS parsed args: None

        """
        return exec_with_tcl('bcinitializepoint', *args, **kwargs)

    @staticmethod
    def bcinitializestep(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: step
        APS parsed args: None

        """
        return exec_with_tcl('bcinitializestep', *args, **kwargs)

    @staticmethod
    def bcmainloop(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcmainloop', *args, **kwargs)

    @staticmethod
    def bcplot(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcplot', *args, **kwargs)

    @staticmethod
    def bcrampval(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: time
        APS parsed args: None

        """
        return exec_with_tcl('bcrampval', *args, **kwargs)

    @staticmethod
    def bcrestore(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcrestore', *args, **kwargs)

    @staticmethod
    def bcsave(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcsave', *args, **kwargs)

    @staticmethod
    def bcsetplane(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcsetplane', *args, **kwargs)

    @staticmethod
    def bcsetup(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcsetup', *args, **kwargs)

    @staticmethod
    def bcstatistics(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('bcstatistics', *args, **kwargs)

    @staticmethod
    def bcstatus(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: color
        APS parsed args: None

        """
        return exec_with_tcl('bcstatus', *args, **kwargs)

    @staticmethod
    def bcverticalstep(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: step
        APS parsed args: None

        """
        return exec_with_tcl('bcverticalstep', *args, **kwargs)

    @staticmethod
    def bchorizontalstep(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: step
        APS parsed args: None

        """
        return exec_with_tcl('bchorizontalstep', *args, **kwargs)

    @staticmethod
    def bcsetstatus(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: string
        APS parsed args: None

        """
        return exec_with_tcl('bcsetstatus', *args, **kwargs)

    @staticmethod
    def makebcrestore(*args, **kwargs):
        """
        Location: bc.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebcrestore', *args, **kwargs)

    @staticmethod
    def makebconfig(*args, **kwargs):
        """
        Location: bconfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('makebconfig', *args, **kwargs)

    @staticmethod
    def makeboosterbuttons(*args, **kwargs):
        """
        Location: bconfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('makeboosterbuttons', *args, **kwargs)

    @staticmethod
    def setboosterbuttonsdefaults(*args, **kwargs):
        """
        Location: bconfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('setboosterbuttonsdefaults', *args, **kwargs)

    @staticmethod
    def setboosterbuttonsflags(*args, **kwargs):
        """
        Location: bconfig.tcl
        TCL function args: w val args
        APS parsed args: None

        """
        return exec_with_tcl('setboosterbuttonsflags', *args, **kwargs)

    @staticmethod
    def writebconfigfile(*args, **kwargs):
        """
        Location: bconfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('writebconfigfile', *args, **kwargs)

    @staticmethod
    def getbcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('getbcorr', *args, **kwargs)

    @staticmethod
    def getbdeltap(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('getbdeltap', *args, **kwargs)

    @staticmethod
    def makegetfilename(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makegetfilename', *args, **kwargs)

    @staticmethod
    def makemonitorbcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makemonitorbcorr', *args, **kwargs)

    @staticmethod
    def makemonitorbcorrfilename(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makemonitorbcorrfilename', *args, **kwargs)

    @staticmethod
    def makebdispersion(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebdispersion', *args, **kwargs)

    @staticmethod
    def makebsetallcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebsetallcorr', *args, **kwargs)

    @staticmethod
    def makesetbcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makesetbcorr', *args, **kwargs)

    @staticmethod
    def makesetbcorrps(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makesetbcorrps', *args, **kwargs)

    @staticmethod
    def monitorbcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: mode args
        APS parsed args: None

        """
        return exec_with_tcl('monitorbcorr', *args, **kwargs)

    @staticmethod
    def setbcorr(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbcorr', *args, **kwargs)

    @staticmethod
    def setbcorrzero(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbcorrzero', *args, **kwargs)

    @staticmethod
    def setbcorrinit(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbcorrinit', *args, **kwargs)

    @staticmethod
    def setbcorrps(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbcorrps', *args, **kwargs)

    @staticmethod
    def setplane(*args, **kwargs):
        """
        Location: bcorr.tcl
        TCL function args: opt
        APS parsed args: None

        """
        return exec_with_tcl('setplane', *args, **kwargs)

    @staticmethod
    def combramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('combramp', *args, **kwargs)

    @staticmethod
    def loadbramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('loadbramp', *args, **kwargs)

    @staticmethod
    def makecombramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makecombramp', *args, **kwargs)

    @staticmethod
    def makecombrampfilenames(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makecombrampfilenames', *args, **kwargs)

    @staticmethod
    def makebrampao(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebrampao', *args, **kwargs)

    @staticmethod
    def makesaveramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makesaveramp', *args, **kwargs)

    @staticmethod
    def plotbramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('plotbramp', *args, **kwargs)

    @staticmethod
    def saveramptable(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('saveramptable', *args, **kwargs)

    @staticmethod
    def savesnap(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('savesnap', *args, **kwargs)

    @staticmethod
    def setbramp2ao(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setbramp2ao', *args, **kwargs)

    @staticmethod
    def setbramp2table(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setbramp2table', *args, **kwargs)

    @staticmethod
    def setbao2ramp(*args, **kwargs):
        """
        Location: bramp.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setbao2ramp', *args, **kwargs)

    @staticmethod
    def APScaWave(*args, **kwargs):
        """
        Location: cawave.tcl
        APScaWave -pvList <list> -variableList <list> -amplitudeList <list> [-period <seconds>] [-decayConstant 1/periods] [-periods <number>] [-stepsPerPeriod <number>] [-dryRun 1] [-postStepCallback <procName>] [-abortVariable <variableName>] [-function {sin | cos | twCenter | random}] [-resetOnAbort 1]TCL function args: args
        APS parsed args: ['pvList', 'variableList', 'amplitudeList', 'period', 'decayConstant', 'periods', 'stepsPerPeriod', 'dryRun', 'postStepCallback', 'abortVariable', 'function', 'resetOnAbort', 'integerList']

        """
        return exec_with_tcl('APScaWave', *args, **kwargs)

    @staticmethod
    def APSGetRandomNumbers(*args, **kwargs):
        """
        Location: cawave.tcl
        APSGetRandomNumbers -n <number> -type {uniform|gaussian}TCL function args: args
        APS parsed args: ['n', 'type']

        """
        return exec_with_tcl('APSGetRandomNumbers', *args, **kwargs)

    @staticmethod
    def setcorbitdefaults(*args, **kwargs):
        """
        Location: corbit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setcorbitdefaults', *args, **kwargs)

    @staticmethod
    def makecorbit(*args, **kwargs):
        """
        Location: corbit.tcl
        TCL function args: w args
        APS parsed args: ['simple']

        """
        return exec_with_tcl('makecorbit', *args, **kwargs)

    @staticmethod
    def corbit(*args, **kwargs):
        """
        Location: corbit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('corbit', *args, **kwargs)

    @staticmethod
    def APSLinkToDeviceConfigPVs(*args, **kwargs):
        """
        Location: devices.tcl
        TCL function args: args
        APS parsed args: ['device']

        """
        return exec_with_tcl('APSLinkToDeviceConfigPVs', *args, **kwargs)

    @staticmethod
    def APSLinkToLINACPVs(*args, **kwargs):
        """
        Location: devices.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSLinkToLINACPVs', *args, **kwargs)

    @staticmethod
    def APSLinkToPTBPVs(*args, **kwargs):
        """
        Location: devices.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSLinkToPTBPVs', *args, **kwargs)

    @staticmethod
    def APSPVValueCompare(*args, **kwargs):
        """
        Location: devices.tcl
        TCL function args: value1 value2
        APS parsed args: None

        """
        return exec_with_tcl('APSPVValueCompare', *args, **kwargs)

    @staticmethod
    def APSLinkToDevicePVs(*args, **kwargs):
        """
        Location: devices.tcl
        TCL function args: args
        APS parsed args: ['fileList']

        """
        return exec_with_tcl('APSLinkToDevicePVs', *args, **kwargs)

    @staticmethod
    def APSDevSend(*args, **kwargs):
        """
        Location: devices.tcl
        Usage: APSDevSend -group <name> [-operation <name> [-deviceList <list> [{-valueList <list> | -value <item>}] [-forceRead 1] [-blunderAhead 1] [-timeout <secs>] [-returnPVList 1] [-releaseLinks 1]]]TCL function args: args
        APS parsed args: ['group', 'operation', 'deviceList', 'valueList', 'value', 'forceRead', 'blunderAhead', 'timeout', 'returnPVList', 'releaseLinks', 'cavput']

        """
        return exec_with_tcl('APSDevSend', *args, **kwargs)

    @staticmethod
    def dp_atexit_appendUnique(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_appendUnique', *args, **kwargs)

    @staticmethod
    def dp_atexit_append(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_append', *args, **kwargs)

    @staticmethod
    def dp_atexit_prepend(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_prepend', *args, **kwargs)

    @staticmethod
    def dp_atexit_insert(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_insert', *args, **kwargs)

    @staticmethod
    def dp_atexit_delete(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_delete', *args, **kwargs)

    @staticmethod
    def dp_atexit_clear(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_clear', *args, **kwargs)

    @staticmethod
    def dp_atexit(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: {option list} args
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit', *args, **kwargs)

    @staticmethod
    def dp_atexit_install_exit(*args, **kwargs):
        """
        Location: dp_atexit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('dp_atexit_install_exit', *args, **kwargs)

    @staticmethod
    def checkfmonoffset(*args, **kwargs):
        """
        Location: feedback.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('checkfmonoffset', *args, **kwargs)

    @staticmethod
    def makecheckfmonoffset(*args, **kwargs):
        """
        Location: feedback.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makecheckfmonoffset', *args, **kwargs)

    @staticmethod
    def bltResetBindings(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph type
        APS parsed args: None

        """
        return exec_with_tcl('bltResetBindings', *args, **kwargs)

    @staticmethod
    def bltActivateLegend(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph name
        APS parsed args: None

        """
        return exec_with_tcl('bltActivateLegend', *args, **kwargs)

    @staticmethod
    def bltSetActiveLegend(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph
        APS parsed args: None

        """
        return exec_with_tcl('bltSetActiveLegend', *args, **kwargs)

    @staticmethod
    def bltSetCrosshairs(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph
        APS parsed args: None

        """
        return exec_with_tcl('bltSetCrosshairs', *args, **kwargs)

    @staticmethod
    def bltFindElement(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph x y
        APS parsed args: None

        """
        return exec_with_tcl('bltFindElement', *args, **kwargs)

    @staticmethod
    def bltFlashPoint(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph name index count
        APS parsed args: None

        """
        return exec_with_tcl('bltFlashPoint', *args, **kwargs)

    @staticmethod
    def bltSetClosestPoint(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph
        APS parsed args: None

        """
        return exec_with_tcl('bltSetClosestPoint', *args, **kwargs)

    @staticmethod
    def bltGetCoords(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph winX winY var index
        APS parsed args: None

        """
        return exec_with_tcl('bltGetCoords', *args, **kwargs)

    @staticmethod
    def bltGetAnchor(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph x y
        APS parsed args: None

        """
        return exec_with_tcl('bltGetAnchor', *args, **kwargs)

    @staticmethod
    def bltBox(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph x1 y1 x2 y2
        APS parsed args: None

        """
        return exec_with_tcl('bltBox', *args, **kwargs)

    @staticmethod
    def bltScan(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph x y
        APS parsed args: None

        """
        return exec_with_tcl('bltScan', *args, **kwargs)

    @staticmethod
    def bltZoom(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph x y
        APS parsed args: None

        """
        return exec_with_tcl('bltZoom', *args, **kwargs)

    @staticmethod
    def bltSetZoom(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph
        APS parsed args: None

        """
        return exec_with_tcl('bltSetZoom', *args, **kwargs)

    @staticmethod
    def bltSetPrint(*args, **kwargs):
        """
        Location: keblt.tcl
        TCL function args:  graph
        APS parsed args: None

        """
        return exec_with_tcl('bltSetPrint', *args, **kwargs)

    @staticmethod
    def printsource(*args, **kwargs):
        """
        Location: kedebug.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('printsource', *args, **kwargs)

    @staticmethod
    def showwidgetnameswithmouse(*args, **kwargs):
        """
        Location: kedebug.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('showwidgetnameswithmouse', *args, **kwargs)

    @staticmethod
    def pvcmon(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var
        APS parsed args: None

        """
        return exec_with_tcl('pvcmon', *args, **kwargs)

    @staticmethod
    def pvget(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var
        APS parsed args: None

        """
        return exec_with_tcl('pvget', *args, **kwargs)

    @staticmethod
    def pvinfo(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var {pvinfolist "NotGiven"}
        APS parsed args: None

        """
        return exec_with_tcl('pvinfo', *args, **kwargs)

    @staticmethod
    def pvlink(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var name
        APS parsed args: None

        """
        return exec_with_tcl('pvlink', *args, **kwargs)

    @staticmethod
    def pvmon(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var
        APS parsed args: None

        """
        return exec_with_tcl('pvmon', *args, **kwargs)

    @staticmethod
    def pvput(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var _val
        APS parsed args: None

        """
        return exec_with_tcl('pvput', *args, **kwargs)

    @staticmethod
    def pvstat(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: _var
        APS parsed args: None

        """
        return exec_with_tcl('pvstat', *args, **kwargs)

    @staticmethod
    def caget(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: name
        APS parsed args: None

        """
        return exec_with_tcl('caget', *args, **kwargs)

    @staticmethod
    def caput(*args, **kwargs):
        """
        Location: keetwrapper.tcl
        TCL function args: name _val
        APS parsed args: None

        """
        return exec_with_tcl('caput', *args, **kwargs)

    @staticmethod
    def addfilebuttons(*args, **kwargs):
        """
        Location: kefileutils.tcl
        TCL function args: parent args
        APS parsed args: ['types', 'variable', 'path', 'pattern', 'checkValidity', 'trim']

        """
        return exec_with_tcl('addfilebuttons', *args, **kwargs)

    @staticmethod
    def findfile(*args, **kwargs):
        """
        Location: kefileutils.tcl
        TCL function args: filenamevariable trim args
        APS parsed args: None

        """
        return exec_with_tcl('findfile', *args, **kwargs)

    @staticmethod
    def incrementname(*args, **kwargs):
        """
        Location: kefileutils.tcl
        TCL function args: filenamevariable increment
        APS parsed args: None

        """
        return exec_with_tcl('incrementname', *args, **kwargs)

    @staticmethod
    def APSMakeToplevel(*args, **kwargs):
        """
        Location: kemaketop.tcl
        TCL function args: w args
        APS parsed args: ['title', 'command', 'contextHelp']

        """
        return exec_with_tcl('APSMakeToplevel', *args, **kwargs)

    @staticmethod
    def APSAlertBox1(*args, **kwargs):
        """
        Location: kewrapper.tcl
        TCL function args: widget args
        APS parsed args: ['unique', 'fg', 'bg']

        """
        return exec_with_tcl('APSAlertBox1', *args, **kwargs)

    @staticmethod
    def APSErrorDialog(*args, **kwargs):
        """
        Location: kewrapper.tcl
        TCL function args: widget args
        APS parsed args: ['unique', 'title', 'errorMessage']

        """
        return exec_with_tcl('APSErrorDialog', *args, **kwargs)

    @staticmethod
    def APSExec1Log(*args, **kwargs):
        """
        Location: kewrapper.tcl
        TCL function args: widget args
        APS parsed args: ['unique']

        """
        return exec_with_tcl('APSExec1Log', *args, **kwargs)

    @staticmethod
    def APSResetDefaultFont(*args, **kwargs):
        """
        Location: kewrapper.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSResetDefaultFont', *args, **kwargs)

    @staticmethod
    def Fit_GetZeroBpms(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['filename', 'threshold', 'column', 'abovebelow']

        """
        return exec_with_tcl('Fit_GetZeroBpms', *args, **kwargs)

    @staticmethod
    def Fit_MakeColumnFromMatrix(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['matrixFile', 'columnFile', 'columnName']

        """
        return exec_with_tcl('Fit_MakeColumnFromMatrix', *args, **kwargs)

    @staticmethod
    def Fit_SplitList(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['List', 'splitTasks']

        """
        return exec_with_tcl('Fit_SplitList', *args, **kwargs)

    @staticmethod
    def Fit_GenerateElegantFileFromLTE1(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('Fit_GenerateElegantFileFromLTE1', *args, **kwargs)

    @staticmethod
    def Fit_WriteToFile(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['filename', 'accessMode', 'line']

        """
        return exec_with_tcl('Fit_WriteToFile', *args, **kwargs)

    @staticmethod
    def Fit_ChooseLOCOConfiguration(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['configDirectory']

        """
        return exec_with_tcl('Fit_ChooseLOCOConfiguration', *args, **kwargs)

    @staticmethod
    def Fit_commentCompare(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  a b
        APS parsed args: None

        """
        return exec_with_tcl('Fit_commentCompare', *args, **kwargs)

    @staticmethod
    def Fit_EnableButtons(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  widgetList
        APS parsed args: None

        """
        return exec_with_tcl('Fit_EnableButtons', *args, **kwargs)

    @staticmethod
    def Fit_DisableButtons(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  widgetList
        APS parsed args: None

        """
        return exec_with_tcl('Fit_DisableButtons', *args, **kwargs)

    @staticmethod
    def Fit_AddLine(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['inputFile', 'outputFile', 'searchString', 'includeString', 'substitute']

        """
        return exec_with_tcl('Fit_AddLine', *args, **kwargs)

    @staticmethod
    def Fit_DeleteElementsFromList(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['elementList', 'deleteElements']

        """
        return exec_with_tcl('Fit_DeleteElementsFromList', *args, **kwargs)

    @staticmethod
    def Fit_LookForDoneFiles(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['jobNameList', 'completedJobList', 'doneFileList', 'waitTime']

        """
        return exec_with_tcl('Fit_LookForDoneFiles', *args, **kwargs)

    @staticmethod
    def Fit_ResubmitLostJobs(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['lostJobList', 'jobNameList', 'commandList', 'doneFileList']

        """
        return exec_with_tcl('Fit_ResubmitLostJobs', *args, **kwargs)

    @staticmethod
    def Fit_GetNewJobList_PBS(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['jobNameList']

        """
        return exec_with_tcl('Fit_GetNewJobList_PBS', *args, **kwargs)

    @staticmethod
    def Fit_GetNewJobList_SGE(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['jobNameList', 'pidList']

        """
        return exec_with_tcl('Fit_GetNewJobList_SGE', *args, **kwargs)

    @staticmethod
    def Fit_GetNewJobList_PS(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['jobNameList', 'pidList']

        """
        return exec_with_tcl('Fit_GetNewJobList_PS', *args, **kwargs)

    @staticmethod
    def Fit_WaitForTasks_New(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['pidList', 'jobNameList', 'commandList', 'logFileList', 'doneFileList', 'useQsub', 'verbose', 'waitTime', 'waitInterval', 'usePopupWindow', 'abortFile']

        """
        return exec_with_tcl('Fit_WaitForTasks_New', *args, **kwargs)

    @staticmethod
    def Fit_SubmitJobs(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args: args
        APS parsed args: ['commandList', 'jobNameList', 'doneFileList', 'verbose']

        """
        return exec_with_tcl('Fit_SubmitJobs', *args, **kwargs)

    @staticmethod
    def Fit_CalculateResponseMatrixDerivative(*args, **kwargs):
        """
        Location: locoFittingProcedures.tcl
        TCL function args:  args
        APS parsed args: ['varList', 'splitTasks', 'scriptName', 'scriptParameters', 'matrixFile', 'tmpDirName', 'useQsub', 'qsubCommand', 'continuePrevious', 'rootTaskName', 'usePopupWindow', 'waitTime', 'waitInterval', 'submissionPause', 'abortFile', 'verbose', 'qsubRespProcCommand', 'queueSystemName']

        """
        return exec_with_tcl('Fit_CalculateResponseMatrixDerivative', *args, **kwargs)

    @staticmethod
    def APSSDDSCheckButtons(*args, **kwargs):
        """
        Location: mbSDDSCheckButtons.tcl
        TCL function args: widget args
        APS parsed args: ['callback', 'modal', 'page', 'arrayName', 'column', 'fileName', 'parent', 'name', 'limit', 'widthLimit', 'duplicate', 'noOk', 'noCancel', 'buttonSize']

        """
        return exec_with_tcl('APSSDDSCheckButtons', *args, **kwargs)

    @staticmethod
    def APSSDDSRadioButtons(*args, **kwargs):
        """
        Location: mbSDDSRadioButtons.tcl
        TCL function args: widget args
        APS parsed args: ['callback', 'modal', 'page', 'variable', 'column', 'fileName', 'parent', 'name', 'limit', 'duplicate']

        """
        return exec_with_tcl('APSSDDSRadioButtons', *args, **kwargs)

    @staticmethod
    def MakeFrameOrWindow(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['toplevel', 'title']

        """
        return exec_with_tcl('MakeFrameOrWindow', *args, **kwargs)

    @staticmethod
    def RunSDDSListboxDataTaker(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: DataTaker widget LBID count x y
        APS parsed args: None

        """
        return exec_with_tcl('RunSDDSListboxDataTaker', *args, **kwargs)

    @staticmethod
    def APSRemoveColData(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: count ID
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveColData', *args, **kwargs)

    @staticmethod
    def APSDefaultLabelMaker(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: data width
        APS parsed args: None

        """
        return exec_with_tcl('APSDefaultLabelMaker', *args, **kwargs)

    @staticmethod
    def APSMakeSDDSListbox(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: filename widget args
        APS parsed args: ['toplevel', 'title', 'page', 'labelmaker', 'callback']

        """
        return exec_with_tcl('APSMakeSDDSListbox', *args, **kwargs)

    @staticmethod
    def GoToNextButtonPage(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: w pane
        APS parsed args: None

        """
        return exec_with_tcl('GoToNextButtonPage', *args, **kwargs)

    @staticmethod
    def GoToLastButtonPage(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: w pane
        APS parsed args: None

        """
        return exec_with_tcl('GoToLastButtonPage', *args, **kwargs)

    @staticmethod
    def APSMakeSDDSButtons(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: filename widget args
        APS parsed args: ['callback', 'toplevel', 'title', 'limit', 'page', 'labelmaker']

        """
        return exec_with_tcl('APSMakeSDDSButtons', *args, **kwargs)

    @staticmethod
    def APSMakeSDDSCheckButtons(*args, **kwargs):
        """
        Location: mbsddsWidgets.tcl
        TCL function args: filename widget column arrayName args
        APS parsed args: ['toplevel', 'title', 'page', 'limit', 'callback', 'nograb']

        """
        return exec_with_tcl('APSMakeSDDSCheckButtons', *args, **kwargs)

    @staticmethod
    def medmbcorr(*args, **kwargs):
        """
        Location: medmgroups.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('medmbcorr', *args, **kwargs)

    @staticmethod
    def Debug(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: msg
        APS parsed args: None

        """
        return exec_with_tcl('Debug', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc1Info(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc1Info', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc2Info(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc2Info', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc3Info(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc3Info', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123SeqInfo(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123SeqInfo', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123ParInfo(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123ParInfo', *args, **kwargs)

    @staticmethod
    def APSPEMTestDummy(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestDummy', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc1(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: hangUp
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc1', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc2(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: hangUp
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc2', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc3(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: hangUp
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc3', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc4(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: hangUp
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc4', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc5(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: hangUp
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc5', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123Seq(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123Seq', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123Par(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123Par', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123SeqInitDialog(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123SeqInitDialog', *args, **kwargs)

    @staticmethod
    def APSPEMTestProc123ParInitDialog(*args, **kwargs):
        """
        Location: pemTestProc.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSPEMTestProc123ParInitDialog', *args, **kwargs)

    @staticmethod
    def findsbadbpms(*args, **kwargs):
        """
        Location: sbpm.tcl
        TCL function args: args
        APS parsed args: ['filename', 'limit', 'plot', 'listGood', 'listBad']

        """
        return exec_with_tcl('findsbadbpms', *args, **kwargs)

    @staticmethod
    def getsbpmsnap(*args, **kwargs):
        """
        Location: sbpm.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('getsbpmsnap', *args, **kwargs)

    @staticmethod
    def makesiocavg(*args, **kwargs):
        """
        Location: sbpm.tcl
        TCL function args: w1
        APS parsed args: None

        """
        return exec_with_tcl('makesiocavg', *args, **kwargs)

    @staticmethod
    def setiocavgparams(*args, **kwargs):
        """
        Location: sbpm.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setiocavgparams', *args, **kwargs)

    @staticmethod
    def setsbpmsnap2setpoints(*args, **kwargs):
        """
        Location: sbpm.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setsbpmsnap2setpoints', *args, **kwargs)

    @staticmethod
    def makesconfig(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('makesconfig', *args, **kwargs)

    @staticmethod
    def makesrbuttons(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: w args
        APS parsed args: None

        """
        return exec_with_tcl('makesrbuttons', *args, **kwargs)

    @staticmethod
    def makesrbpmcorrlist(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makesrbpmcorrlist', *args, **kwargs)

    @staticmethod
    def readsconfigfile(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: filename options
        APS parsed args: None

        """
        return exec_with_tcl('readsconfigfile', *args, **kwargs)

    @staticmethod
    def setsconfiglabel(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setsconfiglabel', *args, **kwargs)

    @staticmethod
    def setsrnonexist(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setsrnonexist', *args, **kwargs)

    @staticmethod
    def setsrbuttonsdefaults(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setsrbuttonsdefaults', *args, **kwargs)

    @staticmethod
    def setsrbuttonsflags(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: val args
        APS parsed args: None

        """
        return exec_with_tcl('setsrbuttonsflags', *args, **kwargs)

    @staticmethod
    def togglesrbuttonsflags(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: w position args
        APS parsed args: None

        """
        return exec_with_tcl('togglesrbuttonsflags', *args, **kwargs)

    @staticmethod
    def writesconfigfile(*args, **kwargs):
        """
        Location: sconfig.tcl
        TCL function args: filename args
        APS parsed args: None

        """
        return exec_with_tcl('writesconfigfile', *args, **kwargs)

    @staticmethod
    def APSExpandSDDSSpaceUsedDirList(*args, **kwargs):
        """
        Location: sddsSpaceUsed.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSExpandSDDSSpaceUsedDirList', *args, **kwargs)

    @staticmethod
    def APSSddsmonitorSlaveCallback(*args, **kwargs):
        """
        Location: sddsmonitor.tcl
        TCL function args: fid flagVariable
        APS parsed args: None

        """
        return exec_with_tcl('APSSddsmonitorSlaveCallback', *args, **kwargs)

    @staticmethod
    def APSStartSddsmonitorSlave(*args, **kwargs):
        """
        Location: sddsmonitor.tcl
        TCL function args: args
        APS parsed args: ['ID', 'sddsmonitorOptions', 'sddsmonitorProgram', 'preacquireCommand']

        """
        return exec_with_tcl('APSStartSddsmonitorSlave', *args, **kwargs)

    @staticmethod
    def APSWaitForSddsmonitorSlave(*args, **kwargs):
        """
        Location: sddsmonitor.tcl
        TCL function args: args
        APS parsed args: ['ID']

        """
        return exec_with_tcl('APSWaitForSddsmonitorSlave', *args, **kwargs)

    @staticmethod
    def APSSddsMonitorSlaveTakePoint(*args, **kwargs):
        """
        Location: sddsmonitor.tcl
        TCL function args: args
        APS parsed args: ['ID', 'postPause']

        """
        return exec_with_tcl('APSSddsMonitorSlaveTakePoint', *args, **kwargs)

    @staticmethod
    def APSStopSddsmonitorSlave(*args, **kwargs):
        """
        Location: sddsmonitor.tcl
        TCL function args: args
        APS parsed args: ['ID']

        """
        return exec_with_tcl('APSStopSddsmonitorSlave', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckInjectionInfo(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckInjectionInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckInjection(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: ['includeBTS', 'includeMPS', 'includeFlags']

        """
        return exec_with_tcl('APSMpSRCheckInjection', *args, **kwargs)

    @staticmethod
    def APSMpSRDiagnoseInjectionDialog(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRDiagnoseInjectionDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckDCPS(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckDCPS', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckDCPSFamily(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckDCPSFamily', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckMPS(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckMPS', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckKickerPS(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckKickerPS', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckSeptumPS(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckSeptumPS', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckFlags(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckFlags', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckRfSystems(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckRfSystems', *args, **kwargs)

    @staticmethod
    def APSMpSRCheckValves(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCheckValves', *args, **kwargs)

    @staticmethod
    def APSMpCheckPVListValues(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCheckPVListValues', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckInjection(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckInjection', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckMode(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckMode', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckDCPS(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckDCPS', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckDCPSFamily(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckDCPSFamily', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckFlags(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckFlags', *args, **kwargs)

    @staticmethod
    def APSMpBTSCheckValves(*args, **kwargs):
        """
        Location: APSMpSRDiagnose.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSCheckValves', *args, **kwargs)

    @staticmethod
    def APSRemoveGzipExtension(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: filename
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveGzipExtension', *args, **kwargs)

    @staticmethod
    def APSStatusLine(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: widget args
        APS parsed args: ['variable', 'parent', 'width']

        """
        return exec_with_tcl('APSStatusLine', *args, **kwargs)

    @staticmethod
    def APSSetAllArrayEntries(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: arrayName value
        APS parsed args: None

        """
        return exec_with_tcl('APSSetAllArrayEntries', *args, **kwargs)

    @staticmethod
    def APSTmpString(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args:
        APS parsed args: None

        """
        return exec_with_tcl('APSTmpString', *args, **kwargs)

    @staticmethod
    def APSYesNoPopUp(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: ques
        APS parsed args: None

        """
        return exec_with_tcl('APSYesNoPopUp', *args, **kwargs)

    @staticmethod
    def APSErrorPopUp(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: message
        APS parsed args: None

        """
        return exec_with_tcl('APSErrorPopUp', *args, **kwargs)

    @staticmethod
    def APSMakeExitButton(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeExitButton', *args, **kwargs)

    @staticmethod
    def APSMakeLabeledEntries(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: widget labelText args
        APS parsed args: ['lwidth', 'ewidth', 'lanchor', 'eside', 'estate', 'erelief', 'fside']

        """
        return exec_with_tcl('APSMakeLabeledEntries', *args, **kwargs)

    @staticmethod
    def APSMakeLabeledOutputs(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: widget labelText args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeLabeledOutputs', *args, **kwargs)

    @staticmethod
    def APSUpdateUseLog(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: filename mode
        APS parsed args: None

        """
        return exec_with_tcl('APSUpdateUseLog', *args, **kwargs)

    @staticmethod
    def APSMakeSafeQualifierString(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: comment
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSafeQualifierString', *args, **kwargs)

    @staticmethod
    def APSMakeSafeQualifierStringForEval(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: comment
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSafeQualifierStringForEval', *args, **kwargs)

    @staticmethod
    def APSMakeSafeQualifierStringForEvalSddsplot(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: comment
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeSafeQualifierStringForEvalSddsplot', *args, **kwargs)

    @staticmethod
    def APSErrorReturn(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: code text
        APS parsed args: None

        """
        return exec_with_tcl('APSErrorReturn', *args, **kwargs)

    @staticmethod
    def APSGetErrorText(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSGetErrorText', *args, **kwargs)

    @staticmethod
    def APSTrimLeadingChars(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: args
        APS parsed args: ['character', 'text']

        """
        return exec_with_tcl('APSTrimLeadingChars', *args, **kwargs)

    @staticmethod
    def APSUnpackFile(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'unpackMode', 'unpackedFile']

        """
        return exec_with_tcl('APSUnpackFile', *args, **kwargs)

    @staticmethod
    def APSSetFACL(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: args
        APS parsed args: ['userList', 'filenameList']

        """
        return exec_with_tcl('APSSetFACL', *args, **kwargs)

    @staticmethod
    def APSSetACL(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: filename acls
        APS parsed args: None

        """
        return exec_with_tcl('APSSetACL', *args, **kwargs)

    @staticmethod
    def APSTmpDir(*args, **kwargs):
        """
        Location: mbutils.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSTmpDir', *args, **kwargs)

    @staticmethod
    def APSInfoDialog(*args, **kwargs):
        """
        Location: mbAPSInfoDialog.tcl
        Usage: APSInfoDialog widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string]
        [-width <width]
        [-infoMessage <string>]
        [-contextHelp <string>]
        [-default <string>]

        Creates	$parent$widget.
        	msg
        	buttonRow.ok.button
        	buttonRow.cancel.buttonTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'infoMessage', 'contextHelp', 'width', 'default']

        """
        return exec_with_tcl('APSInfoDialog', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialog(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
         Usage: APSFileSelectDialog widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string>]
        [-width <string>]
        [-checkValidity 0]
        [-path <string>] (path part of the filter)
        [-pattern <string> (pattern part of the filter)]
        [-title <string>]
        [-contextHelp <string]
        [-selectDir 1]
        [-reverseSort 1]
        TCL function args: widget args
        APS parsed args: ['parent', 'width', 'checkValidity', 'noPack', 'packOption', 'path', 'pattern', 'title', 'contextHelp', 'listDir', 'listFilter', 'modal', 'selectDir', 'reverseSort', 'labelname']

        """
        return exec_with_tcl('APSFileSelectDialog', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogBindings(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  f dirlb filelb s
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogBindings', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogFilter(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  dirlb filelb
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogFilter', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogList(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  dirlb filelb dir {files {}}
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogList', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogOK(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  dirlb filelb
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogOK', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogCancel(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogCancel', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogDoubleClick(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  mode dirlb filelb y
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogDoubleClick', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogClick(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  mode dirlb filelb y
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogClick', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogTake(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  mode dirlb filelb
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogTake', *args, **kwargs)

    @staticmethod
    def APSFileSelectDialogComplete(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args:  dirlb filelb
        APS parsed args: None

        """
        return exec_with_tcl('APSFileSelectDialogComplete', *args, **kwargs)

    @staticmethod
    def APSFileDisplayWindow(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        Usage: APSFileDisplayWindow widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-comment <string>]
        [-fileName <string>]
        [-deleteOnClose 1]
        [-width <string>]
        [-contextHelp <string]
        [-modal 1]
        [-printCommand <string>]
        [-font <string>]
        [-autoWidth 1]
        [-autoWidthLimit <integer>]

        Creates	$parent$widget.
        	userFrame
        	userFrame.file.text
        	buttonRow.close.button
        TCL function args: widget args
        APS parsed args: ['parent', 'comment', 'noPack', 'packOption', 'fileName', 'font', 'deleteOnClose', 'width', 'contextHelp', 'height', 'modal', 'printCommand', 'sddsExportableFile', 'defaultButtons', 'closeButton', 'okButton', 'cancelButton', 'okCommand', 'cancelCommand', 'autoWidth', 'autoWidthLimit']

        """
        return exec_with_tcl('APSFileDisplayWindow', *args, **kwargs)

    @staticmethod
    def APSCustomPrint(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'modal', 'widget', 'printCommand', 'font']

        """
        return exec_with_tcl('APSCustomPrint', *args, **kwargs)

    @staticmethod
    def APSCustomPrintDisableCommand(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('APSCustomPrintDisableCommand', *args, **kwargs)

    @staticmethod
    def APSCustomPrintDisablePageInput(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('APSCustomPrintDisablePageInput', *args, **kwargs)

    @staticmethod
    def APSProceedPrinting(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'font']

        """
        return exec_with_tcl('APSProceedPrinting', *args, **kwargs)

    @staticmethod
    def APSFileDisplayExport(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
        TCL function args: input
        APS parsed args: None

        """
        return exec_with_tcl('APSFileDisplayExport', *args, **kwargs)

    @staticmethod
    def APSRecentFileSelectDialog(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
         Usage: APSRecentFileSelectDialogHelp widget
        [-parent <string>]
        [-packOption <list>]
        [-width <string>]
        [-title <string>]
        [-contextHelp <string]
        TCL function args: widget args
        APS parsed args: ['parent', 'contextHelp', 'title', 'width', 'packOption']

        """
        return exec_with_tcl('APSRecentFileSelectDialog', *args, **kwargs)

    @staticmethod
    def APSAddToRecentFileList(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
         Usage: APSAddToRecentFileList
        [-filename <string>]
        [-limit <integer>]

        Add filenames to the list of
        recently selected files.
        TCL function args: args
        APS parsed args: ['filename', 'limit']

        """
        return exec_with_tcl('APSAddToRecentFileList', *args, **kwargs)

    @staticmethod
    def APSGetRecentFileList(*args, **kwargs):
        """
        Location: APSFileSelect.tcl
         Usage: APSGetRecentFileList

        Returns a list of recently
        selected files.
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetRecentFileList', *args, **kwargs)

    @staticmethod
    def APSMakeDateEntryWidget(*args, **kwargs):
        """
        Location: DateEntry.tcl
        TCL function args: widget args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeDateEntryWidget', *args, **kwargs)

    @staticmethod
    def APSDateEntry(*args, **kwargs):
        """
        Location: DateEntry.tcl
        Usage: APSDateEntry widget -parent name

        	[-label string]
        	[-dayVariable name]

        	[-monthVariable name]
        	[-yearVariable name]

        	[-twoDigitYear 0|1]
        	[-leadingZeros 0|1]TCL function args: widget args
        APS parsed args: ['parent', 'dayVariable', 'yearVariable', 'monthVariable', 'label', 'twoDigitYear', 'leadingZeros', 'packOption']

        """
        return exec_with_tcl('APSDateEntry', *args, **kwargs)

    @staticmethod
    def APSMakeDateTimeEntryWidget(*args, **kwargs):
        """
        Location: DateEntry.tcl
        TCL function args: widget args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeDateTimeEntryWidget', *args, **kwargs)

    @staticmethod
    def APSDateTimeEntry(*args, **kwargs):
        """
        Location: DateEntry.tcl
        Usage: APSDateEntry widget -parent name

        	[-label string]
        	[-dayVariable name]

        	[-monthVariable name]
        	[-yearVariable name]

        	[-hourVariable name]

        	[-twoDigitYear 0|1]
        	[-leadingZeros 0|1]TCL function args: widget args
        APS parsed args: ['parent', 'dayVariable', 'yearVariable', 'monthVariable', 'hourVariable', 'label', 'twoDigitYear', 'leadingZeros', 'packOption']

        """
        return exec_with_tcl('APSDateTimeEntry', *args, **kwargs)

    @staticmethod
    def APSMakeYearMonthEntryWidget(*args, **kwargs):
        """
        Location: DateEntry.tcl
        TCL function args: widget args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeYearMonthEntryWidget', *args, **kwargs)

    @staticmethod
    def APSYearMonthEntry(*args, **kwargs):
        """
        Location: DateEntry.tcl
        Usage: APSYearMonthEntry widget -parent name

        	[-label string]

        	[-monthVariable name]
        	[-yearVariable name]

        	[-twoDigitYear 0|1]
        	[-leadingZeros 0|1]TCL function args: widget args
        APS parsed args: ['parent', 'yearVariable', 'monthVariable', 'label', 'twoDigitYear', 'leadingZeros']

        """
        return exec_with_tcl('APSYearMonthEntry', *args, **kwargs)

    @staticmethod
    def APSDateTimeAdjEntry(*args, **kwargs):
        """
        Location: DateEntry.tcl
        Usage: APSDateTimeAdjEntry widget -parent name
        	[-dayVariable name]

        	[-monthVariable name]
        	[-yearVariable name]

        	[-hourVariable name]
        	[-parent name]
        	[-label string]

        	[-defaultHour number]
        	[-command string]
        	[-twoDigitYear 0|1]TCL function args: widget args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSDateTimeAdjEntry', *args, **kwargs)

    @staticmethod
    def APSGetSDDSColumn(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSColumn
        [-fileName <string>]
        [-sddsFD <fd>]
        [-column <string>]
        [-page <string>]

        Extracts column from sdds file and returns it as a tcl list. File may be specified with explicit path using -fileName, or given as an <fd> from a "sdds open" call. The latter being much more efficient for repeated accesses.TCL function args: args
        APS parsed args: ['fileName', 'column', 'page', 'sddsFD']

        """
        return exec_with_tcl('APSGetSDDSColumn', *args, **kwargs)

    @staticmethod
    def APSGetSDDSParameter(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSParameter
        [-fileName <string>]
        [-sddsFD <fd>]
        [-parameter <string>]
        [-page <string>]

        Extracts parameter from sdds file and returns it. File may be specified with explicit path using -fileName, or given as an <fd> from a "sdds open" call. The latter being much more efficient for repeated accesses.TCL function args: args
        APS parsed args: ['fileName', 'parameter', 'page', 'sddsFD']

        """
        return exec_with_tcl('APSGetSDDSParameter', *args, **kwargs)

    @staticmethod
    def APSGetSDDSNames(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSNames
        [-fileName <string>]
        [-sddsFD <fd>]
        [-class <string>] where <string> is column (default), parameter, or array.

        Extracts data names by class from an sdds file
        and returns it as a tcl list. File may be specified with explicit path using -fileName, or given as an <fd> from a "sdds open" call. The latter being much more efficient for repeated accesses. TCL function args: args
        APS parsed args: ['fileName', 'class', 'sddsFD']

        """
        return exec_with_tcl('APSGetSDDSNames', *args, **kwargs)

    @staticmethod
    def APSCheckSDDSFile(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSCheckSDDSFile
        [-fileName <string>]

        Verify that given fileName is an SDDS1 file.
        Returns 1 if true, 0 otherwise.TCL function args: args
        APS parsed args: ['fileName']

        """
        return exec_with_tcl('APSCheckSDDSFile', *args, **kwargs)

    @staticmethod
    def APSGetSDDSColumns(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSColumns -fileName <string> -columnList <list> -variableList <list>
         Puts column data from an SDDS file for a series of columns into a series of variables.TCL function args: args
        APS parsed args: ['fileName', 'columnList', 'variableList']

        """
        return exec_with_tcl('APSGetSDDSColumns', *args, **kwargs)

    @staticmethod
    def APSGetSDDSColumnOld(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'column', 'page']

        """
        return exec_with_tcl('APSGetSDDSColumnOld', *args, **kwargs)

    @staticmethod
    def APSGetSDDSParameterOld(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'parameter', 'page']

        """
        return exec_with_tcl('APSGetSDDSParameterOld', *args, **kwargs)

    @staticmethod
    def APSGetSDDSNamesOld(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'class']

        """
        return exec_with_tcl('APSGetSDDSNamesOld', *args, **kwargs)

    @staticmethod
    def APSGetSDDSRowCount(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSRowCount
        [-fileName <string>]
        [-sddsFD <fd>]
        [-page <integer>]

        Counts the rows in each page of the sdds file and returns it as a tcl list. If the page option is given, it returns the number of rows in that page only.TCL function args:  args
        APS parsed args: ['fileName', 'page', 'sddsFD']

        """
        return exec_with_tcl('APSGetSDDSRowCount', *args, **kwargs)

    @staticmethod
    def APSSDDSCheck(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSSDDSCheck
        [-fileName <string>]
        [-sddsFD <fd>]
        [-printErrors 1]

        Determines if the sdds file has been corrupted. It reads the entire file and prints a message. If the file is ok, "ok" is printed. If the file has a problem "corrupted" is printed. If -printErrors is used, the first error message will be returned.TCL function args:  args
        APS parsed args: ['fileName', 'printErrors', 'sddsFD']

        """
        return exec_with_tcl('APSSDDSCheck', *args, **kwargs)

    @staticmethod
    def APSSDDSCollapse(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSSDDSCollapse
        [-inputFileName <string>]
        [-outputFileName <string>]
        [-sddsInputFD <fd>]
        [-sddsOutputFD <fd>]

        Reads data pages from the input sdds file and writes a new sdds file containing a single data page. This data page contains the parameters, with each parameter forming a column of the tabular data.TCL function args:  args
        APS parsed args: ['inputFileName', 'outputFileName', 'sddsInputFD', 'sddsOutputFD']

        """
        return exec_with_tcl('APSSDDSCollapse', *args, **kwargs)

    @staticmethod
    def APSSDDSExpand(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSSDDSExpand
        [-inputFileName <string>]
        [-outputFileName <string>]
        [-sddsInputFD <fd>]
        [-sddsOutputFD <fd>]
        [-noWarnings 1]

        All columns in the input file are turned into parameters in the output file. For each row of each page in the input file, APSSDDSExpand creates a new page with parameter values equal to the column values for that page and row.TCL function args:  args
        APS parsed args: ['inputFileName', 'outputFileName', 'sddsInputFD', 'sddsOutputFD', 'noWarnings']

        """
        return exec_with_tcl('APSSDDSExpand', *args, **kwargs)

    @staticmethod
    def APSSDDSConvert(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSSDDSConvert
        [-inputFileName <string>]
        [-outputFileName <string>]
        [-sddsInputFD <fd>]
        [-sddsOutputFD <fd>]
        [-dataMode {ascii | binary}]
        [-fromPage <integer>]
        [-toPage <integer>]
        [-recover {1 | clip}]
        [-delete {column | parameter | array},<matching-string>[,...]]
        [-retain {column | parameter | array},<matching-string>[,...]]
        [-rename {column | parameter | array},<oldname>=<newname>[,...]]
        [-editNames {column | parameter | array},<wildcard-string>,<edit-string>]
        [-acceptAllNames 1]

        Converts sdds files between ascii and binary, and allows wildcard-based filtering-out of unwanted columns and rows. Any column or parameter matched by a deletion string is deleted unless it is matched by a retention string. The acceptAllNames option may be used to force the SDDS library to accept element names that have spaces and other normally unacceptable characters.TCL function args:  args
        APS parsed args: ['inputFileName', 'outputFileName', 'sddsInputFD', 'sddsOutputFD', 'dataMode', 'fromPage', 'toPage', 'recover', 'delete', 'retain', 'rename', 'editNames', 'acceptAllNames']

        """
        return exec_with_tcl('APSSDDSConvert', *args, **kwargs)

    @staticmethod
    def APSGetSDDSUnits(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
        Usage: APSGetSDDSUnits
        [-fileName <string>]
        [-sddsFD <fd>]
        [-class <string>] where <string> is column (default), parameter, or array.

        Extracts data units by class from an sdds file
        and returns it as a tcl list. File may be specified with explicit path using -fileName, or given as an <fd> from a "sdds open" call. The latter being much more efficient for repeated accesses. TCL function args: args
        APS parsed args: ['fileName', 'class', 'sddsFD']

        """
        return exec_with_tcl('APSGetSDDSUnits', *args, **kwargs)

    @staticmethod
    def APSProcessLogOnChangeData(*args, **kwargs):
        """
        Location: APSSDDSdata.tcl
         Usage: APSProcessLogOnChangeData
        -inputFile <string>]
        [-outputFile <string>]

        Inserts extra data points directly
        before changes are logged. This
        makes it easier to plot the data.
        TCL function args: args
        APS parsed args: ['inputFile', 'outputFile']

        """
        return exec_with_tcl('APSProcessLogOnChangeData', *args, **kwargs)

    @staticmethod
    def APSTabFrame(*args, **kwargs):
        """
        Location: APSTabFrame.tcl
        Usage: APSTabFrame <widget>
         -parent <widget>
         -labelList <listOfStrings>
         -width <pixels>
         -height <pixels>
         [-noPack 0|1]
         [-packOption <string>]
         [-label <string>]
         [-frameIndexVariable <name>]
         [-commandList <listOfStrings>]
         [-tabPosition n|s|e|w]
         [-font <fontName>]
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'width', 'height', 'labelList', 'commandList', 'tabPosition', 'font', 'frameIndexVariable']

        """
        return exec_with_tcl('APSTabFrame', *args, **kwargs)

    @staticmethod
    def APSTabFrameChanged(*args, **kwargs):
        """
        Location: APSTabFrame.tcl
        TCL function args: widget commandList
        APS parsed args: None

        """
        return exec_with_tcl('APSTabFrameChanged', *args, **kwargs)

    @staticmethod
    def APSMaxStringLength(*args, **kwargs):
        """
        Location: SDDSListBox.tcl
        Usage: APSMaxStringLength <list>TCL function args: stringList
        APS parsed args: None

        """
        return exec_with_tcl('APSMaxStringLength', *args, **kwargs)

    @staticmethod
    def APSSDDSListboxDefaultLabelMaker(*args, **kwargs):
        """
        Location: SDDSListBox.tcl
        TCL function args: args
        APS parsed args: ['dataList', 'widthList']

        """
        return exec_with_tcl('APSSDDSListboxDefaultLabelMaker', *args, **kwargs)

    @staticmethod
    def APSSDDSListbox(*args, **kwargs):
        """
        Location: SDDSListBox.tcl
        Usage: APSSDDSListbox <widget> -fileName <fileName> [-parent <parent>]  [-label <string>] [-page <page>] [-page <page>] [-labelMaker <procName>] [-callback <procName>]  [-columnList <list>] [-doneButton 0|1] [-height <number>] [-widthLimit <number>]TCL function args: widget args
        APS parsed args: ['fileName', 'parent', 'page', 'labelMaker', 'callback', 'columnList', 'contextHelp', 'arrayName', 'doneButton', 'height', 'label', 'buttonSize', 'widthLimit', 'trim', 'packOption', 'selectMode', 'labelFont']

        """
        return exec_with_tcl('APSSDDSListbox', *args, **kwargs)

    @staticmethod
    def APSSDDSListboxRunCallback(*args, **kwargs):
        """
        Location: SDDSListBox.tcl
        TCL function args: widget args
        APS parsed args: ['callback', 'y']

        """
        return exec_with_tcl('APSSDDSListboxRunCallback', *args, **kwargs)

    @staticmethod
    def APSSRCollectTrippedBeamHistories(*args, **kwargs):
        """
        Location: APSMpGetBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['namePrefix', 'nameSuffix', 'statusCallback', 'useStopOnFull', 'forceAll', 'doGzip', 'minimalData']

        """
        return exec_with_tcl('APSSRCollectTrippedBeamHistories', *args, **kwargs)

    @staticmethod
    def APSSRSetFifoFillModes(*args, **kwargs):
        """
        Location: APSMpGetBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['mode', 'BPMList']

        """
        return exec_with_tcl('APSSRSetFifoFillModes', *args, **kwargs)

    @staticmethod
    def APSSRSetFifoResync(*args, **kwargs):
        """
        Location: APSMpGetBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['state', 'BPMList']

        """
        return exec_with_tcl('APSSRSetFifoResync', *args, **kwargs)

    @staticmethod
    def APSSRGetTrippedBPLDList(*args, **kwargs):
        """
        Location: APSMpGetBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['forceAll']

        """
        return exec_with_tcl('APSSRGetTrippedBPLDList', *args, **kwargs)

    @staticmethod
    def APSSRGetTrippedBeamHistory(*args, **kwargs):
        """
        Location: APSMpGetBeamHistory.tcl
        TCL function args: args
        APS parsed args: ['sector', 'BPMNumber', 'BPMName', 'namePrefix', 'nameSuffix', 'doGzip', 'minimalData']

        """
        return exec_with_tcl('APSSRGetTrippedBeamHistory', *args, **kwargs)

    @staticmethod
    def APSSRAllSCDUCheckout(*args, **kwargs):
        """
        Location: SRSCDUCheckout.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'statusCallback']

        """
        return exec_with_tcl('APSSRAllSCDUCheckout', *args, **kwargs)

    @staticmethod
    def APSSRSCDUCheckout(*args, **kwargs):
        """
        Location: SRSCDUCheckout.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'family', 'sectorList', 'statusCallback']

        """
        return exec_with_tcl('APSSRSCDUCheckout', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrectorInitInfo(*args, **kwargs):
        """
        Location: BCorrSetInit.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrectorInitInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrectorInitDialog(*args, **kwargs):
        """
        Location: BCorrSetInit.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrectorInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrectorInit(*args, **kwargs):
        """
        Location: BCorrSetInit.tcl
        TCL function args: args
        APS parsed args: ['selection']

        """
        return exec_with_tcl('APSMpBoosterSetCorrectorInit', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrectorInitNormal(*args, **kwargs):
        """
        Location: BCorrSetInit.tcl
        TCL function args: args
        APS parsed args: ['selection', 'loadAdl']

        """
        return exec_with_tcl('APSMpBoosterSetCorrectorInitNormal', *args, **kwargs)

    @staticmethod
    def APSMpBoosterLoadCorrectorRampsInfo(*args, **kwargs):
        """
        Location: BCorrLoadRamps.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterLoadCorrectorRampsInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterLoadCorrectorRampsDialog(*args, **kwargs):
        """
        Location: BCorrLoadRamps.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterLoadCorrectorRampsDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterLoadCorrectorRamps(*args, **kwargs):
        """
        Location: BCorrLoadRamps.tcl
        TCL function args: args
        APS parsed args: ['loadAdl', 'lattice']

        """
        return exec_with_tcl('APSMpBoosterLoadCorrectorRamps', *args, **kwargs)

    @staticmethod
    def APSMpBoosterLoadCorrectorRampsNormal(*args, **kwargs):
        """
        Location: BCorrLoadRamps.tcl
        TCL function args: args
        APS parsed args: ['selection', 'filename', 'loadAdl']

        """
        return exec_with_tcl('APSMpBoosterLoadCorrectorRampsNormal', *args, **kwargs)

    @staticmethod
    def APSMpBoosterCheckCorrectorRampTable(*args, **kwargs):
        """
        Location: BCorrLoadRamps.tcl
        TCL function args: args
        APS parsed args: ['BoosterLattice']

        """
        return exec_with_tcl('APSMpBoosterCheckCorrectorRampTable', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrPowerSuppliesOnOffInfo(*args, **kwargs):
        """
        Location: BCorrSetSuppliesOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrPowerSuppliesOnOffInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrPowerSuppliesOnOffDialog(*args, **kwargs):
        """
        Location: BCorrSetSuppliesOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSetCorrPowerSuppliesOnOffDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrPowerSuppliesOnOff(*args, **kwargs):
        """
        Location: BCorrSetSuppliesOnOff.tcl
        TCL function args: args
        APS parsed args: ['state1', 'selection', 'Fast', 'RawOnly']

        """
        return exec_with_tcl('APSMpBoosterSetCorrPowerSuppliesOnOff', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrPowerSuppliesOnOffNormal(*args, **kwargs):
        """
        Location: BCorrSetSuppliesOnOff.tcl
        TCL function args: args
        APS parsed args: ['state1', 'selection', 'Fast', 'RawOnly']

        """
        return exec_with_tcl('APSMpBoosterSetCorrPowerSuppliesOnOffNormal', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSetCorrPowerSuppliesOnOffZero(*args, **kwargs):
        """
        Location: BCorrSetSuppliesOnOff.tcl
        TCL function args: args
        APS parsed args: ['selection']

        """
        return exec_with_tcl('APSMpBoosterSetCorrPowerSuppliesOnOffZero', *args, **kwargs)

    @staticmethod
    def APSRunControlInit(*args, **kwargs):
        """
        Location: APSRunControl.tcl
        Usage: APSRunControlInit [-pv <runcontrolpv>] [-description <string>]
        	[-timeout <ms>]
        Initializes runcontrol session, preventing access by others.
        Returns RUNCONTROL_OK if successful, catchable error otherwise:
        RUNCONTROL_DENIED - someone else is running
        RUNCONTROL_ERROR - unable to access runcontrol recordTCL function args: args
        APS parsed args: ['pv', 'description', 'timeout']

        """
        return exec_with_tcl('APSRunControlInit', *args, **kwargs)

    @staticmethod
    def APSRunControlPing(*args, **kwargs):
        """
        Location: APSRunControl.tcl
        Usage: APSRunControlPing
        Pings runcontrol record to keep it from timing out. Checks for abort and
        suspend. This procedure will block if runcontrol record is suspended,
        although the tcl event loop will still be serviced.
        Returns RUNCONTROL_OK if successful, catchable error otherwise:
        RUNCONTROL_TIMEOUT - runcontrol record not pinged within timeout
        RUNCONTROL_ABORT - runcontrol record is requesting that you exit
        RUNCONTROL_ERROR - unable to access runcontrol recordTCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRunControlPing', *args, **kwargs)

    @staticmethod
    def APSRunControlLogMessage(*args, **kwargs):
        """
        Location: APSRunControl.tcl
        Usage: APSRunControlLogMessage [-message <string>] [-severity <integer>]
        Where <integer> corresponds to EPICS alarm severities
        0 - NO_ALARM
        1 - MINOR_ALARM
        2 - MAJOR_ALARM
        3 - INVALID_ALARM
        Returns RUNCONTROL_OK if successful, catchable error otherwise:
        RUNCONTROL_ERROR - unable to access runcontrol recordTCL function args: args
        APS parsed args: ['message', 'severity']

        """
        return exec_with_tcl('APSRunControlLogMessage', *args, **kwargs)

    @staticmethod
    def APSRunControlExit(*args, **kwargs):
        """
        Location: APSRunControl.tcl
        Usage: APSRunControlExit
        Cleans up open runcontrol session
        Returns RUNCONTROL_OK if successful, catchable error otherwise:
        RUNCONTROL_ERROR - unable to access runcontrol recordTCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRunControlExit', *args, **kwargs)

    @staticmethod
    def APSScrolledText(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrolledText widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-width <string>]
        [-height <string>]
        [-name <string>]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	text
        	scroll
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'width', 'height', 'name', 'contextHelp', 'font']

        """
        return exec_with_tcl('APSScrolledText', *args, **kwargs)

    @staticmethod
    def APSScrolledList(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrolledList widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-height <string>]
        [-name <string>]
        [-itemList <list>]
        [-listvar <listvar>]
        [-callback <proc>] note: procedure must be <proc> listboxItem doubleClick
        [-contextHelp <string>]
        [-selectMode <mode>]
        [-xscroll <1|0>]

        Creates	$parent$widget.
        	listbox
        	scroll
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'height', 'name', 'callback', 'itemList', 'listvar', 'contextHelp', 'selectMode', 'width', 'xscroll']

        """
        return exec_with_tcl('APSScrolledList', *args, **kwargs)

    @staticmethod
    def APSUpdateScrolledSelectionVar(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: listbox selectionVar args
        APS parsed args: None

        """
        return exec_with_tcl('APSUpdateScrolledSelectionVar', *args, **kwargs)

    @staticmethod
    def APSScrolledListWindowCb(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: listbox script
        APS parsed args: None

        """
        return exec_with_tcl('APSScrolledListWindowCb', *args, **kwargs)

    @staticmethod
    def APSScrolledListWindow(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrolledListWindow widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-height <string>]
        [-name <string>]
        [-label <string>]
        [-itemList <list>]
        [-listvar <listvar>]
        [-selectionVar <string>]
        [-callback <script>]
        [-contextHelp <string>]
        [-autoAccept 1]
        [-closeButton 0]
        [-clearButton 1]
        [-clearCommand <string>]
        [-acceptButton 0]
        [-printButton 1][-emailButton 1]
        [-selectMode <mode>]

        Creates	$parent$widget.
        	userFrame
        	userFrame.sl.listbox
        	buttonRow.close.button
        	buttonRow.accept.buttonTCL function args: widget args
        APS parsed args: ['parent', 'name', 'label', 'noPack', 'packOption', 'itemList', 'listvar', 'selectionVar', 'height', 'callback', 'contextHelp', 'autoAccept', 'closeButton', 'clearButton', 'acceptButton', 'selectMode', 'clearCommand', 'printButton', 'selectAllButton', 'mouseClickCallback', 'emailButton', 'descriptionName', 'appendDescription', 'directory', 'rootnameOnly']

        """
        return exec_with_tcl('APSScrolledListWindow', *args, **kwargs)

    @staticmethod
    def APSAppendFileDescriptionToScrolledList(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: arrayIndex listWidget rootnameOnly descriptionName descDir
        APS parsed args: None

        """
        return exec_with_tcl('APSAppendFileDescriptionToScrolledList', *args, **kwargs)

    @staticmethod
    def APSScrolledListWindowPrint(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: args
        APS parsed args: ['widget', 'dialog']

        """
        return exec_with_tcl('APSScrolledListWindowPrint', *args, **kwargs)

    @staticmethod
    def APSScrolledListWindowEMail(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: args
        APS parsed args: ['widget']

        """
        return exec_with_tcl('APSScrolledListWindowEMail', *args, **kwargs)

    @staticmethod
    def APSScroll(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScroll widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string>]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	frame.canvas
        	frame.yscroll
        	frame.canvas.frame

        Returns $parent$widget.frame.canvas.frame into which you pack widgets
        to be scrolled. Then call "APSScrollAdjust $parent$widget"
        to configure scrolling.

        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'contextHelp']

        """
        return exec_with_tcl('APSScroll', *args, **kwargs)

    @staticmethod
    def APSScrollAdjust(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrollAdjust widget
        [-numVisible <string>]
        [-scrollIncrement <string>]

        Widget given must be the base widget from APSScroll ($parent$widget).
        Adjusts the canvas and scrolling parameters to do something reasonable with
        the widgets you have packed into the scrolled frame. In general, it is
        assumed you have packed homogenous widgets, in which case -numVisible
        determines how many you will see at a time. Scrolling is set up to jump in
        increments of one widget.

        TCL function args: widget args
        APS parsed args: ['numVisible', 'scrollIncrement']

        """
        return exec_with_tcl('APSScrollAdjust', *args, **kwargs)

    @staticmethod
    def APSScrolledStatus(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrolledStatus widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-textVariable <string>]
        [-width <string>]
        [-height <string>]
        [-withButtons 1]
        [-name <string>]
        [-contextHelp <string>]
        [-lineLimit <number>]
        [-label <string>]
        [-busyIndicator 0]

        Creates	$parent$widget.
        	frame.text
        	frame.scroll
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'textVariable', 'width', 'height', 'withButtons', 'contextHelp', 'lineLimit', 'label', 'busyIndicator']

        """
        return exec_with_tcl('APSScrolledStatus', *args, **kwargs)

    @staticmethod
    def APSExpandScrolledDialog(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: args
        APS parsed args: ['textVariable', 'textWidget', 'width']

        """
        return exec_with_tcl('APSExpandScrolledDialog', *args, **kwargs)

    @staticmethod
    def APSScrolledTextEMail(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSScrolledTextEMail -textWidget <name> [-width <number>] [-modal 1]
        TCL function args: args
        APS parsed args: ['textWidget', 'width', 'modal']

        """
        return exec_with_tcl('APSScrolledTextEMail', *args, **kwargs)

    @staticmethod
    def APSScrolledStatusUpdate(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: varName index op
        APS parsed args: None

        """
        return exec_with_tcl('APSScrolledStatusUpdate', *args, **kwargs)

    @staticmethod
    def APSListSelectDialogCallback(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        TCL function args: widget item doubleClick
        APS parsed args: None

        """
        return exec_with_tcl('APSListSelectDialogCallback', *args, **kwargs)

    @staticmethod
    def APSListSelectDialog(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSListSelectDialog widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-height <string>]
        [-name <string>]
        [-itemList <list>]
        [-contextHelp <string>]

        TCL function args: widget args
        APS parsed args: ['itemList', 'name', 'parent', 'height', 'noPack', 'packOption', 'contextHelp', 'selectMode']

        """
        return exec_with_tcl('APSListSelectDialog', *args, **kwargs)

    @staticmethod
    def APSChooseItemFromList(*args, **kwargs):
        """
        Location: APSScrolled.tcl
        Usage: APSChooseItemFromList
        [-name <string>]
        [-itemList <list>][-returnList <list>
        [-returnIndices 0]
        [-multiItem 1][
        [-contextHelp <string>]

        TCL function args: args
        APS parsed args: ['itemList', 'name', 'contextHelp', 'height', 'multiItem', 'returnList', 'returnIndices']

        """
        return exec_with_tcl('APSChooseItemFromList', *args, **kwargs)

    @staticmethod
    def APSSRReadBunchCM(*args, **kwargs):
        """
        Location: SRBunchCurrent.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRReadBunchCM', *args, **kwargs)

    @staticmethod
    def APSSRMakeTargetFillPattern(*args, **kwargs):
        """
        Location: SRBunchCurrent.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRMakeTargetFillPattern', *args, **kwargs)

    @staticmethod
    def APSSRReadBunchCMTurnByTurn(*args, **kwargs):
        """
        Location: SRBunchCurrent.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRReadBunchCMTurnByTurn', *args, **kwargs)

    @staticmethod
    def APSSubmitFileToICMS(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSSubmitFileToICMS
         -dDocTitle <title>
         -xDocAuthor <authors>
         -xTopicLevel3 <category>
         -xTopicLevel4 <subcategory>
         -xComments <comments>
         -xDocDate <date>
         -xDivision <division>
         -xGroup <group>
         -primaryFile <filename>
         -icmsPassword <string>
         -icmsUsername <string>
         -dRevLabel <revision number>
         -dDocAccount <security account>
         -dSecurityGroup <security group>
         You can use APSPromptSTDINforICMSinfo to prompt the user for the values to the various arguments first.TCL function args: args
        APS parsed args: ['dDocAccount', 'dDocAuthor', 'dDocName', 'dDocTitle', 'dDocType', 'dRevLabel', 'dSecurityGroup', 'icmsUsername', 'icmsPassword', 'primaryFile', 'returnURL', 'xComments', 'xDocAuthor', 'xDocDate', 'xDivision', 'xGroup', 'xProject', 'xTopicLevel1', 'xTopicLevel2', 'xTopicLevel3', 'xTopicLevel4']

        """
        return exec_with_tcl('APSSubmitFileToICMS', *args, **kwargs)

    @staticmethod
    def APSGetValidICMSSecurityGroups(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSGetValidICMSSecurityGroups
         -icmsUsername <string>
         -icmsPassword <string>
         Returns a list of valid security groups.TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword']

        """
        return exec_with_tcl('APSGetValidICMSSecurityGroups', *args, **kwargs)

    @staticmethod
    def APSGetValidICMSSecurityAccounts(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSGetValidICMSSecurityAccounts
         -icmsUsername <string>
         -icmsPassword <string>
         Returns a list of valid security accounts.TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword']

        """
        return exec_with_tcl('APSGetValidICMSSecurityAccounts', *args, **kwargs)

    @staticmethod
    def APSGetValidICMSTechReportCategories(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSGetValidICMSTechReportCategories
         Returns a list of valid ICMS categories.TCL function args: args
        APS parsed args: ['xDivision', 'xGroup']

        """
        return exec_with_tcl('APSGetValidICMSTechReportCategories', *args, **kwargs)

    @staticmethod
    def APSGetValidICMSTechReportSubCategories(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSGetValidICMSTechReportCategories
        	-category <string>
         Returns a list of valid ICMS sub-categories.TCL function args: args
        APS parsed args: ['xDivision', 'xGroup', 'category']

        """
        return exec_with_tcl('APSGetValidICMSTechReportSubCategories', *args, **kwargs)

    @staticmethod
    def APSPromptSTDINforICMSinfo(*args, **kwargs):
        """
        Location: APSICMS.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPromptSTDINforICMSinfo', *args, **kwargs)

    @staticmethod
    def APSICMSTechReportToSDDS(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSTechReportToSDDS
         -xDivision <division>
         -xGroup <group>
         -icmsPassword <string>
         -icmsUsername <string>
         -fileName <output>
         TCL function args: args
        APS parsed args: ['xDivision', 'xGroup', 'icmsUsername', 'icmsPassword', 'fileName']

        """
        return exec_with_tcl('APSICMSTechReportToSDDS', *args, **kwargs)

    @staticmethod
    def APSICMSUpdateDocInfoFromSDDS(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSUpdateDocInfoFromSDDS
         -icmsPassword <string>
         -icmsUsername <string>
         -fileName <input>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'fileName', 'verbose']

        """
        return exec_with_tcl('APSICMSUpdateDocInfoFromSDDS', *args, **kwargs)

    @staticmethod
    def APSICMSQueryDocNameAndRevision(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSQueryDocNameAndRevision
         -dDocTitle <title>
         -dDocType <type>
         -xComments <comments>
         -xDivision <division>
         -xGroup <group>
         -icmsPassword <string>
         -icmsUsername <string>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'dDocTitle', 'dDocType', 'xComments', 'xDivision', 'xGroup']

        """
        return exec_with_tcl('APSICMSQueryDocNameAndRevision', *args, **kwargs)

    @staticmethod
    def APSICMSQueryRevisionNumber(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSQueryRevisionNumber
         -dDocName <ICMS number>
         -icmsPassword <string>
         -icmsUsername <string>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'dDocName']

        """
        return exec_with_tcl('APSICMSQueryRevisionNumber', *args, **kwargs)

    @staticmethod
    def APSICMSQueryVaultFileSize(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSQueryVaultFileSize
         -dDocName <ICMS ID Number>
         -dRevLabel <revision>
         -icmsPassword <string>
         -icmsUsername <string>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'dDocName', 'dRevLabel']

        """
        return exec_with_tcl('APSICMSQueryVaultFileSize', *args, **kwargs)

    @staticmethod
    def APSICMSQueryTopicLevels(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSQueryTopicLevels
         -dDocName <ICMS ID Number>
         -dRevLabel <revision>
         -icmsPassword <string>
         -icmsUsername <string>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'dDocName', 'dRevLabel']

        """
        return exec_with_tcl('APSICMSQueryTopicLevels', *args, **kwargs)

    @staticmethod
    def APSICMSDocInfoToSDDS(*args, **kwargs):
        """
        Location: APSICMS.tcl
        Usage: APSICMSDocInfoToSDDS
         -dDocName <ICMS ID Number>
         -dRevLabel <revision>
         -icmsPassword <string>
         -icmsUsername <string>
         -fileName <output>
         TCL function args: args
        APS parsed args: ['icmsUsername', 'icmsPassword', 'dDocName', 'dRevLabel', 'fileName']

        """
        return exec_with_tcl('APSICMSDocInfoToSDDS', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDElementSetup(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDElementSetup', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDSetupGlobalVars(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDSetupGlobalVars', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDSetupGUI(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDSetupGUI', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDSetStatus(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: text
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDSetStatus', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDAddPhotonBand(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: ['low', 'high', 'on']

        """
        return exec_with_tcl('APSChooseBestMBAIDAddPhotonBand', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDRunSearch(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDRunSearch', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDReplot(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: tag
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDReplot', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDSavePlots(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: tag
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDSavePlots', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDFindRelevantFiles(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDFindRelevantFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDFindBestFiles(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: ['dataFileList', 'rootname']

        """
        return exec_with_tcl('APSChooseBestMBAIDFindBestFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDFindDataFiles(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: ['dataDirectory', 'straightType', 'feType', 'current', 'gap', 'periodOption', 'type', 'maximumLength', 'periodMin', 'periodMax', 'periodFrac']

        """
        return exec_with_tcl('APSChooseBestMBAIDFindDataFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDFindScuDataFiles(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: ['dataDirectory', 'straightType', 'feType', 'current', 'gap', 'maximumLength', 'periodMin', 'periodMax', 'periodFrac']

        """
        return exec_with_tcl('APSChooseBestMBAIDFindScuDataFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDLatexHeader(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDLatexHeader', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDLatexFooter(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDLatexFooter', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDLatexImage(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: filename
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDLatexImage', *args, **kwargs)

    @staticmethod
    def APSChooseBestMBAIDLatexCalcValues(*args, **kwargs):
        """
        Location: chooseBestMBAID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestMBAIDLatexCalcValues', *args, **kwargs)

    @staticmethod
    def TogglePulsedMagnetEnables(*args, **kwargs):
        """
        Location: timingResets.tcl
        TCL function args: args
        APS parsed args: ['location']

        """
        return exec_with_tcl('TogglePulsedMagnetEnables', *args, **kwargs)

    @staticmethod
    def SetPulsedMagnetEnables(*args, **kwargs):
        """
        Location: timingResets.tcl
        TCL function args: args
        APS parsed args: ['location', 'state']

        """
        return exec_with_tcl('SetPulsedMagnetEnables', *args, **kwargs)

    @staticmethod
    def APSMpRestoreScalarCorrectorsInfo(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreScalarCorrectorsInfo', *args, **kwargs)

    @staticmethod
    def APSMpRestoreScalarCorrectors(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreScalarCorrectors', *args, **kwargs)

    @staticmethod
    def APSOpenRTFBLoops(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSOpenRTFBLoops', *args, **kwargs)

    @staticmethod
    def APSZeroRTBPMSetpoints(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSZeroRTBPMSetpoints', *args, **kwargs)

    @staticmethod
    def APSReadExecuteParamFile(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: ['filename', 'readonly']

        """
        return exec_with_tcl('APSReadExecuteParamFile', *args, **kwargs)

    @staticmethod
    def APSMpRestoreScalarCorrectorsInitDialog(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreScalarCorrectorsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpCloseRTFBLoops(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSMpCloseRTFBLoops', *args, **kwargs)

    @staticmethod
    def APSVerifyCorrectorModeSwitches(*args, **kwargs):
        """
        Location: APSMpRestoreScalarCorrectors.tcl
        TCL function args: args
        APS parsed args: ['wrongMode', 'plane']

        """
        return exec_with_tcl('APSVerifyCorrectorModeSwitches', *args, **kwargs)

    @staticmethod
    def getbres(*args, **kwargs):
        """
        Location: bresponse.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('getbres', *args, **kwargs)

    @staticmethod
    def plotbres(*args, **kwargs):
        """
        Location: bresponse.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('plotbres', *args, **kwargs)

    @staticmethod
    def makebresponse(*args, **kwargs):
        """
        Location: bresponse.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebresponse', *args, **kwargs)

    @staticmethod
    def makeplotbresnames(*args, **kwargs):
        """
        Location: bresponse.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makeplotbresnames', *args, **kwargs)

    @staticmethod
    def baverager(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('baverager', *args, **kwargs)

    @staticmethod
    def bbpmduration(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('bbpmduration', *args, **kwargs)

    @staticmethod
    def bbpmtime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('bbpmtime', *args, **kwargs)

    @staticmethod
    def getbtiming(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('getbtiming', *args, **kwargs)

    @staticmethod
    def getbbpmtime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('getbbpmtime', *args, **kwargs)

    @staticmethod
    def makebbpmtime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebbpmtime', *args, **kwargs)

    @staticmethod
    def makebdelaycount(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebdelaycount', *args, **kwargs)

    @staticmethod
    def makebpscusampletime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebpscusampletime', *args, **kwargs)

    @staticmethod
    def makebgettime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w1
        APS parsed args: None

        """
        return exec_with_tcl('makebgettime', *args, **kwargs)

    @staticmethod
    def makebsettime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w1
        APS parsed args: None

        """
        return exec_with_tcl('makebsettime', *args, **kwargs)

    @staticmethod
    def makebtimingdiagram(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebtimingdiagram', *args, **kwargs)

    @staticmethod
    def printbtiming(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('printbtiming', *args, **kwargs)

    @staticmethod
    def pscusampletime(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('pscusampletime', *args, **kwargs)

    @staticmethod
    def brampstartdelay(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: mode
        APS parsed args: None

        """
        return exec_with_tcl('brampstartdelay', *args, **kwargs)

    @staticmethod
    def setbconstants(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('setbconstants', *args, **kwargs)

    @staticmethod
    def setbdelaycount(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbdelaycount', *args, **kwargs)

    @staticmethod
    def setbforcefreerun(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('setbforcefreerun', *args, **kwargs)

    @staticmethod
    def showtiming(*args, **kwargs):
        """
        Location: btiming.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('showtiming', *args, **kwargs)

    @staticmethod
    def APSMpBoosterShutdownForAccessInfo(*args, **kwargs):
        """
        Location: APSMpBoosterShutdownForAccess.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterShutdownForAccessInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterShutdownForAccessInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterShutdownForAccess.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterShutdownForAccessInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterShutdownForAccess(*args, **kwargs):
        """
        Location: APSMpBoosterShutdownForAccess.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampdownTime', 'BM', 'QF', 'QD', 'SF', 'SD', 'selection', 'turnOffList', 'turnOffListDetailed', 'IS', 'IK', 'ES1', 'ES2', 'EK']

        """
        return exec_with_tcl('APSMpBoosterShutdownForAccess', *args, **kwargs)

    @staticmethod
    def APSMpBooster_ConfigureInfo(*args, **kwargs):
        """
        Location: APSMpBooster_Configure.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBooster_ConfigureInfo', *args, **kwargs)

    @staticmethod
    def APSMpBooster_Configure(*args, **kwargs):
        """
        Location: APSMpBooster_Configure.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBooster_Configure', *args, **kwargs)

    @staticmethod
    def APSMpBooster_ConfigureInitDialog(*args, **kwargs):
        """
        Location: APSMpBooster_Configure.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBooster_ConfigureInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPowerDirectlyInfo(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPowerDirectlyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPowerDirectlyDialog(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPowerDirectlyDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPowerDirectly(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'standbyGainLevel']

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPowerDirectly', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPowerInfo(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPowerDialog(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetDCStandbyPower(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterPSSetDCStandbyPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPowerDirectlyInfo(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPowerDirectlyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPowerDirectlyDialog(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPowerDirectlyDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPowerDirectly(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'setStandby', 'finalGain']

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPowerDirectly', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPowerInfo(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPowerDialog(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSExitDCStandbyPower(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'setStandby', 'finalGain']

        """
        return exec_with_tcl('APSMpBoosterPSExitDCStandbyPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSCheckIfDCStandbyPower(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterPSCheckIfDCStandbyPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSCheckForValidRampControlState(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterPSCheckForValidRampControlState', *args, **kwargs)

    @staticmethod
    def loadDCRamps(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('loadDCRamps', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetFreeWheelPVs(*args, **kwargs):
        """
        Location: BPSSetDCStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'DC']

        """
        return exec_with_tcl('APSMpBoosterPSSetFreeWheelPVs', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDSetupGlobalVars(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDSetupGlobalVars', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDSetupGUI(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDSetupGUI', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDSetStatus(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: text
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDSetStatus', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDAddPhotonBand(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: ['low', 'high', 'on']

        """
        return exec_with_tcl('APSChooseBestIDAddPhotonBand', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDRunSearch(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDRunSearch', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDReplot(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: tag
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDReplot', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDSavePlots(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: tag
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDSavePlots', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDFindRelevantFiles(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDFindRelevantFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDFindBestFiles(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: ['dataFileList', 'rootname']

        """
        return exec_with_tcl('APSChooseBestIDFindBestFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDFindDataFiles(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: ['dataDirectory', 'straightType', 'idLength', 'feType', 'current', 'gap', 'periodOption', 'type', 'maximumLength', 'periodMin', 'periodMax', 'periodFrac']

        """
        return exec_with_tcl('APSChooseBestIDFindDataFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDFindScuDataFiles(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: ['dataDirectory', 'straightType', 'idLength', 'feType', 'current', 'gap', 'maximumLength', 'periodMin', 'periodMax', 'periodFrac']

        """
        return exec_with_tcl('APSChooseBestIDFindScuDataFiles', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDLatexHeader(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDLatexHeader', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDLatexFooter(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDLatexFooter', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDLatexImage(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: filename
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDLatexImage', *args, **kwargs)

    @staticmethod
    def APSChooseBestIDLatexCalcValues(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChooseBestIDLatexCalcValues', *args, **kwargs)

    @staticmethod
    def FindReferenceLength(*args, **kwargs):
        """
        Location: chooseBestID.tcl
        TCL function args: args
        APS parsed args: ['type', 'length', 'feType']

        """
        return exec_with_tcl('FindReferenceLength', *args, **kwargs)

    @staticmethod
    def LASER_StartupFromStandbyInfo(*args, **kwargs):
        """
        Location: LASER_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LASER_StartupFromStandbyInfo', *args, **kwargs)

    @staticmethod
    def LASER_StartupFromStandby(*args, **kwargs):
        """
        Location: LASER_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('LASER_StartupFromStandby', *args, **kwargs)

    @staticmethod
    def LASER_BringDownToStandbyInfo(*args, **kwargs):
        """
        Location: LASER_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LASER_BringDownToStandbyInfo', *args, **kwargs)

    @staticmethod
    def LASER_BringDownToStandby(*args, **kwargs):
        """
        Location: LASER_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('LASER_BringDownToStandby', *args, **kwargs)

    @staticmethod
    def RFGUN_ChangeTimingInfo(*args, **kwargs):
        """
        Location: PCGUN_Shutdown.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_ChangeTimingInfo', *args, **kwargs)

    @staticmethod
    def RFGUN_ChangeTimingDialog(*args, **kwargs):
        """
        Location: PCGUN_Shutdown.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_ChangeTimingDialog', *args, **kwargs)

    @staticmethod
    def RFGUN_ChangeTiming(*args, **kwargs):
        """
        Location: PCGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['includePar', 'bypassPar']

        """
        return exec_with_tcl('RFGUN_ChangeTiming', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToTestStandInfo(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToTestStandInfo', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToTestStandDialog(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToTestStandDialog', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToTestStand(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToTestStand', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToL3DownInfo(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToL3DownInfo', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToL3DownDialog(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToL3DownDialog', *args, **kwargs)

    @staticmethod
    def APSMpITS_SwitchToL3Down(*args, **kwargs):
        """
        Location: ITS_ModeSwitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpITS_SwitchToL3Down', *args, **kwargs)

    @staticmethod
    def LINAC_WaitForPowerControls(*args, **kwargs):
        """
        Location: LINAC_TouchUp.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'suspend']

        """
        return exec_with_tcl('LINAC_WaitForPowerControls', *args, **kwargs)

    @staticmethod
    def APSMenuFrame(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        Usage: APSMenuFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-menuList <string>]
        [-parentLabel <string>]
        [-subMenu 1]
        [-contextHelp <string]

        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'menuList', 'subMenu', 'closeButton', 'parentLabel', 'geometry', 'contextHelp']

        """
        return exec_with_tcl('APSMenuFrame', *args, **kwargs)

    @staticmethod
    def APSMenuFrameEnter(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: args
        APS parsed args: ['widget', 'closeSubmenus', 'menuWidget', 'Y']

        """
        return exec_with_tcl('APSMenuFrameEnter', *args, **kwargs)

    @staticmethod
    def APSMenuFrameExit(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: args
        APS parsed args: ['widget']

        """
        return exec_with_tcl('APSMenuFrameExit', *args, **kwargs)

    @staticmethod
    def APSMenuFrameDelayedExecute(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: args
        APS parsed args: ['widget', 'closeSubmenus', 'menuWidget']

        """
        return exec_with_tcl('APSMenuFrameDelayedExecute', *args, **kwargs)

    @staticmethod
    def APSMenuFrameExec(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: command parentMenuWidget
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameExec', *args, **kwargs)

    @staticmethod
    def APSMenuFrameMenu(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: menuWidget menuList parentLabel parentMenuWidget
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameMenu', *args, **kwargs)

    @staticmethod
    def APSMenuFrameClose(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: parentMenuWidget {closeRoot 1}
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameClose', *args, **kwargs)

    @staticmethod
    def APSMenuFrameKill(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: parentMenuWidget
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameKill', *args, **kwargs)

    @staticmethod
    def APSMenuFrameListAdd(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: list value
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameListAdd', *args, **kwargs)

    @staticmethod
    def APSMenuFrameListDelete(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: list value
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameListDelete', *args, **kwargs)

    @staticmethod
    def APSMenuFramePadLength(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: text maxWidth
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFramePadLength', *args, **kwargs)

    @staticmethod
    def APSMenuFrameMake(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        Usage: APSMenuFrameMake menu
        [-type <string>]
        [-text <string>]
        [-executable <string>]
        [-contextHelp <string>]
        [-allowedUsers <string>]
        [-menuList <list>]
        [-command <string>]
        TCL function args: menu args
        APS parsed args: ['menuList', 'type', 'text', 'executable', 'contextHelp', 'command', 'allowedUsers', 'allowedSubnets']

        """
        return exec_with_tcl('APSMenuFrameMake', *args, **kwargs)

    @staticmethod
    def APSMenuFrameMakeFreeData(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameMakeFreeData', *args, **kwargs)

    @staticmethod
    def APSMenuFrameFindSubMenu(*args, **kwargs):
        """
        Location: APSMenuFrame.tcl
        TCL function args: subMenu menuList
        APS parsed args: None

        """
        return exec_with_tcl('APSMenuFrameFindSubMenu', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetStandbyPowerInfo(*args, **kwargs):
        """
        Location: BPSSetStandbyPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetStandbyPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetStandbyPowerDialog(*args, **kwargs):
        """
        Location: BPSSetStandbyPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetStandbyPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetStandbyPower(*args, **kwargs):
        """
        Location: BPSSetStandbyPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF-U', 'SD', 'exitDC']

        """
        return exec_with_tcl('APSMpBoosterPSSetStandbyPower', *args, **kwargs)

    @staticmethod
    def APScaRamp(*args, **kwargs):
        """
        Location: caramp.tcl
        APScaRamp -pvList <list> -variableList <list> [-beginList <list>] -endList <list> -steps <number> -pause <seconds> [-dryRun 1] [-functionList <list>] [-abortVariable <string>]TCL function args: args
        APS parsed args: ['pvList', 'variableList', 'beginList', 'endList', 'pause', 'steps', 'dryRun', 'abortVariable', 'functionList', 'postStepCallback', 'review']

        """
        return exec_with_tcl('APScaRamp', *args, **kwargs)

    @staticmethod
    def APSStandardizeWithDecay(*args, **kwargs):
        """
        Location: caramp.tcl
        APSStandardizeWithDecay -pv <pv> -lowerLimit <number> -upperLimit <number> -numSteps <integer> -stepInterval <number> -numCycles <integer> -approachFromLowerLimit <0|1> -approachFromUpperLimit <0|1> -finalSetpoint <number>TCL function args: args
        APS parsed args: ['pv', 'lowerLimit', 'upperLimit', 'numSteps', 'stepInterval', 'numCycles', 'approachFromLowerLimit', 'approachFromUpperLimit', 'finalSetpoint', 'decayRate']

        """
        return exec_with_tcl('APSStandardizeWithDecay', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetNoPowerInfo(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetNoPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetNoPowerDialog(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetNoPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetNoPower(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF-U', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterPSSetNoPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSCheckRampTiming(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterPSCheckRampTiming', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSResetRampTiming(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterPSResetRampTiming', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSGetSCRRampTimingValues(*args, **kwargs):
        """
        Location: BPSSetNoPower.tcl
        TCL function args: args
        APS parsed args: ['magnet']

        """
        return exec_with_tcl('APSMpBoosterPSGetSCRRampTimingValues', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToL3DownInfo(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToL3DownInfo', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToL3DownDialog(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToL3DownDialog', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToL3Down(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('APSMpPG1_SwitchToL3Down', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToNormalModeInfo(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToNormalModeInfo', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToNormalModeDialog(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToNormalModeDialog', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToNormalMode(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToNormalMode', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToPG1OperationsModeInfo(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToPG1OperationsModeInfo', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToPG1OperationsModeDialog(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToPG1OperationsModeDialog', *args, **kwargs)

    @staticmethod
    def APSMpPG1_SwitchToPG1OperationsMode(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPG1_SwitchToPG1OperationsMode', *args, **kwargs)

    @staticmethod
    def StartPCGunOnlyInterleaveModeInfo(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('StartPCGunOnlyInterleaveModeInfo', *args, **kwargs)

    @staticmethod
    def StartPCGunOnlyInterleaveMode(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('StartPCGunOnlyInterleaveMode', *args, **kwargs)

    @staticmethod
    def StopPCGunOnlyInterleaveModeInfo(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('StopPCGunOnlyInterleaveModeInfo', *args, **kwargs)

    @staticmethod
    def StopPCGunOnlyInterleaveMode(*args, **kwargs):
        """
        Location: PG1_ModeSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('StopPCGunOnlyInterleaveMode', *args, **kwargs)

    @staticmethod
    def APSMpPARLETConditionInfo(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETConditionInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETConditionInitDialog(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETConditionInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARLETCondition(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: args
        APS parsed args: ['conditioningTime', 'SCRFile', 'PARdipole', 'PARquads', 'PARsextupoles', 'PARcorrectors', 'LTPdipole', 'LTPquads', 'LTPcorrectors', 'PTBdipole', 'PTBquads', 'PTBcorrectors']

        """
        return exec_with_tcl('APSMpPARLETCondition', *args, **kwargs)

    @staticmethod
    def APSMpPARLETTurnOnDCPSInfo(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETTurnOnDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARLETTurnOnDCPSInitDialog(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARLETTurnOnDCPSInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARLETTurnOnDCPS(*args, **kwargs):
        """
        Location: APSMpPARConditioning.tcl
        TCL function args: args
        APS parsed args: ['PARdipole', 'PARquads', 'PARsextupoles', 'PARcorrectors', 'LTPdipole', 'LTPquads', 'LTPcorrectors', 'PTBdipole', 'PTBquads', 'PTBcorrectors']

        """
        return exec_with_tcl('APSMpPARLETTurnOnDCPS', *args, **kwargs)

    @staticmethod
    def APSDialogBox(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        Usage: APSDialogBox widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string>]
        [-width <string>]
        [-height <string>]
        [-contextHelp <string]
        [-buttonSize <size>]
        	[-modal 1]
        [-cancelCommand <command>]
        [-okCommand <command>
        Creates	$parent$widget.
        	userFrame
        	buttonRow.ok.button
        	buttonRow.cancel.buttonTCL function args: widget args
        APS parsed args: ['parent', 'name', 'noPack', 'packOption', 'width', 'height', 'contextHelp', 'buttonSize', 'okCommand', 'cancelCommand', 'modal', 'cancelButton']

        """
        return exec_with_tcl('APSDialogBox', *args, **kwargs)

    @staticmethod
    def APSDialogBoxAddButton(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        Usage: APSDialogBoxAddButton widget
        [-parent <string>]
        [-text <string>]
        [-command <string>]
        [-contextHelp <string>]
        [-size <size>]

        Creates	$parent.buttonRow.$widgetTCL function args: widget args
        APS parsed args: ['parent', 'text', 'command', 'contextHelp', 'size', 'width', 'packOption']

        """
        return exec_with_tcl('APSDialogBoxAddButton', *args, **kwargs)

    @staticmethod
    def APSWindow(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        Usage: APSWindow widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string>]
        [-contextHelp <string]
        	[-closeButton 0]

        Creates	$parent$widget.
        	userFrame
        	buttonRow.close.button
        TCL function args: widget args
        APS parsed args: ['parent', 'name', 'noPack', 'packOption', 'contextHelp', 'closeButton']

        """
        return exec_with_tcl('APSWindow', *args, **kwargs)

    @staticmethod
    def APSEMailDialog(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        Usage: APSEMailDialog widget
        [-message <string>]
        [-address <string>]
        [-modal 1]
        [-width <number>]
        TCL function args: widget args
        APS parsed args: ['message', 'address', 'modal', 'width']

        """
        return exec_with_tcl('APSEMailDialog', *args, **kwargs)

    @staticmethod
    def APSEMailDialogOK(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        TCL function args: dialogWidget commentsWidget messageWidget
        APS parsed args: None

        """
        return exec_with_tcl('APSEMailDialogOK', *args, **kwargs)

    @staticmethod
    def APSSaveDialog(*args, **kwargs):
        """
        Location: APSDialogBox.tcl
        Usage: APSSaveDialog widget
        [-text <string>]
        [-textWidget <string>]
        [-modal 1]
        TCL function args: widget args
        APS parsed args: ['text', 'textWidget', 'modal']

        """
        return exec_with_tcl('APSSaveDialog', *args, **kwargs)

    @staticmethod
    def doMultiScan(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: ['bpm', 'quadLimit', 'quadSteps', 'negativeOnly', 'corrLimit', 'corrSteps', 'num2Ave', 'statusCallback', 'ultimateCallBack']

        """
        return exec_with_tcl('doMultiScan', *args, **kwargs)

    @staticmethod
    def createBPMOffsetDirectory(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: ['dateSubdirectory', 'statusCallback', 'bpmDir']

        """
        return exec_with_tcl('createBPMOffsetDirectory', *args, **kwargs)

    @staticmethod
    def doMultiScanPostCommand(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('doMultiScanPostCommand', *args, **kwargs)

    @staticmethod
    def doQuadScan(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('doQuadScan', *args, **kwargs)

    @staticmethod
    def getOffsetFiles(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: ['bpm', 'suffix']

        """
        return exec_with_tcl('getOffsetFiles', *args, **kwargs)

    @staticmethod
    def processMS(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: ['date', 'bpm', 'index', 'review', 'statusCallback', 'makePlots', 'printout', 'ultimateCallBack']

        """
        return exec_with_tcl('processMS', *args, **kwargs)

    @staticmethod
    def InstallOffset(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('InstallOffset', *args, **kwargs)

    @staticmethod
    def RemoveBadMeasurement(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('RemoveBadMeasurement', *args, **kwargs)

    @staticmethod
    def CleanFiles(*args, **kwargs):
        """
        Location: SRBPMOffset.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('CleanFiles', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetFullPowerInfo(*args, **kwargs):
        """
        Location: BPSSetFullPower.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetFullPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetFullPowerDialog(*args, **kwargs):
        """
        Location: BPSSetFullPower.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSSetFullPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetFullPower(*args, **kwargs):
        """
        Location: BPSSetFullPower.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF-U', 'SF', 'SD', 'startupTime', 'startupSteps', 'coldStart', 'SCRFile', 'doRestore']

        """
        return exec_with_tcl('APSMpBoosterPSSetFullPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSSetFullPowerNormal(*args, **kwargs):
        """
        Location: BPSSetFullPower.tcl
        TCL function args: args
        APS parsed args: ['presentGain', 'fullGain', 'magnet', 'steps', 'time']

        """
        return exec_with_tcl('APSMpBoosterPSSetFullPowerNormal', *args, **kwargs)

    @staticmethod
    def APSRampToSnapshot(*args, **kwargs):
        """
        Location: APSRampToSnapshot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRampToSnapshot', *args, **kwargs)

    @staticmethod
    def APSSRTakeLifetimeDataSeries(*args, **kwargs):
        """
        Location: SRLifetime.tcl
        TCL function args: args
        APS parsed args: ['buttonWidget', 'minCurrentChange', 'maxCurrentChange', 'maxTime', 'minTime', 'timeInterval', 'takeTunes', 'takeOrbit', 'takeBunchPattern', 'rootname', 'comment', 'sets', 'takeSRVSA', 'timeBetweenSets', 'abortVariable', 'statusCallback', 'plot', 'PVToVary', 'PVToVaryStart', 'PVToVaryEnd', 'postChangePause']

        """
        return exec_with_tcl('APSSRTakeLifetimeDataSeries', *args, **kwargs)

    @staticmethod
    def APSSRTakeLifetimeData(*args, **kwargs):
        """
        Location: SRLifetime.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'minCurrentChange', 'maxCurrentChange', 'maxTime', 'minTime', 'timeInterval', 'takeTunes', 'takeOrbit', 'takeBunchPattern', 'abortVariable', 'statusCallback', 'plot', 'comment', 'takeSRVSA', 'PVToVary']

        """
        return exec_with_tcl('APSSRTakeLifetimeData', *args, **kwargs)

    @staticmethod
    def APSSRProcessLifetimeData(*args, **kwargs):
        """
        Location: SRLifetime.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'PVToVary']

        """
        return exec_with_tcl('APSSRProcessLifetimeData', *args, **kwargs)

    @staticmethod
    def submitGridEngineJob(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('submitGridEngineJob', *args, **kwargs)

    @staticmethod
    def APSTimeSinceLastChange(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname']

        """
        return exec_with_tcl('APSTimeSinceLastChange', *args, **kwargs)

    @staticmethod
    def APSElegantPerformRun(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantPerformRun', *args, **kwargs)

    @staticmethod
    def APSElegantPostProcessRun(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'postProcessProc', 'statusCallback', 'makePngFiles', 'noPlots', 'pid']

        """
        return exec_with_tcl('APSElegantPostProcessRun', *args, **kwargs)

    @staticmethod
    def APSElegantPerformRuns(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantPerformRuns', *args, **kwargs)

    @staticmethod
    def APSElegantAffix(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantAffix', *args, **kwargs)

    @staticmethod
    def APSElegantPostProcessRuns(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'runNameList', 'copyList', 'mergeList', 'pidList', 'excludeList', 'combineList', 'postProcessProc', 'makePngFiles', 'firstOnlyList', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantPostProcessRuns', *args, **kwargs)

    @staticmethod
    def APSElegantSaveJobConfiguration(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['filename', 'statusCallback', 'momentum', 'matrixLatticeFile', 'matrixBeamline', 'matrixOffsetElement', 'kickLatticeFile', 'kickBeamline', 'kickOffsetElement', 'forceOccurence', 'mainDirectory', 'mainPrefix', 'gridEngine', 'makePngFiles']

        """
        return exec_with_tcl('APSElegantSaveJobConfiguration', *args, **kwargs)

    @staticmethod
    def APSElegantGetParameterFileList(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantGetParameterFileList', *args, **kwargs)

    @staticmethod
    def APSElegantBasicComputations(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'statusCallback', 'momentum', 'matrixLatticeFile', 'matrixBeamline', 'matrixOffsetElement', 'kickLatticeFile', 'kickBeamline', 'kickOffsetElement', 'forceOccurence', 'mainDirectory', 'mainPrefix', 'gridEngine', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantBasicComputations', *args, **kwargs)

    @staticmethod
    def APSElegantBasicComputationsPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantBasicComputationsPP', *args, **kwargs)

    @staticmethod
    def APSElegantMomentsComputations(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'statusCallback', 'momentum', 'matrixLatticeFile', 'matrixBeamline', 'matrixOffsetElement', 'kickLatticeFile', 'kickBeamline', 'kickOffsetElement', 'forceOccurence', 'mainDirectory', 'mainPrefix', 'gridEngine', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantMomentsComputations', *args, **kwargs)

    @staticmethod
    def APSElegantMomentsComputationsPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantMomentsComputationsPP', *args, **kwargs)

    @staticmethod
    def APSElegantScanCollectiveEffectsProgram(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['template', 'extension', 'type', 'dataFile', 'mainDirectory', 'mainPrefix', 'gridEngine', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantScanCollectiveEffectsProgram', *args, **kwargs)

    @staticmethod
    def APSElegantDetermineScanVariableCollectiveEffects(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['mainDirectory', 'mainPrefix']

        """
        return exec_with_tcl('APSElegantDetermineScanVariableCollectiveEffects', *args, **kwargs)

    @staticmethod
    def APSElegantRunIBS(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantRunIBS', *args, **kwargs)

    @staticmethod
    def APSElegantDisplayIBS(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['makePngFiles', 'statusCallback', 'rootname', 'noPlots']

        """
        return exec_with_tcl('APSElegantDisplayIBS', *args, **kwargs)

    @staticmethod
    def APSElegantRunHaissinski(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantRunHaissinski', *args, **kwargs)

    @staticmethod
    def APSElegantDisplayHaissinski(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['makePngFiles', 'statusCallback', 'rootname', 'noPlots']

        """
        return exec_with_tcl('APSElegantDisplayHaissinski', *args, **kwargs)

    @staticmethod
    def APSElegantRunSCTuneShift(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantRunSCTuneShift', *args, **kwargs)

    @staticmethod
    def APSElegantDisplaySCTuneShift(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['makePngFiles', 'statusCallback', 'rootname', 'noPlots']

        """
        return exec_with_tcl('APSElegantDisplaySCTuneShift', *args, **kwargs)

    @staticmethod
    def APSElegantPhaseSpaceTracking(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantPhaseSpaceTracking', *args, **kwargs)

    @staticmethod
    def APSQueryValuesDialog(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['nameList', 'defaultList', 'typeList', 'name', 'elementList']

        """
        return exec_with_tcl('APSQueryValuesDialog', *args, **kwargs)

    @staticmethod
    def APSElegantMakePhaseSpacePlot(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['plane', 'rootname', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantMakePhaseSpacePlot', *args, **kwargs)

    @staticmethod
    def APSElegantMakeFFTPhaseSpacePlot(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['plane', 'rootname', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantMakeFFTPhaseSpacePlot', *args, **kwargs)

    @staticmethod
    def APSElegantPhaseSpaceTrackingPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantPhaseSpaceTrackingPP', *args, **kwargs)

    @staticmethod
    def APSElegantOffMomentumTuneTracking(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantOffMomentumTuneTracking', *args, **kwargs)

    @staticmethod
    def APSElegantOffMomentumTuneTrackingPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantOffMomentumTuneTrackingPP', *args, **kwargs)

    @staticmethod
    def APSElegantHigherOrderDispersion(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantHigherOrderDispersion', *args, **kwargs)

    @staticmethod
    def APSElegantHigherOrderDispersionPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantHigherOrderDispersionPP', *args, **kwargs)

    @staticmethod
    def APSElegantDynamicAperture(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantDynamicAperture', *args, **kwargs)

    @staticmethod
    def APSElegantDynamicAperturePP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantDynamicAperturePP', *args, **kwargs)

    @staticmethod
    def APSElegantOffMomentumDynamicAperture(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantOffMomentumDynamicAperture', *args, **kwargs)

    @staticmethod
    def APSElegantOffMomentumDynamicAperturePP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantOffMomentumDynamicAperturePP', *args, **kwargs)

    @staticmethod
    def APSElegantDynamicApertureErrors(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantDynamicApertureErrors', *args, **kwargs)

    @staticmethod
    def APSElegantDynamicApertureErrorsPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantDynamicApertureErrorsPP', *args, **kwargs)

    @staticmethod
    def APSElegantKickApertureErrors(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantKickApertureErrors', *args, **kwargs)

    @staticmethod
    def APSElegantKickApertureErrorsPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantKickApertureErrorsPP', *args, **kwargs)

    @staticmethod
    def APSElegantFineDynamicAperture(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantFineDynamicAperture', *args, **kwargs)

    @staticmethod
    def APSElegantFineDynamicAperturePP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantFineDynamicAperturePP', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMap(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMap', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapPP', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapErrorPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapErrorPP', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapDelta(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapDelta', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapDeltaErrors(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['sourceDir', 'forceOccurence', 'momentum', 'matrixLatticeFile', 'kickLatticeFile', 'mainDirectory', 'mainPrefix', 'kickOffsetElement', 'matrixLatticeFile', 'matrixBeamline', 'kickBeamline', 'matrixOffsetElement', 'gridEngine', 'makePngFiles', 'statusCallback', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapDeltaErrors', *args, **kwargs)

    @staticmethod
    def APSElegantInterpolateResonances(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantInterpolateResonances', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapDeltaPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapDeltaPP', *args, **kwargs)

    @staticmethod
    def APSElegantFrequencyMapDeltaErrorsPP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantFrequencyMapDeltaErrorsPP', *args, **kwargs)

    @staticmethod
    def APSElegantMomentumAperture(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSElegantMomentumAperture', *args, **kwargs)

    @staticmethod
    def APSElegantMomentumAperturePP(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'makePngFiles', 'noPlots']

        """
        return exec_with_tcl('APSElegantMomentumAperturePP', *args, **kwargs)

    @staticmethod
    def APSElegantAbortRun(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['postProcessProc', 'statusCallback', 'rootname']

        """
        return exec_with_tcl('APSElegantAbortRun', *args, **kwargs)

    @staticmethod
    def APSElegantAddNewProcess(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: args
        APS parsed args: ['postProcessProc', 'rootname', 'pidList']

        """
        return exec_with_tcl('APSElegantAddNewProcess', *args, **kwargs)

    @staticmethod
    def ExpandFilename(*args, **kwargs):
        """
        Location: elegant.tcl
        TCL function args: filename
        APS parsed args: None

        """
        return exec_with_tcl('ExpandFilename', *args, **kwargs)

    @staticmethod
    def getbbpmevol(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: mode args
        APS parsed args: None

        """
        return exec_with_tcl('getbbpmevol', *args, **kwargs)

    @staticmethod
    def getbcorrevol(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: mode args
        APS parsed args: None

        """
        return exec_with_tcl('getbcorrevol', *args, **kwargs)

    @staticmethod
    def makebbpmevol(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebbpmevol', *args, **kwargs)

    @staticmethod
    def makebcorrevol(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: w
        APS parsed args: None

        """
        return exec_with_tcl('makebcorrevol', *args, **kwargs)

    @staticmethod
    def makebbpmevolfilename(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makebbpmevolfilename', *args, **kwargs)

    @staticmethod
    def makebcorrevolfilename(*args, **kwargs):
        """
        Location: bevol.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('makebcorrevolfilename', *args, **kwargs)

    @staticmethod
    def APSMpMagnetKnLValues(*args, **kwargs):
        """
        Location: APSMpMagnetSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMagnetKnLValues', *args, **kwargs)

    @staticmethod
    def APSMpMagnetSetpoints(*args, **kwargs):
        """
        Location: APSMpMagnetSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMagnetSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpAdjustMagnetSetpoints(*args, **kwargs):
        """
        Location: APSMpMagnetSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpAdjustMagnetSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpAdjustParameterFile(*args, **kwargs):
        """
        Location: APSMpMagnetSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpAdjustParameterFile', *args, **kwargs)

    @staticmethod
    def APSMpLTPStartUpInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPStartUp(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'conditioningTime', 'restoreFile', 'particle', 'standardizeB1', 'DCPS', 'restoreDCPS', 'maxLTPB1Cycles']

        """
        return exec_with_tcl('APSMpLTPStartUp', *args, **kwargs)

    @staticmethod
    def APSMpLTPStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTPTurnOnDCPSInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPTurnOnDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPTurnOnDCPS(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries']

        """
        return exec_with_tcl('APSMpLTPTurnOnDCPS', *args, **kwargs)

    @staticmethod
    def APSMpLTPStandardizeInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStandardizeInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPStandardize(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpLTPStandardize', *args, **kwargs)

    @staticmethod
    def APSMpLTPStandardizeInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStandardizeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTPDegaussInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPDegaussInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPDegauss(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degaussTime', 'block']

        """
        return exec_with_tcl('APSMpLTPDegauss', *args, **kwargs)

    @staticmethod
    def APSMpLTPDegaussInitDialog(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPDegaussInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTPCheckConditioning(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degauss', 'standardize']

        """
        return exec_with_tcl('APSMpLTPCheckConditioning', *args, **kwargs)

    @staticmethod
    def APSMpLTPWaitForConditioning(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPWaitForConditioning', *args, **kwargs)

    @staticmethod
    def APSMpLTPRestoreFile(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'restoreDCPS']

        """
        return exec_with_tcl('APSMpLTPRestoreFile', *args, **kwargs)

    @staticmethod
    def APSMpLTPStopConditioningInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStopConditioningInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPStopConditioning(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpLTPClearApertureInfo(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPClearApertureInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTPClearAperture(*args, **kwargs):
        """
        Location: APSMpLTPTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTPClearAperture', *args, **kwargs)

    @staticmethod
    def APSCheckPVConnections(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCheckPVConnections', *args, **kwargs)

    @staticmethod
    def APSBunchTrainConnect(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSBunchTrainConnect', *args, **kwargs)

    @staticmethod
    def APSTopupConnect(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSTopupConnect', *args, **kwargs)

    @staticmethod
    def APSTopupReadbackConnect(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSTopupReadbackConnect', *args, **kwargs)

    @staticmethod
    def TerminateInjection(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['keepWarm', 'manageLinacBunches']

        """
        return exec_with_tcl('TerminateInjection', *args, **kwargs)

    @staticmethod
    def PauseInjection(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('PauseInjection', *args, **kwargs)

    @staticmethod
    def DoInjection(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: bucket dwell
        APS parsed args: None

        """
        return exec_with_tcl('DoInjection', *args, **kwargs)

    @staticmethod
    def DoBunchTrainInjection(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['start', 'interval', 'number', 'dwell', 'callback', 'fast', 'stopAt', 'stopAtSum', 'useSum', 'cycles', 'multiplet', 'keepWarm', 'manageLinacBunches']

        """
        return exec_with_tcl('DoBunchTrainInjection', *args, **kwargs)

    @staticmethod
    def GetLinacBunches(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('GetLinacBunches', *args, **kwargs)

    @staticmethod
    def SetLinacBunches(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['number']

        """
        return exec_with_tcl('SetLinacBunches', *args, **kwargs)

    @staticmethod
    def AbortInjection(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('AbortInjection', *args, **kwargs)

    @staticmethod
    def APSPARCleaning(*args, **kwargs):
        """
        Location: SRBunchTrain.tcl
        TCL function args: args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSPARCleaning', *args, **kwargs)

    @staticmethod
    def APSRemoveExpiredTimeSeriesData(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveExpiredTimeSeriesData', *args, **kwargs)

    @staticmethod
    def APSPostprocessScalarMonitorData(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPostprocessScalarMonitorData', *args, **kwargs)

    @staticmethod
    def APSPostprocessChargeFastLog(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: ['positrons', 'targetDir', 'force', 'debug', 'year', 'julianDay', 'tag', 'first']

        """
        return exec_with_tcl('APSPostprocessChargeFastLog', *args, **kwargs)

    @staticmethod
    def APSMakeMonthlyChargeFastFile(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: ['offset']

        """
        return exec_with_tcl('APSMakeMonthlyChargeFastFile', *args, **kwargs)

    @staticmethod
    def APSTimeAverageDataLog(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSTimeAverageDataLog', *args, **kwargs)

    @staticmethod
    def APSCreateLockFile(*args, **kwargs):
        """
        Location: postprocessing.tcl
        TCL function args: args
        APS parsed args: ['fileName']

        """
        return exec_with_tcl('APSCreateLockFile', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInfo(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInfo', *args, **kwargs)

    @staticmethod
    def APSMpMatrix(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpMatrix', *args, **kwargs)

    @staticmethod
    def APSMpMatrixTakeDataDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuator', 'question', 'deleteButton']

        """
        return exec_with_tcl('APSMpMatrixTakeDataDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitSecondaryDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInitSecondaryDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitLastDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: frame beamListChoice
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInitLastDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixResetHalfRange(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixResetHalfRange', *args, **kwargs)

    @staticmethod
    def APSActuatorBPMCheckButtons(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['frame']

        """
        return exec_with_tcl('APSActuatorBPMCheckButtons', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitAddRemoveDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['index']

        """
        return exec_with_tcl('APSMpMatrixInitAddRemoveDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitAddRemove2Dialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['index']

        """
        return exec_with_tcl('APSMpMatrixInitAddRemove2Dialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitActuatorDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: beamListChoice
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInitActuatorDialog', *args, **kwargs)

    @staticmethod
    def APSMpMatrixInitBPMDialog(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMatrixInitBPMDialog', *args, **kwargs)

    @staticmethod
    def MpRespMatrixDoExperimentModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList', 'templateFile']

        """
        return exec_with_tcl('MpRespMatrixDoExperimentModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixCalcSlopesModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList']

        """
        return exec_with_tcl('MpRespMatrixCalcSlopesModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixFormMatrixModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuatorList', 'badBpms', 'badActuators', 'outFile', 'beamlineFile', 'filterColumns', 'excludeColumns']

        """
        return exec_with_tcl('MpRespMatrixFormMatrixModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixCalcInverseModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['inFile', 'outFile', 'minimum']

        """
        return exec_with_tcl('MpRespMatrixCalcInverseModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixSetParameterDefaultsModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('MpRespMatrixSetParameterDefaultsModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixRemoveColonsModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: word
        APS parsed args: None

        """
        return exec_with_tcl('MpRespMatrixRemoveColonsModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixSetActuatorParametersModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['actuator']

        """
        return exec_with_tcl('MpRespMatrixSetActuatorParametersModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixInstallDialogModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'matrixRoot', 'copyRoot', 'sourceDir', 'installDir', 'installRoot']

        """
        return exec_with_tcl('MpRespMatrixInstallDialogModified', *args, **kwargs)

    @staticmethod
    def MpRespMatrixInstallModified(*args, **kwargs):
        """
        Location: APSMpMatrix.tcl
        TCL function args: args
        APS parsed args: ['matrixRoot', 'copyRoot', 'installDir', 'installRoot', 'sourceDir', 'comment']

        """
        return exec_with_tcl('MpRespMatrixInstallModified', *args, **kwargs)

    @staticmethod
    def APSBoosterTurnOnOffTuneDrive(*args, **kwargs):
        """
        Location: boosterTune.tcl
        TCL function args: args
        APS parsed args: ['onoff', 'xdrive', 'ydrive', 'statusCallback', 'Xxdrive', 'Xydrive', 'Yxdrive', 'Yydrive']

        """
        return exec_with_tcl('APSBoosterTurnOnOffTuneDrive', *args, **kwargs)

    @staticmethod
    def APSBoosterSwitchTuneInput(*args, **kwargs):
        """
        Location: boosterTune.tcl
        TCL function args: args
        APS parsed args: ['plane', 'Xxdrive', 'Xydrive', 'Yxdrive', 'Yydrive', 'SUMxdrive', 'SUMydrive', 'statusCallback']

        """
        return exec_with_tcl('APSBoosterSwitchTuneInput', *args, **kwargs)

    @staticmethod
    def APSMpOpenCloseGateValvesInfo(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOpenCloseGateValvesInfo', *args, **kwargs)

    @staticmethod
    def APSMpOpenCloseGateValvesInitDialog(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOpenCloseGateValvesInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpCloseGateValvesInfo(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseGateValvesInfo', *args, **kwargs)

    @staticmethod
    def APSMpCloseGateValves(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseGateValves', *args, **kwargs)

    @staticmethod
    def APSMpOpenGateValvesInfo(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOpenGateValvesInfo', *args, **kwargs)

    @staticmethod
    def APSMpOpenGateValves(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpOpenGateValves', *args, **kwargs)

    @staticmethod
    def APSMpCloseInjectorGateValvesInfo(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseInjectorGateValvesInfo', *args, **kwargs)

    @staticmethod
    def APSMpCloseInjectorGateValves(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseInjectorGateValves', *args, **kwargs)

    @staticmethod
    def APSMpCloseLinacGateValvesInfo(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseLinacGateValvesInfo', *args, **kwargs)

    @staticmethod
    def APSMpCloseLinacGateValves(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCloseLinacGateValves', *args, **kwargs)

    @staticmethod
    def APSMpOpenCloseGateValves(*args, **kwargs):
        """
        Location: APSMpGateValves.tcl
        TCL function args: args
        APS parsed args: ['all', 'guns', 'linac', 'operation']

        """
        return exec_with_tcl('APSMpOpenCloseGateValves', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchBPMConfigInfo(*args, **kwargs):
        """
        Location: APSMpBoosterBPMConfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchBPMConfigInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchBPMConfigInitDialog(*args, **kwargs):
        """
        Location: APSMpBoosterBPMConfig.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchBPMConfigInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterSwitchBPMConfig(*args, **kwargs):
        """
        Location: APSMpBoosterBPMConfig.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterSwitchBPMConfig', *args, **kwargs)

    @staticmethod
    def APSGenerateLinacK1Values(*args, **kwargs):
        """
        Location: APSGenerateLinacK1Values.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGenerateLinacK1Values', *args, **kwargs)

    @staticmethod
    def APSMpMeasureTunesInitDialog(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMeasureTunesInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARMeasureTunes(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARMeasureTunes', *args, **kwargs)

    @staticmethod
    def APSMpSRMeasureTunes(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRMeasureTunes', *args, **kwargs)

    @staticmethod
    def APSSetupStriplineDrive(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: ['plane', 'stripline', 'rf', 'xPhase', 'yPhase', 'VSA']

        """
        return exec_with_tcl('APSSetupStriplineDrive', *args, **kwargs)

    @staticmethod
    def APSMpMeasureTunes(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: ['analyzer', 'doSetup', 'setupFile', 'useExistingData', 'averagingSeconds', 'useDividingLine', 'outputFile', 'comment', 'plotData', 'ring', 'lowerTune', 'upperTune', 'dividingLine', 'measureXYtuneTogether', 'xPower', 'yPower', 'xFreq', 'yFreq', 'span', 'xP0ReducedGain', 'yP0ReducedGain', 'xDimtelReducedGain', 'yDimtelReducedGain', 'xPhase', 'yPhase', 'xDelay', 'yDelay']

        """
        return exec_with_tcl('APSMpMeasureTunes', *args, **kwargs)

    @staticmethod
    def APSMpMeasureP0FBTune(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: ['outputFile', 'plot', 'update', 'steps', 'statusCallback', 'archive', 'interval', 'tuneRangeLow', 'system']

        """
        return exec_with_tcl('APSMpMeasureP0FBTune', *args, **kwargs)

    @staticmethod
    def APSGetFBbunchPatternParameters(*args, **kwargs):
        """
        Location: APSMpPARMeasTunes.tcl
        TCL function args: args
        APS parsed args: ['system', 'filename']

        """
        return exec_with_tcl('APSGetFBbunchPatternParameters', *args, **kwargs)

    @staticmethod
    def APSSRApplySteeringSetpoints(*args, **kwargs):
        """
        Location: APSSRSteering.tcl
        TCL function args: args
        APS parsed args: ['sector', 'source', 'plane', 'bpmList', 'deltaList', 'review', 'stepSizeLimit', 'statusCallback', 'dryRun', 'xp', 'yp', 'stepInterval']

        """
        return exec_with_tcl('APSSRApplySteeringSetpoints', *args, **kwargs)

    @staticmethod
    def APSSRSaveSteeringToOps(*args, **kwargs):
        """
        Location: APSSRSteering.tcl
        TCL function args: args
        APS parsed args: ['description', 'statusCallback', 'installUBOP']

        """
        return exec_with_tcl('APSSRSaveSteeringToOps', *args, **kwargs)

    @staticmethod
    def APSCollectFBCorrectorHistory(*args, **kwargs):
        """
        Location: APSGetFBCorHistory.tcl
        TCL function args: args
        APS parsed args: ['filename', 'noUpdate']

        """
        return exec_with_tcl('APSCollectFBCorrectorHistory', *args, **kwargs)

    @staticmethod
    def APSCollectFBbpmHistory(*args, **kwargs):
        """
        Location: APSGetFBCorHistory.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'noUpdate']

        """
        return exec_with_tcl('APSCollectFBbpmHistory', *args, **kwargs)

    @staticmethod
    def APSCollectNbBpmHistory(*args, **kwargs):
        """
        Location: APSGetFBCorHistory.tcl
        TCL function args: args
        APS parsed args: ['rootname']

        """
        return exec_with_tcl('APSCollectNbBpmHistory', *args, **kwargs)

    @staticmethod
    def APSCollectFPGABpmHistory(*args, **kwargs):
        """
        Location: APSGetFBCorHistory.tcl
        TCL function args: args
        APS parsed args: ['turnHistoryName', 'slowHistoryName', 'directory', 'timeout']

        """
        return exec_with_tcl('APSCollectFPGABpmHistory', *args, **kwargs)

    @staticmethod
    def APSProcessFPGABpmHistoryData(*args, **kwargs):
        """
        Location: APSGetFBCorHistory.tcl
        TCL function args: args
        APS parsed args: ['dirName']

        """
        return exec_with_tcl('APSProcessFPGABpmHistoryData', *args, **kwargs)

    @staticmethod
    def APSSetMainStatus(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: text
        APS parsed args: None

        """
        return exec_with_tcl('APSSetMainStatus', *args, **kwargs)

    @staticmethod
    def APSAffix(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: list args
        APS parsed args: ['prefix', 'suffix']

        """
        return exec_with_tcl('APSAffix', *args, **kwargs)

    @staticmethod
    def APSControlLawMakeWidgetGroup(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'group']

        """
        return exec_with_tcl('APSControlLawMakeWidgetGroup', *args, **kwargs)

    @staticmethod
    def APSControlLawMakeBriefWidgetGroup(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'group']

        """
        return exec_with_tcl('APSControlLawMakeBriefWidgetGroup', *args, **kwargs)

    @staticmethod
    def APSControlLawMakeFullWidgetGroup(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'group']

        """
        return exec_with_tcl('APSControlLawMakeFullWidgetGroup', *args, **kwargs)

    @staticmethod
    def APSControlLawMakeWidget(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawMakeWidget', *args, **kwargs)

    @staticmethod
    def CheckLinacLinks(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: w1 w2
        APS parsed args: None

        """
        return exec_with_tcl('CheckLinacLinks', *args, **kwargs)

    @staticmethod
    def APSControlLawMakeBriefWidget(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawMakeBriefWidget', *args, **kwargs)

    @staticmethod
    def APSControlLawIsSlotUsed(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['PV']

        """
        return exec_with_tcl('APSControlLawIsSlotUsed', *args, **kwargs)

    @staticmethod
    def APSControlLawIsSlotTimedOut(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['PV']

        """
        return exec_with_tcl('APSControlLawIsSlotTimedOut', *args, **kwargs)

    @staticmethod
    def APSControlLawStartMonitors(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['PV']

        """
        return exec_with_tcl('APSControlLawStartMonitors', *args, **kwargs)

    @staticmethod
    def APSControlLawRefreshArraysAndButtons(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSControlLawRefreshArraysAndButtons', *args, **kwargs)

    @staticmethod
    def APSControlLawRefreshArrays(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['PV']

        """
        return exec_with_tcl('APSControlLawRefreshArrays', *args, **kwargs)

    @staticmethod
    def APSControlLawStartButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member', 'full']

        """
        return exec_with_tcl('APSControlLawStartButton', *args, **kwargs)

    @staticmethod
    def APSControlLawResumeButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawResumeButton', *args, **kwargs)

    @staticmethod
    def APSControlLawSuspendButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawSuspendButton', *args, **kwargs)

    @staticmethod
    def APSControlLawAbortButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawAbortButton', *args, **kwargs)

    @staticmethod
    def APSControlLawClearButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawClearButton', *args, **kwargs)

    @staticmethod
    def APSControlLawRefreshButtons(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['PV']

        """
        return exec_with_tcl('APSControlLawRefreshButtons', *args, **kwargs)

    @staticmethod
    def APSControlLawInfoButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawInfoButton', *args, **kwargs)

    @staticmethod
    def APSControlLawTestValuesButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawTestValuesButton', *args, **kwargs)

    @staticmethod
    def APSControlLawMatrixButton(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['parent', 'member']

        """
        return exec_with_tcl('APSControlLawMatrixButton', *args, **kwargs)

    @staticmethod
    def APSControlLawSetEnergy(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['member']

        """
        return exec_with_tcl('APSControlLawSetEnergy', *args, **kwargs)

    @staticmethod
    def CheckLongBoosterTestValues(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: args
        APS parsed args: ['member', 'subDir']

        """
        return exec_with_tcl('CheckLongBoosterTestValues', *args, **kwargs)

    @staticmethod
    def APSSetupBoosterSingleTurnBPM(*args, **kwargs):
        """
        Location: controllaw.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSetupBoosterSingleTurnBPM', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeEnergyInfo(*args, **kwargs):
        """
        Location: APSMpSRChangeEnergy.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRChangeEnergyInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeEnergyDialog(*args, **kwargs):
        """
        Location: APSMpSRChangeEnergy.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRChangeEnergyDialog', *args, **kwargs)

    @staticmethod
    def APSMpChangeEnergyExcludeSR(*args, **kwargs):
        """
        Location: APSMpSRChangeEnergy.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpChangeEnergyExcludeSR', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeEnergy(*args, **kwargs):
        """
        Location: APSMpSRChangeEnergy.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRChangeEnergy', *args, **kwargs)

    @staticmethod
    def APSMathStats(*args, **kwargs):
        """
        Location: cautils.tcl
        TCL function args: val1 val2 args
        APS parsed args: None

        """
        return exec_with_tcl('APSMathStats', *args, **kwargs)

    @staticmethod
    def APScagetTextFromWaveform(*args, **kwargs):
        """
        Location: cautils.tcl
        Usage: APScagetTextFromWaveform
        [-pvName <string>]TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APScagetTextFromWaveform', *args, **kwargs)

    @staticmethod
    def APScaputTextToWaveform(*args, **kwargs):
        """
        Location: cautils.tcl
        Usage: APScaputTextToWaveform
        [-pvName <string>]
        [-text <string>]TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APScaputTextToWaveform', *args, **kwargs)

    @staticmethod
    def APScavget(*args, **kwargs):
        """
        Location: cautils.tcl
        Usage: APScavget
                [-pvName=<string>[,<string>...]]
                [-range=begin=<int>,end=<int>[,format=string][,interval=<int>]]
                [-floatformat=<printfString>]
                [-delimiter=<string>]
                [-labeled]
                [-noQuotes]
                [-embrace=start=<string>,end=<string>]
                [-cavputForm]
                [-statistics=number=<value>,pause=<value>[,format=[tagvalue][pretty][SDDS,file=<filename>]]]
                [-pendIoTime=<seconds>]
                [-repeat=number=<int>,pause=<seconds>[,average[,sigma]]]
                [-numerical]
                [-errorValue=<string>]
                [-excludeErrors]
                [-despike=[neighbors=<integer>][,passes=<integer>][,averageOf=<integer>][,threshold=<value>]]
                [-showwarnings] [-printErrors]TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APScavget', *args, **kwargs)

    @staticmethod
    def APScavput(*args, **kwargs):
        """
        Location: cautils.tcl
        Usage: APScavput
        [-pvName=<string>[=<value>][,<string>[=<value>]...]]
        [-range=begin=<int>,end=<int>[,format=string][,interval=<int>]]
        [-pendIoTime=<seconds>]
        [-floatformat=<printfString>]
        [-deltaMode[=factor=<value>]]
        [-ramp=step=<n>,pause=<sec>]
        [-numerical]
        [-blunderAhead[=silently]]TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APScavput', *args, **kwargs)

    @staticmethod
    def APSComputeMoments(*args, **kwargs):
        """
        Location: cautils.tcl
        TCL function args: args
        APS parsed args: ['valueList']

        """
        return exec_with_tcl('APSComputeMoments', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStartUpInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStartUp(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: ['conditioningTime', 'restoreFile', 'DCPS']

        """
        return exec_with_tcl('APSMpParBypassStartUp', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpParBypassTurnOnDCPSInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassTurnOnDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassTurnOnDCPS(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries']

        """
        return exec_with_tcl('APSMpParBypassTurnOnDCPS', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStandardizeInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStandardizeInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStandardize(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpParBypassStandardize', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStandardizeInitDialog(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStandardizeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpParBypassDegaussInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassDegaussInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassDegauss(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degaussTime', 'block', 'restoreFile']

        """
        return exec_with_tcl('APSMpParBypassDegauss', *args, **kwargs)

    @staticmethod
    def APSMpParBypassDegaussInitDialog(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassDegaussInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpParBypassCheckConditioning(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degauss', 'standardize']

        """
        return exec_with_tcl('APSMpParBypassCheckConditioning', *args, **kwargs)

    @staticmethod
    def APSMpParBypassWaitForConditioning(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassWaitForConditioning', *args, **kwargs)

    @staticmethod
    def APSMpParBypassRestoreFile(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile']

        """
        return exec_with_tcl('APSMpParBypassRestoreFile', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStopConditioningInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStopConditioningInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBypassStopConditioning(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBypassStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPARBypassClearApertureInfo(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARBypassClearApertureInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARBypassClearAperture(*args, **kwargs):
        """
        Location: APSMpBypassTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARBypassClearAperture', *args, **kwargs)

    @staticmethod
    def RFGUN_ShutdownWithPSInfo(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_ShutdownWithPSInfo', *args, **kwargs)

    @staticmethod
    def RFGUN_ShutdownWithPS(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['gun']

        """
        return exec_with_tcl('RFGUN_ShutdownWithPS', *args, **kwargs)

    @staticmethod
    def RFGUN_ShutdownInfo(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_ShutdownInfo', *args, **kwargs)

    @staticmethod
    def RFGUN_ShutdownDialog(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_ShutdownDialog', *args, **kwargs)

    @staticmethod
    def RFGUN_Shutdown(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['gun', 'L1VVC1', 'closeGateValves', 'suspendFixedCurrent', 'changeMode']

        """
        return exec_with_tcl('RFGUN_Shutdown', *args, **kwargs)

    @staticmethod
    def APSRFGUN_DetectSelectedGun(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRFGUN_DetectSelectedGun', *args, **kwargs)

    @staticmethod
    def APSRFGUN_UpdateStatusDescription(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['value']

        """
        return exec_with_tcl('APSRFGUN_UpdateStatusDescription', *args, **kwargs)

    @staticmethod
    def APSRFGUN_AbortAllActiveScripts(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRFGUN_AbortAllActiveScripts', *args, **kwargs)

    @staticmethod
    def APSRFGUN_SetCathodeHeaterStandbyCurrent(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['value', 'deviceList']

        """
        return exec_with_tcl('APSRFGUN_SetCathodeHeaterStandbyCurrent', *args, **kwargs)

    @staticmethod
    def APSRFGUN_SetCathodeHeaterCurrent(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['value', 'deviceList']

        """
        return exec_with_tcl('APSRFGUN_SetCathodeHeaterCurrent', *args, **kwargs)

    @staticmethod
    def APSRFGUN_ShutdownAlphaMagnet(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSRFGUN_ShutdownAlphaMagnet', *args, **kwargs)

    @staticmethod
    def APSRFGUN_StartDeguassAlphaMagnet(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSRFGUN_StartDeguassAlphaMagnet', *args, **kwargs)

    @staticmethod
    def APSRFGUN_TurnKickerOnOff(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'value', 'state']

        """
        return exec_with_tcl('APSRFGUN_TurnKickerOnOff', *args, **kwargs)

    @staticmethod
    def APSRFGUN_OpenCloseGateValve(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'value', 'group']

        """
        return exec_with_tcl('APSRFGUN_OpenCloseGateValve', *args, **kwargs)

    @staticmethod
    def APSRFGUN_RampDownLLRF(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'value']

        """
        return exec_with_tcl('APSRFGUN_RampDownLLRF', *args, **kwargs)

    @staticmethod
    def APSRFGUN_WaitForDegaussToComplete(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSRFGUN_WaitForDegaussToComplete', *args, **kwargs)

    @staticmethod
    def APSRFGUN_TurnOffTrimSupply(*args, **kwargs):
        """
        Location: RFGUN_Shutdown.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSRFGUN_TurnOffTrimSupply', *args, **kwargs)

    @staticmethod
    def APSStandardSetup(*args, **kwargs):
        """
        Location: APSStandardSetup.tcl
        Usage: APSStandardSetup
        Initializes a number of global variables and tcl/tk options.
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSStandardSetup', *args, **kwargs)

    @staticmethod
    def bell(*args, **kwargs):
        """
        Location: APSStandardSetup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('bell', *args, **kwargs)

    @staticmethod
    def redef_puts(*args, **kwargs):
        """
        Location: APSStandardSetup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('redef_puts', *args, **kwargs)

    @staticmethod
    def AlarmReviewSetup(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['customSystem']

        """
        return exec_with_tcl('AlarmReviewSetup', *args, **kwargs)

    @staticmethod
    def DereferenceAlarmLoggerData(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'newFile', 'timeMin', 'timeMax', 'timeName', 'isAlarmData']

        """
        return exec_with_tcl('DereferenceAlarmLoggerData', *args, **kwargs)

    @staticmethod
    def AlarmFileIsExplicit(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['fileName']

        """
        return exec_with_tcl('AlarmFileIsExplicit', *args, **kwargs)

    @staticmethod
    def AlarmFileIsIndexed(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['fileName']

        """
        return exec_with_tcl('AlarmFileIsIndexed', *args, **kwargs)

    @staticmethod
    def MakeIndexedControlNameList(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'listFile', 'updateIffOld']

        """
        return exec_with_tcl('MakeIndexedControlNameList', *args, **kwargs)

    @staticmethod
    def MakeAlarmHistograms(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['rootName', 'major', 'minor', 'invalid', 'timeBin', 'pvMatch', 'pvExclude', 'extension', 'noAlarm', 'versus', 'filterFiles', 'isAlarmData']

        """
        return exec_with_tcl('MakeAlarmHistograms', *args, **kwargs)

    @staticmethod
    def PlotAlarmHistograms(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['rootName', 'minor', 'major', 'invalid', 'separate', 'clipHead', 'title', 'extension', 'noAlarm', 'versus', 'topline', 'isAlarmData']

        """
        return exec_with_tcl('PlotAlarmHistograms', *args, **kwargs)

    @staticmethod
    def PrintAlarmLog(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['dataFile', 'outputFile', 'decode', 'pvMatch', 'pvExclude', 'major', 'minor', 'invalid', 'noAlarm', 'sortBy', 'title', 'topline', 'filterFiles', 'isAlarmData', 'intervalAnalysis', 'eventAnalysis']

        """
        return exec_with_tcl('PrintAlarmLog', *args, **kwargs)

    @staticmethod
    def SplitAlarmLoggerData(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'rootName', 'minor', 'major', 'invalid', 'updateIffOld', 'noAlarm', 'isAlarmData']

        """
        return exec_with_tcl('SplitAlarmLoggerData', *args, **kwargs)

    @staticmethod
    def CountAlarmOccurences(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['rootName', 'minor', 'major', 'invalid', 'indexFile', 'pvMatch', 'pvExclude', 'extension', 'countMin', 'sortBy', 'noAlarm', 'filterFiles', 'isAlarmData']

        """
        return exec_with_tcl('CountAlarmOccurences', *args, **kwargs)

    @staticmethod
    def PlotAlarmOccurences(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['rootName', 'minor', 'major', 'invalid', 'title', 'counts', 'extension', 'fixedScale', 'noAlarm', 'topline', 'isAlarmData']

        """
        return exec_with_tcl('PlotAlarmOccurences', *args, **kwargs)

    @staticmethod
    def PrintAlarmOccurences(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['rootName', 'minor', 'major', 'invalid', 'title', 'counts', 'extension', 'noAlarm', 'topline', 'isAlarmData']

        """
        return exec_with_tcl('PrintAlarmOccurences', *args, **kwargs)

    @staticmethod
    def MakeMatchOption(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['pvExclude', 'pvMatch']

        """
        return exec_with_tcl('MakeMatchOption', *args, **kwargs)

    @staticmethod
    def DecodeErrorMessage(*args, **kwargs):
        """
        Location: ReviewAlarmLog.tcl
        TCL function args: args
        APS parsed args: ['file']

        """
        return exec_with_tcl('DecodeErrorMessage', *args, **kwargs)

    @staticmethod
    def RFGUN_StartupInfo(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('RFGUN_StartupInfo', *args, **kwargs)

    @staticmethod
    def RFGUN_Startup(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['gun', 'SCRFile', 'high', 'L1', 'L2', 'L3', 'L4', 'L5', 'skipLLRFChecks']

        """
        return exec_with_tcl('RFGUN_Startup', *args, **kwargs)

    @staticmethod
    def APSLINACFindMostRecentSCRFile(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSLINACFindMostRecentSCRFile', *args, **kwargs)

    @staticmethod
    def APSRFGUN_ResetTimingSystem(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRFGUN_ResetTimingSystem', *args, **kwargs)

    @staticmethod
    def APSMpLSuspendResumeRunControl(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['value', 'name', 'group', 'deviceList', 'waitSeconds', 'port', 'executable']

        """
        return exec_with_tcl('APSMpLSuspendResumeRunControl', *args, **kwargs)

    @staticmethod
    def APSRFGUN_Macropulse(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRFGUN_Macropulse', *args, **kwargs)

    @staticmethod
    def APSRFGUN_CathodeHeaterPower(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'wattsMin', 'watts', 'wattsMax']

        """
        return exec_with_tcl('APSRFGUN_CathodeHeaterPower', *args, **kwargs)

    @staticmethod
    def APSMpLWaitForMinimumValue(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'group', 'operation', 'minValue', 'intervalLimit', 'intervalTime']

        """
        return exec_with_tcl('APSMpLWaitForMinimumValue', *args, **kwargs)

    @staticmethod
    def APSLINAC_LLRFOnOff(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['button', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_LLRFOnOff', *args, **kwargs)

    @staticmethod
    def APSLINAC_CheckModulatorCurrents(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'minValueList']

        """
        return exec_with_tcl('APSLINAC_CheckModulatorCurrents', *args, **kwargs)

    @staticmethod
    def APSLINAC_SetKlystronForwardPower(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'KLYFwdPwr']

        """
        return exec_with_tcl('APSLINAC_SetKlystronForwardPower', *args, **kwargs)

    @staticmethod
    def RestartLinacRFPhaseControllaw(*args, **kwargs):
        """
        Location: RFGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['SCRFile']

        """
        return exec_with_tcl('RestartLinacRFPhaseControllaw', *args, **kwargs)

    @staticmethod
    def APSApplication(*args, **kwargs):
        """
        Location: APSApplication.tcl
        Usage: APSApplication widget
        [-name <string>]
        [-version <string>]
        [-overview <string>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$widget.
        	userFrame
        	menu.file.menu
        	menu.help.menuTCL function args: widget args
        APS parsed args: ['name', 'version', 'overview', 'contextHelp', 'contextHelpImage']

        """
        return exec_with_tcl('APSApplication', *args, **kwargs)

    @staticmethod
    def APSSyncGeometryWithGrid(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSyncGeometryWithGrid', *args, **kwargs)

    @staticmethod
    def APSMenubar(*args, **kwargs):
        """
        Location: APSApplication.tcl
        Usage: APSMenubar widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string>]
        [-version <string>]
        [-overview <string>]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	file.menu
        	help.menuTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'version', 'overview', 'contextHelp', 'busyWidget']

        """
        return exec_with_tcl('APSMenubar', *args, **kwargs)

    @staticmethod
    def APSDrawGradient(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: win col1Str col2Str
        APS parsed args: None

        """
        return exec_with_tcl('APSDrawGradient', *args, **kwargs)

    @staticmethod
    def APSMenubarAddMenu(*args, **kwargs):
        """
        Location: APSApplication.tcl
        Usage: APSMenubarAddMenu widget
        [-parent <string>]
        [-text <string>]
        [-packOption <list>]
        [-underline 1]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	menuTCL function args: widget args
        APS parsed args: ['parent', 'text', 'underline', 'packOption', 'contextHelp']

        """
        return exec_with_tcl('APSMenubarAddMenu', *args, **kwargs)

    @staticmethod
    def APSListAllWidgets(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: root
        APS parsed args: None

        """
        return exec_with_tcl('APSListAllWidgets', *args, **kwargs)

    @staticmethod
    def APSPushHeadBindList(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: widget tag
        APS parsed args: None

        """
        return exec_with_tcl('APSPushHeadBindList', *args, **kwargs)

    @staticmethod
    def APSPopHeadBindList(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSPopHeadBindList', *args, **kwargs)

    @staticmethod
    def APSNearestContextHelpImage(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSNearestContextHelpImage', *args, **kwargs)

    @staticmethod
    def APSExit(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSExit', *args, **kwargs)

    @staticmethod
    def APSLogStart(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSLogStart', *args, **kwargs)

    @staticmethod
    def APSLogFinish(*args, **kwargs):
        """
        Location: APSApplication.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSLogFinish', *args, **kwargs)

    @staticmethod
    def APSGenerateLinacElegantParameters(*args, **kwargs):
        """
        Location: APSGenerateLinacElegantParameters.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGenerateLinacElegantParameters', *args, **kwargs)

    @staticmethod
    def APSButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSButton widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-text <string>]
        [-command <string>]
        [-highlight 1]
        [-size <string>] where <string> is small or medium (default)
        [-contextHelp <string>]

        [-contextHelpImage <filename>]
        [-highlightColor <color>]

        Creates	$parent$widget.
        	buttonTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'text', 'command', 'highlight', 'size', 'contextHelp', 'contextHelpImage', 'highlightColor', 'fastClick', 'gridPack', 'application', 'logcomm', 'width']

        """
        return exec_with_tcl('APSButton', *args, **kwargs)

    @staticmethod
    def APSLogButtonCommand(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['button', 'command', 'application', 'parameters']

        """
        return exec_with_tcl('APSLogButtonCommand', *args, **kwargs)

    @staticmethod
    def APSEnableButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSEnableButton widget
        	Sets button widget state to normal.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSEnableButton', *args, **kwargs)

    @staticmethod
    def APSDisableButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSDisableButton widget
        	Sets button widget state to disabled.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSDisableButton', *args, **kwargs)

    @staticmethod
    def APSChangeButtonHighlight(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSChangeButtonHighlight widget
        	[-highlight {0 | 1}]
        	[-highlightColor <color>]
        	Sets and unsets highlight state of a button.TCL function args: widget args
        APS parsed args: ['highlight', 'highlightColor']

        """
        return exec_with_tcl('APSChangeButtonHighlight', *args, **kwargs)

    @staticmethod
    def APSSecureButtonAlert(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['problem', 'command', 'text', 'allowedUsers']

        """
        return exec_with_tcl('APSSecureButtonAlert', *args, **kwargs)

    @staticmethod
    def APSSecureButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['allowedUsers', 'allowedSubnets']

        """
        return exec_with_tcl('APSSecureButton', *args, **kwargs)

    @staticmethod
    def APSLabeledEntry(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
         Usage: APSLabeledEntry widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-textVariable <string>]
        [-width <string>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]
        [-editButton 0]
        [-editTextWidth <value>]
        [-numberButtons 1]
        [-commandButton 1]
        [-enableVariable <string>]
        [-type {integer|real|alpha}]
        [-fileSelectButton 1]
        [-fileSelectPattern <string>]
        [-fileSelectDirectory 1]
        [-fileSelectValidity 0]
        [-buttonsOnLeft 1]
        Creates	$parent$widget.
        	label
        	entry
        	fileSelectButton (optional)TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'textVariable', 'width', 'contextHelp', 'contextHelpImage', 'numberButtons', 'type', 'gridPack', 'fileSelectButton', 'fileSelectPattern', 'fileSelectPath', 'fileSelectDirectory', 'commandButton', 'buttonsOnLeft', 'enableVariable', 'fileSelectValidity', 'editButton', 'fileSelectReverse']

        """
        return exec_with_tcl('APSLabeledEntry', *args, **kwargs)

    @staticmethod
    def APSCommandButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
         Usage: APSCommandButton widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-textVariable <string>]
        [-fileSelect <1|0>]
        [-selectRecent <1|0>]
        [-fileSelectPattern <string>]
        [-fileSelectDirectory <1|0>]

        Creates	$parent$widget.
        	arrow
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'contextHelp', 'contextHelpImage', 'gridPack', 'textVariable', 'fileSelectPattern', 'fileSelectDirectory', 'fileSelect', 'selectRecent', 'fileSelectValidity']

        """
        return exec_with_tcl('APSCommandButton', *args, **kwargs)

    @staticmethod
    def APSCommandButtonConfigure(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['W', 'commandButtonVar', 'fileSelectPattern', 'fileSelectDirectory', 'fileSelect', 'selectRecent', 'fileSelectValidity']

        """
        return exec_with_tcl('APSCommandButtonConfigure', *args, **kwargs)

    @staticmethod
    def APSCommandButtonExecute(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['command']

        """
        return exec_with_tcl('APSCommandButtonExecute', *args, **kwargs)

    @staticmethod
    def APSForceType(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: type name el op
        APS parsed args: None

        """
        return exec_with_tcl('APSForceType', *args, **kwargs)

    @staticmethod
    def APSEntryIncrementButtons(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSEntryIncrementButtons widget
        [-parent <string>]
        [-variableList <list>]
        [-description <string>]
        [-label <string>]
        [-gridPack <list>]
        TCL function args: widget args
        APS parsed args: ['parent', 'variableList', 'label', 'description', 'gridPack']

        """
        return exec_with_tcl('APSEntryIncrementButtons', *args, **kwargs)

    @staticmethod
    def APSIncrementEntryVariable(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['direction', 'variableList', 'incrementVariable']

        """
        return exec_with_tcl('APSIncrementEntryVariable', *args, **kwargs)

    @staticmethod
    def APSEntryMultiplicationButtons(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSEntryMultiplicationButtons widget
        [-parent <string>]
        [-variableList <list>]
        [-description <string>]
        [-label <string>]
        [-factorList <list>]
        [-gridPack <list>]
        TCL function args: widget args
        APS parsed args: ['parent', 'variableList', 'label', 'description', 'factorList', 'gridPack']

        """
        return exec_with_tcl('APSEntryMultiplicationButtons', *args, **kwargs)

    @staticmethod
    def APSMultiplyEntryVariable(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['variableList', 'factor']

        """
        return exec_with_tcl('APSMultiplyEntryVariable', *args, **kwargs)

    @staticmethod
    def APSLabeledEntryFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSLabeledEntryFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-variableList <list>]
        [-width <string>]
        [-orientation <string>] where <string> is horizontal or vertical (default)
        [-contextHelp <string>]
        [-contextHelpImage <filename>]
        [-type {integer|real|alpha}]

        Creates	$parent$widget.
        	label
        	frame.entry1
        	frame.entry2,...,frame.entry<n>
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'variableList', 'bg', 'labelColor', 'fg', 'font', 'width', 'orientation', 'contextHelp', 'contextHelpImage', 'type', 'gridPack']

        """
        return exec_with_tcl('APSLabeledEntryFrame', *args, **kwargs)

    @staticmethod
    def APSLabeledOutput(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSLabeledOutput widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-textVariable <string>]
        [-width <string>]
        [-backgroundcolor <color>]
        [-commandButton 1]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	entryTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'textVariable', 'width', 'contextHelp', 'contextHelpImage', 'gridPack', 'backgroundcolor', 'commandButton']

        """
        return exec_with_tcl('APSLabeledOutput', *args, **kwargs)

    @staticmethod
    def APSLabeledOutputFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSLabeledOutputFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-variableList <list>]
        [-width <string>]
        [-orientation <string>] where <string> is horizontal or vertical (default)
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	frame.entry1
        	frame.entry2,...,frame.entry<n>
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'variableList', 'width', 'orientation', 'contextHelp', 'contextHelpImage', 'gridPack']

        """
        return exec_with_tcl('APSLabeledOutputFrame', *args, **kwargs)

    @staticmethod
    def APSControlRadioButtonFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        usage: APSControlRadioButtonFrame widget
        [-state {0|1}]
        TCL function args: widget args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSControlRadioButtonFrame', *args, **kwargs)

    @staticmethod
    def APSRadioButtonEntryFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'variable', 'buttonList', 'valueList', 'orientation', 'contextHelp', 'contextHelpImage', 'commandList', 'relief', 'limitPerRow', 'gridPack', 'labelFont', 'entryWidth', 'entryVariableList']

        """
        return exec_with_tcl('APSRadioButtonEntryFrame', *args, **kwargs)

    @staticmethod
    def APSRadioButtonFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSRadioButtonFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-limitPerRow <number>]
        [-variable <string>]
        [-buttonList <list>]
        [-valueList <list>]
        [-orientation <string>] where <string> is horizontal or vertical
        [-commandList <list>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	frame
        	frame.button1
        	frame.button2,...
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'variable', 'buttonList', 'valueList', 'orientation', 'contextHelp', 'contextHelpImage', 'commandList', 'relief', 'limitPerRow', 'gridPack', 'labelFont']

        """
        return exec_with_tcl('APSRadioButtonFrame', *args, **kwargs)

    @staticmethod
    def APSCheckButtonFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSCheckButtonFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-limitPerRow <number>]
        [-buttonList <list>]
        [-variableList <list>]
        [-commandList <list>]
        	[-relief <string>]
        [-orientation <string>] where <string> is horizontal or vertical
        [-allNone 1][-toggle 1] adds All and None buttons
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	frame
        	frame.button1
        	frame.button2,...
        TCL function args:  widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'buttonList', 'variableList', 'orientation', 'allNone', 'commandList', 'contextHelp', 'contextHelpImage', 'relief', 'limitPerRow', 'gridPack', 'toggle']

        """
        return exec_with_tcl('APSCheckButtonFrame', *args, **kwargs)

    @staticmethod
    def APSCheckButtonEntryFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSCheckButtonFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-limitPerRow <number>]
        [-buttonList <list>]
        [-variableList <list>]
        [-commandList <list>]
        	[-relief <string>]
        [-orientation <string>]
        	[-entryVariableList <list of entry variables>]
        	[-entryWidth <value>] where <string> is horizontal or vertical
        [-allNone 1][-toggle 1] adds All and None buttons
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	frame
        	frame.button1
        	frame.button2,...
        If entry variableList provided, an entry will be created for each button.
        TCL function args:  widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'buttonList', 'variableList', 'orientation', 'allNone', 'commandList', 'contextHelp', 'contextHelpImage', 'relief', 'limitPerRow', 'gridPack', 'toggle', 'entryVariableList', 'entryWidth']

        """
        return exec_with_tcl('APSCheckButtonEntryFrame', *args, **kwargs)

    @staticmethod
    def APSFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-width <num>]
        [-height <num>]
        [-orientation <string>] where <string> is horizontal or vertical (default)
        [-geometry <string>]
        [-relief <string>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	label
        	frame
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'labelFont', 'name', 'width', 'height', 'orientation', 'geometry', 'contextHelp', 'contextHelpImage', 'relief', 'gridPack']

        """
        return exec_with_tcl('APSFrame', *args, **kwargs)

    @staticmethod
    def APSFrameGrid(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSFrameGrid widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-xList <list>]
        [-yList <list>]
        [-width <num>]
        [-height <num>]
        [-relief <string>]
        [-bd <string>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        If you supply just -xList or just -yList, it creates:
        $parent$widget.
        	<name1>,...,<namen> where names are from xList or yList

        If both -xList and -yList specified, it creates:
        $parent$widget.
        	<xname1>.<yname1>,...,<xname1>.<ynamen>
        	...
        	<xnamen>.<yname1>,...,<xnamen>.<ynamen>
        TCL function args: widget args
        APS parsed args: ['parent', 'xList', 'yList', 'packOption', 'noPack', 'width', 'height', 'relief', 'bd', 'contextHelp', 'contextHelpImage', 'label']

        """
        return exec_with_tcl('APSFrameGrid', *args, **kwargs)

    @staticmethod
    def APSLabel(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSLabel widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-text <string>]
        [-textVariable <string>]
        [-width <string>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	labelTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'text', 'textVariable', 'width', 'contextHelp', 'contextHelpImage', 'gridPack', 'fgColor', 'bgColor', 'style', 'font']

        """
        return exec_with_tcl('APSLabel', *args, **kwargs)

    @staticmethod
    def APSSetStateButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['variable', 'state']

        """
        return exec_with_tcl('APSSetStateButton', *args, **kwargs)

    @staticmethod
    def APSToggleStateButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['variable']

        """
        return exec_with_tcl('APSToggleStateButton', *args, **kwargs)

    @staticmethod
    def APSStateButton(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSStateButton widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-text <string>]
        [-variable <string>]
        [-command <string>]
        [-highlight 1]
        [-size <string>] where <string> is small or medium (default)
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.
        	buttonTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'text', 'command', 'highlight', 'size', 'contextHelp', 'contextHelpImage', 'variable', 'highlightColorList', 'gridPack']

        """
        return exec_with_tcl('APSStateButton', *args, **kwargs)

    @staticmethod
    def APSComboboxFrame(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        Usage: APSComboboxFrame widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-gridPack <list>]
        [-label <string>]
        [-textVariable <string>]
        [-textFont <string>]
        [-labelFont <string>]
        [-editable <1|0>]
        [-callback <string>]
        [-height <value>]
        [-width <value>]
        [-contextHelp <string>]
        [-contextHelpImage <filename>]

        Creates	$parent$widget.cbTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'label', 'textVariable', 'editable', 'height', 'width', 'contextHelp', 'contextHelpImage', 'gridPack', 'itemList', 'callback', 'labelFont', 'textFont', 'maxWidth']

        """
        return exec_with_tcl('APSComboboxFrame', *args, **kwargs)

    @staticmethod
    def APSComboboxRunCallback(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['callback', 'textFont', 'editable', 'textVariable']

        """
        return exec_with_tcl('APSComboboxRunCallback', *args, **kwargs)

    @staticmethod
    def APSMakeLabelList(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['labelMaker', 'arrayName', 'callback', 'columnList', 'trim', 'filename', 'page']

        """
        return exec_with_tcl('APSMakeLabelList', *args, **kwargs)

    @staticmethod
    def APSPVFilterWidget(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'fileName', 'rootname', 'snapDir', 'limitPerRow', 'showSetpointFilter']

        """
        return exec_with_tcl('APSPVFilterWidget', *args, **kwargs)

    @staticmethod
    def APSBar(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
         Usage: APSBar widget
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-width <integer>]
        [-height <integer>]
        [-min <real>]
        [-max <real>]
        [-value <real>]
        [-color <string>]
        [-label <string>]
        [-direction <right|left|up|down>]

        Creates	$parent$widget.
        	bar

        Returns $parent$widget
        to be used with APSBarAdjust
        TCL function args: widget args
        APS parsed args: ['parent', 'width', 'height', 'min', 'max', 'color', 'value', 'packOption', 'noPack', 'background', 'direction', 'label']

        """
        return exec_with_tcl('APSBar', *args, **kwargs)

    @staticmethod
    def APSBarAdjust(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
         Usage: APSBarAdjust widget
        [-value <real>]
        [-min <real>]
        [-max <real>]

        Adjusts the length of the bar.
        Please see APSBar
        for more information.
        TCL function args: widget args
        APS parsed args: ['value', 'min', 'max']

        """
        return exec_with_tcl('APSBarAdjust', *args, **kwargs)

    @staticmethod
    def APSLargeStringEditor(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['textVariable', 'name', 'widget', 'noLineFeed', 'width']

        """
        return exec_with_tcl('APSLargeStringEditor', *args, **kwargs)

    @staticmethod
    def APSUpdateTextWidgetVariable(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: args
        APS parsed args: ['widget', 'textVariable', 'noLineFeed']

        """
        return exec_with_tcl('APSUpdateTextWidgetVariable', *args, **kwargs)

    @staticmethod
    def shuffle(*args, **kwargs):
        """
        Location: APSBasicWidgets.tcl
        TCL function args: data
        APS parsed args: None

        """
        return exec_with_tcl('shuffle', *args, **kwargs)

    @staticmethod
    def APSSRConfigOrbitCorrection(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'rootname', 'fileFrame', 'buttonOrientation', 'includeP0s', 'includeIDs', 'includeBMs']

        """
        return exec_with_tcl('APSSRConfigOrbitCorrection', *args, **kwargs)

    @staticmethod
    def APSSRInstallOrbCorrFiles(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'application', 'booster']

        """
        return exec_with_tcl('APSSRInstallOrbCorrFiles', *args, **kwargs)

    @staticmethod
    def APSUpdateTimeRegion(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname']

        """
        return exec_with_tcl('APSUpdateTimeRegion', *args, **kwargs)

    @staticmethod
    def APSFileSelectWidget(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'variable', 'contextHelp', 'pathVariableList', 'filter', 'filterVariableList', 'mode', 'incrementButtons', 'noPack', 'noSelect', 'label', 'width']

        """
        return exec_with_tcl('APSFileSelectWidget', *args, **kwargs)

    @staticmethod
    def APSPickFileFromDir(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['pathVariableList', 'filterVariableList', 'type', 'filter', 'default', 'directory']

        """
        return exec_with_tcl('APSPickFileFromDir', *args, **kwargs)

    @staticmethod
    def APSSRGenerateOrbCorrFiles(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['configFile', 'plane', 'outputRoot', 'referenceMatrix', 'generate', 'install', 'rootname', 'singularValues', 'SVDanalysis', 'compensationConfigFile', 'deleteVectors', 'tikhonovFilter', 'tikhonovSVN', 'tikhonovBeta', 'tikhonovType']

        """
        return exec_with_tcl('APSSRGenerateOrbCorrFiles', *args, **kwargs)

    @staticmethod
    def APSIncrementConfigFilename(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['variable', 'amount']

        """
        return exec_with_tcl('APSIncrementConfigFilename', *args, **kwargs)

    @staticmethod
    def APSSRWriteOrbitCorrectionConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'filename', 'description', 'interactive', 'includeP0s', 'includeIDs', 'includeBMs', 'configName']

        """
        return exec_with_tcl('APSSRWriteOrbitCorrectionConfig', *args, **kwargs)

    @staticmethod
    def APSCountSRConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'sectorCount', 'itemList', 'missingList', 'sectorList']

        """
        return exec_with_tcl('APSCountSRConfig', *args, **kwargs)

    @staticmethod
    def APSWriteSRConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'sectorCount', 'filename', 'PVTypeList', 'nameTypeList', 'updateDatabase', 'suffixLists', 'description', 'interactive', 'booster', 'sectorList']

        """
        return exec_with_tcl('APSWriteSRConfig', *args, **kwargs)

    @staticmethod
    def APSReadOrbitCorrectionConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'filename', 'logic', 'includeP0s', 'includeIDs', 'includeBMs', 'booster', 'sectorCount', 'nameTypeList', 'application']

        """
        return exec_with_tcl('APSReadOrbitCorrectionConfig', *args, **kwargs)

    @staticmethod
    def APSReadSRConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'sectorCount', 'filename', 'logic', 'nameTypeList', 'knownSuffixes', 'missingList', 'booster', 'sectorList', 'application']

        """
        return exec_with_tcl('APSReadSRConfig', *args, **kwargs)

    @staticmethod
    def APSSRMonitorCheckButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['rootname', 'parent', 'orientation', 'packOption', 'includeP0s', 'includeIDs', 'includeBMs', 'sectorControl', 'missingList', 'missingListVar', 'noLabel', 'BP5Only']

        """
        return exec_with_tcl('APSSRMonitorCheckButtons', *args, **kwargs)

    @staticmethod
    def APSSRCorrectorCheckButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['rootname', 'plane', 'parent', 'orientation', 'sectorControl', 'packOption', 'missingList', 'noLabel', 'missingListVar', 'globalButtons']

        """
        return exec_with_tcl('APSSRCorrectorCheckButtons', *args, **kwargs)

    @staticmethod
    def APSSRSectorUnsetMissing(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'missingList', 'missingListVar', 'sectorList']

        """
        return exec_with_tcl('APSSRSectorUnsetMissing', *args, **kwargs)

    @staticmethod
    def APSSRSectorButtonsClicked(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['widget', 'var', 'selectcolor']

        """
        return exec_with_tcl('APSSRSectorButtonsClicked', *args, **kwargs)

    @staticmethod
    def APSSRSectorButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'rootname', 'label', 'description', 'itemList', 'globalButtons', 'command', 'sectorCount', 'onePerSector', 'sectorControl', 'missingList', 'missingListVar', 'packOption', 'orientation', 'itemLabelList', 'includeWeights', 'includeDespike', 'sectorList', 'color0', 'separateCountButton', 'allButtons']

        """
        return exec_with_tcl('APSSRSectorButtons', *args, **kwargs)

    @staticmethod
    def APSSRSectorGlobalButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'rootname', 'sectorCount', 'description', 'itemList', 'missingList', 'orientation', 'missingListVar', 'sectorList', 'separateCountButton']

        """
        return exec_with_tcl('APSSRSectorGlobalButtons', *args, **kwargs)

    @staticmethod
    def APSSetSRSectorButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rootname', 'sectorCount', 'itemList', 'missingList', 'missingListVar', 'sectorList']

        """
        return exec_with_tcl('APSSetSRSectorButtons', *args, **kwargs)

    @staticmethod
    def APSSRSectorPositionButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'sectorWidget', 'description', 'itemList', 'rootname', 'sectorCount', 'missingList', 'missingListVar', 'orientation', 'sectorControl', 'sectorList', 'maxSectorLen']

        """
        return exec_with_tcl('APSSRSectorPositionButtons', *args, **kwargs)

    @staticmethod
    def APSSRSectorsToggle(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['widget', 'rootname', 'sectorCount', 'itemList', 'missingList', 'toggleVar', 'missingListVar', 'sectorList']

        """
        return exec_with_tcl('APSSRSectorsToggle', *args, **kwargs)

    @staticmethod
    def APSSRSectorTogglePosition(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['item', 'rootname', 'sectorCount', 'missingList', 'toggleVar', 'missingListVar', 'sectorList']

        """
        return exec_with_tcl('APSSRSectorTogglePosition', *args, **kwargs)

    @staticmethod
    def APSSRItemTogglePosition(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['sector', 'itemList', 'rootname', 'missingList', 'toggleVar', 'missingListVar']

        """
        return exec_with_tcl('APSSRItemTogglePosition', *args, **kwargs)

    @staticmethod
    def APSGetIDXRayBPMList(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane', 'sddsOutput']

        """
        return exec_with_tcl('APSGetIDXRayBPMList', *args, **kwargs)

    @staticmethod
    def APSGetIDXRayEqnList(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSGetIDXRayEqnList', *args, **kwargs)

    @staticmethod
    def APSGetBMXRayBPMList(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane', 'sddsOutput', 'okForDCOrbitCorrection']

        """
        return exec_with_tcl('APSGetBMXRayBPMList', *args, **kwargs)

    @staticmethod
    def APSGetBMXRayEqnList(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSGetBMXRayEqnList', *args, **kwargs)

    @staticmethod
    def APSGetMissingBPMList(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSGetMissingBPMList', *args, **kwargs)

    @staticmethod
    def APSSRConfigWeightDialog(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['weight', 'despike', 'item']

        """
        return exec_with_tcl('APSSRConfigWeightDialog', *args, **kwargs)

    @staticmethod
    def APSSRConfigPlaneOrbitCorrection(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'rootname', 'fileFrame', 'buttonOrientation', 'plane', 'application', 'includeP0s', 'includeIDs', 'includeBMs']

        """
        return exec_with_tcl('APSSRConfigPlaneOrbitCorrection', *args, **kwargs)

    @staticmethod
    def APSSRWritePlaneOrbitCorrectionConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'filename', 'description', 'interactive', 'includeP0s', 'includeIDs', 'includeBMs', 'configName', 'plane', 'BP5Only', 'booster', 'sectorCount', 'sectorList']

        """
        return exec_with_tcl('APSSRWritePlaneOrbitCorrectionConfig', *args, **kwargs)

    @staticmethod
    def APSSRGetBadOrbitDevices(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane', 'application', 'device']

        """
        return exec_with_tcl('APSSRGetBadOrbitDevices', *args, **kwargs)

    @staticmethod
    def APSRescanBadOrbitDevices(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['plane', 'rootname', 'application', 'booster']

        """
        return exec_with_tcl('APSRescanBadOrbitDevices', *args, **kwargs)

    @staticmethod
    def APSSRFreqGenerateOrbCorrFiles(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['configFile', 'plane', 'outputRoot', 'referenceMatrix', 'generate', 'install', 'rootname', 'singularValues', 'SVDanalysis', 'deleteVectors', 'bpmSuffix', 'tikhonovFilter', 'tikhonovSVN', 'tikhonovBeta', 'tikhonovType']

        """
        return exec_with_tcl('APSSRFreqGenerateOrbCorrFiles', *args, **kwargs)

    @staticmethod
    def APSBoosterGenerateOrbCorrFiles(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['configFile', 'plane', 'outputRoot', 'referenceMatrix', 'generate', 'install', 'rootname', 'singularValues', 'SVDanalysis', 'deleteVectors', 'tikhonovFilter', 'tikhonovSVN', 'tikhonovBeta', 'tikhonovType']

        """
        return exec_with_tcl('APSBoosterGenerateOrbCorrFiles', *args, **kwargs)

    @staticmethod
    def APSBoosterPlaneOrbitConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: widget args
        APS parsed args: ['rootname', 'bpm', 'corrector', 'plane', 'bpmItemList', 'bpmItemLabelList', 'corrItemList', 'corrItemLabelList', 'parent', 'fileFrame', 'application', 'bpmCorrTogether']

        """
        return exec_with_tcl('APSBoosterPlaneOrbitConfig', *args, **kwargs)

    @staticmethod
    def APSGetVariableNameOfSRSectorButtons(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'sectorList', 'itemList', 'rootname']

        """
        return exec_with_tcl('APSGetVariableNameOfSRSectorButtons', *args, **kwargs)

    @staticmethod
    def APSWriteSelectionArrayConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'sectorCount', 'filename', 'NameTypeList', 'PVTypeList', 'suffixLists', 'sectorList']

        """
        return exec_with_tcl('APSWriteSelectionArrayConfig', *args, **kwargs)

    @staticmethod
    def APSReadSelectionArrayConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'sectorCount', 'suffixList', 'filename', 'mode', 'sectorList']

        """
        return exec_with_tcl('APSReadSelectionArrayConfig', *args, **kwargs)

    @staticmethod
    def APSUpdateConfigDescriptionDatabase(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['dataDir', 'newConfig', 'plane', 'linkConfig', 'update', 'booster']

        """
        return exec_with_tcl('APSUpdateConfigDescriptionDatabase', *args, **kwargs)

    @staticmethod
    def APSUpdateBoosterOrbitCorrectionConfig(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['dataDir', 'newConfig']

        """
        return exec_with_tcl('APSUpdateBoosterOrbitCorrectionConfig', *args, **kwargs)

    @staticmethod
    def ComputeBoosterBPMTiming(*args, **kwargs):
        """
        Location: SRConfig.tcl
        TCL function args: args
        APS parsed args: ['startRamp']

        """
        return exec_with_tcl('ComputeBoosterBPMTiming', *args, **kwargs)

    @staticmethod
    def APSPARLETDefaultEnergy(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPARLETDefaultEnergy', *args, **kwargs)

    @staticmethod
    def APSMpPARStartUpInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARStartUp(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['rfSystems', 'restoreDCPS', 'useSystemReference']

        """
        return exec_with_tcl('APSMpPARStartUp', *args, **kwargs)

    @staticmethod
    def APSMpPARStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnPulsedPSInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnPulsedPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnPulsedPS(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile']

        """
        return exec_with_tcl('APSMpPARTurnOnPulsedPS', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnPulsedPSInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnPulsedPSInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnDCPS(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnDCPS', *args, **kwargs)

    @staticmethod
    def APSMpPARSextStandardizeInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARSextStandardizeInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARSextStandardize(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'restoreFile', 'block', 'excludeS1']

        """
        return exec_with_tcl('APSMpPARSextStandardize', *args, **kwargs)

    @staticmethod
    def APSMpPARSextStandardizeInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARSextStandardizeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARConditionInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARConditionInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARConditionInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARConditionInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARCondition(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'conditioningTime', 'restoreFile', 'dipoleAndQuads', 'sextupoles', 'correctors']

        """
        return exec_with_tcl('APSMpPARCondition', *args, **kwargs)

    @staticmethod
    def APSMpPARStandardizeBQInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStandardizeBQInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARStandardizeBQInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStandardizeBQInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARStandardizeBQ(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'conditioningTime', 'Q1', 'Q2', 'Q3BP', 'Q4', 'BM', 'restoreFile', 'block']

        """
        return exec_with_tcl('APSMpPARStandardizeBQ', *args, **kwargs)

    @staticmethod
    def APSMpWarmupKickersInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpWarmupKickersInfo', *args, **kwargs)

    @staticmethod
    def APSMpWarmupKickers(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['kickerList']

        """
        return exec_with_tcl('APSMpWarmupKickers', *args, **kwargs)

    @staticmethod
    def APSSelectKickersNeedingWarmUp(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['kickerList']

        """
        return exec_with_tcl('APSSelectKickersNeedingWarmUp', *args, **kwargs)

    @staticmethod
    def APSMpTurnOnSeptum(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries']

        """
        return exec_with_tcl('APSMpTurnOnSeptum', *args, **kwargs)

    @staticmethod
    def APSMpPARStopConditioningInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStopConditioningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARStopConditioning(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpStopConditioning(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['magnetList']

        """
        return exec_with_tcl('APSMpStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPARDegauss(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['block', 'degaussTime', 'excludeSDSF']

        """
        return exec_with_tcl('APSMpPARDegauss', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRfInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRfInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'rf1', 'rf12', 'rf1UseSystemReference', 'rf12UseSystemReference', 'useSystemReference', 'rf1amp', 'rf12amp']

        """
        return exec_with_tcl('APSMpPARTurnOnRf', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRfInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRfInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf1Info(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRf1Info', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf1(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'rf1amp', 'useSystemReference', 'rf12amp']

        """
        return exec_with_tcl('APSMpPARTurnOnRf1', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf1InitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRf1InitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf12Info(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRf12Info', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf12(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'rf12amp', 'useSystemReference', 'rf1amp']

        """
        return exec_with_tcl('APSMpPARTurnOnRf12', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRf12InitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTurnOnRf12InitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARSwitchRfSystem(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['system', 'amp']

        """
        return exec_with_tcl('APSMpPARSwitchRfSystem', *args, **kwargs)

    @staticmethod
    def APSMpPARTurnOnRfSystem(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'system', 'useSystemReference', 'rf1amp', 'rf12amp', 'ampSwitched']

        """
        return exec_with_tcl('APSMpPARTurnOnRfSystem', *args, **kwargs)

    @staticmethod
    def APSSearchAssociateListForValue(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['value', 'list', 'notvalue']

        """
        return exec_with_tcl('APSSearchAssociateListForValue', *args, **kwargs)

    @staticmethod
    def APSMpPARClearAperture(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries']

        """
        return exec_with_tcl('APSMpPARClearAperture', *args, **kwargs)

    @staticmethod
    def APSMpPARTuneRfCavityInfo(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTuneRfCavityInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARTuneRfCavity(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: args
        APS parsed args: ['system', 'settlingTime', 'averages', 'threshold', 'stepSize']

        """
        return exec_with_tcl('APSMpPARTuneRfCavity', *args, **kwargs)

    @staticmethod
    def APSMpPARTuneRfCavityInitDialog(*args, **kwargs):
        """
        Location: APSMpPARTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARTuneRfCavityInitDialog', *args, **kwargs)

    @staticmethod
    def APSInfoWindow(*args, **kwargs):
        """
        Location: APSInfoWindow.tcl
        Usage: APSInfoWindow widget
         [-parent <string>]
         [-noPack 1]
         [-packOption <list>]
         [-name <string]
         [-infoMessage <string>]
         [-modal 1]
         [-copyable 1]
         [-width <chars>]
         [-contextHelp <string>]

         Creates	$parent$widget.
         	msg
         	buttonRow.ok.button
        TCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'infoMessage', 'infoImage', 'contextHelp', 'modal', 'width', 'copyable']

        """
        return exec_with_tcl('APSInfoWindow', *args, **kwargs)

    @staticmethod
    def APSQueryToProceed(*args, **kwargs):
        """
        Location: APSMultipleChoice.tcl
        Usage: APSQueryToProceed -message <string>
         Returns 1 if the user elects to proceed, otherwise returns 0.TCL function args: args
        APS parsed args: ['message']

        """
        return exec_with_tcl('APSQueryToProceed', *args, **kwargs)

    @staticmethod
    def APSMultipleChoice(*args, **kwargs):
        """
        Location: APSMultipleChoice.tcl
        Usage: APSMultipleChoice widget
        -question <string>
        -labelList <list>
        -returnList <list>
        [-parent <string>]
        [-noPack 1]
        [-packOption <list>]
        [-name <string]
        [-announceWorkstation <0|1>]
        [-toneType <default|sr|linac|booster|par>]
        [-contextHelp <string>]

        Creates	$parent$widget.
        	msg
        	buttonRow.*.button
        Returns a string valueTCL function args: widget args
        APS parsed args: ['parent', 'noPack', 'packOption', 'name', 'contextHelp', 'width', 'question', 'labelList', 'returnList', 'type', 'beep', 'announceWorkstation', 'toneType', 'imageFile', 'modal']

        """
        return exec_with_tcl('APSMultipleChoice', *args, **kwargs)

    @staticmethod
    def PCGUN_ChangeTimingInfo(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ChangeTimingInfo', *args, **kwargs)

    @staticmethod
    def PCGUN_ChangeTimingDialog(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ChangeTimingDialog', *args, **kwargs)

    @staticmethod
    def PCGUN_ChangeTiming(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ChangeTiming', *args, **kwargs)

    @staticmethod
    def PCGUN_StartupWithPSInfo(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_StartupWithPSInfo', *args, **kwargs)

    @staticmethod
    def PCGUN_StartupWithPS(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['turnOnList', 'conditionList', 'SCRFile', 'PCGUN', 'PowerSupplies', 'L1', 'L2', 'L3', 'L4', 'L5', 'cycles']

        """
        return exec_with_tcl('PCGUN_StartupWithPS', *args, **kwargs)

    @staticmethod
    def PCGUN_StartupWithPSPackProc(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_StartupWithPSPackProc', *args, **kwargs)

    @staticmethod
    def PCGUN_StartupInfo(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_StartupInfo', *args, **kwargs)

    @staticmethod
    def PCGUN_StartupDialog(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_StartupDialog', *args, **kwargs)

    @staticmethod
    def PCGUN_Startup(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'SCRFile']

        """
        return exec_with_tcl('PCGUN_Startup', *args, **kwargs)

    @staticmethod
    def APSLINAC_IncreaseAttnCtrl(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'minAttenuation']

        """
        return exec_with_tcl('APSLINAC_IncreaseAttnCtrl', *args, **kwargs)

    @staticmethod
    def APSPCGUN_CheckVacuum(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'maxValueList']

        """
        return exec_with_tcl('APSPCGUN_CheckVacuum', *args, **kwargs)

    @staticmethod
    def APSPCGUN_CheckThermocouples(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'maxTemp', 'minTemp', 'tempRange']

        """
        return exec_with_tcl('APSPCGUN_CheckThermocouples', *args, **kwargs)

    @staticmethod
    def APSPCGUN_SetMagnetCurrent(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'value']

        """
        return exec_with_tcl('APSPCGUN_SetMagnetCurrent', *args, **kwargs)

    @staticmethod
    def APSPCGUN_ReadRFSwitch1(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['desiredState']

        """
        return exec_with_tcl('APSPCGUN_ReadRFSwitch1', *args, **kwargs)

    @staticmethod
    def APSLINAC_CheckLLRFStatus(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['desiredState', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_CheckLLRFStatus', *args, **kwargs)

    @staticmethod
    def APSLINAC_CheckLLStatus(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['desiredState', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_CheckLLStatus', *args, **kwargs)

    @staticmethod
    def APSLINAC_SetInjectionTimingTrigger(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSLINAC_SetInjectionTimingTrigger', *args, **kwargs)

    @staticmethod
    def APSLINAC_SetBeamTriggerRate(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSLINAC_SetBeamTriggerRate', *args, **kwargs)

    @staticmethod
    def APSPCGUN_SetLaserTrigger(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSPCGUN_SetLaserTrigger', *args, **kwargs)

    @staticmethod
    def APSLINAC_CheckTimingSource(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['desiredState', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_CheckTimingSource', *args, **kwargs)

    @staticmethod
    def APSLINAC_SetTimingSource(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_SetTimingSource', *args, **kwargs)

    @staticmethod
    def APSLMOCS_CheckSequence3Status(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['desiredState', 'deviceList']

        """
        return exec_with_tcl('APSLMOCS_CheckSequence3Status', *args, **kwargs)

    @staticmethod
    def APSPCGUN_SetTimingForPCGun(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPCGUN_SetTimingForPCGun', *args, **kwargs)

    @staticmethod
    def APSPCGUN_SetTimingForRFGun(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPCGUN_SetTimingForRFGun', *args, **kwargs)

    @staticmethod
    def APSPCGUN_SetPCGunTriggerOnOff(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state']

        """
        return exec_with_tcl('APSPCGUN_SetPCGunTriggerOnOff', *args, **kwargs)

    @staticmethod
    def APSLINAC_SetPhaseControlMode(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['state', 'deviceList']

        """
        return exec_with_tcl('APSLINAC_SetPhaseControlMode', *args, **kwargs)

    @staticmethod
    def PCGUN_ModeSwitchInfo(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ModeSwitchInfo', *args, **kwargs)

    @staticmethod
    def PCGUN_ModeSwitchDialog(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ModeSwitchDialog', *args, **kwargs)

    @staticmethod
    def PCGUN_ModeSwitchPackProc(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('PCGUN_ModeSwitchPackProc', *args, **kwargs)

    @staticmethod
    def PCGUN_ModeSwitch(*args, **kwargs):
        """
        Location: PCGUN_Startup.tcl
        TCL function args: args
        APS parsed args: ['SCRFile', 'conditionList', 'cycles', 'saveSCR']

        """
        return exec_with_tcl('PCGUN_ModeSwitch', *args, **kwargs)

    @staticmethod
    def APSReadHPScopeMeasSpec(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: ['file', 'variableRootname']

        """
        return exec_with_tcl('APSReadHPScopeMeasSpec', *args, **kwargs)

    @staticmethod
    def APSMpDoHPScopeMeas(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: ['dataDir', 'rootname', 'statusCallback', 'doPrompt', 'userDescription', 'doGzip', 'clipLastHalf', 'continuous', 'abortVariable']

        """
        return exec_with_tcl('APSMpDoHPScopeMeas', *args, **kwargs)

    @staticmethod
    def APSProcessKickerParameters(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: ['file']

        """
        return exec_with_tcl('APSProcessKickerParameters', *args, **kwargs)

    @staticmethod
    def APSReadScopeScalars(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: ['dataDir', 'scopeChannel', 'scopeID']

        """
        return exec_with_tcl('APSReadScopeScalars', *args, **kwargs)

    @staticmethod
    def APSMpDoHP9000ScopeMeas(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: ['dataDir', 'rootname', 'statusCallback', 'doPrompt', 'userDescription', 'doGzip', 'clipLastHalf', 'continuous', 'abortVariable', 'ring']

        """
        return exec_with_tcl('APSMpDoHP9000ScopeMeas', *args, **kwargs)

    @staticmethod
    def APSMpCollectHP9000ScopeData(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCollectHP9000ScopeData', *args, **kwargs)

    @staticmethod
    def APSCollectHP9000Data(*args, **kwargs):
        """
        Location: APSMpHP54542AScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCollectHP9000Data', *args, **kwargs)

    @staticmethod
    def APSMpPARScopeMeasPMsInfo(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARScopeMeasPMsInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARScopeMeasPMs(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARScopeMeasPMs', *args, **kwargs)

    @staticmethod
    def APSMpPARScopeMeasRFInfo(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARScopeMeasRFInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARScopeMeasRF(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARScopeMeasRF', *args, **kwargs)

    @staticmethod
    def APSPARScopeMeasPMsSetup(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPARScopeMeasPMsSetup', *args, **kwargs)

    @staticmethod
    def APSPARScopeMeasRFSetup(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPARScopeMeasRFSetup', *args, **kwargs)

    @staticmethod
    def APSPARScopeMeasTopUpKickersSetup(*args, **kwargs):
        """
        Location: APSMpPARScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPARScopeMeasTopUpKickersSetup', *args, **kwargs)

    @staticmethod
    def APSMpBRFStartUpInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFStartUp(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'tempCheck', 'doRestore', 'finalPower']

        """
        return exec_with_tcl('APSMpBRFStartUp', *args, **kwargs)

    @staticmethod
    def APSMpBRFStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandbyInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandby(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'tempCheck', 'doRestore']

        """
        return exec_with_tcl('APSMpBRFStandby', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandbyInitDialog(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStandbyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandbyInitDialogNoSCR(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStandbyInitDialogNoSCR', *args, **kwargs)

    @staticmethod
    def APSMpBRFBringUpToStandbyInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFBringUpToStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFBringUpToStandby(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'tempCheck', 'doRestore', 'noPrompt', 'finalVoltage', 'waveformFile']

        """
        return exec_with_tcl('APSMpBRFBringUpToStandby', *args, **kwargs)

    @staticmethod
    def APSMpBRFBringUpToStandbyInitDialog(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFBringUpToStandbyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBRFFullPowerFromStandbyInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFFullPowerFromStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFFullPowerFromStandby(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['tempCheck', 'finalPower', 'noPrompt', 'cav1phase', 'cav2phase', 'cav3phase', 'cav4phase', 'cav1setpoint', 'cav2setpoint', 'cav3setpoint', 'cav4setpoint', 'finalCurrent']

        """
        return exec_with_tcl('APSMpBRFFullPowerFromStandby', *args, **kwargs)

    @staticmethod
    def APSMpBRFFullPowerFromStandbyInitDialog(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFFullPowerFromStandbyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandbyFromFullPower(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStandbyFromFullPower', *args, **kwargs)

    @staticmethod
    def APSMpBRFStandbyFromFullPowerInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFStandbyFromFullPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFShutdownFromStandby(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFShutdownFromStandby', *args, **kwargs)

    @staticmethod
    def APSMpBRFShutdownFromStandbyInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFShutdownFromStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFShutDown(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFShutDown', *args, **kwargs)

    @staticmethod
    def APSMpBRFShutDownDialog(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFShutDownDialog', *args, **kwargs)

    @staticmethod
    def APSMpBRFShutDownInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFShutDownInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFTouchUpInfo(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTouchUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpBRFTouchUp(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTouchUp', *args, **kwargs)

    @staticmethod
    def APSMpBRFCheckRFRampSignal(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFCheckRFRampSignal', *args, **kwargs)

    @staticmethod
    def APSMpBRFCheckKalmusAmpOutputSignal(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['targetArea', 'maxDiff']

        """
        return exec_with_tcl('APSMpBRFCheckKalmusAmpOutputSignal', *args, **kwargs)

    @staticmethod
    def APSMpBRFCheckCavitySumSignal(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['targetArea', 'maxDiff', 'fullPower']

        """
        return exec_with_tcl('APSMpBRFCheckCavitySumSignal', *args, **kwargs)

    @staticmethod
    def APSMpBRFCheckInjectionPower(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target']

        """
        return exec_with_tcl('APSMpBRFCheckInjectionPower', *args, **kwargs)

    @staticmethod
    def APSMpBRFSystemIsOn(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['level']

        """
        return exec_with_tcl('APSMpBRFSystemIsOn', *args, **kwargs)

    @staticmethod
    def APSMpBRFManualPrepCheck(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFManualPrepCheck', *args, **kwargs)

    @staticmethod
    def APSMpBRFManualPrep(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFManualPrep', *args, **kwargs)

    @staticmethod
    def APSMpBRFHVPSReset(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFHVPSReset', *args, **kwargs)

    @staticmethod
    def APSMpBRFACISReset(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFACISReset', *args, **kwargs)

    @staticmethod
    def APSMpBRFTurnOnBeam(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTurnOnBeam', *args, **kwargs)

    @staticmethod
    def APSMpBRFRaiseBeamVoltage(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target', 'expectedCurrent', 'bePrecise', 'currentTolerance']

        """
        return exec_with_tcl('APSMpBRFRaiseBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSMpBRFAdjustBeamVoltage(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target', 'expectedCurrent', 'currentTolerance', 'maxTries']

        """
        return exec_with_tcl('APSMpBRFAdjustBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSMpBRFTurnOnModAnode(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTurnOnModAnode', *args, **kwargs)

    @staticmethod
    def APSMpBRFRaiseModAnode(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target']

        """
        return exec_with_tcl('APSMpBRFRaiseModAnode', *args, **kwargs)

    @staticmethod
    def APSMpBRFRaiseBeamCurrent(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target', 'tempCheck', 'forceTempCheck', 'reflectedPowerCheck']

        """
        return exec_with_tcl('APSMpBRFRaiseBeamCurrent', *args, **kwargs)

    @staticmethod
    def APSMpBRFLowerBeamCurrent(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target']

        """
        return exec_with_tcl('APSMpBRFLowerBeamCurrent', *args, **kwargs)

    @staticmethod
    def APSMpBRFTurnOnRF(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTurnOnRF', *args, **kwargs)

    @staticmethod
    def APSMpBRFGetTunerLocked(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['cavity']

        """
        return exec_with_tcl('APSMpBRFGetTunerLocked', *args, **kwargs)

    @staticmethod
    def APSMpBRFRaisePower(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['forwardTarget', 'finalCurrent', 'collectorLimit', 'modAnodeLimit']

        """
        return exec_with_tcl('APSMpBRFRaisePower', *args, **kwargs)

    @staticmethod
    def APSMpBRFMinimizeReflectedPower(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['cavity']

        """
        return exec_with_tcl('APSMpBRFMinimizeReflectedPower', *args, **kwargs)

    @staticmethod
    def APSMpBRFLowerModAnode(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target']

        """
        return exec_with_tcl('APSMpBRFLowerModAnode', *args, **kwargs)

    @staticmethod
    def APSMpBRFLowerBeamVoltage(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['target', 'tolerance']

        """
        return exec_with_tcl('APSMpBRFLowerBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSBRFCheckCathodeSupply(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSBRFCheckCathodeSupply', *args, **kwargs)

    @staticmethod
    def APSBRFCheckModAnodeSupply(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSBRFCheckModAnodeSupply', *args, **kwargs)

    @staticmethod
    def APSBRFCheckForwardPower(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: args
        APS parsed args: ['require', 'safeLevel']

        """
        return exec_with_tcl('APSBRFCheckForwardPower', *args, **kwargs)

    @staticmethod
    def APSMpBRFTakeOutOfDiodeMode(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFTakeOutOfDiodeMode', *args, **kwargs)

    @staticmethod
    def APSMpBRFGoToDiodeMode(*args, **kwargs):
        """
        Location: APSMpBRFTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBRFGoToDiodeMode', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSOnOff(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'state1']

        """
        return exec_with_tcl('APSMpBoosterPSOnOff', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSOnOffNormal(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['magnet', 'state1']

        """
        return exec_with_tcl('APSMpBoosterPSOnOffNormal', *args, **kwargs)

    @staticmethod
    def APSDetermineBPSDACThreshold(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['magnetPS']

        """
        return exec_with_tcl('APSDetermineBPSDACThreshold', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSAndCorrOnFullPowerInfo(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSAndCorrOnFullPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSAndCorrOnFullPowerDialog(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSAndCorrOnFullPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSAndCorrOnFullPower(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'startupTime', 'startupSteps', 'selection', 'Fast', 'RawOnly', 'coldStart', 'SCRFile']

        """
        return exec_with_tcl('APSMpBoosterPSAndCorrOnFullPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSandCorrSetNoPowerInfo(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSandCorrSetNoPowerInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSandCorrSetNoPowerDialog(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterPSandCorrSetNoPowerDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSandCorrSetNoPower(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'selection']

        """
        return exec_with_tcl('APSMpBoosterPSandCorrSetNoPower', *args, **kwargs)

    @staticmethod
    def APSMpBoosterPSDetectValidStates(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD']

        """
        return exec_with_tcl('APSMpBoosterPSDetectValidStates', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOnPulsedSuppliesInfo(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBPSTurnOnPulsedSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOnPulsedSuppliesDialog(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBPSTurnOnPulsedSuppliesDialog', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOnPulsedSupplies(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['IS', 'IK', 'ES1', 'ES2', 'EK', 'SCRFile']

        """
        return exec_with_tcl('APSMpBPSTurnOnPulsedSupplies', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOffPulsedSuppliesInfo(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBPSTurnOffPulsedSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOffPulsedSuppliesDialog(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBPSTurnOffPulsedSuppliesDialog', *args, **kwargs)

    @staticmethod
    def APSMpBPSTurnOffPulsedSupplies(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['IS', 'IK', 'ES1', 'ES2', 'EK']

        """
        return exec_with_tcl('APSMpBPSTurnOffPulsedSupplies', *args, **kwargs)

    @staticmethod
    def APSMpBPSPulsedPSDischargeEnable(*args, **kwargs):
        """
        Location: BPSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['PSList', 'disable']

        """
        return exec_with_tcl('APSMpBPSPulsedPSDischargeEnable', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOffPSInfo(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSTurnOffPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOffPS(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOffList', 'turnOffListDetailed']

        """
        return exec_with_tcl('APSMpBTSTurnOffPS', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOffPSPackProc(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSTurnOffPSPackProc', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOnPSInfo(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSTurnOnPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOnPS(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOnList', 'turnOnListDetailed']

        """
        return exec_with_tcl('APSMpBTSTurnOnPS', *args, **kwargs)

    @staticmethod
    def APSMpBTSTurnOnPSPackProc(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSTurnOnPSPackProc', *args, **kwargs)

    @staticmethod
    def APSMpBTSConditionPowerSuppliesInfo(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSConditionPowerSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpBTSConditionPowerSupplies(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['conditionList', 'conditionListDetailed', 'SCRFile', 'configured', 'cycles', 'allSupplies']

        """
        return exec_with_tcl('APSMpBTSConditionPowerSupplies', *args, **kwargs)

    @staticmethod
    def APSMpBTSConditionPSPackProc(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBTSConditionPSPackProc', *args, **kwargs)

    @staticmethod
    def APSMpBTSConditionPS(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'conditionList', 'conditionListDetailed', 'SCRFile']

        """
        return exec_with_tcl('APSMpBTSConditionPS', *args, **kwargs)

    @staticmethod
    def APSMpBTSWaitForConditioningPS(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpBTSWaitForConditioningPS', *args, **kwargs)

    @staticmethod
    def APSMpBoosterDCRampStandardizeInitDialog(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterDCRampStandardizeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpBoosterDCRampStandardizeInfo(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBoosterDCRampStandardizeInfo', *args, **kwargs)

    @staticmethod
    def APSMpBoosterDCRampStandardize(*args, **kwargs):
        """
        Location: BTSTurnOnOff.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QF', 'QD', 'SF', 'SD', 'BMrampStart', 'BMrampEnd', 'QFrampStart', 'QFrampEnd', 'QDrampStart', 'QDrampEnd', 'SFrampStart', 'SFrampEnd', 'SDrampStart', 'SDrampEnd', 'cycles', 'cycleTime', 'rampSteps', 'ShortFilename']

        """
        return exec_with_tcl('APSMpBoosterDCRampStandardize', *args, **kwargs)

    @staticmethod
    def APSSRResponseCheckMonitorCallback(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: fid flagVariable args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSSRResponseCheckMonitorCallback', *args, **kwargs)

    @staticmethod
    def APSSRTakeSamplesForResponseCheck(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: args
        APS parsed args: ['steps', 'corrector', 'delta', 'fileName', 'verbose', 'dryRun', 'statusCallback', 'steps']

        """
        return exec_with_tcl('APSSRTakeSamplesForResponseCheck', *args, **kwargs)

    @staticmethod
    def APSSRProcessResponseCheckData(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRProcessResponseCheckData', *args, **kwargs)

    @staticmethod
    def APSMpSRFindGoodBPMsInfo(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFindGoodBPMsInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFindGoodBPMs(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFindGoodBPMs', *args, **kwargs)

    @staticmethod
    def APSMpSRFindGoodBPMsPlane(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFindGoodBPMsPlane', *args, **kwargs)

    @staticmethod
    def APSMpSRFindGoodBPMsInitDialog(*args, **kwargs):
        """
        Location: APSMpFindGoodBPMs.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFindGoodBPMsInitDialog', *args, **kwargs)

    @staticmethod
    def APSDefineMonitoringVariables(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDefineMonitoringVariables', *args, **kwargs)

    @staticmethod
    def APSSendDataLoggerErrorEmail(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: ['message', 'mailProgram']

        """
        return exec_with_tcl('APSSendDataLoggerErrorEmail', *args, **kwargs)

    @staticmethod
    def APSStartSddslogger(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: ['configFile']

        """
        return exec_with_tcl('APSStartSddslogger', *args, **kwargs)

    @staticmethod
    def APSStartSddspvalogger(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: ['configFile']

        """
        return exec_with_tcl('APSStartSddspvalogger', *args, **kwargs)

    @staticmethod
    def APSStartTimeSeriesLogger(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSStartTimeSeriesLogger', *args, **kwargs)

    @staticmethod
    def APSReadTimeSeriesLoggerConfig(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSReadTimeSeriesLoggerConfig', *args, **kwargs)

    @staticmethod
    def APSLimitFileSize(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSLimitFileSize', *args, **kwargs)

    @staticmethod
    def APSAddToMonitoringLogFile(*args, **kwargs):
        """
        Location: monitoring.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAddToMonitoringLogFile', *args, **kwargs)

    @staticmethod
    def APSMpP0FeedbackLoadParametersInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpP0FeedbackLoadParametersInfo', *args, **kwargs)

    @staticmethod
    def APSMpP0FeedbackLoadParametersInitDialog(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: frame args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpP0FeedbackLoadParametersInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpP0FeedbackLoadParameters(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['ShortFilename']

        """
        return exec_with_tcl('APSMpP0FeedbackLoadParameters', *args, **kwargs)

    @staticmethod
    def APSMpTurnOnP0FeedbackInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOnP0FeedbackInfo', *args, **kwargs)

    @staticmethod
    def APSMpTurnOnP0FeedbackInitDialog(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: frame args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOnP0FeedbackInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpTurnOnP0Feedback(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSMpTurnOnP0Feedback', *args, **kwargs)

    @staticmethod
    def APSMpTurnOffP0FeedbackInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOffP0FeedbackInfo', *args, **kwargs)

    @staticmethod
    def APSMpTurnOffP0FeedbackInitDialog(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: frame args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOffP0FeedbackInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpTurnOffP0Feedback(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSMpTurnOffP0Feedback', *args, **kwargs)

    @staticmethod
    def APSMpTurnOnOffP0Feedback(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['plane', 'onoff']

        """
        return exec_with_tcl('APSMpTurnOnOffP0Feedback', *args, **kwargs)

    @staticmethod
    def APSMpGenerateP0FeedbackFIRInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpGenerateP0FeedbackFIRInfo', *args, **kwargs)

    @staticmethod
    def APSMpGenerateP0FeedbackFIRInitDialog(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: frame args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpGenerateP0FeedbackFIRInitDialog', *args, **kwargs)

    @staticmethod
    def APSLoadTwissParameters(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['twissFile', 'plane', 'sPickup', 'sKickerx', 'sKickery']

        """
        return exec_with_tcl('APSLoadTwissParameters', *args, **kwargs)

    @staticmethod
    def APSMpGenerateP0FeedbackFIR(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['xtune', 'ytune']

        """
        return exec_with_tcl('APSMpGenerateP0FeedbackFIR', *args, **kwargs)

    @staticmethod
    def APSRampP0FeedbackFIR(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSRampP0FeedbackFIR', *args, **kwargs)

    @staticmethod
    def APSMakeFIRFile(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['twissFile', 'plane', 'delay', 'outputFile', 'order', 'deltaNu', 'betaPickup', 'betaKicker', 'alphaPickup', 'alphaKicker', 'psiPickup', 'psiKicker', 'nuxy', 'delay', 'twissFile', 'targetNu']

        """
        return exec_with_tcl('APSMakeFIRFile', *args, **kwargs)

    @staticmethod
    def APSMpRampToHigherChromaticityInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpRampToHigherChromaticityInfo', *args, **kwargs)

    @staticmethod
    def APSMpRampToHigherChromaticity(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRampToHigherChromaticity', *args, **kwargs)

    @staticmethod
    def APSSRUpdateUBOPLink(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['suffix', 'choice']

        """
        return exec_with_tcl('APSSRUpdateUBOPLink', *args, **kwargs)

    @staticmethod
    def APSFindP0FBStartBucket(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['confirm', 'statusCallback', 'gainFile']

        """
        return exec_with_tcl('APSFindP0FBStartBucket', *args, **kwargs)

    @staticmethod
    def APSUpdateP0FBBunchPattern(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSUpdateP0FBBunchPattern', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchFeedbackSystemInfo(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchFeedbackSystemInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSetFBSystem(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['parent', 'system']

        """
        return exec_with_tcl('APSMpSRSetFBSystem', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchFeedbackSystemInitDialog(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchFeedbackSystemInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSetFBGain(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: ['system', 'xgain', 'ygain']

        """
        return exec_with_tcl('APSMpSRSetFBGain', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchFeedbackSystem(*args, **kwargs):
        """
        Location: APSMpP0Feedback.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchFeedbackSystem', *args, **kwargs)

    @staticmethod
    def APSMpRTFBRebootInfo(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBRebootInfo', *args, **kwargs)

    @staticmethod
    def APSMpRTFBReboot(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBReboot', *args, **kwargs)

    @staticmethod
    def APSMpRTFBPreRebootInfo(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBPreRebootInfo', *args, **kwargs)

    @staticmethod
    def APSMpRTFBPreReboot(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBPreReboot', *args, **kwargs)

    @staticmethod
    def APSMpRTFBPostRebootInfo(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBPostRebootInfo', *args, **kwargs)

    @staticmethod
    def APSMpRTFBPostReboot(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRTFBPostReboot', *args, **kwargs)

    @staticmethod
    def APSMpAbortSRControllaw(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpAbortSRControllaw', *args, **kwargs)

    @staticmethod
    def APSMpSetRTFBGlobalParameters(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['filename', 'readonly', 'statusCallback']

        """
        return exec_with_tcl('APSMpSetRTFBGlobalParameters', *args, **kwargs)

    @staticmethod
    def APSMpRTFBResetOpenLoops(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['hpFilterInitialVert', 'hpFilterInitialHoriz', 'runHloop', 'runVloop']

        """
        return exec_with_tcl('APSMpRTFBResetOpenLoops', *args, **kwargs)

    @staticmethod
    def APSMpRestoreSRBPMOffsetsAndSetpoints(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['plane', 'datapool', 'offsetReferenceFile', 'setpointReferenceFile']

        """
        return exec_with_tcl('APSMpRestoreSRBPMOffsetsAndSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpInitializeRTFBSystem(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['paramDir', 'paramFile', 'xconfigDir', 'yconfigDir', 'statusCallback']

        """
        return exec_with_tcl('APSMpInitializeRTFBSystem', *args, **kwargs)

    @staticmethod
    def APSMpEnableFeedForward(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['ffWaveFile', 'upstreamName', 'downstreamName', 'statusCallback']

        """
        return exec_with_tcl('APSMpEnableFeedForward', *args, **kwargs)

    @staticmethod
    def APSMpDisableFeedForward(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['ffWaveFile', 'upstreamName', 'downstreamName', 'statusCallback']

        """
        return exec_with_tcl('APSMpDisableFeedForward', *args, **kwargs)

    @staticmethod
    def APSMpSetP1Enables(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSMpSetP1Enables', *args, **kwargs)

    @staticmethod
    def APSMpZeroRTBPMSetpoints(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['plane', 'statusCallback']

        """
        return exec_with_tcl('APSMpZeroRTBPMSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpCheckCorrectorMode(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['mode', 'plane', 'all']

        """
        return exec_with_tcl('APSMpCheckCorrectorMode', *args, **kwargs)

    @staticmethod
    def APSSetRTFBCorrectorMode(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['all', 'plane', 'mode', 'pscuTolerance', 'readbackTolerance', 'checkStatus']

        """
        return exec_with_tcl('APSSetRTFBCorrectorMode', *args, **kwargs)

    @staticmethod
    def APSGetRTFBCorrectorList(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['all', 'plane']

        """
        return exec_with_tcl('APSGetRTFBCorrectorList', *args, **kwargs)

    @staticmethod
    def APSCheckCorrectorStatus(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['corrList']

        """
        return exec_with_tcl('APSCheckCorrectorStatus', *args, **kwargs)

    @staticmethod
    def APSCheckCorrsPassive(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['tolerance', 'corrList']

        """
        return exec_with_tcl('APSCheckCorrsPassive', *args, **kwargs)

    @staticmethod
    def APSMpRTFBCloseLoops(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'hpFilterCutoffVert', 'hpFilterCutoffHoriz', 'hpFilterInitialVert', 'hpFilterInitialHoriz', 'hpFilterRampPoints', 'hpFilterRampInterval']

        """
        return exec_with_tcl('APSMpRTFBCloseLoops', *args, **kwargs)

    @staticmethod
    def APSMpRTFBCheckCorrReadbacks(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['readbackTolerance', 'statusCallback']

        """
        return exec_with_tcl('APSMpRTFBCheckCorrReadbacks', *args, **kwargs)

    @staticmethod
    def APSMpRTFBLoadResponseMatrix(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['hconfig', 'vconfig', 'baseDir']

        """
        return exec_with_tcl('APSMpRTFBLoadResponseMatrix', *args, **kwargs)

    @staticmethod
    def APSCheckRTFBbpmSetpoints(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['plane', 'bpmLimit']

        """
        return exec_with_tcl('APSCheckRTFBbpmSetpoints', *args, **kwargs)

    @staticmethod
    def APSFixRTFBbpmSetpoints(*args, **kwargs):
        """
        Location: APSMpRTFBReboot.tcl
        TCL function args: args
        APS parsed args: ['plane', 'bpmLimit', 'statusCallback']

        """
        return exec_with_tcl('APSFixRTFBbpmSetpoints', *args, **kwargs)

    @staticmethod
    def APSMpReturnToVectorInfo(*args, **kwargs):
        """
        Location: APSMpReturnToVector.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpReturnToVectorInfo', *args, **kwargs)

    @staticmethod
    def APSMpReturnToVector(*args, **kwargs):
        """
        Location: APSMpReturnToVector.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpReturnToVector', *args, **kwargs)

    @staticmethod
    def APSMpReturnToVectorInitDialog(*args, **kwargs):
        """
        Location: APSMpReturnToVector.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpReturnToVectorInitDialog', *args, **kwargs)

    @staticmethod
    def APSSRSetIOCAveraging(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['num2Ave', 'filterCoeff', 'enable', 'cavputCommand', 'BPMList']

        """
        return exec_with_tcl('APSSRSetIOCAveraging', *args, **kwargs)

    @staticmethod
    def APSSRTransferBPMAdjustedValues(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['msType', 'plane', 'saveSnapshot', 'statusCallback', 'excludeConfigFileList']

        """
        return exec_with_tcl('APSSRTransferBPMAdjustedValues', *args, **kwargs)

    @staticmethod
    def APSSRTransferBPMList(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['list', 'plane', 'msType']

        """
        return exec_with_tcl('APSSRTransferBPMList', *args, **kwargs)

    @staticmethod
    def APSSRGetWorkingP0SectorsList(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['iocs']

        """
        return exec_with_tcl('APSSRGetWorkingP0SectorsList', *args, **kwargs)

    @staticmethod
    def APSSRMeasureBPMoffsetInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSRMeasureBPMoffsetInfo', *args, **kwargs)

    @staticmethod
    def APSSRMeasureBPMoffset(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSRMeasureBPMoffset', *args, **kwargs)

    @staticmethod
    def APSMpSRUncogBPMInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUncogBPMInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRUncogBPM(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUncogBPM', *args, **kwargs)

    @staticmethod
    def APSMpSRCog324FastBPMInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCog324FastBPMInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRCog324FastBPM(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCog324FastBPM', *args, **kwargs)

    @staticmethod
    def APSMpSRCog24SingletsInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCog24SingletsInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRCog24Singlets(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpSRCog24Singlets', *args, **kwargs)

    @staticmethod
    def APSMpSRBTMStatusInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBTMStatusInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRBTMStatus(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBTMStatus', *args, **kwargs)

    @staticmethod
    def APSMpSRBTMSetupInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBTMSetupInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRBTMSetupDialog(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['frame', 'pem']

        """
        return exec_with_tcl('APSMpSRBTMSetupDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRBTMSetup(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['cog']

        """
        return exec_with_tcl('APSMpSRBTMSetup', *args, **kwargs)

    @staticmethod
    def APSMpSRCoggingSetupObsolete(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCoggingSetupObsolete', *args, **kwargs)

    @staticmethod
    def APSMpExcludedBPMList(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['excludeP0s', 'excludeIDXrays', 'excludeBMXrays', 'excludeNbBPMs', 'excludeMpBPMs', 'plane', 'excludeFPGABPMs']

        """
        return exec_with_tcl('APSMpExcludedBPMList', *args, **kwargs)

    @staticmethod
    def APSSRCogBPM(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['cogstate', 'customContentsFile']

        """
        return exec_with_tcl('APSSRCogBPM', *args, **kwargs)

    @staticmethod
    def APSMpForceApplyBPMbladeGainsInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpForceApplyBPMbladeGainsInfo', *args, **kwargs)

    @staticmethod
    def APSMpForceApplyBPMbladeGainsInitDialog(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpForceApplyBPMbladeGainsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpForceApplyBPMbladeGains(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpForceApplyBPMbladeGains', *args, **kwargs)

    @staticmethod
    def APSMpSRResetBPMAveragingInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRResetBPMAveragingInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRResetBPMAveraging(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRResetBPMAveraging', *args, **kwargs)

    @staticmethod
    def APSMpSRBPLDTripLimitAlarmValidationInfo(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBPLDTripLimitAlarmValidationInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRBPLDTripLimitAlarmValidationInitDialog(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBPLDTripLimitAlarmValidationInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRBPLDTripLimitAlarmValidation(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRBPLDTripLimitAlarmValidation', *args, **kwargs)

    @staticmethod
    def APSSetupFPGABpmTriggers(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['enableMPS']

        """
        return exec_with_tcl('APSSetupFPGABpmTriggers', *args, **kwargs)

    @staticmethod
    def APSGetMonopulseBPMIOCList(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetMonopulseBPMIOCList', *args, **kwargs)

    @staticmethod
    def APSGetFPGASectorList(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetFPGASectorList', *args, **kwargs)

    @staticmethod
    def APSArmFPGABpm(*args, **kwargs):
        """
        Location: APSMpSRBPM.tcl
        TCL function args: args
        APS parsed args: ['subSector', 'type', 'application']

        """
        return exec_with_tcl('APSArmFPGABpm', *args, **kwargs)

    @staticmethod
    def APSMpBCMSetBaselineInfo(*args, **kwargs):
        """
        Location: APSMpSRBunchCurrent.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBCMSetBaselineInfo', *args, **kwargs)

    @staticmethod
    def APSMpBCMSetBaseline(*args, **kwargs):
        """
        Location: APSMpSRBunchCurrent.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpBCMSetBaseline', *args, **kwargs)

    @staticmethod
    def APSRemoveIDfromDefaultConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveIDfromDefaultConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveIDfromDefaultConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveIDfromDefaultConfigs', *args, **kwargs)

    @staticmethod
    def APSRemoveIDfromDefaultConfigsDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveIDfromDefaultConfigsDialog', *args, **kwargs)

    @staticmethod
    def APSRemoveBMfromDefaultConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveBMfromDefaultConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveBMfromDefaultConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveBMfromDefaultConfigs', *args, **kwargs)

    @staticmethod
    def APSRemoveBMfromDefaultConfigsDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveBMfromDefaultConfigsDialog', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['reason', 'initials', 'deviceList', 'confirm', 'plane']

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultConfigs', *args, **kwargs)

    @staticmethod
    def APSRemoveBPMFromDefaultRFControllawConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveBPMFromDefaultRFControllawConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveBPMFromDefaultRFControllawConfigsDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveBPMFromDefaultRFControllawConfigsDialog', *args, **kwargs)

    @staticmethod
    def APSRemoveBPMFromDefaultRFControllawConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['reason', 'initials', 'deviceList', 'confirm']

        """
        return exec_with_tcl('APSRemoveBPMFromDefaultRFControllawConfigs', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultConfigsDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultConfigsDialog', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultConfigInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultConfigInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultConfig(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'config', 'confirm', 'comment', 'controllawType', 'initials']

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultConfig', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSAddDeviceToDefaultConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultConfigsDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSAddDeviceToDefaultConfigsDialog', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['reason', 'initials', 'deviceList', 'confirm', 'plane', 'zeroXBPMsetpoint']

        """
        return exec_with_tcl('APSAddDeviceToDefaultConfigs', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultConfigInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAddDeviceToDefaultConfigInfo', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultConfig(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['config', 'deviceList', 'confirm', 'comment', 'rtfeedback', 'initials']

        """
        return exec_with_tcl('APSAddDeviceToDefaultConfig', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultRTFBConfigInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAddDeviceToDefaultRTFBConfigInfo', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultRTFBConfigDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSAddDeviceToDefaultRTFBConfigDialog', *args, **kwargs)

    @staticmethod
    def APSAddDeviceToDefaultRTFBConfig(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['reason', 'initials', 'deviceList', 'confirm', 'plane']

        """
        return exec_with_tcl('APSAddDeviceToDefaultRTFBConfig', *args, **kwargs)

    @staticmethod
    def APSRestoreDefaultConfigsInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSRestoreDefaultConfigsInfo', *args, **kwargs)

    @staticmethod
    def APSRestoreDefaultConfigsInitDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRestoreDefaultConfigsInitDialog', *args, **kwargs)

    @staticmethod
    def APSRestoreDefaultConfigs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRestoreDefaultConfigs', *args, **kwargs)

    @staticmethod
    def APSRestoreDefaultConfigsCallback(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: widget type default arrayName index
        APS parsed args: None

        """
        return exec_with_tcl('APSRestoreDefaultConfigsCallback', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultRTFBConfigInfo(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultRTFBConfigInfo', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultRTFBConfigDialog(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultRTFBConfigDialog', *args, **kwargs)

    @staticmethod
    def APSRemoveDeviceFromDefaultRTFBConfig(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['reason', 'initials', 'deviceList', 'confirm', 'add', 'plane']

        """
        return exec_with_tcl('APSRemoveDeviceFromDefaultRTFBConfig', *args, **kwargs)

    @staticmethod
    def APSMpSRSetXrayBPMStatusPVs(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['config', 'dataDir']

        """
        return exec_with_tcl('APSMpSRSetXrayBPMStatusPVs', *args, **kwargs)

    @staticmethod
    def APSSRRemoveXrayBPMFromOrbitCorrection(*args, **kwargs):
        """
        Location: APSMpSRCorrectionConfiguration.tcl
        TCL function args: args
        APS parsed args: ['sector', 'restart', 'source', 'side']

        """
        return exec_with_tcl('APSSRRemoveXrayBPMFromOrbitCorrection', *args, **kwargs)

    @staticmethod
    def APSMpSRFirstTurnInfo(*args, **kwargs):
        """
        Location: APSMpSRFirstTurn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFirstTurnInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFirstTurn(*args, **kwargs):
        """
        Location: APSMpSRFirstTurn.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpSRFirstTurn', *args, **kwargs)

    @staticmethod
    def APSMpSRFirstTurnInitDialog(*args, **kwargs):
        """
        Location: APSMpSRFirstTurn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFirstTurnInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpRestoreBPMFailSafeReturn(*args, **kwargs):
        """
        Location: APSMpSRFirstTurn.tcl
        TCL function args: code results args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreBPMFailSafeReturn', *args, **kwargs)

    @staticmethod
    def APSSRRestoreBPM(*args, **kwargs):
        """
        Location: APSMpSRFirstTurn.tcl
        TCL function args: args
        APS parsed args: ['correctorCavputSave']

        """
        return exec_with_tcl('APSSRRestoreBPM', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectGapFFTableInfo(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectGapFFTableInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectGapFFTableInitDialog(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectGapFFTableInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectGapFFTable(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectGapFFTable', *args, **kwargs)

    @staticmethod
    def APSSRTransferBPMSetpoint(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSSRTransferBPMSetpoint', *args, **kwargs)

    @staticmethod
    def APSCheckControllawRunning(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['config']

        """
        return exec_with_tcl('APSCheckControllawRunning', *args, **kwargs)

    @staticmethod
    def APSMpSRSingleGapScanInitDialog(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSingleGapScanInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSingleGapScanInfo(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSingleGapScanInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSingleGapScan(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSingleGapScan', *args, **kwargs)

    @staticmethod
    def APSDisplayIDControlMedm(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['IDList']

        """
        return exec_with_tcl('APSDisplayIDControlMedm', *args, **kwargs)

    @staticmethod
    def APSSRCheckGapScanConditions(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['keepFFrunning']

        """
        return exec_with_tcl('APSSRCheckGapScanConditions', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectXrayBPMDataInfo(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectXrayBPMDataInfo', *args, **kwargs)

    @staticmethod
    def APSSelectCantedUndulator(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['type']

        """
        return exec_with_tcl('APSSelectCantedUndulator', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectXrayBPMDataInitDialog(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectXrayBPMDataInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRCollectXrayBPMData(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRCollectXrayBPMData', *args, **kwargs)

    @staticmethod
    def APSPlotXrayBPMData(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['fileList', 'plane']

        """
        return exec_with_tcl('APSPlotXrayBPMData', *args, **kwargs)

    @staticmethod
    def APSSRSetXrayBlades(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['value']

        """
        return exec_with_tcl('APSSRSetXrayBlades', *args, **kwargs)

    @staticmethod
    def APSPlotXrayBPMDataInfo(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSPlotXrayBPMDataInfo', *args, **kwargs)

    @staticmethod
    def APSSRSteerXrayOrbit(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: args
        APS parsed args: ['plane', 'value']

        """
        return exec_with_tcl('APSSRSteerXrayOrbit', *args, **kwargs)

    @staticmethod
    def APSMpSRMoboScanErrorSafeReturn(*args, **kwargs):
        """
        Location: APSMpSRGapFFScan.tcl
        TCL function args: code results args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRMoboScanErrorSafeReturn', *args, **kwargs)

    @staticmethod
    def APSMpSRFillFromZeroInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFillFromZeroInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRReFillInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRReFillInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRTopupInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTopupInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRAbortTopupInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRAbortTopupInfo', *args, **kwargs)

    @staticmethod
    def APSMpStartSIS1FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartSIS1FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStopSIS1FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopSIS1FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStartBES2FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartBES2FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStopBES2FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopBES2FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStartID11FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartID11FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStopID11FeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopID11FeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStartIDOffsetFeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartIDOffsetFeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpStopIDOffsetFeedforwardInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopIDOffsetFeedforwardInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFillFromZero(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFillFromZero', *args, **kwargs)

    @staticmethod
    def APSMpSRReFill(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRReFill', *args, **kwargs)

    @staticmethod
    def APSMpSRTopup(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTopup', *args, **kwargs)

    @staticmethod
    def APSMpStartTopup(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartTopup', *args, **kwargs)

    @staticmethod
    def APSMpSRAbortTopup(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRAbortTopup', *args, **kwargs)

    @staticmethod
    def APSMpStartSIS1Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartSIS1Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStopSIS1Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopSIS1Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStartBES2Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartBES2Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStopBES2Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopBES2Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStartIDOffsetFeedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartIDOffsetFeedforward', *args, **kwargs)

    @staticmethod
    def APSMpStopIDOffsetFeedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopIDOffsetFeedforward', *args, **kwargs)

    @staticmethod
    def APSMpSIS1Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['action', 'mode']

        """
        return exec_with_tcl('APSMpSIS1Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpBES2Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['action', 'mode']

        """
        return exec_with_tcl('APSMpBES2Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStartID11Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartID11Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStopID11Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStopID11Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpID11Feedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['action']

        """
        return exec_with_tcl('APSMpID11Feedforward', *args, **kwargs)

    @staticmethod
    def APSMpStartIDFFExpert(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpStartIDFFExpert', *args, **kwargs)

    @staticmethod
    def APSMpIDOffsetFeedforward(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['action', 'expert']

        """
        return exec_with_tcl('APSMpIDOffsetFeedforward', *args, **kwargs)

    @staticmethod
    def APSMpSRToggleScrapers(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['position']

        """
        return exec_with_tcl('APSMpSRToggleScrapers', *args, **kwargs)

    @staticmethod
    def APSMpDoPreinjectionChecks(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: ['gapLimit']

        """
        return exec_with_tcl('APSMpDoPreinjectionChecks', *args, **kwargs)

    @staticmethod
    def APSMpPreTopupChecks(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPreTopupChecks', *args, **kwargs)

    @staticmethod
    def APSMpSetupTopup(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSetupTopup', *args, **kwargs)

    @staticmethod
    def APSMpApplySIS1Setpoints(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpApplySIS1Setpoints', *args, **kwargs)

    @staticmethod
    def APSMpSetupMultiBunchInject(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSetupMultiBunchInject', *args, **kwargs)

    @staticmethod
    def APSMpRestoreNonTopupState(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreNonTopupState', *args, **kwargs)

    @staticmethod
    def APSMpSetupBunchMonitor(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSetupBunchMonitor', *args, **kwargs)

    @staticmethod
    def APSMpRetimeP0IfAppropriate(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRetimeP0IfAppropriate', *args, **kwargs)

    @staticmethod
    def APSMpMakeTargetBunchPattern(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpMakeTargetBunchPattern', *args, **kwargs)

    @staticmethod
    def APSMpIDOffsetFeedforwardStatusInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDOffsetFeedforwardStatusInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDOffsetFeedforwardStatus(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDOffsetFeedforwardStatus', *args, **kwargs)

    @staticmethod
    def APSMpUpdateS27GapFFTableInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpUpdateS27GapFFTableInfo', *args, **kwargs)

    @staticmethod
    def APSMpUpdateS27GapFFTable(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpUpdateS27GapFFTable', *args, **kwargs)

    @staticmethod
    def APSMpSRDispCorrectionInfo(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRDispCorrectionInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRStartDispCorrectionInitDialog(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRStartDispCorrectionInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRStartDispCorrection(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRStartDispCorrection', *args, **kwargs)

    @staticmethod
    def APSMpSRStopDispCorrection(*args, **kwargs):
        """
        Location: APSMpSRInjection.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRStopDispCorrection', *args, **kwargs)

    @staticmethod
    def APSMpSRTuneUpInjectionInfo(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTuneUpInjectionInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRTuneUpInjection(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRTuneUpInjection', *args, **kwargs)

    @staticmethod
    def APSViewFlag(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: args
        APS parsed args: ['stop', 'flag']

        """
        return exec_with_tcl('APSViewFlag', *args, **kwargs)

    @staticmethod
    def APSSRStoreWithoutAccumulation(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: args
        APS parsed args: ['stop']

        """
        return exec_with_tcl('APSSRStoreWithoutAccumulation', *args, **kwargs)

    @staticmethod
    def APSSRPulsedPSDischargeEnable(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: args
        APS parsed args: ['PSList', 'disable']

        """
        return exec_with_tcl('APSSRPulsedPSDischargeEnable', *args, **kwargs)

    @staticmethod
    def APSShutterPermitGiven(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSShutterPermitGiven', *args, **kwargs)

    @staticmethod
    def APSTopupEnabled(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSTopupEnabled', *args, **kwargs)

    @staticmethod
    def APSDoubleStopClosed(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDoubleStopClosed', *args, **kwargs)

    @staticmethod
    def APSSRGetBeamSwitchState(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGetBeamSwitchState', *args, **kwargs)

    @staticmethod
    def APSSRChangeBeamSwitchState(*args, **kwargs):
        """
        Location: APSMpSRInjectionTuneup.tcl
        TCL function args: args
        APS parsed args: ['goTo']

        """
        return exec_with_tcl('APSSRChangeBeamSwitchState', *args, **kwargs)

    @staticmethod
    def APSSRScopeMeasSetup(*args, **kwargs):
        """
        Location: APSMpSRScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRScopeMeasSetup', *args, **kwargs)

    @staticmethod
    def APSSRScopeMeasTopUpKickersSetup(*args, **kwargs):
        """
        Location: APSMpSRScope.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRScopeMeasTopUpKickersSetup', *args, **kwargs)

    @staticmethod
    def APSMpSRSetupInfo(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSetupInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSetupInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSetupInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSetup(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSetup', *args, **kwargs)

    @staticmethod
    def APSMpSRFBresetOpen(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFBresetOpen', *args, **kwargs)

    @staticmethod
    def APSMpSRFBreleaseCorrs(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFBreleaseCorrs', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeDefault(*args, **kwargs):
        """
        Location: APSMpSRSetup.tcl
        TCL function args: newLattice
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRChangeDefault', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchOrbitInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchOrbitInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchOrbitInfo(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchOrbitInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchOrbit(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSwitchOrbit', *args, **kwargs)

    @staticmethod
    def APSMpSRSanityCheck(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['oldSRFile', 'newSRFile', 'SRXrayBPMFile', 'SRGapFile', 'mode', 'fillPattern']

        """
        return exec_with_tcl('APSMpSRSanityCheck', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeChromaticity(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['mode', 'rampQuads', 'presentFillPattern', 'newFillPattern', 'newCoggingPattern', 'newTopup', 'newSRFile', 'SRGapFile']

        """
        return exec_with_tcl('APSMpSRChangeChromaticity', *args, **kwargs)

    @staticmethod
    def APSMpSRChangeLattice(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['newSRFile', 'newLatticeDir', 'oldLatticeDir', 'presentFillPattern', 'newFillPattern']

        """
        return exec_with_tcl('APSMpSRChangeLattice', *args, **kwargs)

    @staticmethod
    def APSSRSetDefaultLattice(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['newLattice', 'application']

        """
        return exec_with_tcl('APSSRSetDefaultLattice', *args, **kwargs)

    @staticmethod
    def APSMpSRSwitchOrbitFinalAdjustment(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['newFillPattern']

        """
        return exec_with_tcl('APSMpSRSwitchOrbitFinalAdjustment', *args, **kwargs)

    @staticmethod
    def APSSRTransferOrbit(*args, **kwargs):
        """
        Location: APSMpSRSwitch.tcl
        TCL function args: args
        APS parsed args: ['plane', 'readFrom', 'xferTo', 'rfBpm', 'bmBpm', 'idBpm']

        """
        return exec_with_tcl('APSSRTransferOrbit', *args, **kwargs)

    @staticmethod
    def APSUpdateIDScanSelection(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: ID
        APS parsed args: None

        """
        return exec_with_tcl('APSUpdateIDScanSelection', *args, **kwargs)

    @staticmethod
    def APSSRGapScanReturnProc(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGapScanReturnProc', *args, **kwargs)

    @staticmethod
    def APSSRGapScanCallbackProc(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['ok', 'outputFile', 'IDtagList']

        """
        return exec_with_tcl('APSSRGapScanCallbackProc', *args, **kwargs)

    @staticmethod
    def APSSRGetIDGapBriefInfo(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGetIDGapBriefInfo', *args, **kwargs)

    @staticmethod
    def APSMakeIDGapBriefScanSelection(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['type']

        """
        return exec_with_tcl('APSMakeIDGapBriefScanSelection', *args, **kwargs)

    @staticmethod
    def APSSRGapBriefScan(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'outputDir', 'rootname', 'statusCallback', 'keepFFrunning', 'pause', 'preview', 'readingType', 'numToAve', 'fixedGapList', 'fixedIDList', 'togetherList', 'ID01OffsetList']

        """
        return exec_with_tcl('APSSRGapBriefScan', *args, **kwargs)

    @staticmethod
    def APSSRCheckXBPMGains(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'statusCallback']

        """
        return exec_with_tcl('APSSRCheckXBPMGains', *args, **kwargs)

    @staticmethod
    def APSSRUpdateGapScanMonitorFiles(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSSRUpdateGapScanMonitorFiles', *args, **kwargs)

    @staticmethod
    def APSSRGapBriefScanOneGapFit(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['sector', 'inputFile', 'outputFile', 'fitStart', 'fitFactor', 'fitRate', 'CUSectorList']

        """
        return exec_with_tcl('APSSRGapBriefScanOneGapFit', *args, **kwargs)

    @staticmethod
    def APSSRGapBriefScanDataFit(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['inputFile', 'statusCallback', 'tolerance', 'fitStart', 'fitFactor', 'fitRate', 'CUSectorList']

        """
        return exec_with_tcl('APSSRGapBriefScanDataFit', *args, **kwargs)

    @staticmethod
    def APSFixScrewedXbpms(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSFixScrewedXbpms', *args, **kwargs)

    @staticmethod
    def APSSRGapBriefScanLoad(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['loadRate', 'loadOffset', 'dataDir', 'rootname', 'fitTolerance', 'statusCallback', 'CUSectorList', 'filename', 'pem']

        """
        return exec_with_tcl('APSSRGapBriefScanLoad', *args, **kwargs)

    @staticmethod
    def APSMpSRGapBriefScan(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'openOtherGaps', 'numToAve', 'pause', 'rootname', 'lockedIDList', 'keepFFrunning', 'fixedIDList', 'fixedGapList', 'togetherList', 'closeInterval', 'loadOffset', 'loadRate']

        """
        return exec_with_tcl('APSMpSRGapBriefScan', *args, **kwargs)

    @staticmethod
    def APSSRReviewBriefScanFitData(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['fitData', 'sameScale', 'CUSectorList']

        """
        return exec_with_tcl('APSSRReviewBriefScanFitData', *args, **kwargs)

    @staticmethod
    def APSSRReviewBriefScanData(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['sameScale', 'scanData']

        """
        return exec_with_tcl('APSSRReviewBriefScanData', *args, **kwargs)

    @staticmethod
    def APSSRUpdateBladeSelection(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['sector', 'item', 'nameFlag']

        """
        return exec_with_tcl('APSSRUpdateBladeSelection', *args, **kwargs)

    @staticmethod
    def APSSRIDBadBladeSelection(*args, **kwargs):
        """
        Location: APSSRGapBriefScan.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSSRIDBadBladeSelection', *args, **kwargs)

    @staticmethod
    def APSSRGetIDGapFullInfo(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGetIDGapFullInfo', *args, **kwargs)

    @staticmethod
    def APSSRGetSteeringConfigNames(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['pem', 'hCOnfig', 'vConfig']

        """
        return exec_with_tcl('APSSRGetSteeringConfigNames', *args, **kwargs)

    @staticmethod
    def APSSRSetAllMinGaps(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['var']

        """
        return exec_with_tcl('APSSRSetAllMinGaps', *args, **kwargs)

    @staticmethod
    def APSSRUpdateMinGap(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['var']

        """
        return exec_with_tcl('APSSRUpdateMinGap', *args, **kwargs)

    @staticmethod
    def APSSRGapFullScan(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['outputDir', 'rootname', 'start', 'maxGap', 'statusCallback', 'keepFFrunning', 'pause', 'preview', 'IDList', 'transferOrbit', 'readingType', 'numToAve', 'pem', 'minStep', 'maxStep', 'stepInterval', 'factor', 'minGapList', 'deltaToMinGap', 'ignoreXbpms', 'fixedIDList', 'fixedGapList', 'togetherList', 'takeTunes']

        """
        return exec_with_tcl('APSSRGapFullScan', *args, **kwargs)

    @staticmethod
    def APSSRCreateGapScanValuesFile(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['minStep', 'maxStep', 'IDList', 'gapValuesFile', 'stepInterval', 'minGapList', 'maxGap', 'factor']

        """
        return exec_with_tcl('APSSRCreateGapScanValuesFile', *args, **kwargs)

    @staticmethod
    def APSSRPrepareFFData(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['orbitControlDir', 'input', 'CUSectorList', 'gapThresholdVar', 'statusCallback', 'pem', 'fixedGapTolerance', 'gapDiffTolerance']

        """
        return exec_with_tcl('APSSRPrepareFFData', *args, **kwargs)

    @staticmethod
    def APSSRGenerateGainActuatorFile(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['input', 'shutterPVList', 'shutterOneNameList', 'gapThresholdVar', 'statusCallback', 'CUSectorList', 'fixedIDList', 'fixedGapList', 'togetherList', 'gapDiffTolerance', 'fixedGapTolerance']

        """
        return exec_with_tcl('APSSRGenerateGainActuatorFile', *args, **kwargs)

    @staticmethod
    def APSMakeIDGapFullScanSelection(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMakeIDGapFullScanSelection', *args, **kwargs)

    @staticmethod
    def APSMpSRGapFullScan(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'minGapList', 'numToAve', 'pause', 'maxGap', 'gapVar', 'rootname', 'fixedIDList', 'fixedGapList', 'togetherList', 'keepFFrunning', 'transferOrbit', 'maxStep', 'minStep', 'stepInterval', 'deltaToMinGap', 'factor', 'fullScan', 'closeInterval', 'scanOnly']

        """
        return exec_with_tcl('APSMpSRGapFullScan', *args, **kwargs)

    @staticmethod
    def APSSRInstallFeedForward(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'outputDir', 'filename', 'fullScan', 'pem', 'ignoreXbpms']

        """
        return exec_with_tcl('APSSRInstallFeedForward', *args, **kwargs)

    @staticmethod
    def APSZeroXrayBPMSetpoint(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['filename']

        """
        return exec_with_tcl('APSZeroXrayBPMSetpoint', *args, **kwargs)

    @staticmethod
    def APSSRReviewGapFFData(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['gapScanFile', 'pem', 'ignoreXbpms']

        """
        return exec_with_tcl('APSSRReviewGapFFData', *args, **kwargs)

    @staticmethod
    def APSSRGapSetThresholds(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['threshold', 'lowThreshold', 'lowThresholdSectorList', 'thresholdVar']

        """
        return exec_with_tcl('APSSRGapSetThresholds', *args, **kwargs)

    @staticmethod
    def APSSRGetDeviceLimits(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['default', 'initial', 'gapVar', 'deltaToMinGap']

        """
        return exec_with_tcl('APSSRGetDeviceLimits', *args, **kwargs)

    @staticmethod
    def APSSRSetGlobalMinimumGaps(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['minGap', 'gapVar', 'statusCallback']

        """
        return exec_with_tcl('APSSRSetGlobalMinimumGaps', *args, **kwargs)

    @staticmethod
    def APSSRResetDefaultSelection(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['selectType']

        """
        return exec_with_tcl('APSSRResetDefaultSelection', *args, **kwargs)

    @staticmethod
    def APSSRGetLockedIDDevices(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGetLockedIDDevices', *args, **kwargs)

    @staticmethod
    def APSSRDisableLockedIDDeviceSelect(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['buttonNameList', 'IDList', 'enable', 'lockedIDList']

        """
        return exec_with_tcl('APSSRDisableLockedIDDeviceSelect', *args, **kwargs)

    @staticmethod
    def APSSRSetupUndulatorGap(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRSetupUndulatorGap', *args, **kwargs)

    @staticmethod
    def APSSRMakeIDUndulatorScanSelectionWidget(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['sectorList']

        """
        return exec_with_tcl('APSSRMakeIDUndulatorScanSelectionWidget', *args, **kwargs)

    @staticmethod
    def APSSRCheckUndulatorScanType(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['IDList']

        """
        return exec_with_tcl('APSSRCheckUndulatorScanType', *args, **kwargs)

    @staticmethod
    def APSUpdateFFTable(*args, **kwargs):
        """
        Location: APSSRGapFullScan.tcl
        TCL function args: args
        APS parsed args: ['oldTable', 'newTable', 'statusCallback']

        """
        return exec_with_tcl('APSUpdateFFTable', *args, **kwargs)

    @staticmethod
    def APSMpLTS_TurnOnPSInfo(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTS_TurnOnPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTS_TurnOnPS(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOnList', 'turnOnListDetailed']

        """
        return exec_with_tcl('APSMpLTS_TurnOnPS', *args, **kwargs)

    @staticmethod
    def APSMpLTS_TurnOffPSInfo(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTS_TurnOffPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTS_TurnOffPS(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOffList', 'turnOffListDetailed']

        """
        return exec_with_tcl('APSMpLTS_TurnOffPS', *args, **kwargs)

    @staticmethod
    def APSMpLTS_ConditionPowerSuppliesInfo(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTS_ConditionPowerSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTS_ConditionPowerSupplies(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: args
        APS parsed args: ['conditionList', 'conditionListDetailed', 'SCRFile', 'configured', 'cycles']

        """
        return exec_with_tcl('APSMpLTS_ConditionPowerSupplies', *args, **kwargs)

    @staticmethod
    def APSMpLTS_ConditionPS(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'conditionList', 'conditionListDetailed', 'SCRFile']

        """
        return exec_with_tcl('APSMpLTS_ConditionPS', *args, **kwargs)

    @staticmethod
    def APSMpLTS_WaitForConditioningPS(*args, **kwargs):
        """
        Location: TEST_STAND_OnOff.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpLTS_WaitForConditioningPS', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_StartupInfo(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_Modulator_StartupInfo', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_ShutdownInfo(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_Modulator_ShutdownInfo', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_StartupDialog(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_Modulator_StartupDialog', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_ShutdownDialog(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['frame']

        """
        return exec_with_tcl('LMOCS_Modulator_ShutdownDialog', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_Startup(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'SCRFile']

        """
        return exec_with_tcl('LMOCS_Modulator_Startup', *args, **kwargs)

    @staticmethod
    def LMOCS_Modulator_Shutdown(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'includeFilament']

        """
        return exec_with_tcl('LMOCS_Modulator_Shutdown', *args, **kwargs)

    @staticmethod
    def LMOCS_TurnOn(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['sector', 'attnSetPoint', 'attnPVName', 'sledTrig', 'sledTrigVar', 'resumePCS', 'SCRFile']

        """
        return exec_with_tcl('LMOCS_TurnOn', *args, **kwargs)

    @staticmethod
    def LMOCS_TurnOff(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['sector']

        """
        return exec_with_tcl('LMOCS_TurnOff', *args, **kwargs)

    @staticmethod
    def LMOCS_ShutdownTillReadyToPulseOff(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['sector', 'rampPFN']

        """
        return exec_with_tcl('LMOCS_ShutdownTillReadyToPulseOff', *args, **kwargs)

    @staticmethod
    def LMOCS_ResetAutoPhaseControl(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['SCRFile', 'L1', 'L2', 'L3', 'L4', 'L5']

        """
        return exec_with_tcl('LMOCS_ResetAutoPhaseControl', *args, **kwargs)

    @staticmethod
    def LMOCS_PowerControlLawSetup(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'mode']

        """
        return exec_with_tcl('LMOCS_PowerControlLawSetup', *args, **kwargs)

    @staticmethod
    def CheckModulatorInterlocks(*args, **kwargs):
        """
        Location: LMOCS_TurnOn.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5']

        """
        return exec_with_tcl('CheckModulatorInterlocks', *args, **kwargs)

    @staticmethod
    def ReturnFromRampCorrection(*args, **kwargs):
        """
        Location: boosterRamp.tcl
        TCL function args: args
        APS parsed args: ['error', 'supply']

        """
        return exec_with_tcl('ReturnFromRampCorrection', *args, **kwargs)

    @staticmethod
    def BoosterRampVCorrectAndCheck(*args, **kwargs):
        """
        Location: boosterRamp.tcl
        TCL function args: args
        APS parsed args: ['supply', 'application', 'user', 'host', 'runControlPV', 'LLTime1', 'LTime1']

        """
        return exec_with_tcl('BoosterRampVCorrectAndCheck', *args, **kwargs)

    @staticmethod
    def APSBoosterLoadSafetyRamp(*args, **kwargs):
        """
        Location: boosterRamp.tcl
        TCL function args: args
        APS parsed args: ['BM', 'QD', 'QF', 'SD', 'SF', 'statusCallback', 'description', 'Magnet', 'IRamp']

        """
        return exec_with_tcl('APSBoosterLoadSafetyRamp', *args, **kwargs)

    @staticmethod
    def BoosterRampVCurrentCorrectAndCheck(*args, **kwargs):
        """
        Location: boosterRamp.tcl
        TCL function args: args
        APS parsed args: ['supply', 'application', 'user', 'host', 'runControlPV', 'LLTime1', 'LTime1', 'shift0', 'HTime1', 'HHTime1']

        """
        return exec_with_tcl('BoosterRampVCurrentCorrectAndCheck', *args, **kwargs)

    @staticmethod
    def APSSCRDefineVariables(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['topDirectory', 'inhibitLogging']

        """
        return exec_with_tcl('APSSCRDefineVariables', *args, **kwargs)

    @staticmethod
    def APSSCRSRCompareConvertors(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['machine', 'snapshot1', 'snapshot2', 'readback', 'group', 'plots', 'fileDisplay']

        """
        return exec_with_tcl('APSSCRSRCompareConvertors', *args, **kwargs)

    @staticmethod
    def APSSCRSRCompareOrbitSetpoints(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRSRCompareOrbitSetpoints', *args, **kwargs)

    @staticmethod
    def APSSCRSRCompareOrbitOffsets(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRSRCompareOrbitOffsets', *args, **kwargs)

    @staticmethod
    def APSSCRSRCompareBPMQuantities(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['machine', 'snapshot1', 'snapshot2', 'plots', 'fileDisplay', 'quantity', 'mode']

        """
        return exec_with_tcl('APSSCRSRCompareBPMQuantities', *args, **kwargs)

    @staticmethod
    def APSSCRXrayTranslationCompare(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['machine', 'snapshot1', 'snapshot2', 'mode']

        """
        return exec_with_tcl('APSSCRXrayTranslationCompare', *args, **kwargs)

    @staticmethod
    def APSSetTuneMultiplexer(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['mode', 'sum']

        """
        return exec_with_tcl('APSSetTuneMultiplexer', *args, **kwargs)

    @staticmethod
    def APSSCRProcessXrayBPMSnapshot(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['inputFile', 'outputFile', 'bpmType', 'plane']

        """
        return exec_with_tcl('APSSCRProcessXrayBPMSnapshot', *args, **kwargs)

    @staticmethod
    def APSSRXrayBPMCustomCompare(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRXrayBPMCustomCompare', *args, **kwargs)

    @staticmethod
    def APSSCRPrintXrayBPMCompTable(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRPrintXrayBPMCompTable', *args, **kwargs)

    @staticmethod
    def APSSRPlotSCRBPMData(*args, **kwargs):
        """
        Location: SiteSpecificSCR.tcl
        TCL function args: args
        APS parsed args: ['field', 'machine', 'snapshot']

        """
        return exec_with_tcl('APSSRPlotSCRBPMData', *args, **kwargs)

    @staticmethod
    def APSLSuspendResumeRFPowerControllaws(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['klystronList', 'mode', 'valueList']

        """
        return exec_with_tcl('APSLSuspendResumeRFPowerControllaws', *args, **kwargs)

    @staticmethod
    def APSLReduceKlystronOutputPower(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['klystronList', 'powerLevel', 'stepSize', 'iterationLimit', 'pause']

        """
        return exec_with_tcl('APSLReduceKlystronOutputPower', *args, **kwargs)

    @staticmethod
    def APSLRampPFNVoltage(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['klystronList', 'rampTo', 'steps', 'pause', 'rampToList', 'checkVacuum']

        """
        return exec_with_tcl('APSLRampPFNVoltage', *args, **kwargs)

    @staticmethod
    def APSMpGenericPSArrayQuery(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'operation', 'invert']

        """
        return exec_with_tcl('APSMpGenericPSArrayQuery', *args, **kwargs)

    @staticmethod
    def APSLGenericPSArrayQuery(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'operation', 'invert']

        """
        return exec_with_tcl('APSLGenericPSArrayQuery', *args, **kwargs)

    @staticmethod
    def APSMpGenericPSArraySetup(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOnList', 'turnOffList', 'conditionList', 'arrayName', 'SCRFile', 'cycles', 'turnOnListDetailed', 'turnOffListDetailed', 'conditionListDetailed', 'system']

        """
        return exec_with_tcl('APSMpGenericPSArraySetup', *args, **kwargs)

    @staticmethod
    def APSLGenericPSArraySetup(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOnList', 'turnOffList', 'conditionList', 'arrayName', 'SCRFile', 'cycles', 'turnOnListDetailed', 'turnOffListDetailed', 'conditionListDetailed']

        """
        return exec_with_tcl('APSLGenericPSArraySetup', *args, **kwargs)

    @staticmethod
    def APSMpGenericPSDialog(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOn', 'turnOff', 'condition', 'chooseSCR', 'arrayName', 'frame', 'packProc', 'packProcBottom', 'system']

        """
        return exec_with_tcl('APSMpGenericPSDialog', *args, **kwargs)

    @staticmethod
    def APSLGenericPSDialog(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOn', 'turnOff', 'condition', 'chooseSCR', 'arrayName', 'frame', 'packProc', 'packProcBottom', 'system']

        """
        return exec_with_tcl('APSLGenericPSDialog', *args, **kwargs)

    @staticmethod
    def APSMpDetailedPSDialog(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'arrayName', 'frame', 'system']

        """
        return exec_with_tcl('APSMpDetailedPSDialog', *args, **kwargs)

    @staticmethod
    def APSLDetailedPSDialog(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'arrayName', 'frame']

        """
        return exec_with_tcl('APSLDetailedPSDialog', *args, **kwargs)

    @staticmethod
    def APSMpLTurnOffPSInfo(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTurnOffPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTurnOffPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOffList', 'turnOffListDetailed']

        """
        return exec_with_tcl('APSMpLTurnOffPS', *args, **kwargs)

    @staticmethod
    def APSMpLTurnOnPSInfo(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLTurnOnPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLTurnOnPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOnList', 'turnOnListDetailed']

        """
        return exec_with_tcl('APSMpLTurnOnPS', *args, **kwargs)

    @staticmethod
    def APSMpArrayDrivenOperationPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'operation', 'system']

        """
        return exec_with_tcl('APSMpArrayDrivenOperationPS', *args, **kwargs)

    @staticmethod
    def APSLArrayDrivenOperationPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'operation']

        """
        return exec_with_tcl('APSLArrayDrivenOperationPS', *args, **kwargs)

    @staticmethod
    def APSMpLStartUpPSInfo(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLStartUpPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLStartUpPSPackProc(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLStartUpPSPackProc', *args, **kwargs)

    @staticmethod
    def APSMpLStartUpPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOnList', 'conditionList', 'turnOnListDetailed', 'conditionListDetailed', 'SCRFile', 'configured', 'waitForConditioning', 'waitForConditioningOnly', 'cycles', 'turnOffUnused']

        """
        return exec_with_tcl('APSMpLStartUpPS', *args, **kwargs)

    @staticmethod
    def APSMpLConditionPowerSuppliesInfo(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLConditionPowerSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpLConditionPowerSupplies(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['autoAdd', 'conditionList', 'conditionListDetailed', 'SCRFile', 'configured', 'cycles']

        """
        return exec_with_tcl('APSMpLConditionPowerSupplies', *args, **kwargs)

    @staticmethod
    def APSMpLWaitTurnOnPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpLWaitTurnOnPS', *args, **kwargs)

    @staticmethod
    def APSMpLConditionPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'conditionList', 'conditionListDetailed', 'SCRFile']

        """
        return exec_with_tcl('APSMpLConditionPS', *args, **kwargs)

    @staticmethod
    def APSMpLWaitForConditioningPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpLWaitForConditioningPS', *args, **kwargs)

    @staticmethod
    def APSMpLShutDownPSInfo(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLShutDownPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLShutDownPS(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['turnOffList', 'conditionList', 'configured', 'turnOffListDetailed', 'conditionListDetailed', 'SCRFile']

        """
        return exec_with_tcl('APSMpLShutDownPS', *args, **kwargs)

    @staticmethod
    def APSMpConvertDeviceNames(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'deviceList', 'system']

        """
        return exec_with_tcl('APSMpConvertDeviceNames', *args, **kwargs)

    @staticmethod
    def APSMpLConvertDeviceNames(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'deviceList']

        """
        return exec_with_tcl('APSMpLConvertDeviceNames', *args, **kwargs)

    @staticmethod
    def APSMpConvertDetailedDeviceNames(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'deviceList', 'arrayName', 'invert']

        """
        return exec_with_tcl('APSMpConvertDetailedDeviceNames', *args, **kwargs)

    @staticmethod
    def APSMpLConvertDetailedDeviceNames(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: ['operation', 'deviceList', 'arrayName', 'invert']

        """
        return exec_with_tcl('APSMpLConvertDetailedDeviceNames', *args, **kwargs)

    @staticmethod
    def APSPEMTKDialog(*args, **kwargs):
        """
        Location: switch.tcl
        Usage: APSPEMTKDialogHelp widget
        [-title <string>]
        [-text <string>]
        [-bitmap <string>]
        [-default <button index>]
        [-strings <button list>]
        [-wrapLength <length>]
        [-appendtext <1|0>]TCL function args: widget args
        APS parsed args: ['title', 'text', 'bitmap', 'default', 'strings', 'wrapLength', 'appendtext']

        """
        return exec_with_tcl('APSPEMTKDialog', *args, **kwargs)

    @staticmethod
    def tk_dialog2(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: UNKNOWN
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('tk_dialog2', *args, **kwargs)

    @staticmethod
    def APSMpLStartPSConditionLogging(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpLStartPSConditionLogging', *args, **kwargs)

    @staticmethod
    def APSMpLExaminePSConditionLogging(*args, **kwargs):
        """
        Location: switch.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpLExaminePSConditionLogging', *args, **kwargs)

    @staticmethod
    def APSIDGoAndWait(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['ID', 'tolerance', 'timeout', 'retries']

        """
        return exec_with_tcl('APSIDGoAndWait', *args, **kwargs)

    @staticmethod
    def APSIDsGoAndWait(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'tolerance', 'timeout', 'retries']

        """
        return exec_with_tcl('APSIDsGoAndWait', *args, **kwargs)

    @staticmethod
    def APSGetSourcePointSectors(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['numberFormat', 'group']

        """
        return exec_with_tcl('APSGetSourcePointSectors', *args, **kwargs)

    @staticmethod
    def APSIDOpenAllGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSIDOpenAllGaps', *args, **kwargs)

    @staticmethod
    def APSCheckRFPower(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCheckRFPower', *args, **kwargs)

    @staticmethod
    def APSIDStaggerGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'interval', 'returnGaps']

        """
        return exec_with_tcl('APSIDStaggerGaps', *args, **kwargs)

    @staticmethod
    def APSIDMoveRegularGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'interval', 'returnGaps']

        """
        return exec_with_tcl('APSIDMoveRegularGaps', *args, **kwargs)

    @staticmethod
    def APSIDReturnAllGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSIDReturnAllGaps', *args, **kwargs)

    @staticmethod
    def APSIDGetBadDeviceList(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSIDGetBadDeviceList', *args, **kwargs)

    @staticmethod
    def APSIDGetDeviceList(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['full']

        """
        return exec_with_tcl('APSIDGetDeviceList', *args, **kwargs)

    @staticmethod
    def APSIDGetTaperDeviceList(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['full']

        """
        return exec_with_tcl('APSIDGetTaperDeviceList', *args, **kwargs)

    @staticmethod
    def APSIDMinimumActualGap(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSIDMinimumActualGap', *args, **kwargs)

    @staticmethod
    def APSIDSectorList(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSIDSectorList', *args, **kwargs)

    @staticmethod
    def APSBMSectorList(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSBMSectorList', *args, **kwargs)

    @staticmethod
    def APSIDControlGapAccess(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['newModes', 'newMode', 'readOnly']

        """
        return exec_with_tcl('APSIDControlGapAccess', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToMachinePhysicsModeInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSwitchToMachinePhysicsModeInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToMachinePhysicsModeInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSwitchToMachinePhysicsModeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToMachinePhysicsMode(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['openGaps', 'restoreXbpmRefGaps', 'closeInteral']

        """
        return exec_with_tcl('APSMpIDSwitchToMachinePhysicsMode', *args, **kwargs)

    @staticmethod
    def APSMpIDTransferSettingsToReturnValuesInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDTransferSettingsToReturnValuesInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDTransferSettingsToReturnValuesInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDTransferSettingsToReturnValuesInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDTransferSettingsToReturnValues(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpIDTransferSettingsToReturnValues', *args, **kwargs)

    @staticmethod
    def APSSetSCUCurrentReturnValues(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSCUCurrentReturnValues', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToUserModeInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSwitchToUserModeInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToUserModeInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSwitchToUserModeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDSwitchToUserMode(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['returnGaps', 'closeInterval', 'setupCerenkov']

        """
        return exec_with_tcl('APSMpIDSwitchToUserMode', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreUserGapsInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreUserGapsInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreUserGapsInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreUserGapsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreUserGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'closeInterval']

        """
        return exec_with_tcl('APSMpIDRestoreUserGaps', *args, **kwargs)

    @staticmethod
    def APSMpIDTimeRestoreUserGapsInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDTimeRestoreUserGapsInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDTimeRestoreUserGapsInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDTimeRestoreUserGapsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDTimeRestoreUserGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'closeInterval']

        """
        return exec_with_tcl('APSMpIDTimeRestoreUserGaps', *args, **kwargs)

    @staticmethod
    def APSMpCPUInitializeInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCPUInitializeInfo', *args, **kwargs)

    @staticmethod
    def APSMpCPUInitialize(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpCPUInitialize', *args, **kwargs)

    @staticmethod
    def APSMpResetCPUAfgInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpResetCPUAfgInfo', *args, **kwargs)

    @staticmethod
    def APSMpResetCPUAfg(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpResetCPUAfg', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreMinimumGapsInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreMinimumGapsInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreMinimumGapsInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreMinimumGapsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreXbpmRefGapsInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreXbpmRefGapsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreXbpmRefGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['closeInterval', 'group', 'orbitSwitch', 'pem', 'wait']

        """
        return exec_with_tcl('APSMpIDRestoreXbpmRefGaps', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreMinimumGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['closeInterval']

        """
        return exec_with_tcl('APSMpIDRestoreMinimumGaps', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreXbpmRefGapsInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreXbpmRefGapsInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapTo60mmInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSetGapTo60mmInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapTo180mmInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSetGapTo180mmInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapToMinimumInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSetGapToMinimumInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapToMinimumInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSetGapToMinimumInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapToMinimum(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['closeInterval']

        """
        return exec_with_tcl('APSMpIDSetGapToMinimum', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapTo60mmInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDSetGapTo60mmInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapTo60mm(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['closeInterval', 'orbitSwitch']

        """
        return exec_with_tcl('APSMpIDSetGapTo60mm', *args, **kwargs)

    @staticmethod
    def APSMpIDSetGapTo180mm(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['orbitSwitch']

        """
        return exec_with_tcl('APSMpIDSetGapTo180mm', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreOpenGapsInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreOpenGapsInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreOpenGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['orbitSwitch']

        """
        return exec_with_tcl('APSMpIDRestoreOpenGaps', *args, **kwargs)

    @staticmethod
    def APSSRPrepareMovingID01Gaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['dsGap', 'usGap', 'orbitSwitch']

        """
        return exec_with_tcl('APSSRPrepareMovingID01Gaps', *args, **kwargs)

    @staticmethod
    def APSSRPrepareMovingSCU0Gaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['gapList', 'IDList', 'orbitSwitch']

        """
        return exec_with_tcl('APSSRPrepareMovingSCU0Gaps', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['gapfile', 'wait', 'confirm', 'switchToMachinePhysics', 'closeInterval', 'orbitSwitch', 'pem']

        """
        return exec_with_tcl('APSMpIDRestoreGaps', *args, **kwargs)

    @staticmethod
    def APSMpWaitForIDs(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'timeout']

        """
        return exec_with_tcl('APSMpWaitForIDs', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreGapsFromSCRInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIDRestoreGapsFromSCRInfo', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreGapsFromSCRInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame args
        APS parsed args: ['pem', 'label']

        """
        return exec_with_tcl('APSMpIDRestoreGapsFromSCRInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIDRestoreGapsFromSCR(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'closeInterval', 'pem', 'label', 'ShortFilename', 'orbitSwitch']

        """
        return exec_with_tcl('APSMpIDRestoreGapsFromSCR', *args, **kwargs)

    @staticmethod
    def APSMpCheckAndWaitForIDs(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['deviceList', 'tolerance', 'timeout']

        """
        return exec_with_tcl('APSMpCheckAndWaitForIDs', *args, **kwargs)

    @staticmethod
    def TestCheckIDPem(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('TestCheckIDPem', *args, **kwargs)

    @staticmethod
    def APSCloseID35Shutter(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSCloseID35Shutter', *args, **kwargs)

    @staticmethod
    def APSMpRebootCPUIOCInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRebootCPUIOCInfo', *args, **kwargs)

    @staticmethod
    def APSMpRebootCPUIOC(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRebootCPUIOC', *args, **kwargs)

    @staticmethod
    def APSProcessCPUCorrector(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['filename', 'lowLimit', 'tolerance']

        """
        return exec_with_tcl('APSProcessCPUCorrector', *args, **kwargs)

    @staticmethod
    def APSProcessCPUACMode(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['filename', 'voltage', 'tolerance', 'halfPeriod']

        """
        return exec_with_tcl('APSProcessCPUACMode', *args, **kwargs)

    @staticmethod
    def ProcessCPUDCData(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['filename', 'mode', 'tolerance']

        """
        return exec_with_tcl('ProcessCPUDCData', *args, **kwargs)

    @staticmethod
    def APSSetupSRCerenkovDector(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['detectorList', 'filename', 'statusCallback']

        """
        return exec_with_tcl('APSSetupSRCerenkovDector', *args, **kwargs)

    @staticmethod
    def APSGetCherenkovBoard(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['detector']

        """
        return exec_with_tcl('APSGetCherenkovBoard', *args, **kwargs)

    @staticmethod
    def APSMpIEXInitializeInfo(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIEXInitializeInfo', *args, **kwargs)

    @staticmethod
    def UpdateIEXSelection(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('UpdateIEXSelection', *args, **kwargs)

    @staticmethod
    def APSMpIEXInitializeInitDialog(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIEXInitializeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpIEXInitialize(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpIEXInitialize', *args, **kwargs)

    @staticmethod
    def APSSRMoveSCUID(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['ID', 'moveTo']

        """
        return exec_with_tcl('APSSRMoveSCUID', *args, **kwargs)

    @staticmethod
    def APSSRMoveID01US(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['moveTo']

        """
        return exec_with_tcl('APSSRMoveID01US', *args, **kwargs)

    @staticmethod
    def APSSRMoveIDGaps(*args, **kwargs):
        """
        Location: APSMpID.tcl
        TCL function args: args
        APS parsed args: ['IDList', 'open', 'moveTo', 'minGapList', 'deltaToMinGap', 'lockedIDList', 'fixedIDList', 'fixedGapList', 'closeInterval', 'pem']

        """
        return exec_with_tcl('APSSRMoveIDGaps', *args, **kwargs)

    @staticmethod
    def LPL_ConfigureInfo(*args, **kwargs):
        """
        Location: LPL_Configure.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('LPL_ConfigureInfo', *args, **kwargs)

    @staticmethod
    def LPL_Configure(*args, **kwargs):
        """
        Location: LPL_Configure.tcl
        TCL function args: args
        APS parsed args: ['bypass']

        """
        return exec_with_tcl('LPL_Configure', *args, **kwargs)

    @staticmethod
    def LPL_ConfigurePackProc(*args, **kwargs):
        """
        Location: LPL_Configure.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LPL_ConfigurePackProc', *args, **kwargs)

    @staticmethod
    def LPL_ConfigurePackProcBottom(*args, **kwargs):
        """
        Location: LPL_Configure.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LPL_ConfigurePackProcBottom', *args, **kwargs)

    @staticmethod
    def APSMeasureL1Momentum(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMeasureL1Momentum', *args, **kwargs)

    @staticmethod
    def APSGetLinacQuadStrengths(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetLinacQuadStrengths', *args, **kwargs)

    @staticmethod
    def APSGetAllLinacQuadStrengths(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetAllLinacQuadStrengths', *args, **kwargs)

    @staticmethod
    def APSPropagateMeasuredTwissLIFS1(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSPropagateMeasuredTwissLIFS1', *args, **kwargs)

    @staticmethod
    def APSMatchFromMeasuredTwissLIFS1(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMatchFromMeasuredTwissLIFS1', *args, **kwargs)

    @staticmethod
    def APSMatchFromMeasuredTwissBC(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMatchFromMeasuredTwissBC', *args, **kwargs)

    @staticmethod
    def APSGenerateLinacSetpointFile(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'output', 'convertAll', 'beginMomentum', 'postL2Momentum', 'postL4Momentum', 'postL5Momentum', 'rescale', 'includeChicane']

        """
        return exec_with_tcl('APSGenerateLinacSetpointFile', *args, **kwargs)

    @staticmethod
    def APSMakeInjectorConditioningFile(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: ['output', 'sectorList', 'cycles', 'degauss']

        """
        return exec_with_tcl('APSMakeInjectorConditioningFile', *args, **kwargs)

    @staticmethod
    def APSFindL3BMCurrent(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: ['element', 'angle', 'momentum', 'trimForCurrent']

        """
        return exec_with_tcl('APSFindL3BMCurrent', *args, **kwargs)

    @staticmethod
    def APSRestoreLinacSetpointFile(*args, **kwargs):
        """
        Location: measurements.tcl
        TCL function args: args
        APS parsed args: ['fileName', 'statusCallback', 'condition', 'baseline']

        """
        return exec_with_tcl('APSRestoreLinacSetpointFile', *args, **kwargs)

    @staticmethod
    def DebugInfo(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: message
        APS parsed args: None

        """
        return exec_with_tcl('DebugInfo', *args, **kwargs)

    @staticmethod
    def APSTestPort(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSTestPort', *args, **kwargs)

    @staticmethod
    def APSMpParallel(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        Usage: <id> APSMpParallel
        [-procedure <string>] where string is full procedure name with args
        [-host <string>]
        [-interface 1] force creation of a status interface in Automatic mode
        [-mode <string>] where mode is Manual, Semi-Automatic, or Automatic

        Note that mode and host are implied by current context. The mode and
        host options permit overriding current settings.
        Returns a unique id for use by APSMpJoin.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParallel', *args, **kwargs)

    @staticmethod
    def processMpOutput(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: sd
        APS parsed args: None

        """
        return exec_with_tcl('processMpOutput', *args, **kwargs)

    @staticmethod
    def childUp(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: childServerPort
        APS parsed args: None

        """
        return exec_with_tcl('childUp', *args, **kwargs)

    @staticmethod
    def childExit(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: childServerPort childHost childId
        APS parsed args: None

        """
        return exec_with_tcl('childExit', *args, **kwargs)

    @staticmethod
    def childErrorCallback(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: childSd procName errorMessage
        APS parsed args: None

        """
        return exec_with_tcl('childErrorCallback', *args, **kwargs)

    @staticmethod
    def childResultCallback(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: args
        APS parsed args: ['id', 'serial', 'chan', 'code', 'errorcode', 'result']

        """
        return exec_with_tcl('childResultCallback', *args, **kwargs)

    @staticmethod
    def APSMpAbort(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        Usage: APSMpAbort <id>
        Abort the parallel procedure identified by <id>.
        If <id> is "all", then abort all outstanding parallel procedures. Useful
        for aborting a set of parallel procedures when one of them returns an error.
        Otherwise one would block on APSMpReturn/APSMpJoin until the others completed.TCL function args: parallelId args
        APS parsed args: ['onError']

        """
        return exec_with_tcl('APSMpAbort', *args, **kwargs)

    @staticmethod
    def APSMpJoin(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        Usage: <results> APSMpJoin <id>
        Synchronize current execution with parallel procedure identified
        by <id>. This call will cause execution to block until <id> completes.
        Any return value of your parallel procedure is returned in <results>.
        Note: you should surround this with catch, since an error in the parallel
        procedure will generate an error during the later join.TCL function args: parallelId
        APS parsed args: None

        """
        return exec_with_tcl('APSMpJoin', *args, **kwargs)

    @staticmethod
    def APSMpParallelListDelete(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        TCL function args: list value
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParallelListDelete', *args, **kwargs)

    @staticmethod
    def APSMpInterface(*args, **kwargs):
        """
        Location: APSMpParallel.tcl
        Usage: APSMpInterface
        Returns 1 if the current execution environment of your procedure permits
        the use of graphical widgets, 0 otherwise.TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpInterface', *args, **kwargs)

    @staticmethod
    def APSVertSplitSddscontourFlagImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSVertSplitSddscontourFlagImage', *args, **kwargs)

    @staticmethod
    def APSNormalizeSddscontourFlagImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSNormalizeSddscontourFlagImage', *args, **kwargs)

    @staticmethod
    def APSFindEdgesOnFlagHLImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['filename', 'columnFilter', 'threshold', 'centerIndex']

        """
        return exec_with_tcl('APSFindEdgesOnFlagHLImage', *args, **kwargs)

    @staticmethod
    def APSCalibrateLinacFlagHLImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'lineNamePrefix']

        """
        return exec_with_tcl('APSCalibrateLinacFlagHLImage', *args, **kwargs)

    @staticmethod
    def APSCaptureHLImageInSeries(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['beamline', 'rootname', 'numberToAverage', 'numberToAcquire', 'wmonitorFile', 'lineNamePrefix', 'indexDigits', 'index', 'hROI', 'vROI', 'backgroundsToAverage', 'beamTriggerNumber', 'backgroundTriggerNumber', '-statusCallback', 'statusCallback', 'doAnalysis', 'subtractBackground', 'imagePV']

        """
        return exec_with_tcl('APSCaptureHLImageInSeries', *args, **kwargs)

    @staticmethod
    def APSCaptureHLImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['takeBackground', 'beamline', 'rootname', 'backgroundFile', 'numberToAverage', 'wmonitorFile', 'lineNamePrefix', 'vROI', 'hROI', 'beamTriggerNumber', 'backgroundTriggerNumber', 'statusCallback', 'evenOddNorm', 'doAnalysis', 'numberToAcquire', 'imagePV']

        """
        return exec_with_tcl('APSCaptureHLImage', *args, **kwargs)

    @staticmethod
    def APSAnalyzeHLImage(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAnalyzeHLImage', *args, **kwargs)

    @staticmethod
    def APSCaptureImageProfileInSeries(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['beamline', 'rootname', 'numberToAverage', 'wmonitorFile', 'scalarsFile', 'indexDigits', 'index', 'beamTriggerNumber', 'statusCallback', 'backgroundTriggerNumber']

        """
        return exec_with_tcl('APSCaptureImageProfileInSeries', *args, **kwargs)

    @staticmethod
    def APSCaptureImageProfile(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['beamline', 'output', 'numberToAverage', 'wmonitorFile', 'scalarsFile', 'beamTriggerNumber', 'statusCallback', 'backgroundTriggerNumber']

        """
        return exec_with_tcl('APSCaptureImageProfile', *args, **kwargs)

    @staticmethod
    def APSConfigureCameraAndScreenPVs(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['flagIn', 'lampOn', 'flag', 'system', 'statusCallback', 'actuatorNumber', 'ignoreFlagReadback', 'cameraType']

        """
        return exec_with_tcl('APSConfigureCameraAndScreenPVs', *args, **kwargs)

    @staticmethod
    def APSSetBCCameraAperture(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['flagList', 'lowres', 'delta', 'tries', 'statusCallback', 'passes', 'alreadyInserted', 'abortVariable', 'saturatedPixelLimit']

        """
        return exec_with_tcl('APSSetBCCameraAperture', *args, **kwargs)

    @staticmethod
    def APSSetLinacFlagROI(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['flagList', 'lowres', 'statusCallback', 'factor', 'xMinSize', 'yMinSize', 'clipSize', 'xEdgeSize', 'yEdgeSize', 'alreadyInserted', 'samples', 'suppressNoise']

        """
        return exec_with_tcl('APSSetLinacFlagROI', *args, **kwargs)

    @staticmethod
    def APSThreeScreenEmitMeas(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['system', 'abortVariable', 'samples', 'rootname', 'postSwitchPause', 'beamEnergy', 'dataToUse', 'useMV200BGSubtraction', 'statusCallback', 'analyze', 'randomizations', 'autoExclude', 'autoROI', 'autoAperture', 'saveImage']

        """
        return exec_with_tcl('APSThreeScreenEmitMeas', *args, **kwargs)

    @staticmethod
    def APSTakeThreeScreenEmitMeasData(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['configDir', 'abortVariable', 'samplesList', 'screenList', 'positionList', 'actuatorNumberList', 'xCalList', 'yCalList', 'xResList', 'yResList', 'xErrList', 'yErrList', 'cameraTypeList', 'rootname', 'postSwitchPause', 'beamEnergy', 'dataToUse', 'idealBeta', 'idealAlpha', 'useMV200BGSubtraction', 'statusCallback', 'saveImage', 'autoSetROIList', 'autoSetApertureList', 'saturatedPixelLimitList']

        """
        return exec_with_tcl('APSTakeThreeScreenEmitMeasData', *args, **kwargs)

    @staticmethod
    def APSAnalyzeThreeScreenEmitData(*args, **kwargs):
        """
        Location: APSFlags.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'statusCallback', 'displayPrintout', 'randomizations', 'beamEnergy', 'excludeListArray', 'dataToUse', 'autoExclude', 'outlierLimit', 'outlierPasses']

        """
        return exec_with_tcl('APSAnalyzeThreeScreenEmitData', *args, **kwargs)

    @staticmethod
    def APSMpLEA_TurnOnPSInfo(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLEA_TurnOnPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLEA_TurnOnPS(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOnList', 'turnOnListDetailed']

        """
        return exec_with_tcl('APSMpLEA_TurnOnPS', *args, **kwargs)

    @staticmethod
    def APSMpLEA_TurnOffPSInfo(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLEA_TurnOffPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpLEA_TurnOffPS(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'turnOffList', 'turnOffListDetailed']

        """
        return exec_with_tcl('APSMpLEA_TurnOffPS', *args, **kwargs)

    @staticmethod
    def APSMpLEA_ConditionPowerSuppliesInfo(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpLEA_ConditionPowerSuppliesInfo', *args, **kwargs)

    @staticmethod
    def APSMpLEA_ConditionPowerSupplies(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: args
        APS parsed args: ['conditionList', 'conditionListDetailed', 'SCRFile', 'configured', 'cycles']

        """
        return exec_with_tcl('APSMpLEA_ConditionPowerSupplies', *args, **kwargs)

    @staticmethod
    def APSMpLEA_ConditionPS(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: args
        APS parsed args: ['arrayName', 'configured', 'conditionList', 'conditionListDetailed', 'SCRFile']

        """
        return exec_with_tcl('APSMpLEA_ConditionPS', *args, **kwargs)

    @staticmethod
    def APSMpLEA_WaitForConditioningPS(*args, **kwargs):
        """
        Location: LEA_PS_OnOff.tcl
        TCL function args: args
        APS parsed args: ['deviceList']

        """
        return exec_with_tcl('APSMpLEA_WaitForConditioningPS', *args, **kwargs)

    @staticmethod
    def APSMpSRFStartUpInfo(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRFStartUp(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFStartUp', *args, **kwargs)

    @staticmethod
    def APSMpSRFStandbyInfo(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFStandbyInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFStandbyInitDialog(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFStandbyInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRFStandby(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['SRF1', 'SRF2', 'SRF3', 'SRF4']

        """
        return exec_with_tcl('APSMpSRFStandby', *args, **kwargs)

    @staticmethod
    def APSMpSRFShutDownInfo(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFShutDownInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRFShutDownDialog(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRFShutDownDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRFShutDown(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['SRF1', 'SRF2', 'SRF3', 'SRF4']

        """
        return exec_with_tcl('APSMpSRFShutDown', *args, **kwargs)

    @staticmethod
    def APSMpSRFBringUpToFullPower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFBringUpToFullPower', *args, **kwargs)

    @staticmethod
    def APSMpSRFSystemIsOn(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['level', 'rf']

        """
        return exec_with_tcl('APSMpSRFSystemIsOn', *args, **kwargs)

    @staticmethod
    def APSMpSRFManualPrepCheck(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFManualPrepCheck', *args, **kwargs)

    @staticmethod
    def APSMpSRFLowerBeamCurrent(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'rf']

        """
        return exec_with_tcl('APSMpSRFLowerBeamCurrent', *args, **kwargs)

    @staticmethod
    def APSSRFCheckCathodeSupply(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSSRFCheckCathodeSupply', *args, **kwargs)

    @staticmethod
    def APSSRFCheckModAnodeSupply(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSSRFCheckModAnodeSupply', *args, **kwargs)

    @staticmethod
    def APSMpSRFHVPSReset(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFHVPSReset', *args, **kwargs)

    @staticmethod
    def APSMpSRFTurnOnBeam(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFTurnOnBeam', *args, **kwargs)

    @staticmethod
    def APSMpSRFRaiseBeamVoltage(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'expectedCurrent', 'bePrecise', 'currentTolerance', 'rf']

        """
        return exec_with_tcl('APSMpSRFRaiseBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSMpSRFLowerBeamVoltage(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'expectedCurrent', 'currentTolerance', 'rf']

        """
        return exec_with_tcl('APSMpSRFLowerBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSMpSRFAdjustBeamVoltage(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'expectedCurrent', 'currentTolerance', 'maxTries', 'rf']

        """
        return exec_with_tcl('APSMpSRFAdjustBeamVoltage', *args, **kwargs)

    @staticmethod
    def APSMpSRFTakeOutOfDiodeMode(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFTakeOutOfDiodeMode', *args, **kwargs)

    @staticmethod
    def APSMpSRFLowerModAnode(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'rf']

        """
        return exec_with_tcl('APSMpSRFLowerModAnode', *args, **kwargs)

    @staticmethod
    def APSMpSRFTurnOnModAnode(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf', 'zeroValue']

        """
        return exec_with_tcl('APSMpSRFTurnOnModAnode', *args, **kwargs)

    @staticmethod
    def APSMpSRFRaiseModAnode(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'rf']

        """
        return exec_with_tcl('APSMpSRFRaiseModAnode', *args, **kwargs)

    @staticmethod
    def APSMpSRFRaiseBeamCurrent(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'rf']

        """
        return exec_with_tcl('APSMpSRFRaiseBeamCurrent', *args, **kwargs)

    @staticmethod
    def APSMpSRFFullPowerFromStandby(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFFullPowerFromStandby', *args, **kwargs)

    @staticmethod
    def APSMpSRFTurnOnRF(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFTurnOnRF', *args, **kwargs)

    @staticmethod
    def APSSRFCheckForwardPower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['require', 'safeLevel', 'rf']

        """
        return exec_with_tcl('APSSRFCheckForwardPower', *args, **kwargs)

    @staticmethod
    def APSMpSRFRaisePower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['forwardTarget', 'finalCurrent', 'collectorLimit', 'modAnodeLimit', 'rf']

        """
        return exec_with_tcl('APSMpSRFRaisePower', *args, **kwargs)

    @staticmethod
    def APSMpSRFShutdownFromStandby(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFShutdownFromStandby', *args, **kwargs)

    @staticmethod
    def APSMpSRFResetCollectorInterlock(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf', 'timeLimit']

        """
        return exec_with_tcl('APSMpSRFResetCollectorInterlock', *args, **kwargs)

    @staticmethod
    def APSSRFCheckAveragePower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['require', 'rf']

        """
        return exec_with_tcl('APSSRFCheckAveragePower', *args, **kwargs)

    @staticmethod
    def APSMpSRFRaiseOrLowerAverageCavityPower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['target', 'rf']

        """
        return exec_with_tcl('APSMpSRFRaiseOrLowerAverageCavityPower', *args, **kwargs)

    @staticmethod
    def APSMpSRFCheckPhaseDetectorOutputVoltages(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf', 'max']

        """
        return exec_with_tcl('APSMpSRFCheckPhaseDetectorOutputVoltages', *args, **kwargs)

    @staticmethod
    def APSMpSRFBringUpToStandby(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFBringUpToStandby', *args, **kwargs)

    @staticmethod
    def APSMpSRFStandbyFromFullPower(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rf']

        """
        return exec_with_tcl('APSMpSRFStandbyFromFullPower', *args, **kwargs)

    @staticmethod
    def APSMpUpdateRFControllawTestLimitsInfo(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpUpdateRFControllawTestLimitsInfo', *args, **kwargs)

    @staticmethod
    def APSMpUpdateRFControllawTestLimitsDialog(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpUpdateRFControllawTestLimitsDialog', *args, **kwargs)

    @staticmethod
    def APSMpUpdateRFControllawTestLimits(*args, **kwargs):
        """
        Location: APSMpSR_RF_System.tcl
        TCL function args: args
        APS parsed args: ['rfFreqDelta', 'transferBPMrfErrors']

        """
        return exec_with_tcl('APSMpUpdateRFControllawTestLimits', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmErrorsToSetpointInfo(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTransferBpmErrorsToSetpointInfo', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmErrorsToSetpointDialog(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTransferBpmErrorsToSetpointDialog', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmErrorsToSetpoint(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: args
        APS parsed args: ['plane', 'rfMp', 'rfNb', 'ID', 'BM']

        """
        return exec_with_tcl('APSMpTransferBpmErrorsToSetpoint', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmRFErrorsToRFSetpointInfo(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTransferBpmRFErrorsToRFSetpointInfo', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmRFErrorsToRFSetpointDialog(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTransferBpmRFErrorsToRFSetpointDialog', *args, **kwargs)

    @staticmethod
    def APSMpTransferBpmRFErrorsToRFSetpoint(*args, **kwargs):
        """
        Location: APSMpTransferBpmErrorsToSetpoint.tcl
        TCL function args: args
        APS parsed args: ['rfFreqDelta', 'updateRFControlLawTestLimits']

        """
        return exec_with_tcl('APSMpTransferBpmRFErrorsToRFSetpoint', *args, **kwargs)

    @staticmethod
    def APSMpPTBStartUpInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStartUpInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBStartUp(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['energy', 'conditioningTime', 'restoreFile', 'DCPS', 'restoreDCPS']

        """
        return exec_with_tcl('APSMpPTBStartUp', *args, **kwargs)

    @staticmethod
    def APSMpPTBStartUpInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStartUpInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPTBTurnOnDCPSInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBTurnOnDCPSInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBTurnOnDCPS(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['retries']

        """
        return exec_with_tcl('APSMpPTBTurnOnDCPS', *args, **kwargs)

    @staticmethod
    def APSMpPTBStandardizeInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStandardizeInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBStandardize(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: NOT FOUND

        """
        return exec_with_tcl('APSMpPTBStandardize', *args, **kwargs)

    @staticmethod
    def APSMpPTBStandardizeInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStandardizeInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPTBDegaussInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBDegaussInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBDegauss(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degaussTime', 'block']

        """
        return exec_with_tcl('APSMpPTBDegauss', *args, **kwargs)

    @staticmethod
    def APSMpPTBDegaussInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBDegaussInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPTBCheckConditioning(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['degauss', 'standardize']

        """
        return exec_with_tcl('APSMpPTBCheckConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPTBWaitForConditioning(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBWaitForConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPTBRestoreFile(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['restoreFile', 'restoreDCPS']

        """
        return exec_with_tcl('APSMpPTBRestoreFile', *args, **kwargs)

    @staticmethod
    def APSMpPTBStopConditioningInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStopConditioningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBStopConditioning(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBStopConditioning', *args, **kwargs)

    @staticmethod
    def APSMpPTBClearApertureInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBClearApertureInfo', *args, **kwargs)

    @staticmethod
    def APSMpPTBClearAperture(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPTBClearAperture', *args, **kwargs)

    @staticmethod
    def APSMpSwitchLinacParTo1HzInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchLinacParTo1HzInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchLinacParTo1Hz(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchLinacParTo1Hz', *args, **kwargs)

    @staticmethod
    def APSMpSwitchLinacParTo2HzInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchLinacParTo2HzInfo', *args, **kwargs)

    @staticmethod
    def APSMpSwitchLinacParTo2Hz(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSwitchLinacParTo2Hz', *args, **kwargs)

    @staticmethod
    def APSMpParResetStreakCamera(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSMpParResetStreakCamera', *args, **kwargs)

    @staticmethod
    def APSMpParBunchLengthMeasSetupWithStreakCameraInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBunchLengthMeasSetupWithStreakCameraInfo', *args, **kwargs)

    @staticmethod
    def APSMpParBunchLengthMeasSetupWithStreakCameraInitDiag(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBunchLengthMeasSetupWithStreakCameraInitDiag', *args,
                             **kwargs)

    @staticmethod
    def APSMpParBunchLengthMeasSetupWithStreakCamera(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParBunchLengthMeasSetupWithStreakCamera', *args, **kwargs)

    @staticmethod
    def APSMpTurnOffStreakCameraInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOffStreakCameraInfo', *args, **kwargs)

    @staticmethod
    def APSMpTurnOffStreakCamera(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpTurnOffStreakCamera', *args, **kwargs)

    @staticmethod
    def APSMpPARBunchLengthMeasSetupWithDiodeAndScopeInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARBunchLengthMeasSetupWithDiodeAndScopeInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARBunchLengthMeasSetupWithDiodeAndScope(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARBunchLengthMeasSetupWithDiodeAndScope', *args, **kwargs)

    @staticmethod
    def APSMpPARHighChargeSetupInfo(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARHighChargeSetupInfo', *args, **kwargs)

    @staticmethod
    def APSParUpdateHighChargeMode(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSParUpdateHighChargeMode', *args, **kwargs)

    @staticmethod
    def APSMpPARHighChargeSetupInitDialog(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARHighChargeSetupInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARHighChargeSetup(*args, **kwargs):
        """
        Location: APSMpPTBTurnOn.tcl
        TCL function args: args
        APS parsed args: ['ShortFilename', 'mode', 'highCharge', 'useLPL', 'Timing']

        """
        return exec_with_tcl('APSMpPARHighChargeSetup', *args, **kwargs)

    @staticmethod
    def APSMpPARStartBunchCleaningInfo(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStartBunchCleaningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARStartBunchCleaningInitDialog(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStartBunchCleaningInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpPARStartBunchCleaning(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'ShortFilename', 'loadSCR', 'ds345Freq']

        """
        return exec_with_tcl('APSMpPARStartBunchCleaning', *args, **kwargs)

    @staticmethod
    def APSMpPARLoadBunchCleaningPVsFromSCR(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['ShortFilename', 'ds345Freq', 'statusCallback']

        """
        return exec_with_tcl('APSMpPARLoadBunchCleaningPVsFromSCR', *args, **kwargs)

    @staticmethod
    def APSMpPARSetupVSA(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['timeout']

        """
        return exec_with_tcl('APSMpPARSetupVSA', *args, **kwargs)

    @staticmethod
    def APSMpPARMeasureTune(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['timeout', 'setupVSA', 'statusCallback']

        """
        return exec_with_tcl('APSMpPARMeasureTune', *args, **kwargs)

    @staticmethod
    def APSMpPARVerifyBunchCleaningInfo(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARVerifyBunchCleaningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARVerifyBunchCleaning(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSMpPARVerifyBunchCleaning', *args, **kwargs)

    @staticmethod
    def APSMpPARStopBunchCleaningInfo(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpPARStopBunchCleaningInfo', *args, **kwargs)

    @staticmethod
    def APSMpPARStopBunchCleaning(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['statusCallback']

        """
        return exec_with_tcl('APSMpPARStopBunchCleaning', *args, **kwargs)

    @staticmethod
    def APSMpParRestoreBeam(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpParRestoreBeam', *args, **kwargs)

    @staticmethod
    def APSParBunchCleaningDrive(*args, **kwargs):
        """
        Location: APSMpPARBunchCleaning.tcl
        TCL function args: args
        APS parsed args: ['drive']

        """
        return exec_with_tcl('APSParBunchCleaningDrive', *args, **kwargs)

    @staticmethod
    def APSGetSRTuneWaveformHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetSRTuneWaveformHPVSA', *args, **kwargs)

    @staticmethod
    def APSGetSRTunesHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetSRTunesHPVSA', *args, **kwargs)

    @staticmethod
    def APSGetBoosterTunesHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetBoosterTunesHPVSA', *args, **kwargs)

    @staticmethod
    def APSGetBoosterTuneWaveformHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetBoosterTuneWaveformHPVSA', *args, **kwargs)

    @staticmethod
    def APSSetupSRVSAScope(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['sourceLevel', 'plane', 'root', 'freq', 'average', 'MXA', 'span', 'range']

        """
        return exec_with_tcl('APSSetupSRVSAScope', *args, **kwargs)

    @staticmethod
    def APSGetSRTunesVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetSRTunesVSA', *args, **kwargs)

    @staticmethod
    def APSSetupPARVSAScope(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['plane', 'freq', 'sourceLevel', 'span', 'resolution', 'average', 'averageNumber', 'repeat', 'waitTime', 'statusCallback']

        """
        return exec_with_tcl('APSSetupPARVSAScope', *args, **kwargs)

    @staticmethod
    def APSGetPARTuneHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['output', 'description', 'plane', 'freq', 'statusCallback', 'average', 'sourceLevel', 'span', 'resolution', 'freqPoints']

        """
        return exec_with_tcl('APSGetPARTuneHPVSA', *args, **kwargs)

    @staticmethod
    def APSGetPARTunesHPVSA(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGetPARTunesHPVSA', *args, **kwargs)

    @staticmethod
    def APSSetupDimtelForTuneMeasurement(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'xDriveFreq', 'yDriveFreq', 'xDriveFreqSpan', 'yDriveFreqSpan', 'xDrivePeriod', 'yDrivePeriod', 'xDriveAmplitude', 'yDriveAmplitude', 'xMarkerLow', 'xMarkerHigh', 'yMarkerLow', 'yMarkerHigh', 'average']

        """
        return exec_with_tcl('APSSetupDimtelForTuneMeasurement', *args, **kwargs)

    @staticmethod
    def APSSRMeasureTunesWithDimtel(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['statusCallback', 'xDriveFreq', 'yDriveFreq', 'xDriveFreqSpan', 'yDriveFreqSpan', 'average', 'setupDimtel', 'xDrivePeriod', 'yDrivePeriod', 'xDriveAmplitude', 'yDriveAmplitude', 'pause', 'xMarkerLow', 'xMarkerHigh', 'yMarkerLow', 'yMarkerHigh', 'xOnly', 'yOnly', 'rootname', 'plot', 'description']

        """
        return exec_with_tcl('APSSRMeasureTunesWithDimtel', *args, **kwargs)

    @staticmethod
    def APSSRProcessDimtelTunes(*args, **kwargs):
        """
        Location: HPVSATunes.tcl
        TCL function args: args
        APS parsed args: ['rootname', 'plot']

        """
        return exec_with_tcl('APSSRProcessDimtelTunes', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_ChangeAttenuator(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: ['device', 'klyDriveRef']

        """
        return exec_with_tcl('LMOCS_Recover_ChangeAttenuator', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_CheckVacuumAndWait(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: ['vacPVs', 'interval', 'L2', 'L5', 'VacuumLimit', 'readings']

        """
        return exec_with_tcl('LMOCS_Recover_CheckVacuumAndWait', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_CheckKLYForwardPower(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: ['RF', 'KLYForwardPowerRef']

        """
        return exec_with_tcl('LMOCS_Recover_CheckKLYForwardPower', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_In_ParallelInfo(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_Recover_In_ParallelInfo', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_In_ParallelDialog(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_Recover_In_ParallelDialog', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover_In_Parallel(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'SCRFile', 'maxStepSize']

        """
        return exec_with_tcl('LMOCS_Recover_In_Parallel', *args, **kwargs)

    @staticmethod
    def LMOCS_RecoverInfo(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_RecoverInfo', *args, **kwargs)

    @staticmethod
    def LMOCS_RecoverDialog(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('LMOCS_RecoverDialog', *args, **kwargs)

    @staticmethod
    def LMOCS_Recover(*args, **kwargs):
        """
        Location: LMOCS_Recover.tcl
        TCL function args: args
        APS parsed args: ['L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'SCRFile', 'maxStepSize']

        """
        return exec_with_tcl('LMOCS_Recover', *args, **kwargs)

    @staticmethod
    def APSPEMCheckPVs(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['pvList', 'desiredList', 'numerical', 'allowContinue', 'allowRecheck', 'message', 'or', 'greaterThan', 'greaterThanOrEqualTo', 'lessThan', 'lessThanOrEqualTo', 'difference', 'absDifference', 'noDialogs']

        """
        return exec_with_tcl('APSPEMCheckPVs', *args, **kwargs)

    @staticmethod
    def TurnOnK400InitialChecks(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('TurnOnK400InitialChecks', *args, **kwargs)

    @staticmethod
    def TurnOnK400BringUpToStandby(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('TurnOnK400BringUpToStandby', *args, **kwargs)

    @staticmethod
    def TurnOnK400BringUpToHVMode(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('TurnOnK400BringUpToHVMode', *args, **kwargs)

    @staticmethod
    def TurnOnK400BringUpToTrigMode(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('TurnOnK400BringUpToTrigMode', *args, **kwargs)

    @staticmethod
    def TurnOnK400BringUpRFPower(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'ccpsSCRsetpoint']

        """
        return exec_with_tcl('TurnOnK400BringUpRFPower', *args, **kwargs)

    @staticmethod
    def K400IncreaseAttn(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'attenuatorVoltageTarget']

        """
        return exec_with_tcl('K400IncreaseAttn', *args, **kwargs)

    @staticmethod
    def K400DecreaseAttn(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'attenuatorVoltageTarget']

        """
        return exec_with_tcl('K400DecreaseAttn', *args, **kwargs)

    @staticmethod
    def K400DecreaseAttnInTrigState(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'SCRattnCtrlVoltage', 'SCRklystronForwardPower', 'SCRsledForwardPower']

        """
        return exec_with_tcl('K400DecreaseAttnInTrigState', *args, **kwargs)

    @staticmethod
    def K400IncreaseLLRFampDrive(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'SCRllrfAmpDrive', 'SCRklystronForwardPower', 'SCRsledForwardPower']

        """
        return exec_with_tcl('K400IncreaseLLRFampDrive', *args, **kwargs)

    @staticmethod
    def TurnOnK400RampCCPS(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'ccpsSCRsetpoint', 'ccpsTarget', 'ccpsStepSize', 'klyForwardPowerTarget', 'sledExpectedMinMultiplier', 'final']

        """
        return exec_with_tcl('TurnOnK400RampCCPS', *args, **kwargs)

    @staticmethod
    def K400GetVacuumPVs(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('K400GetVacuumPVs', *args, **kwargs)

    @staticmethod
    def K400CheckVacuum(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'vacuumLimit', 'vacPVs']

        """
        return exec_with_tcl('K400CheckVacuum', *args, **kwargs)

    @staticmethod
    def K400CheckVacuumAndWait(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'vacuumLimit', 'vacPVs', 'timeLimit']

        """
        return exec_with_tcl('K400CheckVacuumAndWait', *args, **kwargs)

    @staticmethod
    def K400LowerCCPSToDefaultLowValue(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron']

        """
        return exec_with_tcl('K400LowerCCPSToDefaultLowValue', *args, **kwargs)

    @staticmethod
    def TurnOnK400Info(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('TurnOnK400Info', *args, **kwargs)

    @staticmethod
    def TurnOnK400Dialog(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('TurnOnK400Dialog', *args, **kwargs)

    @staticmethod
    def TurnOnK400(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'SCRFile']

        """
        return exec_with_tcl('TurnOnK400', *args, **kwargs)

    @staticmethod
    def TurnOffK400Info(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('TurnOffK400Info', *args, **kwargs)

    @staticmethod
    def TurnOffK400Dialog(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('TurnOffK400Dialog', *args, **kwargs)

    @staticmethod
    def TurnOffK400(*args, **kwargs):
        """
        Location: LMOCS_K400.tcl
        TCL function args: args
        APS parsed args: ['klystron', 'includeFilament', 'leaveInStandby', 'leaveAfterFullyAttenuated', 'noDialog']

        """
        return exec_with_tcl('TurnOffK400', *args, **kwargs)

    @staticmethod
    def APSMpSRSteerOrbitInfo(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSteerOrbitInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRSteerOrbit(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSteerOrbit', *args, **kwargs)

    @staticmethod
    def APSMpSRTransferCorrectorReference(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'SCRFile']

        """
        return exec_with_tcl('APSMpSRTransferCorrectorReference', *args, **kwargs)

    @staticmethod
    def APSMpSRSteerOrbitInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRSteerOrbitInitDialog', *args, **kwargs)

    @staticmethod
    def getRunControlUser(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['rcPV']

        """
        return exec_with_tcl('getRunControlUser', *args, **kwargs)

    @staticmethod
    def getRunControlPid(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['rcPV']

        """
        return exec_with_tcl('getRunControlPid', *args, **kwargs)

    @staticmethod
    def APSSRCheckOrbitCorrection(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'mode', 'queryIfMissing']

        """
        return exec_with_tcl('APSSRCheckOrbitCorrection', *args, **kwargs)

    @staticmethod
    def APSSRControlOrbitCorrection(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'action']

        """
        return exec_with_tcl('APSSRControlOrbitCorrection', *args, **kwargs)

    @staticmethod
    def APSChangeSROrbitCorrectionMode(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSChangeSROrbitCorrectionMode', *args, **kwargs)

    @staticmethod
    def APSStartSROrbitControllawMode(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSStartSROrbitControllawMode', *args, **kwargs)

    @staticmethod
    def APSSROrbitControllawSendSignal(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSROrbitControllawSendSignal', *args, **kwargs)

    @staticmethod
    def APSMpRestoreSteeringFailSafeReturn(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: code results args
        APS parsed args: ['correctors', 'orbit']

        """
        return exec_with_tcl('APSMpRestoreSteeringFailSafeReturn', *args, **kwargs)

    @staticmethod
    def APSSRRestoreSteering(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['correctors', 'orbit']

        """
        return exec_with_tcl('APSSRRestoreSteering', *args, **kwargs)

    @staticmethod
    def APSCorrectorSanityCheck(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'AOAItolerance', 'dacAOtolerance', 'dacFile']

        """
        return exec_with_tcl('APSCorrectorSanityCheck', *args, **kwargs)

    @staticmethod
    def APSInitializeCorrVector(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'correctorFile', 'stepSizeLimit', 'rampStep', 'AOAItolerance', 'dacAOtolerance', 'setpoint']

        """
        return exec_with_tcl('APSInitializeCorrVector', *args, **kwargs)

    @staticmethod
    def APSRampCorrVectorToSnapshot(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'snapshot', 'stepSizeLimit', 'rampSteps', 'pause']

        """
        return exec_with_tcl('APSRampCorrVectorToSnapshot', *args, **kwargs)

    @staticmethod
    def APSSRCheckCorrectorMode(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane']

        """
        return exec_with_tcl('APSSRCheckCorrectorMode', *args, **kwargs)

    @staticmethod
    def APSTransferVectorAdjust(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['snapshot', 'coord']

        """
        return exec_with_tcl('APSTransferVectorAdjust', *args, **kwargs)

    @staticmethod
    def APSRefreshVectorAdjust(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['pvList', 'plane', 'waveformFile']

        """
        return exec_with_tcl('APSRefreshVectorAdjust', *args, **kwargs)

    @staticmethod
    def APSSRGenerateWaveformFilesForLocalSteering(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSRGenerateWaveformFilesForLocalSteering', *args, **kwargs)

    @staticmethod
    def APSSRStartLocalSteeringInIOC(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['interval', 'average', 'gain', 'timeLimit', 'controllawDir', 'definition', 'runControlPV', 'infiniteLoop']

        """
        return exec_with_tcl('APSSRStartLocalSteeringInIOC', *args, **kwargs)

    @staticmethod
    def APSSetCorrMode(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'sourceMode', 'corrMode', 'unified']

        """
        return exec_with_tcl('APSSetCorrMode', *args, **kwargs)

    @staticmethod
    def APSGenerateControllawFiles(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSGenerateControllawFiles', *args, **kwargs)

    @staticmethod
    def APSMakeFFDefinitions(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['coord']

        """
        return exec_with_tcl('APSMakeFFDefinitions', *args, **kwargs)

    @staticmethod
    def APSCreateDPTestFiles(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'datapool', 'unified']

        """
        return exec_with_tcl('APSCreateDPTestFiles', *args, **kwargs)

    @staticmethod
    def APSCreateWaveformFiles(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['configFile', 'testFile', 'corrLimit', 'CUCorrLimit', 'BPMLimit', 'XBPMLimit', 'type', 'plane', 'corrStatusFile']

        """
        return exec_with_tcl('APSCreateWaveformFiles', *args, **kwargs)

    @staticmethod
    def APSAbortSRControllaw(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['runControlPV', 'sourceId']

        """
        return exec_with_tcl('APSAbortSRControllaw', *args, **kwargs)

    @staticmethod
    def APSSuspendSRControllaw(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['runControlPV', 'sourceId']

        """
        return exec_with_tcl('APSSuspendSRControllaw', *args, **kwargs)

    @staticmethod
    def APSResumeSRControllaw(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['runControlPV', 'sourceId']

        """
        return exec_with_tcl('APSResumeSRControllaw', *args, **kwargs)

    @staticmethod
    def APSTransferVectorGain(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['coord']

        """
        return exec_with_tcl('APSTransferVectorGain', *args, **kwargs)

    @staticmethod
    def APSSRChangeSteeringIndicator(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['toggle', 'mode']

        """
        return exec_with_tcl('APSSRChangeSteeringIndicator', *args, **kwargs)

    @staticmethod
    def APSCheckAndUpdateLocalSteeringConfigs(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['steeringType', 'sector', 'stream', 'statusCallback']

        """
        return exec_with_tcl('APSCheckAndUpdateLocalSteeringConfigs', *args, **kwargs)

    @staticmethod
    def APSCheckLocalSteeringTests(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['sector', 'steeringType', 'statusCallback', 'stream']

        """
        return exec_with_tcl('APSCheckLocalSteeringTests', *args, **kwargs)

    @staticmethod
    def APSMpSRUnstickCorrectorsInfo(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUnstickCorrectorsInfo', *args, **kwargs)

    @staticmethod
    def APSMpSRUnstickCorrectorsInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpSRUnstickCorrectorsInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpSRUnstickCorrectors(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: ['plane', 'delta', 'CUcorrLimit']

        """
        return exec_with_tcl('APSMpSRUnstickCorrectors', *args, **kwargs)

    @staticmethod
    def APSMpRestoreCorrectorsFromSCRInfo(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreCorrectorsFromSCRInfo', *args, **kwargs)

    @staticmethod
    def APSMpRestoreCorrectorsFromSCR(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreCorrectorsFromSCR', *args, **kwargs)

    @staticmethod
    def APSMpRestoreCorrectorsFromSCRInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRestoreCorrectorsFromSCRInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpRampCorrVectorToSCRInfo(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRampCorrVectorToSCRInfo', *args, **kwargs)

    @staticmethod
    def APSMpRampCorrVectorToSCRInitDialog(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: frame
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRampCorrVectorToSCRInitDialog', *args, **kwargs)

    @staticmethod
    def APSMpRampCorrVectorToSCR(*args, **kwargs):
        """
        Location: APSMpSRSteering.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSMpRampCorrVectorToSCR', *args, **kwargs)

    @staticmethod
    def APSReplicateItem(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSReplicateItem -item <string> -number <integer>
         Returns list of <integer> items, each item being <string>.TCL function args: args
        APS parsed args: ['item', 'number']

        """
        return exec_with_tcl('APSReplicateItem', *args, **kwargs)

    @staticmethod
    def APSUniqueNumber(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSUniqueNumber
        Returns a unique number.
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSUniqueNumber', *args, **kwargs)

    @staticmethod
    def APSUniqueName(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSUniqueName prefix
        Returns a unique name which begins with
        the given prefix.
        TCL function args: prefix
        APS parsed args: None

        """
        return exec_with_tcl('APSUniqueName', *args, **kwargs)

    @staticmethod
    def APSGeometryRightRelative(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: parentWidget
        APS parsed args: None

        """
        return exec_with_tcl('APSGeometryRightRelative', *args, **kwargs)

    @staticmethod
    def APSUnmap(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSUnmap widget
        Removes widget from packing order, but keeps the widget in memory. In other
        words, the image of the widget is removed from the screen. Use APSRemap to
        redisplay it.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSUnmap', *args, **kwargs)

    @staticmethod
    def APSRemap(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSRemap widget
        Restores a widget to the display after an APSUnmap has been performed.
        Request is ignored if widget was never unmapped.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSRemap', *args, **kwargs)

    @staticmethod
    def APSRepack(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSRepack widget packOptions
        Repacks widget using packOptions. Ex. APSRepack .button -side top -fill y
        Any specified pack option will override the previous pack option, but all
        previous options are retained otherwise.TCL function args: widget args
        APS parsed args: None

        """
        return exec_with_tcl('APSRepack', *args, **kwargs)

    @staticmethod
    def APSSendEMail(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSSendEMail
        	-address <string>
        	-message <string>
        	[-subject <string>]
        	[-considerate 1]
        	[-earlyHour <number>]
        	[-lateHour <number>]
        	[-mailProgram <string>]
        Sends an email message to the given address.  If considerate mode is requested, won't send to an email pager before earlyHour or after lateHour.TCL function args: args
        APS parsed args: ['address', 'message', 'considerate', 'earlyHour', 'lateHour', 'subject', 'mailProgram']

        """
        return exec_with_tcl('APSSendEMail', *args, **kwargs)

    @staticmethod
    def APSWaitWithUpdate(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSWaitWithUpdate -waitSeconds <secs> -updateInterval <secs> [-abortVariable <name>] [-updateCommand <string>]TCL function args: args
        APS parsed args: ['waitSeconds', 'updateInterval', 'abortVariable', 'updateCommand']

        """
        return exec_with_tcl('APSWaitWithUpdate', *args, **kwargs)

    @staticmethod
    def APSSetVarAndUpdate(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSSetVarAndUpdate <variable> <value>TCL function args: variable value
        APS parsed args: None

        """
        return exec_with_tcl('APSSetVarAndUpdate', *args, **kwargs)

    @staticmethod
    def APSConvertTimeToHours(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSConvertTimeToHours <timeValue>
        Where time value may be of the H:M, H:M:S, or floating point hours.TCL function args: timeValue
        APS parsed args: None

        """
        return exec_with_tcl('APSConvertTimeToHours', *args, **kwargs)

    @staticmethod
    def APSPrint(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSPrint [-text <string>]
        [-textWidget <string>]
        [-cmd <printcommand>]
        Where <printcommand> is lpr or enscript
        TCL function args: args
        APS parsed args: ['text', 'textWidget', 'cmd', 'widgetType']

        """
        return exec_with_tcl('APSPrint', *args, **kwargs)

    @staticmethod
    def APSPrintText(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSPrintText [-text <string>]
        [-cmd <printcommand>]
        Where <printcommand> is lpr or enscript
        TCL function args: args
        APS parsed args: ['text', 'cmd']

        """
        return exec_with_tcl('APSPrintText', *args, **kwargs)

    @staticmethod
    def APSAddToParallelLists(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSAddToParallelLists -listNames <list> -listItems <list>
         Appends ith list item to ith list. Used to construct parallel lists.TCL function args: args
        APS parsed args: ['listNames', 'listItems']

        """
        return exec_with_tcl('APSAddToParallelLists', *args, **kwargs)

    @staticmethod
    def APSAddToTmpFileList(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSAddToTmpFileList -ID <string> -fileList <list>
         Adds to named list of temporary files, creating the list if the ID is new.
        Files are deleted automatically when the script exits, or when
        APSDeleteTmpFileList is called with the same ID. A more flexible variant of APSAddToTempFileList.TCL function args: args
        APS parsed args: ['ID', 'fileList']

        """
        return exec_with_tcl('APSAddToTmpFileList', *args, **kwargs)

    @staticmethod
    def APSDeleteTmpFileList(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSDeleteTmpFileList -ID <string>
         Deletes the temporary files associated with the given ID.
         A more flexible variant of APSDeleteTempFiles.
        TCL function args: args
        APS parsed args: ['ID']

        """
        return exec_with_tcl('APSDeleteTmpFileList', *args, **kwargs)

    @staticmethod
    def APSAddToTempFileList(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSAddToTempFileList <filename> [<filename>...]TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAddToTempFileList', *args, **kwargs)

    @staticmethod
    def APSDeleteTempFiles(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSDeleteTempFilesTCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSDeleteTempFiles', *args, **kwargs)

    @staticmethod
    def APSFreezeVars(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSFreezeVars varname1 ... varnamen
        Given a series of global variables, make them read-only until
        APSUnfreezeVars is invoked. This allows you to freeze a set of variables
        during execution of a critical procedure, preventing a user from
        inadvertently modifying global vars via a widget.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSFreezeVars', *args, **kwargs)

    @staticmethod
    def APSUnfreezeVars(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSUnfreezeVars varname1 ... varnamen
        Remove write-protection from the given global variables. Assumes you have
        done a prior APSFreezeVars.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSUnfreezeVars', *args, **kwargs)

    @staticmethod
    def APSFreezeVarsCallback(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: varName index op
        APS parsed args: None

        """
        return exec_with_tcl('APSFreezeVarsCallback', *args, **kwargs)

    @staticmethod
    def APSUpdateSoftLink(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: args
        APS parsed args: ['link', 'file']

        """
        return exec_with_tcl('APSUpdateSoftLink', *args, **kwargs)

    @staticmethod
    def APSNoOp(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSNoOp <arguments>
        Does nothing but return.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSNoOp', *args, **kwargs)

    @staticmethod
    def APSSplitGenerationedName(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSSplitGenerationedName -name <string> [-separator <char>]
         Expects a name of the form <part1><separator><part2>, where <part2> is a representation of an integer (e.g., 0001).  Returns the list <part1> <part2-as-number> <part2-format>.  E.g., for file.sdds-0001, would return file.sdds 1 %04ld.TCL function args: args
        APS parsed args: ['name', 'separator']

        """
        return exec_with_tcl('APSSplitGenerationedName', *args, **kwargs)

    @staticmethod
    def APSNextGenerationedName(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSNextGenerationedName -name <string> [-separator <char>] [-newFile 1] [-directory <name>]
         Expects a name of the form <part1><separator><part2>, where <part2> is a representation of an integer (e.g., 0001).  Returns the next file in the series.  If -newFile 1 is given, returns the first name that isn't already used; this name may the original name you pass, if that file doesn't exist.TCL function args: args
        APS parsed args: ['name', 'separator', 'newFile', 'directory']

        """
        return exec_with_tcl('APSNextGenerationedName', *args, **kwargs)

    @staticmethod
    def APSResolveLink(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSResolveLink <filename>TCL function args: filename
        APS parsed args: None

        """
        return exec_with_tcl('APSResolveLink', *args, **kwargs)

    @staticmethod
    def APSArchiveGenerationedCopy(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSArchiveGenerationedCopy -name <string> [-separator <char>] [-extension .<string>] [-remove 1]TCL function args: args
        APS parsed args: ['name', 'separator', 'extension', 'remove']

        """
        return exec_with_tcl('APSArchiveGenerationedCopy', *args, **kwargs)

    @staticmethod
    def APSMakeLink(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSMakeLink -filename <string> -linkname <string> -local {0|1} -log {0|1} [-confirm 1] [-confirmMessage <string>]TCL function args: args
        APS parsed args: ['filename', 'linkname', 'local', 'permissions', 'confirm', 'confirmMessage', 'log']

        """
        return exec_with_tcl('APSMakeLink', *args, **kwargs)

    @staticmethod
    def APSGoToDailyDirectory(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSGoToDailyDirectory [-account <user>] [-subdirectory <user>]
        creates a daily directory in the format <rootDir>/<yy><mm>/<dd>/<shift>/<subdirectory>. The user's home directory is the default root directory. The account argument can be used to specify somebody else's root directory. If no subdirectory is given then only <rootDir>/<yy><mm>/<dd>/<shift> is created. The procedure returns the name of the directory and sets the global variable apsOutputDir to the name of the directory. Note this procedure doesn't have any cd commands.TCL function args: args
        APS parsed args: ['account', 'subdirectory', 'fourDigitYear']

        """
        return exec_with_tcl('APSGoToDailyDirectory', *args, **kwargs)

    @staticmethod
    def APSCAAverageAndTransfer(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSCAAverageAndTransfer -readbackList <pvNameList> -setpointList <pvNameList> -average <number> -interval <seconds> -statusCallback <proc> [-flagList <varList>]TCL function args: args
        APS parsed args: ['readbackList', 'setpointList', 'average', 'interval', 'statusCallback', 'flagList', 'verbose', 'checkReadback']

        """
        return exec_with_tcl('APSCAAverageAndTransfer', *args, **kwargs)

    @staticmethod
    def APSEditString(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSEditString -editcommand <command sequence> [<string> ...]

        -editcommand sequences:
        <n>d    delete <n> characters
        <n>f    forward <n> characters
        <n>b    backward <n> characters
        <n>D    delete <n> words
        <n>F    forward <n> words
        <n>B    backward <n> words
        <n>i{delim}text{delim} insert text <n> times
        s{delim}text{delim}    search for text, leave active position at end
        S{delim}text{delim}    search for text, leave active position at start
        <n>k    kill <n> characters
        <n>K    kill <n> words
        z<c>    kill up to <c>
        <n>Z<c> kill up to and including <c>, <n> times
        <n>y    yank kill buffer, <n> times
        <n>%{delim}text1{delim}text2{delim} replace text1 with text2 <n> timesTCL function args: args
        APS parsed args: ['editcommand']

        """
        return exec_with_tcl('APSEditString', *args, **kwargs)

    @staticmethod
    def APSSRFindLattices(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSRFindLattices', *args, **kwargs)

    @staticmethod
    def APSSetSimpleACL(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetSimpleACL', *args, **kwargs)

    @staticmethod
    def APSSetVarsFromList(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSSetVarsFromList -valueList <list> -variableList <list>
        Sets successive variables in variable list to successive values in value list.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSetVarsFromList', *args, **kwargs)

    @staticmethod
    def APSFileCopy(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSFileCopy -from <filename> -to <filename>
        Copies real file even if a symbolic link is used.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSFileCopy', *args, **kwargs)

    @staticmethod
    def APSStackTrace(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSStackTrace [-level <integer>]
        Returns a list of procedure names in which execution is taking place.TCL function args: args
        APS parsed args: ['level']

        """
        return exec_with_tcl('APSStackTrace', *args, **kwargs)

    @staticmethod
    def APSLogScriptAction(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSLogScriptAction
        [-procedure <string>]
        [-action <string>]
        [-parameters <string>]
        [-status <string>]

        Logs script info using logDaemon.TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSLogScriptAction', *args, **kwargs)

    @staticmethod
    def APSEntryInfoBalloon_for(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: win textvar
        APS parsed args: None

        """
        return exec_with_tcl('APSEntryInfoBalloon_for', *args, **kwargs)

    @staticmethod
    def APSEntryInfoBalloon_pending(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: win
        APS parsed args: None

        """
        return exec_with_tcl('APSEntryInfoBalloon_pending', *args, **kwargs)

    @staticmethod
    def APSEntryInfoBalloon_cancel(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSEntryInfoBalloon_cancel', *args, **kwargs)

    @staticmethod
    def APSEntryInfoBalloon_show(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: win
        APS parsed args: None

        """
        return exec_with_tcl('APSEntryInfoBalloon_show', *args, **kwargs)

    @staticmethod
    def APSEntryInfoBalloon_control(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: state
        APS parsed args: None

        """
        return exec_with_tcl('APSEntryInfoBalloon_control', *args, **kwargs)

    @staticmethod
    def APSDisableWidget(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSDisableWidget <widgetName>
         Disables the named widget and all of its child widgets.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSDisableWidget', *args, **kwargs)

    @staticmethod
    def APSEnableWidget(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSEnableWidget <widgetName>
         Enables the named widget and all of its child widgets.TCL function args: widget
        APS parsed args: None

        """
        return exec_with_tcl('APSEnableWidget', *args, **kwargs)

    @staticmethod
    def APSEnableDisableWidget(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSEnableDisableWidget <widgetName> {-enable {0|1} | -toggle {0|1}}
         Enables or disables the named widget and all of its child widgets.TCL function args: widget args
        APS parsed args: ['enable', 'toggle', 'button']

        """
        return exec_with_tcl('APSEnableDisableWidget', *args, **kwargs)

    @staticmethod
    def APSClearRCRecord(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSClearRCRecord', *args, **kwargs)

    @staticmethod
    def APSFileLineCount(*args, **kwargs):
        """
        Location: APSMisc.tcl
        Usage: APSFileLineCount <fileName>
        Returns number of lines in a file.
        TCL function args: fileName
        APS parsed args: None

        """
        return exec_with_tcl('APSFileLineCount', *args, **kwargs)

    @staticmethod
    def APSStringTrimRight(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: s {chars " "}
        APS parsed args: None

        """
        return exec_with_tcl('APSStringTrimRight', *args, **kwargs)

    @staticmethod
    def APSStringTrimLeft(*args, **kwargs):
        """
        Location: APSMisc.tcl
        TCL function args: s {chars " "}
        APS parsed args: None

        """
        return exec_with_tcl('APSStringTrimLeft', *args, **kwargs)

    @staticmethod
    def APSLatticeToSetpointsQuadSext(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'includeQuadrupoles', 'includeSextupoles', 'energyGeV']

        """
        return exec_with_tcl('APSLatticeToSetpointsQuadSext', *args, **kwargs)

    @staticmethod
    def APSSetpointsToLatticeQuadSext(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'energyGeV']

        """
        return exec_with_tcl('APSSetpointsToLatticeQuadSext', *args, **kwargs)

    @staticmethod
    def APSLatticeToSetpointsTGD(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'type', 'energyGeV']

        """
        return exec_with_tcl('APSLatticeToSetpointsTGD', *args, **kwargs)

    @staticmethod
    def APSSetpointsToLatticeTGD(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'type', 'energyGeV']

        """
        return exec_with_tcl('APSSetpointsToLatticeTGD', *args, **kwargs)

    @staticmethod
    def APSLatticeToSetpoints(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'energyGeV']

        """
        return exec_with_tcl('APSLatticeToSetpoints', *args, **kwargs)

    @staticmethod
    def APSSetpointsToLattice(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'energyGeV']

        """
        return exec_with_tcl('APSSetpointsToLattice', *args, **kwargs)

    @staticmethod
    def APSUAdjustMagnetSetpoints(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSUAdjustMagnetSetpoints', *args, **kwargs)

    @staticmethod
    def APSUAdjustParameterFile(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSUAdjustParameterFile', *args, **kwargs)

    @staticmethod
    def APSLatticeToSetpointsDeltaK1(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'energyGeV', 'referenceParameters', 'referenceSnapshot', 'referenceEnergyGeV']

        """
        return exec_with_tcl('APSLatticeToSetpointsDeltaK1', *args, **kwargs)

    @staticmethod
    def APSDeltaK1ToSetpoints(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSDeltaK1ToSetpoints', *args, **kwargs)

    @staticmethod
    def BTSLatticeToSetpoints(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'includeQuadrupoles', 'includeDipoles', 'energyGeV']

        """
        return exec_with_tcl('BTSLatticeToSetpoints', *args, **kwargs)

    @staticmethod
    def BTSSetpointsToLattice(*args, **kwargs):
        """
        Location: APSULatticeAndSetpoints.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'energyGeV']

        """
        return exec_with_tcl('BTSSetpointsToLattice', *args, **kwargs)

    @staticmethod
    def APSSetOAGGlobal(*args, **kwargs):
        """
        Location: APSSetOAGGlobal.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSetOAGGlobal', *args, **kwargs)

    @staticmethod
    def APSSetElegantGlobals(*args, **kwargs):
        """
        Location: APSSetOAGGlobal.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSetElegantGlobals', *args, **kwargs)

    @staticmethod
    def APSSCRLogAction(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRLogAction', *args, **kwargs)

    @staticmethod
    def APSSCRGetUBOPLink(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRGetUBOPLink', *args, **kwargs)

    @staticmethod
    def APSSCRSystemChoiceWidget(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'variable', 'command', 'menuParent', 'mode']

        """
        return exec_with_tcl('APSSCRSystemChoiceWidget', *args, **kwargs)

    @staticmethod
    def APSSCRMakeSystemSubMenu(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'label', 'systemList', 'variable', 'command', 'groupName']

        """
        return exec_with_tcl('APSSCRMakeSystemSubMenu', *args, **kwargs)

    @staticmethod
    def APSSCRSetSystemList(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: systemList
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRSetSystemList', *args, **kwargs)

    @staticmethod
    def APSMakeSCRMatchOptions(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: file args
        APS parsed args: ['includeReadOnlys', 'protectionLock', 'pvNameFilter', 'manualFieldsOnly', 'invertChoices', 'noConnections']

        """
        return exec_with_tcl('APSMakeSCRMatchOptions', *args, **kwargs)

    @staticmethod
    def APSCheckSCRSelections(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSCheckSCRSelections', *args, **kwargs)

    @staticmethod
    def APSClearSCRFilterFlags(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSClearSCRFilterFlags', *args, **kwargs)

    @staticmethod
    def APSSCRMakeSnapshotFilename(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRMakeSnapshotFilename', *args, **kwargs)

    @staticmethod
    def APSSaveMachine(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSaveMachine', *args, **kwargs)

    @staticmethod
    def APSSaveMachineByCasr(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSSaveMachineByCasr', *args, **kwargs)

    @staticmethod
    def APSCASRSaveMachine(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCASRSaveMachine', *args, **kwargs)

    @staticmethod
    def APSSCRCheckCasrRunControl(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['initialOutput', 'machine']

        """
        return exec_with_tcl('APSSCRCheckCasrRunControl', *args, **kwargs)

    @staticmethod
    def APSSCRAbortCASRRunControl(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['machine', 'statusCallback']

        """
        return exec_with_tcl('APSSCRAbortCASRRunControl', *args, **kwargs)

    @staticmethod
    def APSSCRProcessSnapshot(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['SCRdebug', 'snapshot', 'logFile', 'statusCallback', 'requestFile']

        """
        return exec_with_tcl('APSSCRProcessSnapshot', *args, **kwargs)

    @staticmethod
    def APSSCRCheckCASRSnapshot(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['snapshot', 'logFile']

        """
        return exec_with_tcl('APSSCRCheckCASRSnapshot', *args, **kwargs)

    @staticmethod
    def APSSCRCheckSnapshot(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['snapshot', 'logFile', 'GPServer']

        """
        return exec_with_tcl('APSSCRCheckSnapshot', *args, **kwargs)

    @staticmethod
    def APSCompareMachine(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSCompareMachine', *args, **kwargs)

    @staticmethod
    def APSCompareNonMatchingPVs(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['snapshot1', 'snapshot2', 'snap1Label', 'snap2Label']

        """
        return exec_with_tcl('APSCompareNonMatchingPVs', *args, **kwargs)

    @staticmethod
    def APSListSCRMatch(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSListSCRMatch', *args, **kwargs)

    @staticmethod
    def APSListSCRMatchSetArray(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSListSCRMatchSetArray', *args, **kwargs)

    @staticmethod
    def APSListSCRMatchSetArrayCallback(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: machine sourceArray callback mode arrayName index
        APS parsed args: None

        """
        return exec_with_tcl('APSListSCRMatchSetArrayCallback', *args, **kwargs)

    @staticmethod
    def APSSCRMakePrefLBoxTextLine(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['dataList', 'widthList']

        """
        return exec_with_tcl('APSSCRMakePrefLBoxTextLine', *args, **kwargs)

    @staticmethod
    def APSSCRMakeLBoxTextLine(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['dataList', 'widthList']

        """
        return exec_with_tcl('APSSCRMakeLBoxTextLine', *args, **kwargs)

    @staticmethod
    def APSSCRFilterFileCallback(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: index
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRFilterFileCallback', *args, **kwargs)

    @staticmethod
    def APSSCRMakeLBoxTextFilterFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['dataList', 'widthList']

        """
        return exec_with_tcl('APSSCRMakeLBoxTextFilterFile', *args, **kwargs)

    @staticmethod
    def APSSCRPVFilterWidget(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'fileName', 'rootname', 'snapDir']

        """
        return exec_with_tcl('APSSCRPVFilterWidget', *args, **kwargs)

    @staticmethod
    def APSSCRInvertFilterFileCallback(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: UNKNOWN
        APS parsed args: None

        """
        return exec_with_tcl('APSSCRInvertFilterFileCallback', *args, **kwargs)

    @staticmethod
    def APSSCRDateTimeEntryWidget(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'command', 'relief']

        """
        return exec_with_tcl('APSSCRDateTimeEntryWidget', *args, **kwargs)

    @staticmethod
    def APSSCRResolvePreferredFileChoice(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['system', 'choice']

        """
        return exec_with_tcl('APSSCRResolvePreferredFileChoice', *args, **kwargs)

    @staticmethod
    def APSSCRGetPreferredChoiceList(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['system']

        """
        return exec_with_tcl('APSSCRGetPreferredChoiceList', *args, **kwargs)

    @staticmethod
    def APSSCRGetPreferredDataLists(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['system']

        """
        return exec_with_tcl('APSSCRGetPreferredDataLists', *args, **kwargs)

    @staticmethod
    def APSSCRInstallPreferredFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['system', 'choice', 'filename']

        """
        return exec_with_tcl('APSSCRInstallPreferredFile', *args, **kwargs)

    @staticmethod
    def APSSCRAlterSnapshot(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['sourceSnapshot', 'replacementData', 'description', 'machine']

        """
        return exec_with_tcl('APSSCRAlterSnapshot', *args, **kwargs)

    @staticmethod
    def APSAlterSCRRequestFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSAlterSCRRequestFile', *args, **kwargs)

    @staticmethod
    def APSAddToSCRRequestFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['input', 'output', 'add']

        """
        return exec_with_tcl('APSAddToSCRRequestFile', *args, **kwargs)

    @staticmethod
    def APSRemoveFromSCRRequestFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRemoveFromSCRRequestFile', *args, **kwargs)

    @staticmethod
    def APSRenameInSCRRequestFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSRenameInSCRRequestFile', *args, **kwargs)

    @staticmethod
    def APSMakeSCRCategoryFiles(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['input']

        """
        return exec_with_tcl('APSMakeSCRCategoryFiles', *args, **kwargs)

    @staticmethod
    def APSScaleSnapshot(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: None

        """
        return exec_with_tcl('APSScaleSnapshot', *args, **kwargs)

    @staticmethod
    def CompareRequestOrMonitorFiles(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['lastFile', 'newFile', 'root', 'type', 'install']

        """
        return exec_with_tcl('CompareRequestOrMonitorFiles', *args, **kwargs)

    @staticmethod
    def APSSCRRampSRMagnets(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['doQuads', 'doSextoples', 'SCRFile', 'machine']

        """
        return exec_with_tcl('APSSCRRampSRMagnets', *args, **kwargs)

    @staticmethod
    def APSSCRTrackRestoreFile(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: args
        APS parsed args: ['sourceFile', 'machine', 'restoreFile', 'timeStamp']

        """
        return exec_with_tcl('APSSCRTrackRestoreFile', *args, **kwargs)

    @staticmethod
    def APSAddSCRDialog(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: widget args
        APS parsed args: ['parent', 'label', 'arrayName', 'daysPast', 'system', 'defaultFile', 'description', 'PreferredOnly', 'searchDescription']

        """
        return exec_with_tcl('APSAddSCRDialog', *args, **kwargs)

    @staticmethod
    def APSAddSCRDialogCallback(*args, **kwargs):
        """
        Location: SCRprocedures.tcl
        TCL function args: arrayName machine
        APS parsed args: None

        """
        return exec_with_tcl('APSAddSCRDialogCallback', *args, **kwargs)