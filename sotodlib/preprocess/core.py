"""Base Class and PIPELINE register for the preprocessing pipeline scripts."""

PIPELINE = {}

class _Preprocess(object):
    """The base class for Preprocessing modules which defines the required
    functions and keys required in the configurations.

    Each preprocess module has four overwritable functions that are called by
    the processing scripts in site_pipeline. These four functions are each
    controlled by a specific key in a configuration dictionary passed to the
    module on creation.

    The configuration dictionary has 5 special keys: ``name``, ``process``,
    ``calc``, ``save``, and ``select``. ``name`` is the name used to register 
    the module with the PIPELINE registry. The other four keys are matched to 
    functions in the module, if the key is not present then that function will 
    be skipped when the preprocessing pipeline is run.

    There are two special AxisManagers expected to be part of the preprocessing
    pipeline. ``aman`` is the "standard" time ordered data AxisManager that is
    loaded via our default styles. ``proc_aman`` is the preprocess AxisManager,
    this is carry the data products that will be saved to whatever Metadata
    Archive is connected to the preprocessing pipeline. 
    """    

    def __init__(self, step_cfgs):
        self.process_cfgs = step_cfgs.get("process")
        self.calc_cfgs = step_cfgs.get("calc")
        self.save_cfgs = step_cfgs.get("save")
        self.select_cfgs = step_cfgs.get("select")
    
    def process(self, aman, proc_aman):
        """ This function makes changes to the time ordered data AxisManager.
        Ex: calibrating or detrending the timestreams. This function will use
        any configuration information under the ``process`` key of the
        configuration dictionary and is not expected to change or alter
        proc_aman.


        Arguments
        ---------
        aman : AxisManager 
            The time ordered data
        proc_aman : AxisManager 
            Any information generated by previous elements in the preprocessing 
            pipeline.
        """
        if self.process_cfgs is None:
            return
        raise NotImplementedError
        
    def calc_and_save(self, aman, proc_aman):
        """ This function calculates data products of some sort off of the time
        ordered data AxisManager.

        Ex: Calcuating the white noise of the timestream. This function will use
        any configuration information under the ``calc`` key of the
        configuration dictionary and can call the save function to make
        changes to proc_aman.

        Arguments
        ---------
        aman : AxisManager 
            The time ordered data
        proc_aman : AxisManager 
            Any information generated by previous elements in the preprocessing 
            pipeline.
        """
        if self.calc_cfgs is None:
            return
        raise NotImplementedError
    
    def save(self, proc_aman, *args):
        """ This function wraps new information into the proc_aman and will use
        any configuration information under the ``save`` key of the
        configuration dictionary.

        Arguments
        ---------
        proc_aman : AxisManager 
            Any information generated by previous elements in the preprocessing 
            pipeline.
        args : any
            Any additional information ``calc_and_save`` needs to send to the
            save function.
        """
        if self.save_cfgs is None:
            return
        raise NotImplementedError
        
    def select(self, meta):
        """ This function runs any desired data selection of the preprocessing
        pipeline results. Assumes the pipeline has already been run and that the
        resulting proc_aman is now saved under the ``preprocess`` key in the
        ``meta`` AxisManager loaded via context.

        Ex: removing detectors with white noise above some limit. This function will use
        any configuration information under the ``select`` key.


        Arguments
        ---------
        meta : AxisManager 
            Metadata related to the specific observation

        Returns
        -------
        meta : AxisManager 
            Metadata where non-selected detectors have been removed
        """

        if self.select_cfgs is None:
            return meta
        raise NotImplementedError
    
    @staticmethod
    def register(name, process_class):
        """Registers a new modules with the PIPELINE"""

        if PIPELINE.get(name) is None:
            PIPELINE[name] = process_class



