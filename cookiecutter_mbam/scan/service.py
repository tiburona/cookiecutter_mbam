# -*- coding: utf-8 -*-
"""Scan service.

This module implements uploading a scan file to XNAT and adding a scan to the database.

:Todo: Maybe the public method should be called add, and that should kick off an upload procedure, rather than the
other way around.

"""

from cookiecutter_mbam.xnat import XNATConnection
from cookiecutter_mbam.experiment import Experiment
from cookiecutter_mbam.user import User
from .models import Scan
import os
import gzip

from flask import current_app

def debug():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"


class ScanService:

    def __init__(self, user_id, exp_id):
        self.user_id = user_id
        self.user = User.get_by_id(self.user_id)
        self.experiment = Experiment.get_by_id(exp_id)
        self.xc = XNATConnection()

    def upload(self, image_file, image_file_name):
        """The top level public method for adding a scan

        Calls methods to infer file type and further process the fiile, generate xnat identifiers and query strings,
        check what XNAT identifers objects have, upload the scan to XNAT, add the scan to the database, and update
        user, experiment, and scan database objects with their XNAT-related attributes.

        :param file image_file: the file object
        :param str image_file_name: the file name
        :return: None

        """
        file, import_service = self._process_file(image_file, image_file_name)
        xnat_ids = self._generate_xnat_identifiers()
        existing_attributes = self._check_for_existing_xnat_ids()
        uris = self.xc.upload_scan(xnat_ids, existing_attributes, image_file, import_service=import_service)
        scan = self._add_scan()
        keywords = ['subject', 'experiment', 'scan']
        self._update_database_objects(keywords=keywords, objects=[self.user, self.experiment, scan],
                                     ids=['{}_id'.format(xnat_ids[kw]['xnat_id']) for kw in keywords], uris=uris)
        # todo: what is the actual URI of the experiment I've created?  Why does it have the XNAT prefix?

    def _add_scan(self):
        """Add a scan to the database

        Creates the scan object, adds it to the database, and increments the parent experiment's scan count
        :return: scan
        """
        scan = Scan.create(experiment_id=self.experiment.id)
        self.experiment.num_scans += 1
        return scan


    def _process_file(self, image_file, image_file_name):
        """Infer file type from extension and respond to file type as necessary

        Uses file extension to infer whether file should be left alone or gzipped, or whether zip file will be sent to
        import service. A private method not designed to be accessed by other classes.

        :param file image_file: the file object
        :param str image_file_name: the file name
        :return: a two-tuple of the image file (either .gz or .zip) and a boolean indicating whether to invoke the
        import service
        :rtype: tuple

        """
        file_name, file_ext = os.path.splitext(image_file_name)
        import_service = False
        if file_ext == '.nii':
            image_file = (self._gzip_file(image_file, file_name))
        if file_ext == '.zip':
            import_service = True
        return (image_file, import_service)

    def _gzip_file(self, file, file_name):
        """ Gzip a file
        :param file file:
        :param str file_name:
        :return: the gzipped file
        :rtype: gzip file
        :todo: move this to a utilities module
        """
        with gzip.open(file_name + '.gz', 'wb') as gzipped_file:
            gzipped_file.writelines(file)
        return gzipped_file

    def _generate_xnat_identifiers(self):
        """Generate object ids for use in XNAT

        Creates a dictionary with keys for type of XNAT object, including subject, experiment, scan, resource and file.
        The values in the dictionary are dictionaries with keys 'xnat_id' and, optionally, 'query_string'.  'xnat_id'
        points to the identifier of the object in XNAT, and 'query_string' to the query that will be used in the put
        request to create the object. A private method not designed to be accessed by other classes.

        :return: xnat_id dictionary
        :rtype: dict
        """
        xnat_ids = {}

        xnat_ids['subject'] = {'xnat_id': str(self.user_id).zfill(6)}


        xnat_exp_id = '{}_MR{}'.format(xnat_ids['subject']['xnat_id'], self.user.num_experiments)
        exp_date = self.experiment.date.strftime('%m/%d/%Y')
        xnat_ids['experiment'] = {'xnat_id': xnat_exp_id, 'query_string':'?xnat:mrSessionData/date={}'.format(exp_date)}

        scan_number = self.experiment.num_scans + 1
        xnat_scan_id = 'T1_{}'.format(scan_number)
        xnat_ids['scan'] = {'xnat_id':xnat_scan_id, 'query_string':'?xsiType=xnat:mrScanData'}  # Todo: This needs to be made dynamic bc there can be more than one T1

        xnat_ids['resource'] = {'xnat_id':'NIFTI'} # Todo: obv. needs to be made dynamic

        xnat_ids['file'] = {'xnat_id':'T1.nii.gz', 'query_string':'?xsi:type=xnat:mrScanData'}

        return xnat_ids

    def _check_for_existing_xnat_ids(self):
        """Check for existing attributes on the user and experiment

        Generates a dictionary with current xnat_subject_id for the user, xnat_experiment_id for the experiment as
        values if they exist (empty string if they do not exist). A private method not designed to be accessed by other
        classes.

        :return: a dictionary with two keys with the xnat subject id and xnat experiment id.
        :rtype: dict
        """
        return {k: getattr(v, k) if getattr(v, k) else '' for k, v in {'xnat_subject_id': self.user,
                                                                       'xnat_experiment_id': self.experiment}.items()}


    def _update_database_objects(self, objects=[], keywords=[], uris=[], ids=[],):
        """Update database objects

        After uploading a scan, ensures that user, experient, and scan are updated in the database with their xnat uri
        and xnat id.

        :param list objects: user, experiment, and scan
        :param list keywords: 'subject', 'experiment', and 'scan'
        :param list uris: xnat uris
        :param list ids: xnat ids
        :return: None
        :todo: the check for existence before reassigning the values is verbose.  Decide whether its important.
        """
        attributes = zip(objects, keywords, uris, ids)
        for (obj, kw, uri, id) in attributes:
            if not hasattr(obj, 'xnat_uri'):
                obj.update({'xnat_uri': uri})
            if not hasattr(obj,'xnat_{}_id'.format(kw)):
                obj.update({'xnat_{}_id'.format(kw): id})












