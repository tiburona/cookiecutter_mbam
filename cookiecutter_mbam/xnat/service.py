import xnat
import configparser
import os

from flask import current_app

def debug():
    assert current_app.debug == False, "Don't panic! You're here by request of debug()"

class XNATConnection:

    def __init__(self):
        self._read_xnat_config()
        self._set_attributes()
        self.xnat_hierarchy = ['subject', 'experiment', 'scan', 'resource', 'file']

    def _read_xnat_config(self):
        """

        :return: None
        """
        config = configparser.ConfigParser()
        config.read('/Users/katie/spiro/cookiecutter_mbam/setup.cfg')
        self.xnat_config = config['XNAT']

    def _set_attributes(self):
        [setattr(self, k, v) for k, v in self.xnat_config.items()]
        for dest in ['archive', 'prearchive']:
            setattr(self, dest + '_prefix', '/data/{}/projects/{}'.format(dest, self.project))

    def xnat_put(self, url='', file=None, imp=False, **kwargs):
        with xnat.connect(self.server, self.user, self.password) as session:
            try:
                if imp:
                    session.services.import_(file, **kwargs)
                    # need to call something like xnat_get to get the scan uri and return it to calling method
                elif file:
                    session.upload(url, file)
                else:
                    session.put(url)
            except:
                # what should we do with errors?
                # probably depends on what the error is.  if we don't succeed in uploading the file
                # we need to send a message back to the user
                # but some errors here could be recoverable.


                pass

    def xnat_get(self):
        # This needs to be a method that gets the name of the scan uri some how.
        pass

    def upload_scan(self, xnat_ids, existing_xnat_ids, image_file, import_service=False):
        """

        :param dict xnat_ids: a dictionary of xnat identifiers and query strings for put urls
        :param dict existing_xnat_ids: a dictionary of XNAT attributes that already existed on user and experiment
        :param file image_file: the scan file to upload
        :param bool import_service: whether to use the XNAT import service. True if file is a .zip, default False.
        :return: three-tuple of the xnat uris for subject, experiment, and scan
        :rtype: tuple
        """

        self.xnat_ids = xnat_ids
        uri = self.archive_prefix
        uris = {}

        if import_service:
            levels = self.xnat_hierarchy[:-3]
        else:
            levels = self.xnat_hierarchy

        for level in levels:
            attr = 'xnat_{}_id'.format(level)
            if attr in existing_xnat_ids and len(existing_xnat_ids[attr]):
                uri = os.path.join(uri, level + 's', existing_xnat_ids[attr])
            else:
                uri = os.path.join(uri, level + 's', xnat_ids[level]['xnat_id'])

            uris[level] = uri

            try:
                query = xnat_ids[level]['query_string']
            except: #todo specify KeyError here?
                query = ''

            if level == 'file':
                self.xnat_put(url=uri + query, file=image_file)
                image_file.close()
            else:
                self.xnat_put(url=uri + query)

        if import_service:
            self.xnat_put(file=image_file, imp=True, project=self.project,
                          subject = self.xnat_ids['subject']['xnat_id'],
                          experiment = self.xnat_ids['experiment']['xnat_id'])

        try:
            uris['scan']
        except:
            uris['scan'] = 'hello'

        return (uris['subject'], uris['experiment'], uris['scan'])












