import os
import sys
import hl7
import pandas as pd


class frameHL7Reader(object):
    def __init__(self, inPath, query):
        self.inPath = inPath
        self.lines = self.loadSampleData()
        self.records = []
        self.frameIndexes, self.cols = self.defineIndexes()
        if query == "Q1":
            self.cols = [f'col_{n}' for n in range(0, 5)]
            base_index = 14
            self.__load_data(filter='EVN', base_index=base_index)
        elif query == "Q2":
            self.cols = [f'col_{n}' for n in range(0, 21)]
            base_index = 19
            self.__load_data(filter='PID', base_index=base_index)
        elif "F" in query:
            number_of_fields = query[1:]
            nof = int(number_of_fields) * 10
            self.cols = [f'col_{n}' for n in range(0, nof)]
            self.__load_dataF(end_index=nof)
        else:
            self.__load_data(filter=None, base_index=0)
        self.data = pd.DataFrame(self.records, dtype=str)

    def defineIndexes(self):
        index = 0
        msh = [n for n in range(0, 14)]
        index += 14
        evn = [n for n in range(index, index + 5)]
        index += 5
        pid = [n for n in range(index, index + 21)]
        index += 21
        pv1 = [n for n in range(index, index + 10)]
        index += 10
        dg1 = [n for n in range(index, index + 9)]
        index += 9
        gt1 = [n for n in range(index, index + 12)]
        index += 12
        in1 = [n for n in range(index, index + 26)]
        index += 26
        in2 = [n for n in range(index, index + 4)]
        index += 4

        hm = {"MSH": msh, "EVN": evn, "PID": pid, "PV1": pv1, "DG1": dg1, "GT1": gt1, "IN1": in1, "IN2": in2}

        cols = [f'col_{n}' for n in range(0, index)]
        return hm, cols

    def __load_data(self, filter, base_index):
        msg = ""
        begin = None
        i = 0
        for l in self.lines:
            ls = l.strip()
            head = ls[:3]
            if head == "MSH" and begin is not None:  # process the record
                h = hl7.parse(msg)
                record = ["" for n in range(0, len(self.cols))]
                for segment in h:
                    if isinstance(segment, hl7.Segment):
                        index = 0
                        root = segment[0]
                        map = self.frameIndexes[f'{root}']
                        if filter == None or filter == f'{root}':
                            for attribute in segment[1:]:
                                for field in attribute:
                                    if isinstance(field, hl7.containers.Repetition):
                                        for rep in field:
                                            if isinstance(rep, hl7.containers.Component):
                                                for comp in rep:
                                                    if len(comp) > 0:
                                                        record[map[index] - base_index] = comp
                                                        index += 1

                                    elif isinstance(field, hl7.containers.Component):
                                        for comp in field:
                                            if len(comp) > 0:
                                                record[map[index] - base_index] = comp
                                                index += 1
                                    else:
                                        if len(field) > 0 and field != '|' and field != '^~\&':
                                            record[map[index] - base_index] = field
                                            index += 1
                msg = ls + "\r"
                i += 1
                self.records.append(record)

            elif head == "MSH" and begin is None:
                msg += ls + "\r"
                begin = "MSH"
            else:
                msg += ls + "\r"

    def __load_dataF(self, end_index):
        msg = ""
        begin = None
        i = 0
        for l in self.lines:
            ls = l.strip()
            head = ls[:3]
            if head == "MSH" and begin is not None:  # process the record
                h = hl7.parse(msg)
                record = ["" for n in range(0, len(self.cols))]
                for segment in h:
                    if isinstance(segment, hl7.Segment):
                        index = 0
                        map = self.frameIndexes[f'{segment[0]}']
                        for attribute in segment[1:]:
                            if index>= end_index:
                                break
                            for field in attribute:
                                if index >= end_index:
                                    break
                                if isinstance(field, hl7.containers.Repetition):
                                    for rep in field:
                                        if index >= end_index:
                                            break
                                        if isinstance(rep, hl7.containers.Component):
                                            for comp in rep:
                                                if len(comp) > 0:
                                                    if map[index] >= end_index:
                                                        break
                                                    record[map[index]] = comp
                                                    index += 1

                                elif isinstance(field, hl7.containers.Component):
                                    for comp in field:
                                        if map[index] >= end_index:
                                            break
                                        if len(comp) > 0:
                                            record[map[index]] = comp
                                            index += 1
                                else:
                                    if len(field) > 0 and field != '|' and field != '^~\&':
                                        if map[index] >= end_index:
                                           continue
                                        record[map[index]] = field
                                        index += 1
                msg = ls + "\r"
                i += 1
                self.records.append(record)

            elif head == "MSH" and begin is None:
                msg += ls + "\r"
                begin = "MSH"
            else:
                msg += ls + "\r"


    def loadSampleData(self):
        with open(self.inPath, "r", encoding='latin-1') as file:
            lines = file.readlines()
            return lines


if __name__ == '__main__':
    data_file_name = sys.argv[1]
    projection = sys.argv[2]
    frameHL7Reader(inPath=data_file_name, query=projection)
