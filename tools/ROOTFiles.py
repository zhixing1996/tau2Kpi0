import subprocess
import os
import sys
import attr
from ROOT import TChain

class ROOTFiles:
    def __init__(self, file_locs = None):
        if file_locs == None:
            self.file_locs = self.find_locs()
        elif isinstance(file_locs, list):
            self.file_locs = file_locs
        elif isinstance(file_locs, str):
            self.file_locs = self.find_locs(file_locs)
        else:
            raise TypeError('type error, please check!')

    def find_locs(self, file_locs = ''):
        locs_ls = []
        if file_locs == '':
            for project in attr.projects:
                file_loc = attr.cur_dir + '/rootfiles/' + project + '/sub00/'
                locs_ls.append(file_loc)
        else:
            file_loc = attr.cur_dir + '/rootfiles/' + file_locs + '/sub00/'
            locs_ls.append(file_loc)
        return locs_ls

    def merge(self):
        ch = TChain('tau2Kpi0')
        for file_loc in self.file_locs:
            print('merging ROOT files in : ' + file_loc + '...')
            project = file_loc.split('/')[-3]
            dest_file = attr.cur_dir + '/rootfiles/' + project + '/' + project + '-source.root'
            source_file = file_loc + '*.root'
            if os.path.isfile(dest_file): os.remove(dest_file)
            ch.Add(source_file)
            ch.Merge(dest_file)
            ch.Reset()

    def make_one(self, file_locs = ''):
        ch = TChain('tau2Kpi0')
        if file_locs == '':
            for sample, projects in attr.samples.items():
                if len(projects) > 1:
                    self.merge_make_one(ch, sample, projects)
        else:
            try:
                if len(attr.samples[file_locs]) > 1:
                    self.merge_make_one(ch, file_locs, attr.samples[file_locs])
                else:
                    print('{} has already been one, no need to use this function...'.format(file_locs))
                    sys.exit()
            except Exception as error:
                if attr.debug: print('DEBGUG: \n {}'.format(error))
                print('you have entered an unknown sample: {0}, please check list files in {1}/samples'.format(file_locs, attr.cur_dir))
                sys.exit()

    def merge_make_one(self, ch, sample, projects):
        print('making one file from splitted files for: ' + sample)
        if not os.path.exists(attr.cur_dir + '/rootfiles/' + sample): os.makedirs(attr.cur_dir + '/rootfiles/' + sample)
        dest_file = attr.cur_dir + '/rootfiles/' + sample + '/' + sample + '-source.root'
        if os.path.isfile(dest_file): os.remove(dest_file)
        source_files = [(attr.cur_dir + '/rootfiles/' + project + '/' + project + '-source.root') for project in projects]
        for source_file in source_files: ch.Add(source_file)
        ch.Merge(dest_file)
        ch.Reset()
