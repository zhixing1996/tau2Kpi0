import sys
import attr
import os

class CmdColls:
    def __init__(self, coll, projects = None, run_type = '--dry_run', cmd_coll = []):
        self.coll = coll
        if projects == None:
            self.projects = attr.projects[attr.sample_type]
        elif isinstance(projects, str):
            self.projects = [projects]
        else:
            raise TypeError('type error, please check!')
        self.run_type = run_type
        self.cmd_coll = self.const_cmd()

    def const_cmd(self):
        cmd_coll = []
        for project in self.projects:
            if self.coll == 'project_sub': 
                cmd = 'gbasf2 --input_dslist ' + attr.cur_dir + '/samples/' + attr.campaign[attr.sample_type] + '/' + attr.campaign[attr.sample_type] + '_' + project + '.list -s ' + attr.release + ' -p ' + project + ' ' + attr.steering_file + ' -n ' + attr.files_perjob + ' ' + self.run_type
                cmd_coll.append(cmd)
            elif self.coll == 'project_reschedule':
                cmd = 'gb2_job_reschedule -p ' + project
                cmd_coll.append(cmd)
            elif self.coll == 'ds_get':
                if not os.path.exists('./rootfiles/'):
                    os.makedirs('./rootfiles/')
                cmd = 'cd ' + attr.cur_dir + '/rootfiles && gb2_ds_get ' + project
                cmd_coll.append(cmd)
            else:
                print('not considered command collection, please add!')
                sys.exit()
        return cmd_coll

    def process(self):
        for cmd in self.cmd_coll:
            print('processing: ' + cmd + '...')
            try:
                os.system(cmd)
            except Exception as error:
                print('error:')
                print(error)
