import sys
import os
import csv
sys.path.append('../slicenet')
from slicenet.mgrs.nfMgr import NfMgr
from slicenet.mgrs.sliceMgr import SliceMgr
from slicenet.mgrs.serviceMgr import ServiceMgr
from slicenet.entities.slicelet import Slicelet
from slicenet.utils.experiment import Experiment
from slicenet.utils.slicenetlogger import slicenetLogger as logger
from datetime import datetime


from typing import List


class ExperimentMgr:

    def __init__(self):
        self.experiments : List[Experiment] = []
        self.exp_dir = ""

    def loadExperimentsFromDir(self, exp_dir: str):
        if os.path.exists(exp_dir):
            self.exp_dir = exp_dir
            for f in os.listdir(exp_dir):
                if f.endswith('.yaml'):
                    abs_f = exp_dir + "/" + f
                    self.experiments.append(Experiment(abs_f))
                    return True 
        else:
            return False
    
    def prepareRow(self, eType: str, name: str, id :str, adm: str, his: str) -> List[str]:
        row = []
        row.append(eType)
        row.append(name)
        row.append(id)
        row.append(adm)
        row.append(his)
        return row

    
    def saveInference(self):
        ts = datetime.now().strftime('%d%m%Y%H%M%S')
        for exp in self.experiments:
            fname = exp.exp_name + "_" + ts
            with open(f"{self.exp_dir}/{fname}.csv", 'w', newline='') as f:
                csvW = csv.writer(f)
                header = ["Entity", "Name", "ID", "Admitted?", "Event History"]
                csvW.writerow(header)
                for _,v in exp.exp_clouds.items():
                    aRow = self.prepareRow("Cloud", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)
                for _,v in exp.exp_nfs.items():
                    aRow = self.prepareRow("NFs", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)
                for _,v in exp.exp_slices.items():
                    aRow = self.prepareRow("Slices", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)
                for _,v in exp.exp_slicelets.items():
                    aRow = self.prepareRow("Slicelets", v.name, str(v.id), str(v.get_exp_status()), str(v.eventHistory))
                    csvW.writerow(aRow)

    def deployAndLaunch(self):
        for exp in self.experiments:
            # Register Clouds
            for _,v in exp.exp_clouds.items():
                NfMgr.registerCloud(v)
            
            for k,v in exp.exp_policies.items():
                if k == "NfMgr":
                    NfMgr.setSchedularPolicy(v)

            # Deploy Nfs
            for _,v in exp.exp_nfs.items():
                v.exp_admitted = NfMgr.deployNf(v)

            # Deploy Slices
            for _,v in exp.exp_slices.items():
                v.exp_admitted = SliceMgr.deploySlice(v)

            # Register Services
            for _,v in exp.exp_services.items():
                v.exp_admitted = ServiceMgr.registerService(v)

            # Schedule Slicelets
            for _,v in exp.exp_slicelets.items():
                ServiceMgr.scheduleSlicelet(v)

            # Launch Experiment
            ServiceMgr.launchExperiment()

            # update Slicelets with experiment data
            for _,v in ServiceMgr.slicelets.items():
                exp.exp_slicelets[v.name] = v
            
            # tear down slicelet services
            ServiceMgr.slicelets.clear()

if __name__ == '__main__':
    import os
    import logging
    
    logger = logging.getLogger('example')

    logging.basicConfig(format='%(asctime)s %(name)s %(module)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
    
    example_config = os.getcwd() + "/examples/example1.yaml"

    experiment1 = Experiment(example_config)
    ExperimentMgr.deployAndLaunch(exp=experiment1)
    logger.info("After experiment")
    #experiment1.displaySliceletStatistics()
    for k,v in experiment1.exp_nfs.items():
        logger.info(f"{k} was admitted? {v.get_exp_status()}")
    for k,v in experiment1.exp_slicelets.items():
        logger.info(f"Slicelet {v.name} {v.eventHistory} {v.initRandomDelaySecs}")
    logger.info("Checking if this prints")