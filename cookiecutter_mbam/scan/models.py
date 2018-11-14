# -*- coding: utf-8 -*-
"""Scan model."""

from sqlalchemy import event
from cookiecutter_mbam.experiment import Experiment
from cookiecutter_mbam.database import Column, Model, SurrogatePK, db, reference_col, relationship

class Scan(SurrogatePK, Model):
    """A user's scan."""

    __tablename__ = 'scan'
    xnat_uri = db.Column(db.String(255))
    experiment_id = reference_col('experiments', nullable=True)
    experiment = relationship('Experiment', backref='scans')

    def __init__(self, experiment_id, **kwargs):
        """Create instance."""
        db.Model.__init__(self, experiment_id=experiment_id, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Scan({uri})>'.format(uri=self.xnat_uri)

# def update_experiment_scan_count(mapper, connection, target):
#     exp_id = target.experiment_id
#     exp = Experiment.get_by_id(exp_id)
#     exp.update({'num_scans', exp.num_scans + 1})
#
# event.listen(Scan, 'after_insert', update_experiment_scan_count)