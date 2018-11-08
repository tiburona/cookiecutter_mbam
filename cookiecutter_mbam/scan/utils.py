

def generate_xnat_identifiers(self):  # Todo: should this info be someplace else -- a helper function maybe?
    xnat_ids = {}
    xnat_ids['subject'] = self.user_id.zfill(6)
    xnat_ids['experiment'] = self.experiment_id.zfill(6)
    xnat_ids['scan'] = 'T1'  # This needs to be made dynamic bc there can be more than one Tq
    xnat_ids['resource'] = 'NIFTI'  # obv. needs to be made dynamic
    xnat_ids['file'] = 'T1.nii.gz?xsi:type=xnat:mrScanData'  # needs to be made dynamic for many reasons
    return xnat_ids



