import sys, os
import attr
from tools import print_sep
from array import array
from ROOT import TFile, TTree, TLorentzVector, TH1D, TChain, TCanvas, THStack
from style import pub_style, set_hist_style, set_canvas_style, set_legend, set_arrow

class EventSelect:
    def __init__(self, mode, sample = 'all', vars = 'all', target = 'all'):
        self.mode = mode
        if sample == 'all':
            self.samples = attr.samples[attr.sample_type].keys()
        else: self.samples = [sample]
        self.vars = vars
        if target == 'all': self.target_paths = self.locate()
        else: self.target_paths = [target]

    def locate(self):
        file_liest = []
        path_list = [self.path(sample) for sample in self.samples]
        return path_list

    def path(self, sample):
        return attr.cur_dir + '/rootfiles/' + sample + '/' + sample

    def extract(self):
        m_dmID_1prong0 = array('i', [0])
        m_dmID_1prong1 = array('i', [0])
        m_n_e = array('i', [0])
        m_n_mu = array('i', [0])
        m_n_K = array('i', [0])
        m_n_pi0 = array('i', [0])
        m_thrust = array('d', [0])
        m_foxWolframR2 = array('d', [0])
        m_E_visible_cms = array('d', [0])
        m_p_miss_lab = array('d', [0])
        m_p_miss_theta_lab = array('d', [0])
        m_p_miss_cms = array('d', [0])
        m_p_miss_theta_cms = array('d', [0])
        m_mm_miss = array('d', [0])
        m_m_pi0 = array('d', [0])
        m_m_Kpi0 = array('d', [0])
        if attr.sample_type != 'data':
            m_mode_taup = array('i', [0])
            m_mode_taum = array('i', [0])
        m_pt_K = array('d', [0])
        m_theta_K = array('d', [0])
        m_costheta_K = array('d', [0])
        m_p_K_cms = array('d', [0])
        m_pt_K_cms = array('d', [0])
        m_E_K_cluster = array('d', [0])
        m_Ep_K = array('d', [0])
        m_pid_K_K = array('d', [0])
        m_pid_K_pi = array('d', [0])
        m_pid_K_p = array('d', [0])
        m_pid_K_mu = array('d', [0])
        m_pid_K_e = array('d', [0])
        m_pid_K_d = array('d', [0])
        m_dz_K = array('d', [0])
        m_dr_K = array('d', [0])
        m_pt_pi0 = array('d', [0])
        m_theta_pi0 = array('d', [0])
        m_costheta_pi0 = array('d', [0])
        m_p_pi0_cms = array('d', [0])
        m_E_pi0_cms = array('d', [0])
        m_pt_pi0_cms = array('d', [0])
        m_E_pi0_cluster = array('d', [0])
        m_pt_l = array('d', [0])
        m_theta_l = array('d', [0])
        m_costheta_l = array('d', [0])
        m_p_l_cms = array('d', [0])
        m_pt_l_cms = array('d', [0])
        m_E_l_cluster = array('d', [0])
        m_Ep_l = array('d', [0])
        m_pid_l_K = array('d', [0])
        m_pid_l_pi = array('d', [0])
        m_pid_l_p = array('d', [0])
        m_pid_l_mu = array('d', [0])
        m_pid_l_e = array('d', [0])
        m_pid_l_d = array('d', [0])
        m_dz_l = array('d', [0])
        m_dr_l = array('d', [0])
        m_charge_K = array('i', [0])
        m_charge_pi0 = array('i', [0])
        m_charge_l = array('i', [0])
        m_p_cms = array('d', [0])
        m_angle_Kl = array('d', [0])
        m_angle_Kpi0 = array('d', [0])
        t_out = TTree(attr.tree_name, attr.tree_name)
        t_out.Branch('dmID_1prong0', m_dmID_1prong0, 'dmID_1prong0/I')
        t_out.Branch('dmID_1prong1', m_dmID_1prong1, 'dmID_1prong1/I')
        t_out.Branch('n_e', m_n_e, 'n_e/I')
        t_out.Branch('n_mu', m_n_mu, 'n_mu/I')
        t_out.Branch('n_K', m_n_K, 'n_K/I')
        t_out.Branch('n_pi0', m_n_pi0, 'n_pi0/I')
        t_out.Branch('thrust', m_thrust, 'thrust/D')
        t_out.Branch('foxWolframR2', m_foxWolframR2, 'foxWolframR2/D')
        t_out.Branch('E_visible_cms', m_E_visible_cms, 'E_visible_cms/D')
        t_out.Branch('p_miss_lab', m_p_miss_lab, 'p_miss_lab/D')
        t_out.Branch('p_miss_theta_lab', m_p_miss_theta_lab, 'p_miss_theta_lab/D')
        t_out.Branch('p_miss_cms', m_p_miss_cms, 'p_miss_cms/D')
        t_out.Branch('p_miss_theta_cms', m_p_miss_theta_cms, 'p_miss_theta_cms/D')
        t_out.Branch('mm_miss', m_mm_miss, 'mm_miss/D')
        t_out.Branch('m_pi0', m_m_pi0, 'm_pi0/D')
        t_out.Branch('m_Kpi0', m_m_Kpi0, 'm_Kpi0/D')
        if attr.sample_type != 'data':
            t_out.Branch('mode_taup', m_mode_taup, 'mode_taup/I')
            t_out.Branch('mode_taum', m_mode_taum, 'mode_taum/I')
        t_out.Branch('pt_K', m_pt_K, 'pt_K/D')
        t_out.Branch('theta_K', m_theta_K, 'theta_K/D')
        t_out.Branch('costheta_K', m_costheta_K, 'costheta_K/D')
        t_out.Branch('p_K_cms', m_p_K_cms, 'p_K_cms/D')
        t_out.Branch('pt_K_cms', m_pt_K_cms, 'pt_K_cms/D')
        t_out.Branch('E_K_cluster', m_E_K_cluster, 'E_K_cluster/D')
        t_out.Branch('Ep_K', m_Ep_K, 'Ep_K/D')
        t_out.Branch('pid_K_K', m_pid_K_K, 'pid_K_K/D')
        t_out.Branch('pid_K_pi', m_pid_K_pi, 'pid_K_pi/D')
        t_out.Branch('pid_K_p', m_pid_K_p, 'pid_K_p/D')
        t_out.Branch('pid_K_mu', m_pid_K_mu, 'pid_K_mu/D')
        t_out.Branch('pid_K_e', m_pid_K_e, 'pid_K_e/D')
        t_out.Branch('pid_K_d', m_pid_K_d, 'pid_K_d/D')
        t_out.Branch('dz_K', m_dz_K, 'dz_K/D')
        t_out.Branch('dr_K', m_dr_K, 'dr_K/D')
        t_out.Branch('pt_pi0', m_pt_pi0, 'pt_pi0/D')
        t_out.Branch('theta_pi0', m_theta_pi0, 'theta_pi0/D')
        t_out.Branch('costheta_pi0', m_costheta_pi0, 'costheta_pi0/D')
        t_out.Branch('p_pi0_cms', m_p_pi0_cms, 'p_pi0_cms/D')
        t_out.Branch('E_pi0_cms', m_E_pi0_cms, 'E_pi0_cms/D')
        t_out.Branch('pt_pi0_cms', m_pt_pi0_cms, 'pt_pi0_cms/D')
        t_out.Branch('E_pi0_cluster', m_E_pi0_cluster, 'E_pi0_cluster/D')
        t_out.Branch('pt_l', m_pt_l, 'pt_l/D')
        t_out.Branch('theta_l', m_theta_l, 'theta_l/D')
        t_out.Branch('costheta_l', m_costheta_l, 'costheta_l/D')
        t_out.Branch('p_l_cms', m_p_l_cms, 'p_l_cms/D')
        t_out.Branch('pt_l_cms', m_pt_l_cms, 'pt_l_cms/D')
        t_out.Branch('E_l_cluster', m_E_l_cluster, 'E_l_cluster/D')
        t_out.Branch('Ep_l', m_Ep_l, 'Ep_l/D')
        t_out.Branch('pid_l_K', m_pid_l_K, 'pid_l_K/D')
        t_out.Branch('pid_l_pi', m_pid_l_pi, 'pid_l_pi/D')
        t_out.Branch('pid_l_p', m_pid_l_p, 'pid_l_p/D')
        t_out.Branch('pid_l_mu', m_pid_l_mu, 'pid_l_mu/D')
        t_out.Branch('pid_l_e', m_pid_l_e, 'pid_l_e/D')
        t_out.Branch('pid_l_d', m_pid_l_d, 'pid_l_d/D')
        t_out.Branch('dz_l', m_dz_l, 'dz_l/D')
        t_out.Branch('dr_l', m_dr_l, 'dr_l/D')
        t_out.Branch('charge_K', m_charge_K, 'charge_K/I')
        t_out.Branch('charge_pi0', m_charge_pi0, 'charge_pi0/I')
        t_out.Branch('charge_l', m_charge_l, 'charge_l/I')
        t_out.Branch('p_cms', m_p_cms, 'p_cms/D')
        t_out.Branch('angle_Kl', m_angle_Kl, 'angle_Kl/D')
        t_out.Branch('angle_Kpi0', m_angle_Kpi0, 'angle_Kpi0/D')
        for target_path in self.target_paths:
            print_sep('/')
            print('extract information')
            if not '-source.root' in target_path:
                source_file = target_path + '-source.root'
                dest_file = target_path + '-raw.root'
            else:
                source_file = target_path
                dest_file = target_path.replace('source', 'raw')
            print('input file: ' + source_file)
            f_in = TFile(source_file)
            t_in = f_in.Get(attr.tree_name)
            f_out = TFile(dest_file, 'recreate')
            NEntries = t_in.GetEntries()
            for ientry in range(NEntries):
                t_in.GetEntry(ientry)
                m_dmID_1prong0[0] = int(t_in.dmID_1prong0)
                m_dmID_1prong1[0] = int(t_in.dmID_1prong1)
                m_n_e[0] = int(t_in.nElectronTracks)
                m_n_mu[0] = int(t_in.nMuonTracks)
                m_n_K[0] = int(t_in.nKaonTracks)
                m_n_pi0[0] = int(t_in.nPi0)
                m_thrust[0] = t_in.thrust
                m_foxWolframR2[0] = t_in.foxWolframR2
                m_E_visible_cms[0] = t_in.visibleEnergyOfEventCMS
                m_p_miss_lab[0] = t_in.missingMomentumOfEvent
                m_p_miss_theta_lab[0] = t_in.missingMomentumOfEvent_theta
                m_p_miss_cms[0] = t_in.missingMomentumOfEventCMS
                m_p_miss_theta_cms[0] = t_in.missingMomentumOfEventCMS_theta
                m_mm_miss[0] = t_in.missingMass2OfEvent
                m_m_pi0[0] = t_in.pi0_1prong0_InvM
                p_K = TLorentzVector(0, 0, 0, 0)
                p_K.SetPxPyPzE(t_in.track_1prong0_px, t_in.track_1prong0_py, t_in.track_1prong0_pz, t_in.track_1prong0_E)
                m_m_Kpi0[0] = t_in.tau_1prong0_M
                if attr.sample_type != 'data':
                    m_mode_taup[0] = int(t_in.tauPlusMCMode)
                    m_mode_taum[0] = int(t_in.tauMinusMCMode)
                m_pt_K[0] = t_in.track_1prong0_pt
                m_theta_K[0] = t_in.track_1prong0_theta
                m_costheta_K[0] = t_in.track_1prong0_cosTheta
                m_p_K_cms[0] = t_in.track_1prong0_p_CMS
                m_pt_K_cms[0] = t_in.track_1prong0_pt_CMS
                m_E_K_cluster[0] = t_in.track_1prong0_clusterE
                m_Ep_K[0] = t_in.track_1prong0_EoverP
                m_pid_K_K[0] = t_in.track_1prong0_kaonID
                m_pid_K_pi[0] = t_in.track_1prong0_pionID
                m_pid_K_p[0] = t_in.track_1prong0_protonID
                m_pid_K_mu[0] = t_in.track_1prong0_muonID
                m_pid_K_e[0] = t_in.track_1prong0_electronID
                m_pid_K_d[0] = t_in.track_1prong0_deuteronID
                m_dz_K[0] = t_in.track_1prong0_dz
                m_dr_K[0] = t_in.track_1prong0_dr
                m_pt_pi0[0] = t_in.pi0_1prong0_pt
                m_theta_pi0[0] = t_in.pi0_1prong0_theta
                m_costheta_pi0[0] = t_in.pi0_1prong0_cosTheta
                m_p_pi0_cms[0] = t_in.pi0_1prong0_p_CMS
                m_E_pi0_cms[0] = t_in.pi0_1prong0_E_CMS
                m_pt_pi0_cms[0] = t_in.pi0_1prong0_pt_CMS
                m_E_pi0_cluster[0] = t_in.pi0_1prong0_clusterE
                m_charge_K[0] = int(t_in.track_1prong0_charge)
                m_charge_pi0[0] = int(t_in.pi0_1prong0_charge)
                m_charge_l[0] = int(t_in.track_1prong1_charge)
                m_pt_l[0] = t_in.track_1prong1_pt
                m_theta_l[0] = t_in.track_1prong1_theta
                m_costheta_l[0] = t_in.track_1prong1_cosTheta
                m_p_l_cms[0] = t_in.track_1prong1_p_CMS
                m_pt_l_cms[0] = t_in.track_1prong1_pt_CMS
                m_E_l_cluster[0] = t_in.track_1prong1_clusterE
                m_Ep_l[0] = t_in.track_1prong1_EoverP
                m_pid_l_K[0] = t_in.track_1prong1_kaonID
                m_pid_l_pi[0] = t_in.track_1prong1_pionID
                m_pid_l_p[0] = t_in.track_1prong1_protonID
                m_pid_l_mu[0] = t_in.track_1prong1_muonID
                m_pid_l_e[0] = t_in.track_1prong1_electronID
                m_pid_l_d[0] = t_in.track_1prong1_deuteronID
                m_dz_l[0] = t_in.track_1prong1_dz
                m_dr_l[0] = t_in.track_1prong1_dr
                p_K = TLorentzVector(0, 0, 0, 0)
                p_l = TLorentzVector(0, 0, 0, 0)
                p_K.SetPxPyPzE(t_in.track_1prong0_px_CMS, t_in.track_1prong0_py_CMS, t_in.track_1prong0_pz_CMS, t_in.track_1prong0_E_CMS)
                p_l.SetPxPyPzE(t_in.track_1prong1_px_CMS, t_in.track_1prong1_py_CMS, t_in.track_1prong1_pz_CMS, t_in.track_1prong1_E_CMS)
                m_p_cms[0] = (p_K + p_l).P()
                m_angle_Kl[0] = abs(t_in.track_1prong0_theta_CMS - t_in.track_1prong1_theta_CMS)
                m_angle_Kpi0[0] = abs(t_in.pi0_1prong0_theta_CMS - t_in.track_1prong0_theta_CMS)
                t_out.Fill()
            f_out.cd()
            t_out.Write()
            f_out.Close()
            t_out.Reset()
            print('output file: ' + dest_file)
            print_sep('/')

    def cuts(self):
        if not os.path.exists('./figs/'):
            os.makedirs('./figs/')
        ch = TChain(attr.tree_name)
        for k, v in attr.cut_vars[self.vars]['var'].items():
            pub_style()
            hist_list = []
            mbc = TCanvas('mbc_' + k, '', 800, 600)
            set_canvas_style(mbc)
            for target_path, sample in zip(self.target_paths, self.samples):
                xmin, xmax, xbins = attr.cut_vars[self.vars]['xrange']
                if not '-raw.root' in target_path:
                    source_file = target_path + '-raw.root'
                else:
                    source_file = target_path
                hist_name = k + '_' + v + '_' + sample
                hist = TH1D(hist_name, '', xbins, xmin, xmax)
                ch.Add(source_file)
                ch.Draw(v + '>>' + hist_name, attr.cut_vars[self.vars]['cut'])
                set_hist_style(hist, attr.cut_vars[self.vars]['xtitle'][k], attr.cut_vars[self.vars]['ytitle'], attr.samples_text[sample][1], attr.samples_text[sample][2])
                hist_list.append(hist)
                ch.Reset()
            y_num = []
            hs = THStack('hs', 'Stacked')
            for hist in hist_list:
                hs.Add(hist)
                y_num.append(hist.GetMaximum())
            hist_list[0].Draw()
            hs.Draw('same')
            hist_list[0].GetYaxis().SetRangeUser(0, 1.1*sum(y_num))
            if 'legend' in attr.cut_vars[self.vars]['widget']:
                from ROOT import TLegend
                left, bottom, right, top = attr.cut_vars[self.vars]['legend']
                legend = TLegend(left, bottom, right, top)
                set_legend(legend, hist_list, [v[0] for k, v in attr.samples_text.items()])
                legend.Draw()
            if 'arrow' in attr.cut_vars[self.vars]['widget']:
                from ROOT import TArrow
                size, type, color = attr.cut_vars[self.vars]['arrow']
                arrow = TArrow(attr.cut_vars[self.vars]['pos'][k], 0, attr.cut_vars[self.vars]['pos'][k], 0.8*sum(y_num), size, type)
                set_arrow(arrow, color)
                arrow.Draw()
            mbc.SaveAs('./figs/' + k + '_' + self.vars + '.pdf')
            input('Press <Enter> to exit...')
