import os
import sys
import attr
from ROOT import TChain

class ROOTFiles:
    def __init__(self, project = None):
        if project == None:
            self.file_locs = self.find_locs()
        elif isinstance(project, str):
            self.file_locs = self.find_locs(project)
        else:
            raise TypeError('type error, please check!')

    def find_locs(self, project = ''):
        locs_ls = []
        if project == '':
            for p in attr.projects[attr.sample_type]:
                file_loc = attr.cur_dir + '/rootfiles/' + p + '/sub00/'
                locs_ls.append(file_loc)
        else:
            file_loc = attr.cur_dir + '/rootfiles/' + project + '/sub00/'
            locs_ls.append(file_loc)
        return locs_ls

    def merge(self):
        ch = TChain(attr.tree_name)
        for file_loc in self.file_locs:
            print('merging ROOT files in : ' + file_loc + '...')
            p = file_loc.split('/')[-3]
            dest_file = attr.cur_dir + '/rootfiles/' + p + '/' + p + '-source.root'
            source_file = file_loc + '*.root'
            if os.path.isfile(dest_file): os.remove(dest_file)
            ch.Add(source_file)
            ch.Merge(dest_file)
            ch.Reset()

    def make_one(self, project = ''):
        ch = TChain(attr.tree_name)
        if project == '':
            for sample, projects in attr.samples[attr.sample_type].items():
                if len(projects) > 1:
                    self.merge_make_one(ch, sample, projects)
        else:
            try:
                if len(attr.samples[attr.sample_type][project]) > 1:
                    self.merge_make_one(ch, project, attr.samples[attr.sample_type][project])
                else:
                    print('{} has already been one, no need to use this function...'.format(project))
                    sys.exit()
            except Exception as error:
                if attr.debug: print('DEBGUG: \n {}'.format(error))
                print('you have entered an unknown sample: {0}, please check list files in {1}/samples'.format(project, attr.cur_dir))
                sys.exit()

    def merge_make_one(self, ch, sample, projects):
        print('making one file from splitted files for: ' + sample)
        if not os.path.exists(attr.cur_dir + '/rootfiles/' + sample): os.makedirs(attr.cur_dir + '/rootfiles/' + sample)
        dest_file = attr.cur_dir + '/rootfiles/' + sample + '/' + sample + '-source.root'
        if os.path.isfile(dest_file): os.remove(dest_file)
        source_files = [(attr.cur_dir + '/rootfiles/' + p + '/' + p + '-source.root') for p in projects]
        for source_file in source_files: ch.Add(source_file)
        ch.Merge(dest_file)
        ch.Reset()
