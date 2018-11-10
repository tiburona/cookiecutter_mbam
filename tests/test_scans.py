import pytest
from datetime import datetime
from cookiecutter_mbam.user import User
from cookiecutter_mbam.experiment.service import ExperimentService
from cookiecutter_mbam.scan.service import ScanService


@pytest.fixture(scope='function')
@pytest.mark.usefixtures('db')
def new_scan_service(db):
    user = User.create(username='Princess Leia', email='dontatme@me.com')
    date = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
    es = ExperimentService()
    experiment1 = es.add(date=date, scanner='GE', num_scans=2, user=user)
    experiment2 = es.add(date=date, scanner='GE', num_scans=2, user=user)
    ss1 = ScanService(user.id, experiment2.id)
    ss1._add_scan()
    ss2 = ScanService(user.id, experiment2.id)

    db.session.commit()
    print('I just put the user and two experiments into the database. user.num_experiments is ', user.num_experiments)
    s = ScanService(user.id, experiment2.id)
    return s

class TestScanUpload:

    def test_unzipped_scan(self, new_scan_service):
        """
        Given that an unzipped nii file is passed to the scan service upload method
        When the upload method calls _process_file
        _process_file returns a two tuple: (the gzipped file object, False)
        """

        with open('/Users/katie/spiro/cookiecutter_mbam/files/T1.nii', 'rb') as f:
            file_object, import_service = new_scan_service._process_file(f, 'T1.nii')
            assert not import_service
            assert type(file_object).__name__ == 'GzipFile'


    def test_xnat_ids_correctly_generated_for_multiple_experiments_and_scans(self, new_scan_service):
        """
        Given a subject with more than one experiment, and an experiment with more than one scan
        When xnat ids are generated
        Then test that xnat_experiment_id and xnat_scan_id are as expected
        """

        with open('/Users/katie/spiro/cookiecutter_mbam/files/T1.nii.gz', 'rb') as f:
            xnat_ids = new_scan_service._generate_xnat_identifiers()
            assert xnat_ids['experiment']['xnat_id'] == '000001_MR2'
            assert xnat_ids['scan']['xnat_id'] == 'T1_2'
