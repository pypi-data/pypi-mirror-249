import yaml
import sys
sys.path.append('../slicenet')

from slicenet.entities.cloud import Cloud
from slicenet.entities.nf import Nf
from slicenet.mgrs.nfMgr import NfMgr
from slicenet.mgrs.sliceMgr import SliceMgr
from slicenet.mgrs.serviceMgr import ServiceMgr
from slicenet.entities.staticslice import StaticSlice
from slicenet.entities.service import Service
from slicenet.entities.slicelet import Slicelet
from slicenet.utils.slicenetlogger import slicenetLogger as logger

from numpy import random

from tabulate import tabulate
from typing import Dict, List
from pprint import pprint

class YamlConfig:

    def __init__(self):
        self.clouds = []
        self.nfs = []
        self.policies = []
        self.slices = []
        self.services = []
        self.slicelets = []

class Experiment:

    def __init__(self, fname: str):
        self.exp_name = ""
        self.exp_descp = ""
        self.exp_delay_pattern = "default"
        self.exp_delay_pattern_threshold = 1
        self.exp_clouds : Dict[str, Cloud] = {}
        self.exp_nfs : Dict[str, Nf] = {}
        self.exp_policies : Dict[str, str] = {}
        self.exp_slices : Dict[str, StaticSlice] = {}
        self.exp_services : Dict[str, Service] = {}
        self.exp_slicelets : Dict[str, Slicelet] = {}
        self.yamlConfig = YamlConfig()

        if fname != str:
            self.loadYAML(fname)
        else:
            logger.error("Empty YAML file. Please check the file")
            sys.exit(1)

        try:    
            self.loadClouds()
            self.loadNfs()
            self.loadPolicies()
            self.loadSlices()
            self.loadServices()
            self.loadSlicelets()
            self.introduceRandomnessForSlicelets()
        except Exception as e:
            logger.error(f"YAML parser error {e.__str__()} cause : {e.__doc__}")
            sys.exit(1)


    def loadClouds(self):
        for c in self.yamlConfig.clouds:
            aCloud = Cloud(ram=c['ram'], hdd=c['hdd'], cpu=c['cpu'], name=c['name'])
            #pprint(aCloud)
            self.exp_clouds[aCloud.name] = aCloud
    
    def loadNfs(self):
        for n in self.yamlConfig.nfs:
            aNf = Nf(name = n['name'], ram = n['ram'], cpu = n['cpu'], hdd = n['hdd'])
            #pprint(aNf)
            self.exp_nfs[aNf.name] = aNf
    
    def loadPolicies(self):
        for policy in self.yamlConfig.policies:
            self.exp_policies[policy['type']] = policy['policy']
    
    def loadSlices(self):
        for sliceItem in self.yamlConfig.slices:
            slice = StaticSlice(sliceItem['name'])
            for comp in sliceItem['composition']:
                nfId = (self.exp_nfs[comp['nf']]).id
                if nfId != None:
                    slice.composeSlice(nfId, comp['weight'])
                else:
                    raise Exception(f"Unable to find {comp['nf']} for {slice.name}")
            #pprint(slice)
            self.exp_slices[slice.name] = slice

    def loadServices(self):
        for serviceItem in self.yamlConfig.services:
            service = Service(serviceItem['name'])
            for comp in serviceItem['composition']:
                try:
                    sliceId = (self.exp_slices[comp['slice']]).id
                    service.composeService(sliceId, comp['weight'])
                except:
                    logger.error(f"YAML Error : Unable to find {comp['slice']} for {service.name}. Check your YAML file")
                    sys.exit(1)
            #pprint(service)
            self.exp_services[service.name] = service

    def loadSlicelets(self):
        for sliceletItem in self.yamlConfig.slicelets:
            try:
                sId = self.exp_services[sliceletItem['service']].id
                slicelet = Slicelet(name = sliceletItem['name'], duration=sliceletItem['duration'], service_id=sId)
                #pprint(slicelet)
                self.exp_slicelets[slicelet.name] = slicelet
            except:
                logger.error(f"YAML Error : Unable to find {sliceletItem['service']} for {sliceletItem['name']}. Please check your YAML", exc_info=1)
                sys.exit(1)
    
    def getDelays(self, total, limit):
        logger.debug(f"Trying to get delays for {total} and {limit} with pattern {self.exp_delay_pattern}")
        match self.exp_delay_pattern:
            case "uniform": 
                return random.normal(loc=limit, size=total).tolist()
            case "exponential":
                logger.debug(f"generating expotential delays")
                return list(random.exponential(scale=limit, size=total))
            case _:
                zList = [0] * total
                return zList


    def introduceRandomnessForSlicelets(self):
        logger.info(f"Introducing Randomness for Slicelets")
        total_slicelets = len(self.exp_slicelets)
        delayList = self.getDelays(total_slicelets, self.exp_delay_pattern_threshold)
        logger.info(delayList)
        cnt = 0
        for _,v in self.exp_slicelets.items():
            v.initRandomDelaySecs = delayList[cnt]
            logger.info(f"Slicelet {v.name} has {v.initRandomDelaySecs} init delay")
            cnt += 1

    def displaySliceletStatistics(self):
        """Dump slice info statistics on std out."""
        headers = ["Slicelet ID", "Slicelet Name", "Slicelet Admitted?", "SLA Violation?", "Event History"]
        items = []
        for _,v in self.exp_slicelets.items():
            item = [str(v.id), v.name, str(v.get_exp_status()), str(v.slaViolation), str(v.eventHistory)]
            items.append(item)
        print(tabulate(items, headers, tablefmt="simple_grid"))
    
    def loadSlices_removethis(self):
        for sliceItem in self.yamlConfig.slices:
            slice = StaticSlice(sliceItem['name'])
            skipSlice = False
            for comp in sliceItem['composition']:
                nfId = NfMgr.getNfIdByName(comp['nf'])
                if nfId != None:
                    slice.composeSlice(nfId, comp['weight'])
                else:
                    logger.info(f"Unable to find {comp['nf']} for {slice.name}")
                    skipSlice = True
            if skipSlice:
                logger.info(f"Skipping {slice.name} due to NF composition issues")
                continue
            SliceMgr.deploySlice(slice)


    def loadYAML(self, fname: str):
        try:
            parsedYaml = yaml.load(open(fname, 'r'), yaml.SafeLoader)
            if "name" in parsedYaml:
                self.exp_name = parsedYaml['name']
            if "description" in parsedYaml:
                self.exp_descp = parsedYaml['description']
            if "delay_pattern" in parsedYaml:
                self.exp_delay_pattern = parsedYaml['delay_pattern']
            if "delay_pattern_threshold" in parsedYaml:
                self.exp_delay_pattern_threshold = parsedYaml['delay_pattern_threshold']
            if "clouds" in parsedYaml:
                self.yamlConfig.clouds = parsedYaml['clouds']
            if "nfs" in parsedYaml:
                self.yamlConfig.nfs = parsedYaml['nfs']
            if "slices" in parsedYaml:
                self.yamlConfig.slices = parsedYaml['slices']
            if "services" in parsedYaml:
                self.yamlConfig.services = parsedYaml['services']
            if "slicelets" in parsedYaml:
                self.yamlConfig.slicelets = parsedYaml['slicelets']
            if "policies" in parsedYaml:
                self.yamlConfig.policies = parsedYaml['policies']
        except Exception as e :
            logger.error(f"YAML parser error {e}")
            sys.exit(1)