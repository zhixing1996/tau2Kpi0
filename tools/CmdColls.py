import subprocess
import sys
import attr

class CmdColls:
    def __init__(self, coll, run_type = '--dry_run', cmd_coll = []):
        self.coll = coll
        self.run_type = run_type
        self.cmd_coll = self.const_cmd()

    def const_cmd(self):
        cmd_coll = []
        for project in attr.projects[attr.run_type]:
            if self.coll == 'project_sub': 
                cmd = 'gbasf2 --input_dslist ' + attr.cur_dir + '/samples/' + attr.campaign[attr.run_type] + '_' + project + '.list -s ' + attr.release + ' -p ' + project + ' ' + attr.steering_file + ' -n ' + attr.files_perjob + ' ' + self.run_type
                cmd_coll.append(cmd)
            elif self.coll == 'project_reschedule':
                cmd = 'gb2_job_reschedule -p ' + project
                cmd_coll.append(cmd)
            else:
                print('not considered command collection, please add!')
                sys.exit()
        return cmd_coll

    def process(self):
        for cmd in self.cmd_coll:
            print('processing: ' + cmd + '...')
            process = subprocess.Popen([cmd], shell = True, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
            stderr = process.stderr.read()
            stdout = process.stdout.read()
            if not stderr:
                print('success: \n')
                print(stdout.decode('utf-8'))
            else:
                print('failed: \n')
                print(stderr.decode('utf-8'))
